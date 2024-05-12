# Serverless Function for CSYE6225 Cloud Webapp 
## Link to main webapp repo: [webapp](https://github.com/siddharthdashcsye6225/webapp)

### Assignment 7: Cloud Function for Email Verification with Pub/Sub Trigger
### Overview
For Assignment 7, I developed a cloud function responsible for sending verification emails to newly registered users. Triggered by messages from a Pub/Sub topic, this function efficiently handles user verification.

## Summary of Serverless Function for User Verification

This serverless function is designed to handle the verification process for newly registered users in a web application. Key features include:

- **Pub/Sub Trigger**: Listens for messages from a Pub/Sub topic containing user registration data.
- **Verification Link Generation**: Constructs a verification link based on user data received.
- **Database Interaction**: Inserts a verification record into a PostgreSQL database to track user verification status.
- **Email Notification**: Utilizes the Mailgun API to send a verification email containing the generated link to the user.

The function seamlessly integrates with other components of the web application, enhancing user experience and ensuring a smooth onboarding process.

