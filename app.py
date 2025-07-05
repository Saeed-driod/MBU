from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
import sqlite3
from datetime import datetime, timedelta
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'supersecretkey123'  # Change this in production

USER_FILE = 'userpass.txt'
DEFAULT_USER = 'userpassword'

# Ensure password file exists
if not os.path.exists(USER_FILE):
    with open(USER_FILE, 'w', encoding='utf-8') as f:
        f.write(DEFAULT_USER)

def get_password():
    with open(USER_FILE, 'r', encoding='utf-8') as f:
        return f.read().strip()

def set_password(new_pass):
    with open(USER_FILE, 'w', encoding='utf-8') as f:
        f.write(new_pass)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == DEFAULT_USER and password == get_password():
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('غلط یوزر یا پاسورڈ!')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    msg = ''
    if request.method == 'POST':
        old = request.form.get('old_password')
        new = request.form.get('new_password')
        confirm = request.form.get('confirm_password')
        if old != get_password():
            msg = 'پرانا پاسورڈ غلط ہے!'
        elif new != confirm:
            msg = 'نیا پاسورڈ اور تصدیق میچ نہیں کرتے!'
        elif not new:
            msg = 'نیا پاسورڈ خالی نہیں ہو سکتا!'
        else:
            set_password(new)
            msg = 'پاسورڈ کامیابی سے تبدیل ہو گیا!'
    return render_template('change_password.html', msg=msg)

# ---------- Database Connection ----------
def get_db_connection():
    conn = sqlite3.connect('fruitshop.db')
    conn.row_factory = sqlite3.Row
    return conn

# ---------- Web Pages ----------
@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/new-account')
@login_required
def new_account():
    return render_template('new-account.html')

@app.route('/agrahi')
@login_required
def agrahi():
    return render_template('agrahi.html')

# ---------- API: Accounts ----------
@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    conn = get_db_connection()
    accounts = conn.execute('SELECT * FROM accounts ORDER BY id ASC').fetchall()
    conn.close()
    return jsonify([dict(row) for row in accounts])

@app.route('/api/accounts', methods=['POST'])
def add_account():
    data = request.get_json(force=True)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Calculate total_amount and remaining
    total_amount = data.get('pichla', 0) + data.get('new_item', 0)
    remaining = total_amount - data.get('jama', 0)
    
    cursor.execute('''
        INSERT INTO accounts (date, account_name, new_item, jama, total_amount, remaining)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        data['date'], 
        data['account_name'], 
        data.get('new_item', 0), 
        data.get('jama', 0), 
        total_amount,
        remaining
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Record added successfully"}), 201

@app.route('/api/accounts/<int:id>', methods=['PUT'])
def update_account(id):
    data = request.get_json(force=True)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Calculate total_amount and remaining
    total_amount = data.get('pichla', 0) + data.get('new_item', 0)
    remaining = total_amount - data.get('jama', 0)
    
    cursor.execute('''
        UPDATE accounts
        SET date = ?, account_name = ?, new_item = ?, jama = ?, total_amount = ?, remaining = ?
        WHERE id = ?
    ''', (
        data['date'],
        data['account_name'],
        data.get('new_item', 0),
        data.get('jama', 0),
        total_amount,
        remaining,
        id
    ))
    conn.commit()
    rows_updated = cursor.rowcount
    conn.close()

    if rows_updated > 0:
        return jsonify({"message": "✅ Row updated successfully", "rows_updated": rows_updated}), 200
    else:
        return jsonify({"message": "⚠️ No record updated (ID may not exist)", "rows_updated": 0}), 404

# ---------- API: Agrahi ----------
@app.route('/api/agrahi', methods=['GET'])
def get_agrahi():
    conn = get_db_connection()
    agrahi = conn.execute('SELECT * FROM agrahi ORDER BY id DESC').fetchall()
    conn.close()
    return jsonify([dict(row) for row in agrahi])

@app.route('/api/agrahi', methods=['POST'])
def add_agrahi():
    data = request.get_json(force=True)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Calculate baqaya
    pichla = data.get('pichla', 0)
    new_item = data.get('new_item', 0)
    jama = data.get('jama', 0)
    baqaya = pichla + new_item - jama
    
    cursor.execute('''
        INSERT INTO agrahi (account_name, date, pichla, new_item, jama, baqaya)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        data['account_name'], 
        data['date'], 
        pichla, 
        new_item, 
        jama, 
        baqaya
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Record added successfully"}), 201

# ---------- Print Route ----------
@app.route('/print')
@login_required
def print_accounts():
    conn = get_db_connection()
    accounts = conn.execute('SELECT * FROM accounts ORDER BY id ASC').fetchall()
    conn.close()
    return render_template('print.html', accounts=accounts)

@app.route('/api/daily-report', methods=['GET'])
def daily_report():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Get all records, sorted by date
    cursor.execute('''
        SELECT date, SUM(jama) as total_jama, SUM(new_item) as total_newitem
        FROM accounts
        GROUP BY date
        ORDER BY date ASC
    ''')
    rows = cursor.fetchall()
    conn.close()
    # Build a dict: date -> {jama, newitem}
    date_map = {row['date']: {'jama': row['total_jama'] or 0, 'newitem': row['total_newitem'] or 0} for row in rows}
    # Always start from 2025-02-24
    start_date = datetime.strptime('2025-02-24', '%Y-%m-%d')
    end_date = datetime.today()
    result = []
    prev_baqaya = 29130573
    current_date = start_date
    while current_date <= end_date:
        dstr = current_date.strftime('%Y-%m-%d')
        jama = date_map.get(dstr, {}).get('jama', 0)
        newitem = date_map.get(dstr, {}).get('newitem', 0)
        sabiqa = prev_baqaya
        baqaya = sabiqa + newitem - jama
        result.append({
            'date': dstr,
            'total_sabiqa': sabiqa,
            'total_jama': jama,
            'total_newitem': newitem,
            'total_baqaya': baqaya
        })
        prev_baqaya = baqaya
        current_date += timedelta(days=1)
    result.reverse()
    return jsonify(result)

@app.route('/daily-report')
@login_required
def daily_report_page():
    return render_template('daily_report.html')

# ---------- Run Server ----------
if __name__ == '__main__':
    app.run(debug=True)