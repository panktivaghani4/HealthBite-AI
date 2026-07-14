from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import SignUpForm, UserHealthForm
from .models import UserHealth


class SignUp(CreateView):

    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def form_valid(self, form):

        user = form.save()

        UserHealth.objects.create(
            user=user,
            mobile=form.cleaned_data['mobile'],
            age=form.cleaned_data['age'],
            gender=form.cleaned_data['gender'],
            height=form.cleaned_data['height'],
            weight=form.cleaned_data['weight'],
            goal=form.cleaned_data['goal'],
            activity_level=form.cleaned_data['activity_level']
        )

        return super().form_valid(form)


# ======================================
# My Profile
# ======================================

@login_required
def profile(request):

    health = UserHealth.objects.get(
        user=request.user
    )

    bmi = round(
        health.weight / ((health.height / 100) ** 2),
        2
    )

    if bmi < 18.5:
        bmi_status = "Underweight"

    elif bmi < 25:
        bmi_status = "Normal"

    elif bmi < 30:
        bmi_status = "Overweight"

    else:
        bmi_status = "Obese"

    context = {
        "health": health,
        "bmi": bmi,
        "bmi_status": bmi_status,
    }

    return render(
        request,
        "accounts/profile.html",
        context
    )

    # ======================================
# Edit Profile
# ======================================

@login_required
def edit_profile(request):

    health = UserHealth.objects.get(
        user=request.user
    )

    if request.method == "POST":

        form = UserHealthForm(
            request.POST,
            request.FILES,
            instance=health
        )

        if form.is_valid():

            form.save()

            return redirect("profile")

    else:

        form = UserHealthForm(
            instance=health
        )

    return render(
        request,
        "accounts/edit_profile.html",
        {
            "form": form,
            "health": health,
        }
    )