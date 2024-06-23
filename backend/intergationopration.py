import streamlit as st
import mysql.connector

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="admin",
            database="ticketdb",
            auth_plugin='mysql_native_password'
        )
        return connection
    except mysql.connector.Error as err:
        st.error(f"Error connecting to the database: {err}")
        return None

# Function to read all records from tdatabase table
def read_records(connection):
    try:
        cursor = connection.cursor()
        select_query = "SELECT * FROM tdatabase"
        cursor.execute(select_query)
        records = cursor.fetchall()
        cursor.close()
        return records
    except mysql.connector.Error as err:
        st.error(f"Error reading records: {err}")
        return []

# Function to update a record in tdatabase table
def update_record(connection, user_name, temail, tickettype, tenquiry, ticketid, tproblem, tpriority):
    try:
        cursor = connection.cursor()
        update_query = "UPDATE tdatabase SET user_name = %s, temail = %s, tickettype = %s, tenquiry = %s, ticketid = %s, tproblem = %s, tpriority = %s WHERE user_name = %s"
        cursor.execute(update_query, (user_name, temail, tickettype, tenquiry, ticketid, tproblem, tpriority, user_name))
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as err:
        st.error(f"Error updating the record: {err}")
        return False

# Function to delete a record from tdatabase table
def delete_record(connection, account_name):
    try:
        cursor = connection.cursor()
        delete_query = "DELETE FROM tdatabase WHERE user_name = %s"
        cursor.execute(delete_query, (account_name,))
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as err:
        st.error(f"Error deleting the record: {err}")
        return False

def operation():
    connection = create_connection()
    col1, col2 = st.columns(2)
    if connection:
        action = st.selectbox("Select an Action:", ("Read", "Update", "Delete"))

        if action == "Read":
            st.subheader("Read Records")
            records = read_records(connection)
            if records:
                st.write("All Records:")
                for record in records:
                    st.write(f"ID: {record[0]}, Username: {record[1]}, Email: {record[2]}, Ticket Type: {record[3]}, Ticket Problem: {record[5]}, Priority: {record[6]}")

        elif action == "Update":
            st.subheader("Update Record")
            with col1:
                user_name = st.text_input('Enter User Name',)
                temail = st.text_input('Enter Email',)
                tickettype = st.selectbox('Select Ticket Type:', ('Product Enquiry', 'Problem Enquiry', 'Other Enquiry'))
                if tickettype == "Product Enquiry":
                    tenquiry = st.text_input("Enter Product Enquiry:")
                elif tickettype == "Problem Enquiry":
                    tenquiry = st.text_input("Enter Problem Enquiry:")
                elif tickettype == "Other Enquiry":
                    tenquiry = st.text_input("Enter Other Enquiry:")

            with col2:
                ticketid = st.text_input('Enter Generated Ticket Id')
                tproblem = st.text_input('Enter Ticket Problem')
                tpriority = st.selectbox('Select Priority:', ('HIGH', 'LOW'))

                if st.button("Update"):
                    if update_record(connection, user_name, temail, tickettype, tenquiry, ticketid, tproblem, tpriority):
                        st.success(f"Record with Username '{user_name}' updated successfully!")

        elif action == "Delete":
            st.subheader("Delete Record")
            with col1:
                account_name = st.text_input('Enter User Name')
            if st.button("Delete"):
                if delete_record(connection, account_name):
                    st.success(f"Record with Username '{account_name}' deleted successfully!")

        connection.close()

