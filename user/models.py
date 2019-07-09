from django.db import models
from decimal import Decimal
from django.db.models import F
from math import fabs
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('consumer', 'Consumer'),
        ('executor', 'Executor'),
    )

    role = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)

    def update_balance(self, money, task):
        log_filter = {'user': self, 'task': task, 'debit': fabs(money) if money < 0 else 0,
                      'credit': fabs(money) if money > 0 else 0}
        current_balance = User.objects.get(id=self.id).balance
        log_filter['balance'] = current_balance + Decimal(money)

        LogTransaction.objects.get_or_create(**log_filter)

        User.objects.select_for_update().filter(id=self.id).update(balance=F('balance') + Decimal(money))


class LogTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey('task.Task', on_delete=models.CASCADE, default=None, null=True)
    date = models.DateTimeField(auto_now_add=True)
    debit = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0)
