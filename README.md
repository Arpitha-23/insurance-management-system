# Insurance Management System

A full-stack web-based Insurance Management System developed using Django and MySQL. The application provides a centralized platform for managing insurance policies, customers, claims, premium payments, agents, commissions, renewals, and reports.

## Features

* User authentication and login
* Customer profile management
* Insurance policy management
* Policy types and status tracking
* Insurance claim submission and processing
* Claim verification and approval workflow
* Premium payment tracking
* Agent management
* Agent commission tracking
* Policy renewal management
* Dashboard with insurance statistics
* Reports and analytics
* Chart.js data visualization
* PDF report generation
* Excel report generation
* Django Admin interface
* MySQL database integration

## Technology Stack

### Backend

* Python
* Django 4.2
* Django REST Framework
* Django ORM

### Database

* MySQL 8.0
* MySQL Workbench

### Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript
* Chart.js

### Reporting

* ReportLab
* OpenPyXL

### Development Tools

* Visual Studio Code
* Git
* GitHub

## Main Modules

### Customer Management

Customers can maintain their personal information and view their insurance-related details.

### Policy Management

The system allows policies to be created and managed with information such as policy number, policy type, premium amount, sum insured, dates, payment frequency, and status.

### Claims Management

Customers and administrators can manage insurance claims, including claim amounts, incident details, verification status, approved amounts, documents, and payment information.

### Premium Tracking

Premium payments can be recorded with payment dates, amounts, payment methods, transaction IDs, receipt numbers, and payment status.

### Agent Management

Insurance agents can be managed with agent codes, company information, license details, commission rates, and active status.

### Renewal Management

The system tracks policy renewals, previous premiums, new premiums, renewal dates, and renewal status.

### Reports & Analytics

The dashboard and reports section provides statistical information about policies, claims, and premium payments using charts and summary cards. Reports can also be exported to PDF and Excel.

## Database

The application uses MySQL as the primary database.

Major entities include:

* User
* CustomerProfile
* InsuranceCompany
* Policy
* Claim
* ClaimDocument
* PremiumPayment
* Agent
* Commission
* PolicyRenewal
* InsuranceProduct

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd insurance_system
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL

Create a MySQL database:

```sql
CREATE DATABASE insurance_db CHARACTER SET utf8mb4;
```

Update the database configuration in:

```text
insurance/settings.py
```

Use your own local MySQL username and password.

### 5. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create an administrator

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Admin panel:

```text
http://127.0.0.1:8000/admin/
```

## Project Structure

```text
insurance_system/
│
├── insurance/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── policies/
│   ├── migrations/
│   ├── templates/
│   │   └── policies/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Security

Sensitive information such as database passwords and environment variables should not be committed to GitHub.

Use environment variables for production credentials.

## Future Improvements

* Online premium payment gateway
* Email/SMS renewal reminders
* Advanced role-based access control
* Insurance product comparison
* Mobile application
* Cloud deployment
* Advanced analytics
* Automated claim verification
* REST API expansion

## Project Purpose

This project was developed as a Python Full Stack internship project to demonstrate practical implementation of Django, MySQL, frontend development, database management, authentication, reporting, and full-stack application development.
