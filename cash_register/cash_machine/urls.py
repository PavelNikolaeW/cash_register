from django.urls import path
from .views import ItemView

app_name = "cash_machine"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('cash_machine/', ItemView.as_view()),
    path('cash_machine/<int:pk>', ItemView.as_view()),
]