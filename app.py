from flask import Flask, render_template, request # type: ignore
import os
import re
import smtplib
from email.message import EmailMessage
from topsis import topsis

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

from dotenv import load_dotenv # type: ignore
import os

load_dotenv()


SENDER_EMAIL = os.getenv("SENDER_EMAIL")      
APP_PASSWORD = os.getenv("APP_PASSWORD")    

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        file = request.files["file"]
        weights = request.form.get("weights")
        impacts = request.form.get("impacts")
        email = request.form.get("email")

        # Basic validations
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return "Invalid email format"

        if file.filename == "":
            return "No file selected"

        # Save file
        input_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(input_path)

        output_path = os.path.join(app.config["UPLOAD_FOLDER"], "result.csv")

        try:
            topsis(input_path, weights, impacts, output_path)
        except Exception as e:
            return str(e)

        # Send email
        try:
            msg = EmailMessage()
            msg["Subject"] = "TOPSIS Result"
            msg["From"] = SENDER_EMAIL
            msg["To"] = email
            msg.set_content("Please find attached the TOPSIS result file.")

            with open(output_path, "rb") as f:
                msg.add_attachment(
                    f.read(),
                    maintype="application",
                    subtype="octet-stream",
                    filename="result.csv"
                )

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(SENDER_EMAIL, APP_PASSWORD)
                server.send_message(msg)

        except Exception as e:
            return "Error sending email: " + str(e)

        return "TOPSIS completed and result sent to email!"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
