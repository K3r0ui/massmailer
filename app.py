from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)
app.secret_key = "dfgjliedjgldjflgjdfl"  # Change this to a random string

@app.route("/")
def index():
    return render_template("email_form.html")

UPLOAD_FOLDER = 'C://Users/Public/Documents'
ALLOWED_EXTENSIONS = {'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/send_email", methods=["POST"])
def send_email():
    recipient_file = request.files.get("recipient_file")
    
    # Check if a file was uploaded and if it is allowed
    if recipient_file and allowed_file(recipient_file.filename):
        filename = secure_filename(recipient_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        recipient_file.save(filepath)
        
        with open(filepath, "r") as f:
            recipients = f.read().splitlines()
        
        subject = request.form.get("subject")
        body = request.form.get("body")

        # Send an email to each recipient
        for recipient in recipients:
            try:
                send_email_via_smtp(recipient, subject, body)
                flash("Emails sent successfully!", "success")
            except Exception as e:
                flash(str(e), "error")
                return redirect(url_for("index"))
                
    else:
        flash("Invalid file type. Please upload a .txt file.", "error")
    
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