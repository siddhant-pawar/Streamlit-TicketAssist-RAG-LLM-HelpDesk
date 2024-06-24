# Ticket_Management_and_Rag-LLM-HelpBot 
Ticket_Management_and_Rag-LLM-HelpBot is a comprehensive system designed to streamline ticket management and enhance customer support through AI automation. The system allows users to efficiently create, update, and search tickets, improving organizational efficiency. Integration of Langchain (LLM) and Python facilitates an AI-powered chatbot that offers automated customer support. This integration enhances responsiveness and interaction quality, providing users with timely assistance and resolving queries effectively.

### Environment Setup:-
- Requirements:
  - Python 3.9+
  - Nmap
  - Npcap (Windows Only if required)
- ### Create by using Python venv
    - Create a Python venv: ```python -m <envname> .venv```
    - Activate the Python venv: ```.venv/Scripts/activate.bat```
- ### Create by using conda env - python 3.9
    - Create a Python venv: ```conda create -n <envname> python=3.9```

- ### activate and initialize virtual env
    - ```conda activate <envname>```

- Clone this git repository: ```git clone https://github.com/siddhant-pawar/Ticket_management_and_Rag-LLM-HelpBot```
- Go into the project: ```cd Ticket_management_and_Rag-LLM-HelpBot```
- To securely store and load sensitive information, create a .env file with the following content:
```
# .env file
OPENAI_API_KEY=your_openai_api_key
```
- RUN ```pip install -r requirements.txt```:
  - This line installs the Python dependencies listed in the ```requirements.txt``` file using pip. This step is done within the container during the image build process
- Run the multipage app
To run streamlit app, run:
```shell
streamlit run charboy.py
```

## Overall Structure and Functionality: 

### 1) chatboy.py:- 
- Streamlit Setup: Streamlit is used as the framework for creating a web-based user interface.
It allows for interactive elements like buttons, text inputs, and selection boxes to manage different aspects of ticket management and customer support.
- Session Management: Session state (```st.session_state```) is used to manage the state of buttons (```button_login``` and ```button_register```) to control page flow and prevent multiple instances from running simultaneously.
Sidebar Navigation: The sidebar provides navigation options for login (```button_login```) and registration (```button_register```). Clicking these buttons starts corresponding backend processes using subprocess.Popen.
- Ticket Submission: Users can submit tickets via a multiselect dropdown (```tproblem```) for various issues like account access, billing, etc.
Depending on the selected action ("```Create ticket```", "```Update ticket```", "```Delete ticket```"), different forms are presented to gather necessary details from the user.
- Database Interaction: The application interacts with a database (```cd.create_connection()``` and subsequent database operations using functions from cd module) to store and retrieve ticket information.
Operations include creating, updating, and deleting ticket records based on user inputs.
- Integration with Langchain (LLM):The chatbot functionality is integrated using ```llmf.show_chat_interface()```, powered by Langchain (LLM). This feature provides automated customer support and enhances interaction quality by leveraging AI.
Styling and UI Control: Custom CSS (```<style>```) is used to hide main menu, footer, and header elements (```#MainMenu, footer, header```). This ensures a clean and focused UI experience for the ticket management and chatbot interface.

### 2) backend/cuad.py

- MySQL Database Integration: MySQL Connector is used to establish a connection (```create_connection()``` function) with the database (```ticketdb```).
Functions (```create_record(), update_record(), delete_record(), fetch_ticketid_record()```) interact with the database to perform CRUD operations on ticket records.
- Ticket Management Functions:
  - Create Record: Allows users to create a new ticket record. Generates a unique ticket ID (```ticketid```) using Faker library and stores details such as user name, email, ticket type, enquiry details, problem type (```tproblem```), and priority based on problem type.
  - Update Record: Updates ticket details based on email (```temail```). Allows modification of ticket type and enquiry details.
  - Delete Record: Deletes a ticket record based on ```ticketid```.
  - Fetch Ticket ID: Retrieves ticket IDs associated with a given email (```temail```).

- Email Notification: ```send_email()``` function sends an email notification to users upon successful creation of a ticket. Uses SMTP for email delivery, requiring SMTP server details (```smtp.gmail.com```), sender email, and sender password.
- Priority Calculation and Display:
  - ```calculate_priority()``` calculates the age of a ticket to determine its priority.
  - ```priority()``` function demonstrates ticket prioritization based on age, sorting tickets into high, medium, and low priority levels. Displays prioritized tickets in Streamlit UI with color-coded indications of priority status.

