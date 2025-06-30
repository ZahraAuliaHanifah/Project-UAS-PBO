from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('penjualan_umkm.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM penjualan').fetchall()

    # Hitung total pendapatan
    total = conn.execute('SELECT SUM(quantity * price) AS total FROM penjualan').fetchone()['total']
    total = total if total is not None else 0

    conn.close()
    return render_template('index.html', data=data, total=total)

@app.route('/add', methods=['POST'])
def add():
    item = request.form['item']
    quantity = request.form['quantity']
    price = request.form['price']
    date = request.form['date']

    conn = get_db_connection()
    conn.execute('INSERT INTO penjualan (item, quantity, price, date) VALUES (?, ?, ?, ?)',
                 (item, quantity, price, date))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM penjualan WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    item = request.form['item']
    quantity = request.form['quantity']
    price = request.form['price']
    date = request.form['date']

    conn = get_db_connection()
    conn.execute('UPDATE penjualan SET item=?, quantity=?, price=?, date=? WHERE id=?',
                 (item, quantity, price, date, id))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)