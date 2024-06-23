import streamlit as st
import database as conn  # Assuming this file has the create_connection() function

# Assuming create_connection() returns a valid connection
connection = conn.create_connection()
cursor = connection.cursor()

def update_account(username, password, email, role, phone):
    try:
        # Check if the username already exists
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()

        if user is None:
            st.error('User does not exist.')
        else:
            # Update the existing user details
            update_query = "UPDATE users SET password = %s, email = %s, role = %s, phone = %s WHERE username = %s"
            cursor.execute(update_query, (password, email, role, phone, username))
            connection.commit()
            st.success('User details updated successfully.')

    except Exception as e:
        st.error(f"Error: {str(e)}")
        connection.rollback()  # Rollback any changes if an error occurs

def delete_account(username):
    try:
        # Check if the username exists
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()

        if user is None:
            st.error('User does not exist.')
        else:
            # Delete the user from the database
            delete_query = "DELETE FROM users WHERE username = %s"
            cursor.execute(delete_query, (username,))
            connection.commit()
            st.success('User deleted successfully.')

    except Exception as e:
        st.error(f"Error: {str(e)}")
        connection.rollback()  # Rollback any changes if an error occurs

def account_detailadmin():
    st.subheader('User Account Details', divider='rainbow')

    col1, col2 = st.columns(2)

    with col1:
        username = st.text_input('Enter User Name', key="usernameacc")
        password = st.text_input('Enter Password', type="password", key="userpass")
        email = st.text_input('Enter Email Id')

    with col2:
        role = st.selectbox('Select Role:', ('user',))  # Ensure the tuple has a comma to make it a tuple
        phone = st.text_input('Enter Phone Number')

    # Buttons for Submit, Update, and Delete
    submit_button = st.button("Submit")
    update_button = st.button("Update")
    delete_button = st.button("Delete")

    if submit_button:
        try:
            # Check if the username already exists
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            user = cursor.fetchone()

            if user is None:
                # Insert the new user into the database
                insert_query = "INSERT INTO users (username, password, email, role, phone) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(insert_query, (username, password, email, role, phone))
                connection.commit()
                st.success('User details added successfully!')
            else:
                st.error('User already exists.')

        except Exception as e:
            st.error(f"Error: {str(e)}")
            connection.rollback()  # Rollback any changes if an error occurs

    elif update_button:
        update_account(username, password, email, role, phone)

    elif delete_button:
        delete_account(username)

@st.cache(allow_output_mutation=True)
def create_connection():
    return conn.create_connection()

if __name__ == '__main__':
    account_detailadmin()
