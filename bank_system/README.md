
# Online Banking System

This project is an **Online Banking System** built using **Python** and **Django**. The system allows users to perform basic banking operations, including:

- User registration and login.
- Managing loans (requesting, approving, and rejecting loans).
- Sending money to other users using their User ID.
- Viewing account balance.

---

## Distinctiveness and Complexity

I believe that this project is distinct and complex, because I have not yet seen anyone in the community make such a project and it utilizes the skills learned from the course. The project includes P2P interactions, loaning system and 
each user has their unique balance, id, mail etc.

## Features

### 1. User Authentication
- Secure registration and login system.
- Password hashing and validation.
- Functional Remember me button

### 2. Loan Management
- Users can request loans.
- Admin can approve or reject loan requests.
- Approved loan amount is added to the balance.
- Approved loan amounts are added to the user's balance.

### 3. Fund Transfer
- Users can send money to other users using their unique User ID.
- Real-time balance updates after each transfer.

### 4. Account Management
- Users can view their current balance.

---

## Prerequisites

- Python 3.8+
- Django 4.0+
- A database (SQLite is used by default, but you can configure PostgreSQL or MySQL).

---

## Installation

### Step 1: Clone the Repository
```bash
$ git clone https://github.com/RobMDev1/online-banking-system.git
$ cd bank_system
```

### Step 2: Set Up a Virtual Environment
```bash
$ python3 -m venv env
$ source env/bin/activate   # On Windows: env\Scripts\activate
```

### Step 3: Apply Migrations
```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

### Step 4: Create a Superuser (Admin)
```bash
$ python manage.py createsuperuser
```

### Step 5: Run the Development Server
```bash
$ python manage.py runserver
```

Access the application at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## Usage

### Loan Management (Admin Panel)
- Navigate to `/manage_loans/` as an admin.
- Approve or reject loan requests.
- Approved loan amounts will be credited to the user's account.

### Sending Money
- Users can transfer money to another user by providing the recipient's User ID and the amount.
- Ensure sufficient balance before transferring funds.

---

## Models Overview

### User
- Inherits Django's default User model.

### BankAccount
- Linked to the User model (OneToOne relationship).
- Stores user balance.

### Loan
- Linked to the User model.
- Tracks loan requests, statuses, and amounts.

### Transaction
- Records details of money transfers between users.

---

## Project Structure
```
project-root/
|
├── accounts/
|   ├── migrations/          # Database migrations
|   ├── templates/accounts/  # HTML templates
|   ├── models.py            # Application models
|   ├── views.py             # Application views
|   ├── forms.py             # Application forms
|   ├── admin.py             # Application admin 
|
├── static/                  # Static files (CSS, JS)
|
├── templates/               # Project-wide templates
|
├── manage.py                # Django management script
|
└──
```

---

## Future Enhancements

- Add email notifications for loan approvals and rejections.
- Implement a dashboard for viewing transaction analytics.
- Add live support chat.
- Add Cards.

