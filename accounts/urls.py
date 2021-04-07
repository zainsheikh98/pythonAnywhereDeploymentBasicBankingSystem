from django.urls import path
from .views import signupView, transactionView, transactionLISTView, usersListView
from rest_framework.routers import DefaultRouter  

urlpatterns = [
    path('signup/', signupView.as_view(), name="signup"),
    path('send/', transactionView.as_view(), name="transaction"),
    path('transactions/', transactionLISTView.as_view(), name="Transactions_History"),
    path('users/', usersListView.as_view(), name="Users_List"),
]