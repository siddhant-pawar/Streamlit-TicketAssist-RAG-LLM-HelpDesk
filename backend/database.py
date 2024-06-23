# Connect to the MySQL database
import mysql.connector
import streamlit as st
#def db():
#    conn = mysql.connector.connect(host='localhost',auth_plugin = 'mysql_native_password',user="root", password="admin", database="interappdata")
#    return conn


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
