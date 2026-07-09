from django.views.generic import DetailView, ListView, CreateView
from .models import Product, Order, Review
from .forms import OrderForm, SearchForm, ReviewForm
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.models import UserHealth
from django.db.models import Avg


# -------------------- PRODUCT --------------------

class ProductListView(ListView):
    model = Product
    template_name = "Product/product_list.html"
    context_object_name = "object_list"

    def get_queryset(self):

        queryset = Product.objects.all()

        # Search
        search = self.request.GET.get("search")
        food_type = self.request.GET.get("food_type")

        if search:
            queryset = queryset.filter(
                name__icontains=search
            )

        if food_type:
            queryset = queryset.filter(
                food_type=food_type
            )

            # Sort Products

            sort_by = self.request.GET.get("sort_by")

            if sort_by == "low_calories":

                queryset = queryset.order_by("calories")

            elif sort_by == "high_protein":

                queryset = queryset.order_by("-protein")

            elif sort_by == "low_price":

                queryset = queryset.order_by("price")

            elif sort_by == "high_price":

                queryset = queryset.order_by("-price")

        # AI Recommendation Order
        if self.request.user.is_authenticated:

            try:

                health = UserHealth.objects.get(
                    user=self.request.user
                )

                recommended = queryset.filter(
                    food_type=health.goal
                )

                others = queryset.exclude(
                    food_type=health.goal
                )

                queryset = recommended | others

            except UserHealth.DoesNotExist:
                pass

        return queryset


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["search_form"] = SearchForm(
            self.request.GET
        )

        if self.request.user.is_authenticated:

            try:

                context["health"] = UserHealth.objects.get(
                    user=self.request.user
                )

            except UserHealth.DoesNotExist:

                context["health"] = None

        else:

            context["health"] = None

        return context

class ProductDetailView(DetailView):

    model = Product

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["reviews"] = Review.objects.filter(
            product=self.object
        )

        average_rating = Review.objects.filter(
            product=self.object
        ).aggregate(
            Avg("rating")
        )

        context["average_rating"] = average_rating["rating__avg"]

        context["review_count"] = Review.objects.filter(
            product=self.object
        ).count()
        
        if self.request.user.is_authenticated:

             existing_review = Review.objects.filter(
                  product=self.object,
                  user=self.request.user
        ).first()

        context["existing_review"] = existing_review

        if not existing_review:
                context["review_form"] = ReviewForm()

        return context
    
            


# -------------------- ORDERS --------------------

@method_decorator(login_required, name='dispatch')
class OrderListView(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(order_by=self.request.user)


@method_decorator(login_required, name='dispatch')
class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    success_url = '/order/conformed/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = get_object_or_404(
            Product,
            slug=self.kwargs['slug']
        )
        return context

    def form_valid(self, form):
        product = Product.objects.get(
            slug=self.kwargs['slug']
        )

        form.instance.product = product
        form.instance.cost = int(form.instance.count) * int(product.price)

        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class OrderDetailView(DetailView):
    model = Order


# -------------------- THANK YOU PAGE --------------------

def order_conform(request):
    return render(request, "Product/thanks.html")
from django.shortcuts import redirect


@login_required
def add_review(request, slug):

    product = get_object_or_404(
        Product,
        slug=slug
    )

    if request.method == "POST":
        
        existing_review = Review.objects.filter(
            product=product,
            user=request.user
        ).first()

        if existing_review:
            return redirect(
                 "Product_product_detail",
                slug=product.slug
        )

        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)

            review.product = product
            review.user = request.user

            review.save()

            return redirect(
                "Product_product_detail",
                slug=product.slug
            )

    return redirect(
        "Product_product_detail",
        slug=product.slug
    )

# -------------------- DASHBOARD --------------------

@login_required
def dashboard(request):

    try:
        health = UserHealth.objects.get(user=request.user)

        # BMI
        bmi = round(
            health.weight / ((health.height / 100) ** 2),
            2
        )

        # BMR
        if health.gender == "Male":
            bmr = round(
                10 * health.weight +
                6.25 * health.height -
                5 * health.age + 5
            )
        else:
            bmr = round(
                10 * health.weight +
                6.25 * health.height -
                5 * health.age - 161
            )

        # Daily Calories
        if health.activity_level == "Sedentary":
            calories = int(bmr * 1.2)

        elif health.activity_level == "Light":
            calories = int(bmr * 1.375)

        elif health.activity_level == "Moderate":
            calories = int(bmr * 1.55)

        elif health.activity_level == "Active":
            calories = int(bmr * 1.725)

        else:
            calories = int(bmr * 1.9)

        # Water Intake
        water = round(health.weight * 0.035, 1)

        # BMI Status
        if bmi < 18.5:
            bmi_status = "Underweight"
        elif bmi < 25:
            bmi_status = "Normal"
        elif bmi < 30:
            bmi_status = "Overweight"
        else:
            bmi_status = "Obese"

        # ==========================
        # AI Food Recommendation
        # ==========================
        recommended_foods = Product.objects.filter(
            food_type=health.goal
        ).order_by("-protein")[:6]

        # ==========================
        # Dashboard Analytics   
        # ==========================

        orders = Order.objects.filter(
            order_by=request.user
        )

        total_orders = orders.count()

        total_spent = sum(
            order.cost for order in orders
        )

        recent_order = orders.order_by("-created").first()

        favorite_category = ""

        if orders.exists():

             categories = {}

             for order in orders:

                category = order.product.category

                categories[category] = categories.get(category, 0) + 1

                favorite_category = max(
                 categories,
                key=categories.get
    )

    
        # ==========================
        # Recent Orders
        # ==========================

        recent_orders = Order.objects.filter(
        order_by=request.user
        ).order_by("-created")[:5]

    except UserHealth.DoesNotExist:
        health = None
        bmi = 0
        bmr = 0
        calories = 0
        water = 0
        bmi_status = ""
        recommended_foods = Product.objects.none()
        total_orders = 0
        total_spent = 0
        recent_order = None
        favorite_category = ""

    context = {
        "health": health,
        "bmi": bmi,
        "bmr": bmr,
        "calories": calories,
        "water": water,
        "bmi_status": bmi_status,
        "recommended_foods": recommended_foods,
        "recent_orders": recent_orders,

        "total_orders": total_orders,
        "total_spent": total_spent,
        "recent_order": recent_order,
        "favorite_category": favorite_category,

    }

    return render(request, "Product/dashboard.html", context)