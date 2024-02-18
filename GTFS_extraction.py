import requests, zipfile, io  # For retrieving and extracting zip file
import filecmp, os            # For updating and comparing files
import shutil                 # For deleting directories
from datetime import datetime # For creating archive directory names

filename = 'GTFS.zip'
url = 'https://www.capitolcorridor.org/googletransit/GTFS.zip'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}


temp = './GTFS_Temp'
current_dir = './GTFS'
old_dir = './GTFS-Old'
archive = './GTFS-Archive'
datetime_format = '%d-%b-%Y_%H:%M:%S.%f'

GTFS_CHANGED = False
GTFS_DATE_CHANGED = "Not Changed Yet"

# If archive directory doesn't exist, then create it
if not os.path.exists(archive):
    print("Creating archive directory")
    os.mkdir(archive)

# Retrieves and extracts zip file to temp directory
print("Downloading...")
# r = requests.get(url, stream=True)
r = requests.get(url, headers=headers,stream=True)
z = zipfile.ZipFile(io.BytesIO(r.content))
print("Extracting...")
z.extractall(temp)

# Checks if we already have existing files
if os.path.exists(current_dir) and os.listdir(current_dir):

    # Compares old files with new files
    print("Comparing...")
    comparison = filecmp.dircmp(temp, current_dir)

    # If they are different sets of files, updates GTFS
    if comparison.left_only or comparison.right_only and comparison.diff_files:
        
        # Adds copy of new files to archive
        print("Archiving...")
        GTFS_DATE_CHANGED = datetime.now().strftime(datetime_format)
        shutil.copytree(temp, archive + '/GTFS_' + GTFS_DATE_CHANGED)

        # Updates current and old GTFS directories
        print("Updating GTFS...")
        if os.path.exists(old_dir):
            shutil.rmtree(old_dir)
        os.rename(current_dir, old_dir)
        os.rename(temp, current_dir)
        GTFS_CHANGED = True

    # Otherwise discards new files
    else:
        print("No need to update")
        shutil.rmtree(temp)
        GTFS_CHANGED = False

# First time downloading the zip file
else:
    print("No new files to check")
    
    # Adds copy of new files to archive
    print("Archiving...")
    GTFS_DATE_CHANGED = datetime.now().strftime(datetime_format)
    shutil.copytree(temp, archive + '/GTFS_' + GTFS_DATE_CHANGED)

    # Sets the current directory
    os.rename(temp, current_dir)
    GTFS_CHANGED = True

# print(f"Content type: {r.headers['content-type']}")
# print(f"Content: {r.content}") 