import requests
from tqdm import tqdm
import zipfile
import os
import csv

# Download dataset
url = "https://www.dropbox.com/scl/fi/i9yvfqpf7p8uye5o8k1sj/common_voice.zip?rlkey=lz3dtjuhekc3xw4jnoeoqy5yu&dl=1"
download_path = "./cv-data/common_voice.zip"

if not os.path.exists(download_path):
    response = requests.get(url, stream=True, allow_redirects=True)
    # Get the total file size from the headers
    total_size_in_bytes = int(response.headers.get("content-length", 0))

    # Create a progress bar using tqdm
    with open(download_path, "wb") as file, tqdm(
        desc="Downloading", total=total_size_in_bytes, unit="B", unit_scale=True
    ) as bar:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)
            bar.update(len(chunk))

# Extract the zip file
if not os.path.exists("./cv-data/common-voice"):
    with zipfile.ZipFile(download_path, "r") as zip_ref:
        zip_ref.extractall("./cv-data/common-voice")


# Path to the folder containing mp3 files and the CSV file
folder_path = "cv-data/common-voice"
csv_file_path = os.path.join(folder_path, "cv-valid-dev.csv")


# Function to send a file to the ASR API and get the transcription
def transcribe_audio(file_path):
    with open(file_path, "rb") as f:
        files = {"file": (file_path, f, "audio/mpeg")}
        response = requests.post("http://localhost:8001/asr", files=files)
        if response.status_code == 201:
            return response.json().get("transcription", "")
        else:
            print(f"Error processing {file_path}: {response.text}")
            return None


# Read the existing CSV file
with open(csv_file_path, mode="r", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Loop through each row and process the corresponding audio file
for row in rows:
    mp3_file_path = os.path.join(
        folder_path, "cv-valid-dev", row["filename"]
    )  # Assuming the 'filename' column contains the file name
    transcription = transcribe_audio(mp3_file_path)
    if transcription:
        row["generated_text"] = transcription
    else:
        row["generated_text"] = "Error"

# Write the updated CSV with the new "generated_text" column
with open(csv_file_path, mode="w", newline="", encoding="utf-8") as f:
    fieldnames = reader.fieldnames + [
        "generated_text"
    ]  # Add new column for transcriptions
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("Transcriptions saved to cv-valid-dev.csv.")
