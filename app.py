from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import pandas as pd
import numpy as np
import re
import os

app = Flask(__name__)

# Load or initialize data from JSON file
DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        # Return an empty list if the file doesn't exist or is empty
        return []
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        # Handle corrupted JSON by returning an empty list
        return []

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def index():
    employees = load_data()
    df = pd.DataFrame(employees)
    
    if not df.empty:
        df['Salary'] = df['Days Worked'] * df['Pay Per Day']
        avg_salary = df['Salary'].mean()
        highest_earner = df.loc[df['Salary'].idxmax()]['Name'] if not df.empty else "N/A"
        lowest_earner = df.loc[df['Salary'].idxmin()]['Name'] if not df.empty else "N/A"
    else:
        avg_salary = 0
        highest_earner = "N/A"
        lowest_earner = "N/A"

    return render_template('index.html', employees=employees, avg_salary=avg_salary,
                           highest_earner=highest_earner, lowest_earner=lowest_earner)

@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        # Validate inputs
        employee_id = request.form['employee_id']
        name = request.form['name']
        email = request.form['email']
        days_worked = int(request.form['days_worked'])
        pay_per_day = int(request.form['pay_per_day'])

        if not re.match(r'^EMP\d{3}$', employee_id):
            return "Invalid Employee ID format (e.g., EMP001).", 400
        if not re.match(r'^[A-Za-z\s]+$', name):
            return "Name must contain only letters.", 400
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            return "Invalid email format.", 400

        # Add employee to data
        employees = load_data()
        employees.append({
            'Employee ID': employee_id,
            'Name': name,
            'Email': email,
            'Days Worked': days_worked,
            'Pay Per Day': pay_per_day
        })
        save_data(employees)
        return redirect(url_for('index'))

    return render_template('add_employee.html')

@app.route('/delete/<string:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    employees = load_data()
    employees = [emp for emp in employees if emp['Employee ID'] != employee_id]
    save_data(employees)
    return redirect(url_for('index'))

@app.route('/attendance')
def attendance():
    employees = load_data()
    return render_template('attendance.html', employees=employees)

# New Route for Mark Attendance
@app.route('/mark_attendance', methods=['GET', 'POST'])
def mark_attendance():
    employees = load_data()
    if request.method == 'POST':
        # Process attendance marking logic here
        employee_id = request.form['employee_id']
        days_worked = int(request.form['days_worked'])

        # Update the employee's days worked
        for emp in employees:
            if emp['Employee ID'] == employee_id:
                emp['Days Worked'] += days_worked
                break

        save_data(employees)
        return redirect(url_for('index'))

    return render_template('mark_attendance.html', employees=employees)

if __name__ == '__main__':
    app.run(debug=True)