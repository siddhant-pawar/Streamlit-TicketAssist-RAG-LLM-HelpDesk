import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from listalldata import filter_dataframe
from cuad import priority,fetch_last_inserted_data
import cuad as cd
connection = cd.create_connection()
# Function to fetch data from the MySQL database
def fetch_data():
    conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="admin",
                database="ticketdb",
                auth_plugin = 'mysql_native_password'
    )
    query = "SELECT * FROM tdatabase" 
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def Dashboard():
    st.title("Ticket Data Dashboard")

    # Fetch data from the database
    data = fetch_data()
    total1,total2=st.columns(2,gap='large')
    with total1:
        st.info('Total Users,Ticket ID, Problem',icon="📌")
        st.subheader("Total Number of Users")
        total_users = data['user_name'].nunique()
        total_ticketid  = data['ticketid'].nunique()
        total_problem = data['tproblem'].nunique()
        st.metric(label="Total Users:",value=f"{total_users}")
        st.metric(label="Total Ticket Id:",value=f"{total_ticketid}")
        st.metric(label="Total Problem:",value=f"{total_problem}")

        st.info('Total Priority for each ticket as per to dates',icon="📌")
        tab1, tab2= st.tabs(["last priority", "time priority"])
        with tab1:
            fetch_last_inserted_data(connection)
        with tab2:
            priority()
        

            
    with total2:
        st.info('Ticket ID and Enquiry',icon="📌")
        st.subheader("Enquiry with Ticket ID")
        problem_data = fetch_data()
        print(problem_data['ticketid'],['tproblem'])
        st.dataframe(filter_dataframe(problem_data))


    col1,col2=st.columns(2,gap='large')
    with col1:
        st.info('Central Earnings',icon="📌")
        st.subheader("Problem Type Count")
        problem_type_counts = data['tproblem'].value_counts()
        st.bar_chart(problem_type_counts)

    with col2:
        st.info('Most frequent',icon="📌")
        st.subheader("Ticket Type Count")
        ticket_type_counts = data['tickettype'].value_counts()
        st.bar_chart(ticket_type_counts)


    st.info('Most frequent',icon="📌")
    st.subheader("Priority Count")
    priority_counts = data['tpriority'].value_counts()
    st.bar_chart(priority_counts)



    hide_st_style=""" 
    <style>
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden;}
    </style>
    """