### 3) backend/dashboard.py
- Imports: 
  - ```streamlit``` for creating the web-based dashboard.
  - ```mysql.connector``` for connecting to the MySQL database.
  - ```pandas``` for data manipulation and analysis.
  - ```plotly.express``` and ```matplotlib.pyplot``` for data visualization.
  - ```filter_dataframe``` from ```listalldata``` and functions from ```cuad``` (like ```priority, fetch_last_inserted_data, create_connection```) for additional data processing and database interactions.

- Functions:
  - ```fetch_data()```: Queries the ticketdb database to retrieve all data from the tdatabase table into a Pandas DataFrame (```df```).
  - ```Dashboard()```: Main function that builds the Streamlit dashboard interface.

- Dashboard Interface:
  - Title and Metrics:
    - Displays the title "Ticket Data Dashboard" using ```st.title()```.
    - Uses ```st.metric()``` to show total counts of unique users (```total_users```), unique ticket IDs (```total_ticketid```), and unique problems (```total_problem```).

  - Tabs:
      - Utilizes ```st.tabs()``` to organize content into tabs ("last priority" and "time priority").
      - Inside tabs, calls ```fetch_last_inserted_data(connection)``` and ```priority()``` functions to display relevant data related to ticket priorities and dates.
- Dataframes and Charts:
  - Dataframe Display: Uses ```st.dataframe()``` to display filtered data (```filter_dataframe(problem_data)```).
  - Bar Charts: Utilizes ```st.bar_chart()``` to visualize counts of problem types (```problem_type_counts```), ticket types (```ticket_type_counts```), and priority levels (```priority_counts```).
- Styling: Includes a custom CSS style (```hide_st_style```) to hide the main menu, footer, and header for a cleaner dashboard appearance.

### 4) /backend/intergationopration.py

- CRUD Operations Functions:
  - ```read_records(connection)```:
     - Executes a query to fetch all records from the ```tdatabase``` table using a cursor.
     - Returns fetched records as a list of tuples.
  - ```update_record(connection, user_name, temail, tickettype, tenquiry, ticketid, tproblem, tpriority)```:
       - Updates a record in the ```tdatabase``` table based on ```user_name```.
       - Executes an update query using provided parameters (```user_name, temail, tickettype, tenquiry, ticketid, tproblem, tpriority```).
       - Commits the transaction and returns ```True``` if successful, otherwise returns False.
         
  - ```delete_record(connection, account_name)```:
    - Deletes a record from the ```tdatabase``` table based on ```account_name```.
    - Executes a delete query using ```account_name``` as a parameter.
    - Commits the transaction and returns ```True``` if successful, otherwise returns False.

- ```operation()`` Function:
  - Main function that constructs the Streamlit interface.
  - Initializes a connection to the database using ```create_connection()```.
  - Creates two columns (col1 and col2) using ```st.columns(2)``` for organizing UI elements.

  - Action Selection (``` `st.selectbox("Select an Action:", ...)```):
      - Provides options ```(Read, Update, Delete)``` for CRUD operations via a select box.
  - Read Operation:
    - Fetches and displays all records from the database using ```read_records(connection)```.
  - Update Operation: Allows users to input parameters (```user_name, temail, tickettype, tenquiry, ticketid, tproblem, tpriority```) to update a record.
    - Displays input fields and selects for updating ticket details.
  - Delete Operation:
    - Enables users to input ```account_name``` to delete a record.
    - Deletes the record upon clicking the delete button.
### 4) /backend/main.py
- Imports:
  - streamlit: For creating the web application interface.
  - database as conn: Custom module (```database.py```) for database connection (```create_connection()``` function).
  - Various other custom modules (```register, streamlit_option_menu, home, account_details, video, listalldata, intergationopration, useroparation, useraccountdetail, llmper```) for specific functionalities.

- Function Definitions:
  - ```create_connection()```: Establishes a connection to the database (```ticketdb```) using ```conn.create_connection()```.
