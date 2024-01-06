import os
import zipfile
from datetime import datetime


def zip():
    log_folder = "log/"

    # Get the current month
    # Get the current month and year
    now = datetime.now()
    current_month = now.month
    current_year = now.year
    previous_month = now.month - 1

    # Check if a new month has arrived
    if current_month != int(open("last_month.txt").read().strip()):
        # Zip the log files
        zip_filename = f"{current_year}{previous_month:02d}.zip"
        zip_filepath = os.path.join(log_folder, zip_filename)

        # Get all files in the log folder with .log extension
        log_files = [file for file in os.listdir(log_folder) if file.endswith(".log")]

        # Add log folder path to each log file
        log_filepaths = [os.path.join(log_folder, file) for file in log_files]

        # Zip the log files
        with zipfile.ZipFile(zip_filepath, "w") as zipf:
            for file in log_filepaths:
                zipf.write(file, os.path.basename(file))

        # Remove all .log files
        for file in log_filepaths:
            if file.endswith(".log"):
                os.remove(file)

        # Update the last_month.txt file with the current month
        with open("last_month.txt", "w") as file:
            file.write(str(current_month))
        
