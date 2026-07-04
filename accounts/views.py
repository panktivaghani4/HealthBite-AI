from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import SignUpForm
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