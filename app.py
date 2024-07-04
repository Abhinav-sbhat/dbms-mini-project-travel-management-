import mysql.connector
from flask import Flask, render_template, request, redirect, url_for
import setting as sett
from connector import connect_database , disconnect_database

app = Flask(__name__)

# Function to create the tours table if it doesn't exist
def create_table():
    conn = connect_database()
    cursor = conn.cursor()

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS tours (
        Date DATE,
        Destination_From VARCHAR(50),
        Destination_To VARCHAR(50),
        Price_per_Person INT,
        Number_of_Persons INT,
        Total_Price INT
    );
    '''

    cursor.execute(create_table_query)
    conn.commit()
    conn.close()

# Route for the booking form
@app.route('/', methods=['GET', 'POST'])
def booking_form():
    if request.method == 'POST':
        date = request.form['date']
        from_dest = request.form['from']
        to_dest = request.form['to']
        price_per_person = request.form['price']
        num_persons = request.form['persons']
        total_price = request.form['total']

        # Store data in the database
        conn = connect_database()
        cursor = conn.cursor()

        insert_query = '''
        INSERT INTO tours (Date, Destination_From, Destination_To, Price_per_Person, Number_of_Persons, Total_Price)
        VALUES (%s, %s, %s, %s, %s, %s)
        '''

        # Execute the query with parameters
        cursor.execute(insert_query, (date, from_dest, to_dest, price_per_person, num_persons, total_price))

        # Commit the transaction
        conn.commit()

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Redirect to confirmation page after successful insertion
        return redirect(url_for('confirmation'))

    # Render the booking form template for GET requests
    return render_template('booking_form.html')

# Route for confirmation page
@app.route('/confirmation')
def confirmation():
    # Render the confirmation page template
    return render_template('confirmation.html')

# Initialize the database and run the Flask application
if __name__ == '__main__':
    create_table()  # Ensure the table is created when the application starts
    app.run(debug=True)