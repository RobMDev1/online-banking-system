from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import BankAccount, Loan  # Import the BankAccount model
from .forms import TransactionForm, LoanRequestForm, TransferForm
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.timezone import now
from decimal import Decimal

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')  # Checkbox value

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = redirect('home')  # Redirect to home after login

            # Set the "remember_me" cookie if checkbox is selected
            if remember_me:
                response.set_cookie('remember_me', 'true', max_age=30*24*60*60)  # 30 days
            else:
                response.delete_cookie('remember_me')  # Remove the cookie if not selected

            return response
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})

    return render(request, 'accounts/login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Validate form inputs
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use.")
            return redirect('register')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Log the user in immediately after registration
        login(request, user)

        # Create the BankAccount for the user
        BankAccount.objects.create(
            user=user,
            email=email,
            balance=0.00,  # Initial balance is 0
            has_loan=False,  # No loan initially
            loan_amount=0.00,  # No loan amount
            loan_percent=0.00,  # No loan interest
        )

        return redirect('home')  # Redirect to the home page after successful registration and login
    
    return render(request, 'accounts/register.html')


def logout_view(request):
    try:
        bank_account = BankAccount.objects.get(user=request.user)
        account_id = bank_account.account_id  # Get the account_id
    except BankAccount.DoesNotExist:
        account_id = None  # Handle case where the user does not have a BankAccount

    logout(request)  # This logs out the user
    return redirect('login')  # Redirect to the login page or any other page you prefer


def root_view(request):
    try:
        bank_account = BankAccount.objects.get(user=request.user)
        account_id = bank_account.account_id  # Get the account_id
    except BankAccount.DoesNotExist:
        account_id = None  # Handle case where the user does not have a BankAccount

    # Check if the "remember_me" cookie exists
    if request.COOKIES.get('remember_me') == 'true':
        # Redirect to the home page if "remember_me" is set
        return redirect('home')
    else:
        # Otherwise, redirect to the login page
        return redirect('login')
    
@login_required
def home_view(request):
    try:
        # Retrieve the BankAccount for the logged-in user
        bank_account = BankAccount.objects.get(user=request.user)
        account_id = bank_account.account_id  # Extract account ID
    except BankAccount.DoesNotExist:
        bank_account = None
        account_id = None  # No account ID if no BankAccount exists
    loans = Loan.objects.filter(user=request.user, status='approved')

    # Pass both bank_account and account_id to the template
    return render(request, 'accounts/home.html', {
        'bank_account': bank_account,
        'account_id': account_id,
        'loans': loans,
    })



@login_required
def transaction(request, account_id):
    # Ensure the account_id belongs to the logged-in user
    bank_account = get_object_or_404(BankAccount, account_id=account_id, user=request.user)
    try:
        # Retrieve the BankAccount for the logged-in user
        bank_account = BankAccount.objects.get(user=request.user)
        account_id = bank_account.account_id  # Extract account ID
    except BankAccount.DoesNotExist:
        bank_account = None
        account_id = None  # No account ID if no BankAccount exists
    loans = Loan.objects.filter(user=request.user, status='approved')


    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            transaction_type = form.cleaned_data['transaction_type']

            # Check for sufficient balance if withdrawing
            if transaction_type == 'withdraw' and amount > bank_account.balance:
                messages.error(request, "Insufficient balance for this transaction.")
                return redirect('accounts/transaction', account_id=bank_account.account_id)  # Redirect back to the transaction page

            # Process the transaction
            if transaction_type == 'deposit':
                bank_account.balance += amount
            elif transaction_type == 'withdraw':
                bank_account.balance -= amount
            bank_account.save()

            messages.success(request, f"{transaction_type.capitalize()} successful!")
            return render(request, 'accounts/transaction_success.html', {'account': bank_account, 'account_id': account_id,})
    else:
        form = TransactionForm()

    return render(request, 'accounts/transaction.html', {'form': form, 'account': bank_account, 'account_id': account_id,})
@login_required
def request_loan(request):
    try:
        # Retrieve the BankAccount for the logged-in user
        bank_account = BankAccount.objects.get(user=request.user)
        account_id = bank_account.account_id  # Extract account ID
    except BankAccount.DoesNotExist:
        bank_account = None
        account_id = None  # No account ID if no BankAccount exists
    if request.method == "POST":
        form = LoanRequestForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            Loan.objects.create(user=request.user, amount=amount, interest_rate=Decimal("5.0"))
            messages.success(request, f"Loan request submitted! You requested ${amount:.2f}.")
            return redirect('loan_status')
    else:
        form = LoanRequestForm()
    return render(request, 'accounts/request_loan.html', {'form': form, 'account_id': account_id,})



@login_required
def loan_status(request):
    loans = Loan.objects.filter(user=request.user).order_by('-request_date')
    return render(request, 'accounts/loan_status.html', {'loans': loans})

@staff_member_required
def manage_loans(request):
    loans = Loan.objects.filter(status='pending')

    if request.method == "POST":
        loan_id = request.POST.get('loan_id')
        action = request.POST.get('action')
        loan = Loan.objects.get(id=loan_id)

        if action == 'approve':
            loan.status = 'approved'
            loan.approved_date = now()

            bank_account = BankAccount.objects.get(user=loan.user)

            bank_account.balance += loan.amount
            bank_account.has_loan = True
            bank_account.loan_amount = loan.amount
            bank_account.save()

        elif action == 'reject':
            loan.status = 'rejected'

        loan.save()

    return render(request, 'accounts/manage_loans.html', {'loans': loans})

@login_required
def transfer_money(request):
    try:
        sender_account = BankAccount.objects.get(user=request.user)
        account_id = sender_account.account_id 
    except BankAccount.DoesNotExist:
        sender_account = None
        account_id = None 

    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            recipient_id = form.cleaned_data['recipient_id'] 
            amount = form.cleaned_data['amount']

            try:
                recipient_account = BankAccount.objects.get(account_id=recipient_id)
            except (User.DoesNotExist, BankAccount.DoesNotExist):
                messages.error(request, "Recipient account not found.")
                return redirect('transfer_money')

            if sender_account.balance < amount:
                messages.error(request, "Insufficient balance for this transfer.")
                return redirect('transfer_money')

            print(f"Sender balance before: {sender_account.balance}")
            print(f"Recipient balance before: {recipient_account.balance}")

            sender_account.balance -= amount 
            recipient_account.balance += amount 

            print(f"Sender balance after: {sender_account.balance}")
            print(f"Recipient balance after: {recipient_account.balance}")

            sender_account.save()
            recipient_account.save()

            messages.success(request, f"Successfully transferred ${amount:.2f} to .")
            return redirect('home')

    else:
        form = TransferForm()

    return render(request, 'accounts/transfer_money.html', {'form': form, 'account_id': account_id,})
