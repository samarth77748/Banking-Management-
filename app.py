import mysql.connector
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret123"

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="roshani",
    database="bankdb"
)

cursor = db.cursor()

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('login.html')


# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        cursor = db.cursor()
        query = "SELECT * FROM users WHERE username=%s AND password=%s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]
            return redirect('/dashboard')
        else:
            return "Invalid username or password"

    return render_template('login.html')
# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html')
    return redirect('/')


# ---------------- CREATE ACCOUNT ----------------
import random

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        name = request.form.get('name')
        mobile = request.form.get('mobile')
        email = request.form.get('email')
        amount = request.form.get('amount')

        account_number = str(random.randint(1000000000, 9999999999))

        cursor.execute(
            "INSERT INTO accounts (account_number, name, mobile, email, balance) VALUES (%s, %s, %s, %s, %s)",
            (account_number, name, mobile, email, amount)
        )
        db.commit()

        return render_template(
            'success.html',
            account_number=account_number,
            name=name,
            mobile=mobile,
            email=email,
            amount=amount
        )

    return render_template('create_account.html')
# ---------------- DEPOSIT ----------------
@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if request.method == 'POST':
        username = request.form.get('username')
        amount = int(request.form.get('amount'))

        cursor.execute(
            "UPDATE users SET balance = balance + %s WHERE username = %s",
            (amount, username)
        )
        db.commit()

        return "Amount deposited successfully"

    return render_template('deposit.html')


# ---------------- WITHDRAW ----------------
@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if request.method == 'POST':
        username = request.form.get('username')
        amount = int(request.form.get('amount'))

        cursor.execute(
            "SELECT balance FROM users WHERE username=%s",
            (username,)
        )
        result = cursor.fetchone()

        if result and result[0] >= amount:
            cursor.execute(
                "UPDATE users SET balance = balance - %s WHERE username = %s",
                (amount, username)
            )
            db.commit()
            return "Withdrawal successful"
        else:
            return "Insufficient balance or user not found"

    return render_template('withdraw.html')


# ---------------- BALANCE ----------------
@app.route('/balance', methods=['GET', 'POST'])
def balance():
    if request.method == 'POST':
        username = request.form.get('username')

        cursor.execute(
            "SELECT balance FROM users WHERE username=%s",
            (username,)
        )
        result = cursor.fetchone()

        if result:
            return f"Your Balance is {result[0]}"
        else:
            return "User not found"

    return render_template('balance.html')


# ---------------- TRANSACTION ----------------
@app.route('/transaction')
def transaction():
    cursor.execute("SELECT username, 'info', balance, NOW() FROM users")
    data = cursor.fetchall()

    return render_template('transaction.html', data=data)


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


# ---------------- RUN APP ----------------
if __name__ == '__main__':
    print ("Server Starting ..." )
app.run(debug=True)