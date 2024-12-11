import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from chains import Chain
from Portfolio import Portfolio
from utils import clean_text

# Define fixed sender email address
SENDER_EMAIL = "aniketjad2121@gmail.com"  # Replace with your Gmail address

def generate_emails_from_url(url, llm, portfolio):
    """Generates a list of emails based on the content retrieved from the provided URL."""
    try:
        loader = WebBaseLoader([url])
        data = clean_text(loader.load().pop().page_content)
        portfolio.load_portfolio()
        jobs = llm.extract_jobs(data)

        # Generate emails for all jobs found
        emails = []
        for job in jobs:
            skills = job.get('skills', [])
            links = portfolio.query_links(skills)
            email = llm.write_mail(job, links)
            emails.append(email)

        return emails
    except Exception as e:
        return [f"Error generating emails: {e}"]

def export_email_via_gmail(subject, body, receiver_email, app_password):
    """Sends an email using Gmail's SMTP server with fixed sender and specified receiver addresses."""
    try:
        # Setting up the MIME structure
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Attach the email body to the message
        msg.attach(MIMEText(body, 'plain'))

        # Establishing connection with Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Upgrade the connection to a secure TLS one
        server.login(SENDER_EMAIL, app_password)  # Log in to Gmail

        # Send the email
        server.send_message(msg)
        server.quit()

        return f"Email sent successfully to {receiver_email}!"
    except Exception as e:
        return f"Failed to send email: {e}"

def create_export_email_app():
    st.title("📧 Export Email via Gmail")
    
    # URL input for generating the emails
    url_input = st.text_input("Enter a URL to generate the emails:")
    receiver_email = st.text_input("Receiver's Email", "hiring.manager@example.com")  # Default email address
    app_password = st.text_input("Gmail App Password", type="password")

    email_bodies = []

    if st.button("Generate Emails"):
        if url_input:
            # Generate email content from the URL
            chain = Chain()
            portfolio = Portfolio()
            email_bodies = generate_emails_from_url(url_input, chain, portfolio)

            if any("Error" in email for email in email_bodies):
                st.error(email_bodies[0])  # Show the first error
            else:
                for i, email_body in enumerate(email_bodies):
                    st.subheader(f"Email {i + 1}:")
                    st.code(email_body, language='markdown')  # Display the generated emails
                    
                    # Send button for each email
                    if st.button(f"Send Email {i + 1}", key=f"send_button_{i}"):
                        subject = f"Cold Email {i + 1}"  # Unique subject for each email
                        result = export_email_via_gmail(subject, email_body, receiver_email, app_password)
                        st.success(result)  # Display success or failure message

        else:
            st.error("Please enter a URL.")

if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Export Email via Gmail", page_icon="📧")
    create_export_email_app()
