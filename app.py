from flask import Flask, render_template, request
import os
import re
import requests
import base64
from dotenv import load_dotenv
from topsis import topsis

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

if not RESEND_API_KEY:
    raise Exception("RESEND_API_KEY not set in .env")

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        file = request.files.get("file")
        weights = request.form.get("weights")
        impacts = request.form.get("impacts")
        email = request.form.get("email")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return "Invalid email format"

        if not file or file.filename == "":
            return "No file selected"

        input_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(input_path)

        output_path = os.path.join(app.config["UPLOAD_FOLDER"], "result.csv")

        try:
            topsis(input_path, weights, impacts, output_path)
        except Exception as e:
            return str(e)

        try:
            with open(output_path, "rb") as f:
                file_data = f.read()

            encoded_file = base64.b64encode(file_data).decode("utf-8")

            response = requests.post(
                "https://api.resend.com/emails",
                headers={
                    "Authorization": f"Bearer {RESEND_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "from": "onboarding@resend.dev",
                    "to": [email],
                    "subject": "TOPSIS Result",
                    "text": "Please find the attached TOPSIS result file.",
                    "attachments": [
                        {
                            "filename": "result.csv",
                            "content": encoded_file
                        }
                    ]
                }
            )

            if response.status_code not in [200, 201]:
                return f"Email failed: {response.text}"

        except Exception as e:
            return f"Error sending email: {e}"

        return "TOPSIS completed and result sent to email!"

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
