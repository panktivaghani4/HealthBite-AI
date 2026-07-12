from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),

    # ==========================
    # My Profile
    # ==========================
    path('profile/', views.profile, name='profile'),
]