# Online Banking System

This project is an **Online Banking System** built using **Python** and **Django**. It provides users with the ability to manage their banking needs online, including:

- User registration and secure login.
- Managing loans (requesting, approving, and rejecting loans).
- Sending money to other users using their unique User ID.
- Viewing and managing account balances.

---

## Distinctiveness and Complexity

This project stands out for the following reasons:

1. **Distinctiveness**:
   - The project combines multiple functionalities that simulate real-world online banking systems.
   - Unlike simpler projects, it incorporates features like loan management, peer-to-peer money transfers, and secure account handling, making it unique.
   - The project demonstrates a practical implementation of financial workflows, including transaction validation, which is not commonly seen in basic Django projects.
   - Custom integrations such as user-specific balances, transaction histories, and loan statuses distinguish this project from generic Django applications. These features were implemented by creating a robust database schema with advanced relationships, including one-to-one and foreign key associations. For instance, the `BankAccount` model tracks user-specific balances with automatic updates upon transactions, ensuring accuracy and reliability. Transaction histories were developed using the `Transaction` model, which records each transfer between users with timestamps and unique references. Loan statuses leverage conditional logic in the `Loan` model, enabling the system to handle various states such as pending, approved, or rejected. These integrations enhance the project’s utility and complexity, providing a seamless and realistic banking experience that goes beyond basic implementations.

2. **Complexity**:
   - It uses Django’s user authentication system with custom enhancements such as hashed passwords and a “Remember Me” feature.
   - Advanced database relationships are implemented:
     - **One-to-One Relationship**: Between `User` and `BankAccount`, ensuring each user has a dedicated financial account.
     - **Foreign Keys**: Linking loans and transactions to users, facilitating accurate tracking of financial data.
   - Loan management involves conditional logic, such as approving or rejecting loans and updating user balances accordingly, requiring careful backend handling.
   - Peer-to-peer money transfers implement safeguards against overdrawn accounts, ensuring that business rules are consistently enforced.
   - The admin panel is customized to allow administrative users to efficiently manage loan requests and oversee financial activities, showcasing backend extensibility.
   - Dynamic updates ensure that all user balances, transactions, and loan statuses are reflected in real-time, adding an interactive layer of complexity. This was achieved using AJAX calls to update specific parts of the web application without reloading the entire page. By leveraging Django’s backend views and JSON responses, combined with JavaScript on the client side, the application ensures real-time consistency of financial data after actions like money transfers or loan approvals. These techniques enhance user experience by making the interface more responsive and interactive.

These aspects highlight the project’s ability to address distinctiveness and complexity requirements, combining user-centric design with backend sophistication to deliver a comprehensive solution.

---

## Features

### 1. User Authentication
- Secure registration and login system.
- Password hashing and validation.
- Functional "Remember Me" button for persistent logins.

### 2. Loan Management
- Users can request loans with specified amounts.
- Admins can approve or reject loan requests.
- Approved loans are credited directly to the user's account balance.

### 3. Fund Transfers
- Users can transfer funds to others using their unique User ID.
- Real-time balance updates after transfers, ensuring data consistency.

### 4. Account Management
- Users can view their current balance and loan status in the dashboard.

---

## Prerequisites

- **Python**: Version 3.8 or higher.
- **Django**: Version 4.0 or higher.
- **Database**: SQLite by default (can be configured to use PostgreSQL or MySQL).

---

## Installation

### Step 1: Clone the Repository
```bash
$ git clone https://github.com/RobMDev1/online-banking-system.git
$ cd online-banking-system
```

### Step 2: Set Up a Virtual Environment
```bash
$ python3 -m venv env
$ source env/bin/activate   # On Windows: env\Scripts\activate
```

### Step 3: Install Dependencies
Install all required Python packages using:
```bash
$ pip install -r requirements.txt
```

### Step 4: Apply Migrations
```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

### Step 5: Create a Superuser (Admin)
```bash
$ python manage.py createsuperuser
```

### Step 6: Run the Development Server
```bash
$ python manage.py runserver
```

Access the application at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## File Descriptions

### Main Files
- **`manage.py`**:
  - Django's command-line utility for administrative tasks.
  - No modifications were made to this file.

- **`requirements.txt`**:
  - Contains a list of all Python dependencies required to run the project.
  - I ensured all necessary packages, such as Django and database connectors, are included.

### App: `accounts`

- **`models.py`**:
  - Defines the database schema for:
    - **`User`**: Extends Django's default `AbstractUser` model to add functionality.
    - **`BankAccount`**: One-to-one relationship with `User`, storing user balances.
    - **`Loan`**: Tracks loan requests, statuses, and amounts linked to users.
    - **`Transaction`**: Records money transfers between users.
  - Custom logic for financial management was added here.

- **`views.py`**:
  - Contains the logic for handling user requests, such as:
    - Registering users.
    - Logging in and out.
    - Transferring money and managing loans.
  - I implemented robust error handling for edge cases (e.g., insufficient balance).

- **`forms.py`**:
  - Handles input validation for registration, login, and loan requests.
  - Custom forms were created to improve user experience and security.

- **`admin.py`**:
  - Configures the admin panel to manage users, loans, and transactions.
  - Added search functionality and filters to improve usability.

- **`migrations/`**:
  - Auto-generated files for database schema changes.
  - These files reflect changes I made in `models.py`.

- **`templates/`**:
  - Contains HTML templates for the user interface.
  - Custom templates were added for pages like registration, login, and the dashboard.
  - Responsive design principles were applied.

- **`static/`**:
  - Stores CSS and JavaScript files for styling and interactivity.
  - I added custom styles to improve the visual appeal and usability.

---

## Usage

### Loan Management (Admin Panel)
- Navigate to `/manage_loans/` while logged in as an admin to manage loan requests(create an admin user beforehand).
- Approve or reject loans. Approved amounts are credited to the user's account balance.

### Sending Money
- Log in as a user.
- Use the transfer feature to send money to another user by entering their unique User ID and the amount.
- Ensure sufficient balance before making a transfer.

---

## Future Enhancements

- **Email Notifications**: Notify users about loan approvals and rejections.
- **Transaction Analytics Dashboard**: Provide users with detailed insights into their transactions.
- **Support Chat**: Add a live support chat feature.
- **Bank Cards**: Integrate virtual or physical bank card functionality.

---

Feel free to reach out with any questions or feedback about the project!

