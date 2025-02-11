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
]
