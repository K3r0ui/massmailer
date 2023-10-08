from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = "dfgjliedjgldjflgjdfl"  # Change this to a random string

@app.route("/")
def index():
    return render_template("email_form.html")

@app.route("/send_email", methods=["POST"])
def send_email():
    recipient = request.form.get("recipient")
    subject = request.form.get("subject")
    body = request.form.get("body")
    
    # SMTP Settings
    # Note: Make sure to handle exceptions, log errors, and possibly inform the user

    # Let's assume you have a function `send_email_via_smtp` to handle the email sending.
    try:
        send_email_via_smtp(recipient, subject, body)
        flash("Email sent successfully!", "success")
    except Exception as e:
        flash(str(e), "error")

    return redirect(url_for("index"))

def send_email_via_smtp(recipient, subject, body):
    # Here put ur email server, port, and login creds
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "tradevestoteam@gmail.com"
    smtp_password = "mywyiutlmnfcxsxm"
    
    try:
        # Connect to the server, login, and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        
        # Create the email
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = smtp_user
        msg["To"] = recipient
        part1 = MIMEText(body, "html")
        msg.attach(part1)
        
        # Send the email
        server.sendmail(smtp_user, recipient, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")
if __name__ == "__main__":
    app.run(debug=True)