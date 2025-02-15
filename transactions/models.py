from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    CATEGORY_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=10, choices=CATEGORY_TYPE_CHOICES)  # เพิ่มฟิลด์นี้

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, related_name='transactions', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.get_type_display()} {self.amount} - {self.category.name}"
