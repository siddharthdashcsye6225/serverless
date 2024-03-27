import os
import base64
import json
import requests
from uuid import UUID
import psycopg2
from datetime import datetime

# Define your FastAPI endpoint URL
FASTAPI_ENDPOINT = "http://siddharthdash.me:8000/v1/user/verification"
# SQL configuration
SQL_INSTANCE_IP = os.environ['DB_HOST']  
SQL_INSTANCE_PORT = 5432  
SQL_DB_NAME = os.environ['DB_NAME'] 
SQL_TABLE_NAME = "verification"  
SQL_USER = os.environ['DB_USER']  
SQL_PASSWORD = os.environ['DB_PASS']  

def send_verification_email(email, verification_link):
    # Here you can use any email service provider like Mailgun, SendGrid, etc.
    # Below is an example using Mailgun API to send an email

    # Replace these values with your Mailgun credentials
    MAILGUN_API_KEY = "85dea98e37f8be518dc06c81d079c84c-f68a26c9-7ae0099b"
    MAILGUN_DOMAIN = "siddharthdash.me"
    SENDER_EMAIL = "admin@siddharthdash.me"

    # Compose the email message
    subject = "CSYE6225: WEBAPP: Verify Your Email Address"
    body = f"Hi! Thank you for registering for Webapp. Click the following link to verify your email address: {verification_link}"
    recipient_email = email

    # Send the email via Mailgun API
    response = requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": f"Cloud Function <{SENDER_EMAIL}>",
            "to": recipient_email,
            "subject": subject,
            "text": body
        }
    )

    # Check if the email was sent successfully
    if response.status_code == 200:
        print("Verification email sent successfully!")
    else:
        print(f"Failed to send verification email: {response.text}")

def process_pubsub(event,context):
    # Check if the event contains data
    if 'data' in event:
        # Decode the Pub/Sub message
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        message_data = json.loads(pubsub_message)

        # Extracting necessary data from the message
        user_id = message_data.get("user_id")
        user_id_sql = str(message_data.get("user_id"))
        username = message_data.get("username")
        first_name = message_data.get("first_name")
        last_name = message_data.get("last_name")
        created_at = message_data.get("created_at")
        updated_at = message_data.get("updated_at")

        # Construct the verification link
        verification_link = f"{FASTAPI_ENDPOINT}/{user_id}"

        # Insert the verification record into the database
        try:
            with psycopg2.connect(host=SQL_INSTANCE_IP, port=SQL_INSTANCE_PORT, dbname=SQL_DB_NAME, user=SQL_USER, password=SQL_PASSWORD) as conn:
                with conn.cursor() as cursor:
                    # Construct the SQL query to insert the record
                    insert_query = f"INSERT INTO {SQL_TABLE_NAME} (id, email, verified, created_at) VALUES (%s, %s, %s, %s)"
                    cursor.execute(insert_query, (user_id_sql, username, False, datetime.now()))

            print("Verification record inserted successfully.")
        except Exception as e:
            print("Failed to insert verification record:", e)

        # Send the verification email
        send_verification_email(username, verification_link)

        # Acknowledge the message
        print("Processed message:", pubsub_message)
    else:
        print("No 'data' key found in the event.")