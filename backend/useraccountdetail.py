import streamlit as st
import database as conn  

# Function to create a connection to MySQL database
def create_connection():
    return conn.create_connection()

def update_account(username, password, email, role, phone):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        update_query = "UPDATE users SET password = %s, email = %s, role = %s, phone = %s WHERE username = %s"
        cursor.execute(update_query, (password, email, role, phone, username))
        connection.commit()
        st.success('User details updated successfully.')
    except Exception as e:
        st.error(f"Error updating user details: {str(e)}")
        connection.rollback()  
    finally:
        cursor.close()
        connection.close()

def delete_account(username):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        delete_query = "DELETE FROM users WHERE username = %s"
        cursor.execute(delete_query, (username,))
        connection.commit()
        st.success('User deleted successfully.')
    except Exception as e:
        st.error(f"Error deleting user: {str(e)}")
        connection.rollback()  
    finally:
        cursor.close()
        connection.close()

def account_detail(logged_in_username):
    connection = create_connection()
    cursor = connection.cursor()

    st.subheader('User Account Details', divider='rainbow')

    col1, col2 = st.columns(2)

    with col1:
        username = st.text_input('Enter User Name', key="usernameacc", value=logged_in_username, disabled=True)
        password = st.text_input('Enter Password', type="password", key="userpass")
        email = st.text_input('Enter Email Id')

    with col2:
        role = st.selectbox('Select Role:', ('user',), index=0)  
        phone = st.text_input('Enter Phone Number')

    update_button = st.button("Update")
    delete_button = st.button("Delete")

    if update_button:
        update_account(logged_in_username, password, email, role, phone)

    elif delete_button:
        delete_account(logged_in_username)

    cursor.close()
    connection.close()

