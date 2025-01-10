from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
import random
from django.utils.timezone import now

class BankAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    has_loan = models.BooleanField(default=False)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    loan_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Account ID will be a unique 8-digit number
    account_id = models.CharField(max_length=8, unique=True, editable=False)

    def __str__(self):
        return f"{self.user.username}'s Bank Account"

    def generate_unique_account_id(self):
        """Generate a random 8-digit account ID and ensure it is unique."""
        while True:
            # Generate a random 8-digit account ID
            account_id = str(random.randint(10000000, 99999999))

            # Check if the account ID already exists
            if not BankAccount.objects.filter(account_id=account_id).exists():
                return account_id

    def save(self, *args, **kwargs):
        # If this is a new instance, generate a new unique account_id
        if not self.account_id:
            self.account_id = self.generate_unique_account_id()
        
        super().save(*args, **kwargs)

class Loan(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.0)
    total_repayable = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    request_date = models.DateTimeField(auto_now_add=True)
    approved_date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.amount <= 0:
            raise ValueError("Loan amount must be positive.")

        self.total_repayable = self.amount + (self.amount * self.interest_rate / 100)

        if self.status == 'approved' and not self.approved_date:
            self.approved_date = now()

            bank_account = BankAccount.objects.get(user=self.user)
            bank_account.balance += self.amount
            bank_account.has_loan = True
            bank_account.loan_amount = self.amount
            bank_account.save()

        super().save(*args, **kwargs)
