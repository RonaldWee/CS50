import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    users = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
    stocks = db.execute("SELECT symbol, SUM(shares) as t_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING t_shares > 0", user_id=session["user_id"])
    quotes = {}
    stock_value = 0
    for stock in stocks:
        quotes[stock["symbol"]] = lookup(stock["symbol"])
        stock_value += quotes[stock["symbol"]]["price"] * stock["t_shares"]


    cash_left = users[0]["cash"]
    total_value = cash_left + stock_value



    return render_template("summary.html", quotes=quotes, stocks=stocks, total=total_value, cash_left=cash_left)




@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        if quote == None:
            return apology("You must provide a valid symbol", 400)

        shares = request.form.get("shares")
        try:
            shares = int(shares)
        except:
            return apology("You must provide an integer", 400)
        if shares <= 0:
            return apology("You must provide a positive integer", 400)

        user = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

        cash_available = user[0]["cash"]
        total_price = quote["price"] * shares
        if total_price > cash_available:
            return apology("not enough funds", 400)

        db.execute("UPDATE users SET cash = cash - :price WHERE id = :user_id", price=total_price, user_id=session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price_per_share) VALUES(:user_id, :symbol, :shares, :price)",
                    user_id=session["user_id"],
                    symbol=symbol.upper(),
                    shares=shares,
                    price=quote["price"])

        flash("Bought!")

        return redirect("/")





@app.route("/history")
@login_required
def history():
    transactions = db.execute("SELECT symbol, shares, price_per_share, created_at FROM transactions WHERE user_id = :user_id ORDER BY created_at DESC", user_id=session["user_id"])
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("You must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("You must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        flash("Welcome")
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()


    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("You must provide a symbol", 400)
        quote = lookup(symbol)
        if quote == None:
            return apology("You must provide a valid symbol", 400)
        return render_template("quoted.html", quote=quote)




@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        if not username:
            return render_template("apology.html", message="You must provide a username")

        password1 = request.form.get("password1")
        if not password1:
            return render_template("apology.html", message="You must provide a password")

        password2 = request.form.get("password2")
        if not password2:
            return render_template("apology.html", message="You must provide a password")

        if password1 != password2:
            return render_template("apology.html", message="Your passwords must match")

        password = generate_password_hash(password1)

        new = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=password)

        if not new:
            return apology("Username is taken", 400)

        session["user_id"] = new

        return redirect("/")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "GET":
        return render_template("change_password.html")
    else:
        current_password = request.form.get("current_password")
        if not current_password:
            return apology("You must provide current password")

        old_password = db.execute("SELECT hash FROM users WHERE id = :user_id", user_id=session["user_id"])
        if len(old_password) != 1 or not check_password_hash(old_password[0]["hash"], current_password):
            return apology("Invalid current password given", 400)

        new_password = request.form.get("new_password")
        if not new_password:
            return apology("You must provide a new password", 400)
        new_password2 = request.form.get("new_password2")
        if not new_password2:
            return apology("You must provide a new password confirmation", 400)
        if new_password != new_password2:
            return apology("Your passwords must match", 400)

        hash = generate_password_hash(new_password)
        rows = db.execute("UPDATE users SET hash = :hash WHERE id = :user_id", hash=hash, user_id=session["user_id"])

        flash("Password changed successfully")
        return redirect("/")


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    if request.method == "GET":
        return render_template("add_cash.html")
    else:
        cash_to_add = request.form.get("amount")
        try:
            amount = float(cash_to_add)
        except:
            return apology("Amount must be positive")

        db.execute("UPDATE users SET cash = cash + :amount WHERE id= :user_id", amount=amount, user_id=session["user_id"])
        flash("Cash added successfully")
        return redirect("/")




@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "GET":
        stocks = db.execute(
            "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0", user_id=session["user_id"])
        return render_template("sell.html",stocks=stocks)
    else:
        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        if quote == None:
            return apology("You must provide a valid symbol", 400)

        shares = request.form.get("shares")
        try:
            shares = int(shares)
        except:
            return apology("You must provide an integer", 400)
        if shares <= 0:
            return apology("You must provide a positive integer", 400)

        stock = db.execute("SELECT SUM(shares) as shares FROM transactions WHERE user_id = :user_id AND symbol = :symbol GROUP BY symbol",
                            user_id=session["user_id"], symbol=symbol)
        if len(stock) != 1 or stock[0]["shares"] <= 0 or stock[0]["shares"] < shares:
            return apology("You can't sell more than what you own or less than 0", 400)

        total_price = quote["price"] * shares
        db.execute("UPDATE users SET cash = cash + :price WHERE id = :user_id", price=total_price, user_id=session["user_id"])

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price_per_share) VALUES(:user_id, :symbol, :shares, :price)",
                    user_id=session["user_id"],
                    symbol=symbol,
                    shares=-shares,
                    price=quote["price"])
        flash("Sold!")
        return redirect("/")





def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
