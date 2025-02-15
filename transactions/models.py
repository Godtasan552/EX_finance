from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Category(models.Model):
    CATEGORY_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=10, choices=CATEGORY_TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


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
    category = models.ForeignKey(
        Category, 
        related_name='transactions', 
        on_delete=models.CASCADE
    )

    def clean(self):
        """ ตรวจสอบว่าหมวดหมู่ที่เลือกตรงกับประเภทของธุรกรรม """
        if self.category and self.category.type != self.type:
            raise ValidationError("Category type must match transaction type.")

    def save(self, *args, **kwargs):
        self.clean()  # เรียกใช้ clean() เพื่อตรวจสอบก่อนบันทึก
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.get_type_display()} {self.amount} - {self.category.name}"
