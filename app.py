from flask import (Flask,render_template,request,redirect,url_for,flash,send_from_directory,send_file)
import smtplib
from dotenv import load_dotenv
import os


load_dotenv("./keys.env")

app = Flask(__name__)
app.secret_key = os.environ.get("APP_PASSWORD")


def mail_me(name,email,message):
    my_email = os.environ.get("EMAIL")
    password = os.getenv("PASSWORD")
    message = f"Subject:mssg from {name}\n\nEmail: {email}\nMssg: {message}"
    with smtplib.SMTP('smtp.mail.yahoo.com') as mailer:
        mailer.starttls()
        mailer.login(my_email,password)
        mailer.sendmail(
            from_addr=my_email,
            to_addrs="maobiekwe@gmail.com",
            msg=message
        )
    
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/send-mail',methods=['GET',"POST"])
def send_email():
    error = None
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # print(name,email,message)
        try:
            mail_me(name,email,message)
            flash("Message Sent!",'info')
            return redirect(url_for('home'))
        except:
            flash("Error! Check network connection and try again.",'error')
            return redirect(url_for('home'))

@app.route("/download-resume")
def download():
    folder = "./files"
    file_name = "Adolphus.docx"
    return send_from_directory(folder,filename=file_name,as_attachment=True)

if __name__ == "__main__":
    app.run()