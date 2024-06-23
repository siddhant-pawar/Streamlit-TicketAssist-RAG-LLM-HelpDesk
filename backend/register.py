import streamlit as st
import database as conn  # Assuming database.py contains create_connection function

# Function to register a user
def register_user(role='user'):
    # Display the register user form
    st.title('Register User')   

    # Input fields
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    # Role selection
    if role == 'admin':
        role_options = ['user', 'admin']
    else:
        role_options = ['user']
    
    role = st.selectbox('Role', role_options)

    if st.button('Register'):
        # Connect to the database
        with conn.create_connection() as connection:
            with connection.cursor() as cursor:
                try:
                    # Check if the username already exists
                    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
                    user = cursor.fetchone()

                    if user is None:
                        # Insert the new user into the database
                        cursor.execute('INSERT INTO users (username, password, role) VALUES (%s, %s, %s)', (username, password, role))
                        connection.commit()

                        # Success message
                        st.success('User registered successfully!')
                    
                    else:
                        # Error message
                        st.error('Username already exists.')

                except Exception as e:
                    st.error(f"Error: {e}")

# Run the Streamlit application
if __name__ == '__main__':
    register_user()
