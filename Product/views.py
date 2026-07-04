from django.views.generic import DetailView, ListView, CreateView
from .models import Product, Order
from .forms import OrderForm, SearchForm
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.models import UserHealth

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

    context = {
        "health": health,
        "bmi": bmi,
        "bmr": bmr,
        "calories": calories,
        "water": water,
        "bmi_status": bmi_status,
        "recommended_foods": recommended_foods,
        "recent_orders": recent_orders,
    }

    return render(request, "Product/dashboard.html", context)