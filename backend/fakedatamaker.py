from faker import Faker
import random
import mysql.connector


fake = Faker()
try:
    conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="admin",
                database="ticketdb",
                auth_plugin = 'mysql_native_password'
    )

except mysql.connector.Error as err:
    print(f"Error connecting to the database: {err}")


#user_name, temail, tickettype, tenquiry, ticketid, tproblem, tpriority
cursor = conn.cursor()
# Generate a list of sample data
for i in range(25):  # Change the number to the desired number of entries
    user_name = fake.name().replace(" ", "").lower()
    temail = fake.email()
    tickettype = random.choice(['Product Enquiry', 'Problem Enquiry', 'Other Enquiry'])
    tenquiry = random.choice(['How do I install the software?','What are the system requirements for running the software?','Is there a free trial available?',
' How do I activate or register the software?','Can I use the software on multiple devices?','Is there a mobile version of the software available?',
'Are there any known compatibility issues with other software or hardware?','What are the key features of the software?',
'How do I update the software to the latest version?','Is there a user manual or documentation available?',
'What are the different pricing plans and their features?', 'Does the software have a customer support helpline or live chat option?',
'Can I import/export data from/to other software?','How can I customize the settings or preferences in the software?',
'Is the software available in multiple languages?','Can I transfer the software license to another person or organization?','Does the software have any security measures or encryption features?',
'Are there any training resources or tutorials available for learning how to use the software?','Can I integrate the software with other applications or services?',
'What is the refund policy if I"m not satisfied with the software?'])
    ticketid = "TID-"+ str(fake.unique.random_int(min=1000, max=9999))
    tproblem = random.choice(['Account access','Billing','Domains','Domain Transfers','Transfer Disputes','Hosting','Security Tools','Dedicated Servers','SSL','VPN Application',
    'Abuse Reports and Cases','Feedback'])
    tpriority = random.choice(['high','medium','low'])
    insert_query = "INSERT INTO tdatabase (user_name,temail,tickettype,tenquiry,ticketid,tproblem,tpriority) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(insert_query,(user_name,temail,tickettype,tenquiry,ticketid,tproblem,tpriority))

conn.commit()
cursor.close()
print("done")
    

