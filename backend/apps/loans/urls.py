from django.urls import path

from .views import ApplyLoanView

urlpatterns = [
    path("apply/", ApplyLoanView.as_view(), name="loan-apply"),
]

