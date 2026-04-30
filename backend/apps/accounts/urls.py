from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import FraudAwareTokenObtainPairView, SignupView, VerifyOTPView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="auth-signup"),
    path("verify-otp/", VerifyOTPView.as_view(), name="auth-verify-otp"),
    path("token/", FraudAwareTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
