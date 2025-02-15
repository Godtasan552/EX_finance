from django.urls import path
from transactions.views import (
    home,
    register,
    user_login,
    user_logout,
    dashboard,
    add_category,
    generate_report,
    transaction_delete,
    transaction_edit,
    add_transaction,
    delete_category,
)

urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path("add-category/", add_category, name="add_category"),
    path("generate-report/", generate_report, name="generate_report"),
    path("transaction/delete/<int:transaction_id>/", transaction_delete, name="transaction_delete"),
    path("transaction/edit/<int:transaction_id>/", transaction_edit, name="transaction_edit"),
    path('add_transaction/', add_transaction, name='add_transaction'),
    path('category/delete/<int:category_id>/', delete_category, name='delete_category'),
]
