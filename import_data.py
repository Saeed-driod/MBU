import sqlite3
import csv

def import_data():
    # Connect to SQLite database
    conn = sqlite3.connect('fruitshop.db')
    cursor = conn.cursor()
    
    # Read CSV file and insert data into accounts table
    with open('MalikBota/account.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Convert empty strings to 0 for numeric fields
            remaining = float(row['remaining']) if row['remaining'] else 0
            submite = float(row['submite']) if row['submite'] else 0
            newitem = float(row['newitem']) if row['newitem'] else 0
            total = float(row['total']) if row['total'] else 0
            
            cursor.execute("""
                INSERT INTO accounts (date, account_name, new_item, jama, total_amount, remaining)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                row['tareekh'],
                row['naam'],
                newitem,
                submite,  # submite maps to jama
                total,
                remaining
            ))
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Data imported successfully!")

if __name__ == '__main__':
    import_data()