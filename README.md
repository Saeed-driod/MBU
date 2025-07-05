# Malik Boota And Brothers - Financial Management System

A web-based financial management system for Malik Boota And Brothers, built with Flask and SQLite.

## Setup Instructions

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize the database:
```bash
python database_setup.py
```

3. Start the Flask server:
```bash
python app.py
```

4. Open your web browser and navigate to:
```
http://localhost:5000
```

## Features

1. نیا کھاتا (New Account)
   - Create new customer accounts
   - Track new items, credits, and remaining balances
   - View all account records

2. اگرائی (Agrahi)
   - Record agrahi transactions
   - Auto-populate previous balance from accounts
   - Calculate remaining balance
   - View all agrahi records

## Database Structure

The system uses SQLite3 with two main tables:

1. `accounts` - For new account entries
2. `agrahi` - For agrahi transactions

## Usage

1. To create a new account:
   - Click on نیا کھاتا
   - Fill in the account details
   - Submit the form

2. To record an agrahi:
   - Click on اگرائی
   - Select the customer name
   - Previous balance will auto-populate
   - Enter new items and credits
   - Submit the form 