from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('IN', 'Income'),
        ('OUT', 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    description = models.CharField(max_length=255, blank=True, null=True)
    tags = models.ManyToManyField('Tag', related_name='transactions')

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} on {self.date}"