Returns the connection object or displays an error if connection fails.
  - ```init_session_state()```: Initializes session state variables (```logged_in, logged_in_user, role```) if they do not exist in ```st.session_state```.
  - ```login()```:
      -  Manages user login functionality.
      -  If not logged in, displays login form (```username``` and ```password``` fields).
      -  Validates credentials against the users table in the database.
      -  Sets session variables upon successful login (```logged_in, logged_in_user, role```).
      -  Redirects to appropriate actions based on user role (```admin_actions()``` or ```user_actions()```).
  - ```admin_actions(connection)```:
      - Defines actions available to admin users in the sidebar using ```option_menu```.
      - Options include viewing home page, listing all data (```tdatabase```), performing ticket operations (```operation()```), registering users (```register_user()```), uploading LLM (```show_upload_interface()```), adding videos (```videos()```), and signing out (```clear_session()```).
        
  - ```user_actions(connection, username)```:
    - Defines actions available to regular users in the sidebar using ```option_menu```.
    - Options include viewing home page, viewing account details (```account_detail()```), performing user operations (```useroperation()```), viewing operation videos (```show_videos()```), and signing out (```clear_session()```).
  - clear_session(): Clears session variables (logged_in, logged_in_user, role) to log out the user.

- Main Execution (```__name__ == '__main__'```):
  - Calls the ```login()``` function to start the application.
  - Depending on the user's role (```admin``` or ```user```), appropriate actions and menus are displayed using Streamlit's sidebar and tabs.

### 5) /backend/llmper.py

- Imports
    - The script imports necessary libraries and modules:
        - ```os```: For interacting with the operating system, specifically to manage directories and file operations.
        - ```streamlit```: Framework for creating web applications with Python.
        - ```PdfReader``` from ```PyPDF2```: Used to read text content from PDF files.
        - Various modules from ```langchain```, including tools for text splitting, embeddings, vector stores, and chatbot interactions.
        - ```dotenv```: For loading environment variables from a ```.env``` file.

- Initialization and Environment Variables
    - ```PDFS_DIR```: Directory path (```pdfs```) where uploaded PDF files are stored.
    - ```embeddings```: Initializes Spacy embeddings (```en_core_web_sm```) for text processing.
    - ```openai_api_key```: Retrieves the OpenAI API key from environment variables stored in ```.env```.

- Functions
    - ```pdf_read(pdf_docs)```: Reads text content from uploaded PDF documents (```pdf_docs```).
    - ```get_chunks(text)```: Splits the text into manageable chunks using ```RecursiveCharacterTextSplitter```.
    - ```vector_store(text_chunks)```: Creates a ```FAISS vector store``` from the text chunks using ```embeddings``` and saves it locally.
    - ```get_conversational_chain(tools, question)```: Sets up a chatbot chain (```ChatOpenAI```) to interact with the user based on retrieved documents and provided tools.
    - ```user_input(user_question)```: Loads the FAISS vector store (```new_db```) and initiates a conversation with the chatbot based on user input.
    - ```process_pdf_upload(pdf_docs)```: Handles PDF file uploads, saves them locally, reads their text content, splits into chunks, and creates a vector store.
    - ```show_upload_interface()```: Displays a file uploader interface in Streamlit to upload PDF files, processes them on button click, and shows success message upon completion.
    - ```show_chat_interface()```: Sets up the Streamlit interface for chatting with the assistant.
        - Manages user messages and assistant responses using a persistent session state (```st.session_state.messages```).

### 5) /backend/video.py

- Setup and Sidebar:
    - Checks if the "```uploaded_videos```" directory exists. If not, it creates one.
    - Creates a sidebar with options to upload videos (```file_uploader```).
      
- Video Upload Section:
    - Allows users to upload videos (```.mp4``` or ```.avi```) through the sidebar. It validates the file format and saves uploaded videos to the "```uploaded_videos```" directory.
- List of Uploaded Videos:
    - Displays a header and lists all videos currently stored in the "```uploaded_videos```" directory using ```os.listdir```.
    - For each video found, it displays the video using ```st.video``` and shows the video's filename as a caption.

- Grid Display of Videos:
    - If videos are found in the specified ```video_folder```, they are displayed in a grid pattern (```num_columns``` across).
    - Each video is displayed using ```st.video``` within a column (```st.columns```), along with its filename as a caption.

- No Videos Found:
    - If no videos are found in the "```uploaded_videos```" directory, it displays an informational message using ```st.warning```.
      
