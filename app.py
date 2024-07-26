from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import logging

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

# Function to connect to the database
def connect_database():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='abhi2003',
            database='db'
        )
        return conn
    except mysql.connector.Error as err:
        app.logger.error(f"Error connecting to database: {err}")
        return None

# Function to disconnect from the database
def disconnect_database(conn):
    try:
        conn.close()
    except mysql.connector.Error as err:
        app.logger.error(f"Error disconnecting from database: {err}")

# Route to render the index page (dbindex.html)
@app.route('/')
def dbindex():
    app.logger.debug("Rendering dbindex.html")
    return render_template('dbindex.html')

# Route to render the second_view page (second.html)
@app.route('/second.html', methods=['GET', 'POST'])
def second():
    app.logger.debug("Rendering second.html")
    return render_template('second.html')

# Route to handle form submission from sammm.html
@app.route('/sammm.html', methods=['GET', 'POST'])
def sammm():
    if request.method == 'POST':
        app.logger.debug("Handling POST request in /sammm")
        date = request.form['date']
        from_dest = request.form['from']
        to_dest = request.form['to']
        price_per_person = float(request.form['price'])
        num_persons = int(request.form['persons'])
        total_price = price_per_person * num_persons

        conn = connect_database()
        if conn is None:
            return "Database connection error", 500
        cursor = conn.cursor()

        # Insert data into the database
        sql = "INSERT INTO tours (Date, Destination_From, Destination_To, Price_per_Person, Number_of_Persons, Total_Price) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (date, from_dest, to_dest, price_per_person, num_persons, total_price)
        cursor.execute(sql, values)

        conn.commit()
        disconnect_database(conn)

        app.logger.debug("Redirecting to /dbindex")
        return redirect(url_for('dbindex')) 
    app.logger.debug("Rendering sammm.html")
    return render_template('sammm.html')

# Confirmation route
@app.route('/confirmation.html', methods=['GET', 'POST'])
def confirmation():
    app.logger.debug("Rendering confirmation.html")
    return render_template('confirmation.html')

if __name__ == '__main__':
    app.run(debug=True)
