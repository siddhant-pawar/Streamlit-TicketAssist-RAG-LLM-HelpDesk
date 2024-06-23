import streamlit as st
import mysql.connector
import openai 
from faker import Faker
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
fake = Faker()
def create_connection():
    try:
        connection = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="admin",
                    database="ticketdb",
                    auth_plugin = 'mysql_native_password'
        )
        return connection
    except mysql.connector.Error as err:
        st.error(f"Error connecting to the database: {err}")
        return None   

def create_record(connection, user_name, temail, tickettype, tenquiry, tproblem):
    try:
        cursor = connection.cursor()
        problem_to_priority = {
            'Account access': 'Low',
            'Billing': 'High',
            'Domains': 'Medium',
            'ESDS VTMScan': 'Medium',
            'eNlight Web VPN': 'Low',
            'Anti Ransomware': 'High',
            'Transfer Disputes': 'Medium',
            'Hosting': 'Medium',
            'Security Tools': 'High',
            'Dedicated Servers': 'Medium',
            'SSL': 'High',
            'VPN Application': 'Low',
            'Abuse Reports and Cases': 'High',
            'Feedback': 'Low'
        }
        priority = problem_to_priority.get(tproblem, 'Low')
        ticketid = f"TID-{fake.unique.random_int(min=1000, max=9999)}"
        query = "SELECT temail FROM tdatabase WHERE temail = %s"
        cursor.execute(query, (temail,))
        result = cursor.fetchone()

        if not result:
            insert_query = "INSERT INTO tdatabase (user_name, temail, tickettype, tenquiry, ticketid, tproblem, tpriority) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (user_name, temail, tickettype, tenquiry, ticketid, tproblem, priority))
            connection.commit()
            # Notify user via email
            send_email(temail, ticketid, tickettype, tproblem)
            print(f"Your ticket ID is: {ticketid}")
            cursor.close()
            return ticketid
        else:
            print("Email already exists in the database.")
            cursor.close()
            return None
    
    except mysql.connector.Error as err:
        print(f"Error creating a new record: {err}")
        return None

def update_record(connection, temail, tickettype, tenquiry):
    try:
        cursor = connection.cursor()
        update_query = "UPDATE tdatabase SET tickettype = %s, tenquiry = %s WHERE temail = %s"
        cursor.execute(update_query, (tickettype, tenquiry, temail))
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error updating the record: {err}")
        return False

def delete_record(connection, ticketid):
    try:
        cursor = connection.cursor()
        delete_query = "DELETE FROM tdatabase WHERE ticketid = %s"
        cursor.execute(delete_query, (ticketid,))
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error deleting the record: {err}")
        return False

# Function to send email notification
def send_email(temail, ticketid, tickettype, tproblem):
    sender_email = "your_email@example.com"  # Update with your email address
    sender_password = "your_password"  # Update with your email password

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = temail
    message['Subject'] = f"Ticket Created: {ticketid}"
    body = f"Dear User,\n\nYour ticket with ID {ticketid} has been successfully created.\n\nType: {tickettype}\nProblem: {tproblem}\n\nThank you."
    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp_server:  # Update with your SMTP server details
            smtp_server.starttls()
            smtp_server.login(sender_email, sender_password)
            smtp_server.sendmail(sender_email, temail, message.as_string())
            print(f"Email sent to {temail} successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def fetch_last_inserted_data(connection):
    try:
        cursor = connection.cursor()
        query = "SELECT tproblem, tpriority FROM tdatabase ORDER BY tpriority ASC LIMIT 5"
        cursor.execute(query)
        last_inserted_data = cursor.fetchall()
        cursor.close()
        return last_inserted_data
    except mysql.connector.Error as err:
        print(f"Error fetching last inserted data: {err}")
        return None

def fetch_ticketid_record(connection, temail):
    try:
        cursor = connection.cursor()
        query = "SELECT ticketid FROM tdatabase WHERE temail = %s"
        cursor.execute(query, (temail,))
        ticket_ids = cursor.fetchall()
        cursor.close()
        return ticket_ids
    except mysql.connector.Error as err:
        st.error(f"Error fetching ticket IDs: {err}")
        return []
def calculate_priority(ticket):
    current_date = datetime.now().date()
    ticket_date = ticket['date'].date()
    age = (current_date - ticket_date).days
    return age

def priority():
    now = datetime.now()
    lastprevious_month = now - timedelta(days=80)
    lastprevious_month20 = now - timedelta(days=20)
    lastprevious_month10 = now - timedelta(days=10)
    
    previous_month80 = lastprevious_month.month
    previous_month20 = lastprevious_month20.month
    previous_month10 = lastprevious_month10.month
    
    tickets = [
        {'id': 1, 'date': datetime(now.year, previous_month80, 30)},
        {'id': 2, 'date': datetime(now.year, previous_month80, 25)},
        {'id': 3, 'date': datetime(now.year, previous_month80, 15)},
        {'id': 4, 'date': datetime(now.year, previous_month20, 10)},
        {'id': 5, 'date': datetime(now.year, previous_month10, 1)}
    ]
    
    for ticket in tickets:
        ticket['priority'] = calculate_priority(ticket)
    
    # Sort tickets based on priority (in ascending order)
    tickets = sorted(tickets, key=lambda x: x['priority'])
    
    priority_levels = {
        'high': 35,
        'medium': 20,
        'low': 10
    }
    
    selected_priority = st.selectbox('Select Priority Level', options=list(priority_levels.keys()))
    
    for ticket in tickets:
        priority = ticket['priority']
        if priority >= priority_levels[selected_priority]:
            st.markdown(f"<font color='red'>Ticket #{ticket['id']}: Priority - {priority} days</font>", unsafe_allow_html=True)
        else:
            st.markdown(f"<font color='green'>Ticket #{ticket['id']}: Priority - {priority} days</font>", unsafe_allow_html=True)

