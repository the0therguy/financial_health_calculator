from django.db import models
from django.contrib.auth.models import User

# Create your models here.
MONTH_CHOICES = (
    ('1', 'January'),
    ('2', 'February'),
    ('3', 'March'),
    ('4', 'April'),
    ('5', 'May'),
    ('6', 'June'),
    ('7', 'July'),
    ('8', 'August'),
    ('9', 'September'),
    ('10', 'October'),
    ('11', 'November'),
    ('12', 'December'),
)

HEALTH_CHOICE = (('Excellent', 'Excellent'), ('Good', 'Good'), ('Average', 'Average'), ('Poor', 'Poor'))


class FinancialData(models.Model):
    business_name = models.CharField(max_length=255)
    month_name = models.CharField(max_length=255, choices=MONTH_CHOICES, default='January')
    year = models.IntegerField()
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    debts = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    assets = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    income_ratio = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    debt_to_asset_ratio = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    financial_health_score = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    financial_health_description = models.CharField(max_length=255, choices=HEALTH_CHOICE, default='Average')
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " - " + str(self.year) + " - " + self.month_name + "-" + self.business_name
