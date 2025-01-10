from django import forms
from django.contrib.auth.models import User
from .models import BankAccount

class TransactionForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
    ]
    transaction_type = forms.ChoiceField(choices=TRANSACTION_TYPE_CHOICES)

class LoanRequestForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label="Loan Amount")

class TransferForm(forms.Form):
    recipient_id = forms.IntegerField(label="Recipient ID")  # Accept recipient's ID
    amount = forms.DecimalField(label="Amount", max_digits=10, decimal_places=2)