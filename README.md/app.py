from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL

from functools import wraps
from flask import session, redirect, url_for, flash
app = Flask(__name__)
app.secret_key = "explore_bharat_secret_key_2024"

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rajee'
app.config['MYSQL_DB'] = 'bvcdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# ============== HOME PAGES ==============
@app.route("/")
def home():
    return render_template("home.html")

@app.route('/homeaccess')
def homeaccess():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('homeaccess.html')


@app.route("/about")
def about():
    return render_template("about.html")

# ============== AUTHENTICATION ==============
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        first_name = request.form.get('firstName', '').strip()
        last_name = request.form.get('lastName', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        dob = request.form.get('dob', None)
        phone = request.form.get('phone', '').strip()

        # Validation
        if not all([first_name, last_name, email, password, confirm_password, phone]):
            flash("Please fill in all required fields.", "error")
            return redirect(url_for('register'))
            
        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for('register'))
            
        if len(password) < 4 or len(password) > 10:
            flash("Password must be 4-10 characters long.", "error")
            return redirect(url_for('register'))
            
        if len(first_name) < 4 or len(last_name) < 4:
            flash("First and last name must be at least 4 characters.", "error")
            return redirect(url_for('register'))
            
        if len(phone) != 10 or not phone.isdigit():
            flash("Phone number must be exactly 10 digits.", "error")
            return redirect(url_for('register'))

        hashed_password = password


        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT id FROM users WHERE email = %s", (email,))
            existing_user = cur.fetchone()
            
            if existing_user:
                flash("Email already registered. Please use a different email.", "error")
                cur.close()
                return redirect(url_for('register'))

            cur.execute(
                """INSERT INTO users (first_name, last_name, email, password, dob, phone) 
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (first_name, last_name, email, hashed_password, dob, phone)
            )
            
            mysql.connection.commit()
            cur.close()

            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))
            
        except Exception as e:
            flash("An error occurred during registration.", "error")
            print(f"Registration error: {e}")
            return redirect(url_for('register'))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            flash("Please enter both email and password.", "error")
            return redirect(url_for('login'))

        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT id, password, first_name FROM users WHERE email = %s", (email,))
            user = cur.fetchone()
            cur.close()

            if user and user['password'] == password:

                session['user_id'] = user['id']
                session['email'] = email
                session['name'] = user['first_name']
                
                flash(f"Welcome back, {user['first_name']}!", "success")
                return redirect(url_for('homeaccess'))
            else:
                flash("Invalid email or password.", "error")
                return redirect(url_for('login'))
                
        except Exception as e:
            flash("An error occurred during login.", "error")
            print(f"Login error: {e}")
            import traceback
            traceback.print_exc()
            return redirect(url_for('login'))

    return render_template("login.html")

@app.route("/logout")
def logout():
    name = session.get('name', 'User')
    session.clear()
    flash(f"Goodbye {name}! You have been logged out.", "success")
    return redirect(url_for("home"))

# ============== CONTACT ==============
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                """INSERT INTO contact_messages (name, email, phone, days, address, message)
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (
                    request.form["name"],
                    request.form["email"],
                    request.form["phone"],
                    request.form["days"],
                    request.form["address"],
                    request.form["message"],
                )
            )
            mysql.connection.commit()
            cur.close()
            flash("✅ Contact submitted successfully!", "success")
        except Exception as e:
            flash("Error submitting contact form.", "error")
            print(f"Contact error: {e}")
        return redirect(url_for("contact"))

    return render_template("contact.html")

# ============== PROTECTED PLACE ROUTES ==============

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("You have to login first.", "error")
            return redirect(url_for('kerala'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/kerala")
def kerala():
    if 'user_id' not in session:
        flash("Please log in to access places.", "error")
        return redirect(url_for('login'))
    return render_template("kerala.html")

@app.route("/punjab")
def punjab():
    if 'user_id' not in session:
        flash("Please log in to access places.", "error")
        return redirect(url_for('login'))
    return render_template("punjab.html")

@app.route("/rajasthan")
def rajasthan():
    if 'user_id' not in session:
        flash("Please log in to access places.", "error")
        return redirect(url_for('login'))
    return render_template("rajasthan.html")

@app.route("/tamilnadu")
def tamilnadu():
    if 'user_id' not in session:
        flash("Please log in to access places.", "error")
        return redirect(url_for('login'))
    return render_template("tamilnadu.html")

@app.route("/uttarpradesh")
def uttarpradesh():
    if 'user_id' not in session:
        flash("Please log in to access places.", "error")
        return redirect(url_for('login'))
    return render_template("uttarpradesh.html")

@app.route("/uttarakhand")
def uttarakhand():
    if 'user_id' not in session:
        flash("Please log in to access places.", "error")
        return redirect(url_for('login'))
    return render_template("uttarakhand.html")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)