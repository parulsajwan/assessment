from django.urls import path
from .views import (
    SignupView,
    LoginView,
    SummaryReportView
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('summary-report/', SummaryReportView.as_view(), name='summary-report'),
]
