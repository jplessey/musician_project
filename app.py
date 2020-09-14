from flask import Flask, flash, render_template, redirect, url_for, request
from flask_mail import Mail, Message
import base64
from dotenv import load_dotenv
import os


load_dotenv()
app = Flask(__name__)
app.secret_key = "la_galleta"
email_pass = base64.b64decode(os.getenv("SER").encode())
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'ele.pe.arq@gmail.com',
    MAIL_PASSWORD = email_pass.decode()[::2],
))
mail = Mail(app)


body_html = """
<!DOCTYPE html>
<html lang="en">
    <body>
        <h1 style="color:SlateGray;">J&P Guitars. You're now subscribed to our newsletter!</h1>
        <img src="https://drive.google.com/uc?export=view&id=1D_BbH3Z4_D-CKt2SU05Jf_f7TwcKwFkM" alt="Electric Guitar">
    </body>    
</html>
"""


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def send_email():
    if request.method == 'POST' and request.form['email']:
        email = request.form['email']
        msg = Message(sender="ele.pe.arq@gmail.com")
        msg.recipients = [f"{email}"]
        msg.body = "J&P Guitars. Newsletter"
        msg.html = body_html
        msg.subject = "J&P Guitars. Newsletter"
        mail.send(msg)
        flash("Rock On! You're now subscribed to our newsletter. Check your email!")
        print(f"Email sent to {email}")
        return redirect(url_for('home'))
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
