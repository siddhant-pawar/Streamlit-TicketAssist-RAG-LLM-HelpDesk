import streamlit as st
import backend.cuad as cd
import subprocess
import backend.llmper as llmf
connection = cd.create_connection()

# Initialize button state in session state
col1, col2 = st.columns(2)
with col1:
    try:
        if 'button_login' not in st.session_state:
            st.session_state.button_login = False
            st.write()
        if not st.session_state.button_login:
            button_login = st.sidebar.button("Login")
            if button_login:  
                st.session_state.button_login = True
                subprocess.Popen(["streamlit", "run", "backend/main.py"])
        else:
            st.sidebar.warning("already login page is running.")
    except :
        st.sidebar.warning("already login page is running.")
with col2:
    try:
        if 'button_register' not in st.session_state:
            st.session_state.button_register = False
            st.write()
        if not st.session_state.button_register:
            button_register = st.sidebar.button("register")
            if button_register:  
                st.session_state.button_register = True
                subprocess.Popen(["streamlit", "run", "backend/register.py"])
        else:
            st.sidebar.warning("already button_register page is running.")
    except :
        st.sidebar.warning("already button_register page is running.")

st.sidebar.subheader("Submit a ticket →")
tproblem = st.sidebar.multiselect(
    "If you can't find a solution to your problem in our knowledgebase, you can submit a ticket by selecting the appropriate problem below.",
    ['Account access','Billing','Domains','ESDS VTMScan','eNlight Web VPN','Anti Ransomware','Transfer Disputes','Hosting','Security Tools','Dedicated Servers','SSL','VPN Application',
    'Abuse Reports and Cases','Feedback'])

st.sidebar.subheader("Your ticket details →")
with st.sidebar:
    if connection:
        action = st.selectbox("Select an Action:", ("Create ticket", "Update ticket", "Delete ticket"))
        if action == "Create ticket":
            st.sidebar.subheader("Create New Record")
            user_name = st.text_input("Username:")
            temail = st.text_input("email:")
            tickettype = st.selectbox('what you want to do Enquiry or create ticket?', ('Product Enquiry', 'Problem Enquiry', 'Other Enquiry'))
            if tickettype == "Product Enquiry":
                tenquiry = st.text_input("Product Enquiry:")
            if tickettype == "Problem Enquiry":
                tenquiry = st.text_input("Your Problem Enquiry:")
            if tickettype == "Other Enquiry":
                tenquiry = st.text_input("Your Enquiry:")
            if st.button("Create"):
                if cd.create_record(connection, user_name.strip(), temail.strip(),tickettype.strip(),tenquiry.strip(), tproblem[0].strip()):
                    tid = cd.fetch_ticketid_record(connection,temail.strip())
                    st.success(f"Record created successfully! your ticket id is {tid[0]} ..") 
                else:
                     st.error("already exits")

        elif action == "Update ticket":
            st.subheader("Update Record")
            temail = st.text_input("Enter Email:", placeholder="Type a Email...")
            tickettype = st.selectbox('You want to Update Enquiry Type?', ('Product Enquiry', 'Problem Enquiry', 'Other Enquiry'))
            if tickettype == "Product Enquiry":
                tenquiry = st.text_input("Product Enquiry:")
            if tickettype == "Problem Enquiry":
                tenquiry = st.text_input("Your Problem Enquiry:")
            if tickettype == "Other Enquiry":
                tenquiry = st.text_input("Your Enquiry:")
            if st.button("Update"):
                if cd.update_record(connection, temail.strip(),tickettype.strip(),tenquiry.strip()):
                    st.success(f"Record created successfully!")

        elif action == "Delete ticket":
            st.subheader("Delete Record")
            ticketid = st.text_input("Enter Your Ticket ID", value=None, placeholder="Type a Ticket ID...")
            if st.button("Delete"):
                if cd.delete_record(connection,ticketid.strip()):
                    st.success(f"Record with ID {ticketid} deleted successfully!")
        connection.close()
connection = cd.create_connection()

# Chatbot Code:- 
llmf.show_chat_interface()
"""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""
