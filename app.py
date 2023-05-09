from flask import Flask, render_template, request, session, redirect, url_for
import random
import time
from initial_stock_prices import stocks

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Define a function to update the values of the stocks
def update_stocks():
    for key in stocks:
        time.sleep(0.7)
        change = round(random.uniform(-10, 10),2)
        if stocks[key] + change > 0:
            stocks[key] += change

# Define a route to display the homepage
@app.route('/')
def index():
    if 'portfolio' not in session:
        session['portfolio'] = {}
    update_stocks()
    return render_template('index.html', stocks=stocks, portfolio=session['portfolio'])

# Define a route to buy a stock
@app.route('/buy', methods=['POST'])
def buy():
    symbol = request.form['symbol']
    quantity = int(request.form['quantity'])
    price = stocks.get(symbol, None)
    if price is None:
        return redirect(url_for('index'))
    cost = price * quantity
    if cost > session.get('balance', 0):
        return redirect(url_for('index'))
    session['balance'] -= cost
    if symbol in session['portfolio']:
        session['portfolio'][symbol]['quantity'] += quantity
    else:
        session['portfolio'][symbol] = {'quantity': quantity, 'price': price}
    session.modified = True
    return redirect(url_for('index'))

# Define a route to sell a stock
@app.route('/sell', methods=['POST'])
def sell():
    symbol = request.form['symbol']
    quantity = int(request.form['quantity'])
    price = stocks.get(symbol, None)
    if price is None or symbol not in session['portfolio']:
        return redirect(url_for('index'))
    if quantity > session['portfolio'][symbol]['quantity']:
        return redirect(url_for('index'))
    revenue = price * quantity
    session['balance'] += revenue
    session['portfolio'][symbol]['quantity'] -= quantity
    if session['portfolio'][symbol]['quantity'] == 0:
        del session['portfolio'][symbol]
    session.modified = True
    return redirect(url_for('index'))

# Define a route to reset the simulation
@app.route('/reset')
def reset():
    session.pop('portfolio', None)
    session['balance'] = 20000
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)