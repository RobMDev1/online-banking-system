from django.contrib import admin
from django.urls import path
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.root_view, name='root'),
    path('home/', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('transaction/<int:account_id>/', views.transaction, name='transaction'),
    path('request_loan/', views.request_loan, name='request_loan'),
    path('loan_status/', views.loan_status, name='loan_status'),
    path('manage_loans/', views.manage_loans, name='manage_loans'),
    path('transfer/', views.transfer_money, name='transfer_money'),
]