2. ```show_videos()```

- Title:
    - Displays a title "List of Videos".
- List of Videos:
   - Retrieves all ```.mp4``` files from the ```video_folder``` directory using ```os.listdir``` and ```filters``` them based on the file extension.
   - Displays each video using ```st.video``` with the video content read directly from the file using open and read.
- Error Handling:
    - Uses a try-except block to catch and display errors if there are any issues loading a video file.
 
# SCREENSHORT:-
![alt text](https://github.com/siddhant-pawar/Ticket_management_and_Rag-LLM-HelpBot/blob/main/op/frontendcreateticket.PNG)
![alt text](https://github.com/siddhant-pawar/Ticket_management_and_Rag-LLM-HelpBot/blob/main/op/frontendcreateticketsub.PNG)
![alt text](https://github.com/siddhant-pawar/Ticket_management_and_Rag-LLM-HelpBot/blob/main/op/frontendupdateticketsub.PNG)
![alt text](https://github.com/siddhant-pawar/Ticket_management_and_Rag-LLM-HelpBot/blob/main/op/login-admin-user.PNG)
![alt text](https://github.com/siddhant-pawar/Ticket_management_and_Rag-LLM-HelpBot/blob/main/op/adminsideTicketDataDashboard.PNG)
![alt text](https://github.com/siddhant-pawar/Ticket_management_and_Rag-LLM-HelpBot/blob/main/op/adminsideTicketDataDashboardvis1.PNG)
![alt text](https://github.com/siddhant-pawar/Ticket_management_and_Rag-LLM-HelpBot/blob/main/op/adminsideTicketDataDashboardvis2.PNG)
![alt text](https://github.com/siddhant-pawar/Ticket_management_and_Rag-LLM-HelpBot/blob/main/op/listalldataFilterdataframe.PNG)
![alt text](https://github.com/siddhant-pawar/Ticket_management_and_Rag-LLM-HelpBot/blob/main/op/adminsideReadRecordsforadmin.PNG)
![alt text](https://github.com/siddhant-pawar/Ticket_management_and_Rag-LLM-HelpBot/blob/main/op/adminsideupdateRecordsforadmin.PNG)
![alt text](https://github.com/siddhant-pawar/Ticket_management_and_Rag-LLM-HelpBot/blob/main/op/adminsidedeleteRecordsforadmin.PNG)
![alt text](https://github.com/siddhant-pawar/Ticket_management_and_Rag-LLM-HelpBot/blob/main/op/adminsidellmragUploadPDFFile.PNG)
![alt text](https://github.com/siddhant-pawar/Ticket_management_and_Rag-LLM-HelpBot/blob/main/op/adminsideRegisterUserbyadmin.PNG)
![alt text](https://github.com/siddhant-pawar/Ticket_management_and_Rag-LLM-HelpBot/blob/main/op/adminsideUserAccountDetailsbyadmin.PNG)
![alt text](https://github.com/siddhant-pawar/Ticket_management_and_Rag-LLM-HelpBot/blob/main/op/adminsideuploadvideouserbyadmin.PNG)
![alt text](https://github.com/siddhant-pawar/Ticket_management_and_Rag-LLM-HelpBot/blob/main/op/adminsideSignOut.PNG)
![alt text](https://github.com/siddhant-pawar/Ticket_management_and_Rag-LLM-HelpBot/blob/main/op/homeandwelcomejoke.PNG)
![alt text](https://github.com/siddhant-pawar/Ticket_management_and_Rag-LLM-HelpBot/blob/main/op/UsersideAccountDetails.PNG)
![alt text](https://github.com/siddhant-pawar/Ticket_management_and_Rag-LLM-HelpBot/blob/main/op/usersideReadRecordsforUser.PNG)
![alt text](https://github.com/siddhant-pawar/Ticket_management_and_Rag-LLM-HelpBot/blob/main/op/usersideupdateRecordsforUser.PNG)
![alt text](https://github.com/siddhant-pawar/Ticket_management_and_Rag-LLM-HelpBot/blob/main/op/usersidedeleteRecordsforUser.PNG)
![alt text](https://github.com/siddhant-pawar/Ticket_management_and_Rag-LLM-HelpBot/blob/main/op/usersidevideoUser.PNG)



