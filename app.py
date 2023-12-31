from flask import Flask, render_template, request, redirect, url_for, flash ,send_file , session
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from werkzeug.utils import secure_filename
import os



app = Flask(__name__)
app.secret_key = "dfgjliedjgldjflgjdfl"  # Change this to a random string
app.config.from_pyfile('config.py')
UPLOAD_FOLDER = app.config["UPLOAD_FOLDER"]
smtp_password = app.config["SMTP_PASSWORD"]
smtp_user = app.config["SMTP_USER"]
ALLOWED_EXTENSIONS = {'txt'}

if os.path.exists('config.py'):
    print("Config file exists")
else:
    print("Config file does not exist")

try:
    app.config.from_pyfile('config.py')
    # Print a config value to ensure it is loaded
except Exception as e:
    print(f"Error: {e}")






#Functions 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Routes

## default route           
@app.route("/")
def index():
    return render_template("email_form.html")


## filter emails route
@app.route("/filter" , methods=["GET","POST"])
def fmail():  
    if request.method == 'POST':
        
        country_code = request.form.get('country_code')
        print(country_code)
        recipient_file = request.files.get("recipient_file")
        if recipient_file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(recipient_file.filename))
            recipient_file.save(filepath)
            output_file_path = UPLOAD_FOLDER+"/fresh5.txt"  # Specify your output file path

            try:
                with open(filepath, 'r', encoding='utf-8') as infile, \
                     open(output_file_path, 'w', encoding='utf-8') as outfile:

                    for line in infile:
                        if line.strip().endswith(country_code):
                            outfile.write(line)
                    
                print(f"Emails extracted successfully to: {output_file_path}")
                return send_file(output_file_path, as_attachment=True, download_name='filtered_emails.txt')

            except FileNotFoundError:
                print(f"File not found: {filepath}")  
            except Exception as e:
                print(f"An error occurred: {str(e)}")

    # If GET request or if POST request does not redirect, show form page (or any other page you'd like to redirect to)
    return render_template("fmail.html")


## send email route
@app.route("/send_email", methods=["POST"])
def send_email():
    recipient_file = request.files.get("recipient_file")
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
                print ("GG")
                flash("Emails sent successfully!", "success")
            except Exception as e:
                flash(str(e), "error")
                return redirect(url_for("index"))
                
    else:
        flash("Invalid file type. Please upload a .txt file.", "error")
    
    return redirect(url_for("index"))

def send_email_via_smtp(recipient, subject, body):
    app.config.from_pyfile('config.py')
    # Here put ur email server, port, and login creds
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    try:
        # Connect to the server, login, and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        login_response = server.login(smtp_user, smtp_password)
        
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
    app.run(debug=True, host='0.0.0.0')