from flask import Flask, request, render_template, redirect, url_for
from google.cloud import storage
import os

app = Flask(__name__)

GCS_BUCKET_NAME = "mybucketname"

storage_client = storage.Client()

@app.route('/', methods = ["GET","POST"])
def upload_file():
    if request.method == "POST":
        if 'file' not in request.files:
            return "No file part"
        
        file = request.files['files']
        if file.filename == "":
            return "No selected file"
        
        if file:
            # Upload the file to GCS
            bucket = storage_client.bucket(GCS_BUCKET_NAME)
            blob = bucket.blob(file.filename)
            blob.upload_from_file(file)
            return f"File {file.filename} uploaded to {GCS_BUCKET_NAME}."
        
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)