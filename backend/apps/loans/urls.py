from django.urls import path

from .views import ApplyLoanView, LoanListView

urlpatterns = [
    path("", LoanListView.as_view(), name="loan-list"),
    path("apply/", ApplyLoanView.as_view(), name="loan-apply"),
]

