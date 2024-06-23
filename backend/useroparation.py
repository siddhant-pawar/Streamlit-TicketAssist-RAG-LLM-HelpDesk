import streamlit as st
import mysql.connector

# Function to create a connection to MySQL database
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

# Function to read records for the logged-in user from tdatabase table
def read_user_records(connection, logged_in_username):
    try:
        cursor = connection.cursor()
        select_query = "SELECT * FROM tdatabase WHERE user_name = %s"
        cursor.execute(select_query, (logged_in_username,))
        records = cursor.fetchall()
        cursor.close()
        return records
    except mysql.connector.Error as err:
        st.error(f"Error reading records: {err}")
        return []

# Function to update a record for the logged-in user in tdatabase table
def update_user_record(connection, logged_in_username, temail, tickettype, tenquiry, ticketid, tproblem, tpriority):
    try:
        cursor = connection.cursor()
        update_query = "UPDATE tdatabase SET temail = %s, tickettype = %s, tenquiry = %s, ticketid = %s, tproblem = %s, tpriority = %s WHERE user_name = %s AND ticketid = %s"
        cursor.execute(update_query, (temail, tickettype, tenquiry, ticketid, tproblem, tpriority, logged_in_username, ticketid))
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as err:
        st.error(f"Error updating the record: {err}")
        return False

# Function to delete a record for the logged-in user from tdatabase table
def delete_user_record(connection, logged_in_username, ticketid):
    try:
        cursor = connection.cursor()
        delete_query = "DELETE FROM tdatabase WHERE user_name = %s AND ticketid = %s"
        cursor.execute(delete_query, (logged_in_username, ticketid))
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as err:
        st.error(f"Error deleting the record: {err}")
        return False

# Main function to operate the Streamlit UI
def useroperation(logged_in_username):
    connection = create_connection()
    col1, col2 = st.columns(2)
    if connection:
        action = st.selectbox("Select an Action:", ("Read", "Update", "Delete"))

        if action == "Read":
            st.subheader(f"Read Records for User: {logged_in_username}")
            records = read_user_records(connection, logged_in_username)
            if records:
                st.write("All Records:")
                for record in records:
                    st.write(f"ID: {record[0]}, Username: {record[1]}, Email: {record[2]}, Ticket Type: {record[3]}, Ticket Problem: {record[5]}, Priority: {record[6]}")

        elif action == "Update":
            st.subheader("Update Record")
            with col1:
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
                    if update_user_record(connection, logged_in_username, temail, tickettype, tenquiry, ticketid, tproblem, tpriority):
                        st.success(f"Record updated successfully!")

        elif action == "Delete":
            st.subheader("Delete Record")
            with col1:
                ticketid = st.text_input('Enter Ticket Id')
            if st.button("Delete"):
                if delete_user_record(connection, logged_in_username, ticketid):
                    st.success(f"Record deleted successfully!")

        # Close the database connection
        connection.close()

# Assuming you have a way to authenticate and retrieve the logged-in username
#logged_in_username = "example_user"  # Replace with actual logged-in user's username

#if __name__ == '__main__':
#    useroperation(logged_in_username)
