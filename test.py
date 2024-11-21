from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Connect to the database
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create Database and Table
def create_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            mobile_number TEXT NOT NULL,
            level TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
create_db()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        mobile_number = request.form['mobile_number']
        level = request.form['level']

        conn = get_db_connection()
        conn.execute('INSERT INTO users (full_name, email, mobile_number, level) VALUES (?, ?, ?, ?)',
                     (full_name, email, mobile_number, level))
        conn.commit()
        conn.close()
        return redirect(url_for('account'))

    return render_template_string('''
        <html>
        <head>
            <title>User Login</title>
            <style>
                body { display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #a0c814; font-family: Arial, sans-serif; }
                .login-container { text-align: center; background-color: rgba(255, 255, 255, 0.9); padding: 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); }
                img { max-width: 150px; height: auto; margin-bottom: 20px; }
                form { display: flex; flex-direction: column; }
                input, select { margin-bottom: 15px; padding: 10px; font-size: 16px; border-radius: 4px; border: 1px solid #ccc; }
                button { background-color: #4CAF50; border: none; color: white; padding: 15px 32px; font-size: 16px; cursor: pointer; }
            </style>
        </head>
        <body>
            <div class="login-container">
                <img src="/static/goeath.jpeg" alt="Goethe Logo">
                <h1>Login</h1>
                <form method="POST">
                    <input type="text" name="full_name" placeholder="Enter your full name" required>
                    <input type="email" name="email" placeholder="Enter your email" required>
                    <input type="text" name="mobile_number" placeholder="Enter your mobile number" required>
                    <select name="level" required>
                        <option value="">Select your level</option>
                        <option value="A1">A1</option>
                        <option value="A2">A2</option>
                        <option value="B1">B1</option>
                        <option value="B2">B2</option>
                    </select>
                    <button type="submit">Submit</button>
                </form>
            </div>
        </body>
        </html>
    ''')

@app.route('/account', methods=['GET', 'POST'])
def account():
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users ORDER BY id DESC LIMIT 1').fetchone()
    conn.close()

    if request.method == 'POST':
        if 'edit' in request.form:
            return redirect(url_for('edit_account'))
        elif 'delete' in request.form:
            conn = get_db_connection()
            conn.execute('DELETE FROM users WHERE id = ?', (user['id'],))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))

    return render_template_string(f'''
        <html>
        <head>
            <title>Account Page</title>
            <style>
                body {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background-color: #a0c814;
                    font-family: Arial, sans-serif;
                }}
                .account-container {{
                    text-align: center;
                    background-color: rgba(255, 255, 255, 0.9);
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                }}
                button {{
                    background-color: #4CAF50;
                    border: none;
                    color: white;
                    padding: 15px 32px;
                    font-size: 16px;
                    margin: 5px;
                    cursor: pointer;
                }}
                button.delete {{
                    background-color: red;
                }}
            </style>
        </head>
        <body>
            <div class="account-container">
                <h1>Your Account</h1>
                <p><strong>Full Name:</strong> {user['full_name']}</p>
                <p><strong>Email:</strong> {user['email']}</p>
                <p><strong>Mobile Number:</strong> {user['mobile_number']}</p>
                <p><strong>Level:</strong> {user['level']}</p>
                <form method="POST">
                    <button type="submit" name="edit">Edit</button>
                    <button type="submit" name="delete" class="delete">Delete</button>
                </form>
            </div>
        </body>
        </html>
    ''')

@app.route('/edit', methods=['GET', 'POST'])
def edit_account():
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users ORDER BY id DESC LIMIT 1').fetchone()

    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        mobile_number = request.form['mobile_number']
        level = request.form['level']

        conn.execute('UPDATE users SET full_name = ?, email = ?, mobile_number = ?, level = ? WHERE id = ?',
                     (full_name, email, mobile_number, level, user['id']))
        conn.commit()
        conn.close()

        return redirect(url_for('account'))

    return render_template_string(f'''
        <html>
        <head>
            <title>Edit Account</title>
            <style>
                body {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background-color: #a0c814;
                    font-family: Arial, sans-serif;
                }}
                .edit-container {{
                    text-align: center;
                    background-color: rgba(255, 255, 255, 0.9);
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                }}
                input, select {{
                    margin-bottom: 15px;
                    padding: 10px;
                    font-size: 16px;
                    border-radius: 4px;
                    border: 1px solid #ccc;
                }}
                button {{
                    background-color: #4CAF50;
                    border: none;
                    color: white;
                    padding: 15px 32px;
                    font-size: 16px;
                    cursor: pointer;
                }}
            </style>
        </head>
        <body>
            <div class="edit-container">
                <h1>Edit Your Account</h1>
                <form method="POST">
                    <input type="text" name="full_name" value="{user['full_name']}" required>
                    <input type="email" name="email" value="{user['email']}" required>
                    <input type="text" name="mobile_number" value="{user['mobile_number']}" required>
                    <select name="level" required>
                        <option value="{user['level']}" selected>{user['level']}</option>
                        <option value="A1">A1</option>
                        <option value="A2">A2</option>
                        <option value="B1">B1</option>
                        <option value="B2">B2</option>
                    </select>
                    <button type="submit">Save Changes</button>
                </form>
            </div>
        </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
