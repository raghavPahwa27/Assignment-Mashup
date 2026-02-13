from flask import Flask, render_template, request
import os
import shutil
import zipfile
import smtplib
from email.message import EmailMessage
from yt_dlp import YoutubeDL
from pydub import AudioSegment
from email_validator import validate_email, EmailNotValidError

app = Flask(__name__)

# ------------------- SETTINGS -------------------
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")  # Gmail App Password
# ------------------------------------------------


def create_folders():
    # Delete old folders to avoid mixing old + new files
    shutil.rmtree("audios", ignore_errors=True)
    shutil.rmtree("cuts", ignore_errors=True)
    shutil.rmtree("output", ignore_errors=True)

    # Create fresh folders
    folders = ["audios", "cuts", "output"]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)


def get_writable_cookies_path():
    """
    Render stores secret files in /etc/secrets (read-only).
    yt-dlp tries to update cookies file, so we copy it to /tmp (writable).
    """
    src = "/etc/secrets/cookies.txt"
    dst = "/tmp/cookies.txt"

    if os.path.exists(src):
        shutil.copy(src, dst)

    return dst


def download_audios(singer, n):
    query = f"ytsearch{n}:{singer} song"

    cookie_path = get_writable_cookies_path()

    ydl_opts = {
        "cookiefile": cookie_path,
        "format": "bestaudio/best",
        "outtmpl": "audios/%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
        "socket_timeout": 30,
        "retries": 10,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([query])


def cut_audios(duration_sec):
    files = os.listdir("audios")
    for file in files:
        if file.endswith(".mp3"):
            path = os.path.join("audios", file)
            audio = AudioSegment.from_mp3(path)
            cut_audio = audio[:duration_sec * 1000]
            cut_audio.export(os.path.join("cuts", file), format="mp3")


def merge_audios(output_file):
    final_audio = AudioSegment.empty()

    files = os.listdir("cuts")
    for file in files:
        if file.endswith(".mp3"):
            audio = AudioSegment.from_mp3(os.path.join("cuts", file))
            final_audio += audio

    final_audio.export(os.path.join("output", output_file), format="mp3")


def make_zip(mp3_file, zip_name):
    zip_path = os.path.join("output", zip_name)
    mp3_path = os.path.join("output", mp3_file)

    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.write(mp3_path, arcname=mp3_file)

    return zip_path


def send_email(receiver_email, zip_path):
    msg = EmailMessage()
    msg["Subject"] = "Your Mashup File (ZIP)"
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg.set_content("Hello,\n\nYour mashup ZIP file is attached.\n\nThanks!")

    with open(zip_path, "rb") as f:
        file_data = f.read()
        file_name = os.path.basename(zip_path)

    msg.add_attachment(
        file_data,
        maintype="application",
        subtype="zip",
        filename=file_name
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
        smtp.send_message(msg)


def cleanup():
    shutil.rmtree("audios", ignore_errors=True)
    shutil.rmtree("cuts", ignore_errors=True)
    shutil.rmtree("output", ignore_errors=True)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        singer = request.form.get("singer")
        n = request.form.get("videos")
        duration = request.form.get("duration")
        email = request.form.get("email")

        # Validation
        try:
            n = int(n)
            duration = int(duration)
        except:
            return "Error: Videos and Duration must be integers"

        if n <= 10:
            return "Error: Number of videos must be greater than 10"

        if duration <= 20:
            return "Error: Duration must be greater than 20 seconds"

        try:
            validate_email(email)
        except EmailNotValidError:
            return "Error: Invalid Email ID"

        try:
            create_folders()

            output_mp3 = "mashup.mp3"
            output_zip = "mashup.zip"

            download_audios(singer, n)
            cut_audios(duration)
            merge_audios(output_mp3)

            zip_path = make_zip(output_mp3, output_zip)
            send_email(email, zip_path)

            cleanup()

            return f"SUCCESS: Mashup ZIP sent to {email}"

        except Exception as e:
            return f"ERROR: {str(e)}"

    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)