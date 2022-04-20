from django.urls import path
from .views import ItemView, ReceiptView

app_name = "cash_machine"

urlpatterns = [
    path('cash_machine/', ItemView.as_view()),
    path('cash_machine/<int:pk>', ItemView.as_view()),
    path('get_receipt/<int:pk>', ReceiptView.as_view()),
]