import streamlit as st
import database as conn  
from register import register_user
from streamlit_option_menu import option_menu
from home import home_admin, home_user
from account_details import account_detailadmin
from video import videos, show_videos
from listalldata import filter_dataframe, fetch_data
from intergationopration import operation
from useroparation import useroperation
from useraccountdetail import account_detail
from llmper import show_upload_interface

def create_connection():
    try:
        connection = conn.create_connection()
        return connection
    except Exception as e:
        st.error(f"Error connecting to the database: {str(e)}")
        return None

def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'logged_in_user' not in st.session_state:
        st.session_state['logged_in_user'] = None
    if 'role' not in st.session_state:
        st.session_state['role'] = None

def login():
    connection = create_connection()
    if not connection:
        st.error("Failed to connect to the database.")
        return

    cursor = connection.cursor()
    
    try:
        init_session_state()

        if not st.session_state['logged_in']:
            st.title('Login')
            username = st.text_input('Username', key='mainUsername')
            password = st.text_input('Password', type='password', key="mainpass")

            if st.button('Login', key="loginkey"):
                cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
                user = cursor.fetchone()

                if user is not None:
                    st.session_state['logged_in'] = True
                    st.session_state['logged_in_user'] = user[1]  
                    st.session_state['role'] = user[4]  

                    if st.session_state['role'] == 'admin':
                        admin_actions(connection)
                    else:
                        user_actions(connection, user[1])
                else:
                    st.error('Invalid username or password.')

        else:
            if st.session_state['role'] == 'admin':
                admin_actions(connection)
            else:
                user_actions(connection, st.session_state['logged_in_user'])

    except Exception as e:
        st.error(f"Error: {str(e)}")

    finally:
        cursor.close()
        connection.close()

def admin_actions(connection):
    with st.sidebar:
        selected = option_menu("Main Menu", ["Home", 'List All Data', 'Ticket Operation', 'Upload LLM','Add Users', 'Add Videos', 'Sign Out'],
                              icons=['house', 'gear'], menu_icon="cast", default_index=0)
        selected

    if selected == "Home":
        home_admin()

    elif selected == "List All Data":
        query = "SELECT * FROM tdatabase"
        data = fetch_data(connection, query)
        st.dataframe(filter_dataframe(data))

    elif selected == "Ticket Operation":
        operation()

    elif selected == "Add Users":
        registeruser, accountdetail = st.tabs(["Register user", "Account detail"])

        with registeruser:
            register_user(role='admin')
        with accountdetail:
            account_detailadmin()
    elif selected == "Upload LLM":
        show_upload_interface()

    elif selected == "Add Videos":
        videos()

    elif selected == "Sign Out":
        clear_session()

def user_actions(connection, username):
    with st.sidebar:
        selected2 = option_menu("User Menu", ["Home", 'Account Details', 'User Operation', 'Operations Videos', 'Sign Out'],
                               icons=['house', 'gear'], menu_icon="cast", default_index=0)
        selected2

    if selected2 == "Home":
        home_user()

    elif selected2 == "Account Details":
        account_detail(username)

    elif selected2 == "User Operation":
        useroperation(username)

    elif selected2 == "Operations Videos":
        show_videos()

    elif selected2 == "Sign Out":
        clear_session()

def clear_session():
    st.session_state['logged_in'] = False
    st.session_state['logged_in_user'] = None
    st.session_state['role'] = None

if __name__ == '__main__':
    login()
