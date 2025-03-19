from django.urls import path
from .views.activation_view import MerchantActivateView
from .views.profile_comple_view import MerchantCompleteProfileView
from .views.login import MerchantLoginView
from .views.registration_view import MerchantRegisterView


urlpatterns = [
    path("register/", MerchantRegisterView.as_view(), name="merchant-register"),
    path("activate/", MerchantActivateView.as_view(), name="merchant-activate"),
    path(
        "complete-profile/",
        MerchantCompleteProfileView.as_view(),
        name="merchant-complete-profile",
    ),
    path("login/", MerchantLoginView.as_view(), name="merchant-login"),
]
