import requests, zipfile, io  # For retrieving and extracting zip file
import filecmp, os            # For updating and comparing files
import shutil                 # For deleting directories

filename = 'GTFS.zip'
url = 'https://www.capitolcorridor.org/googletransit/GTFS.zip'
temp_dest = './temp'
final_dest = './GTFS'

# Retrieves and extracts zip file
print("Downloading...")
r = requests.get(url, stream=True)
z = zipfile.ZipFile(io.BytesIO(r.content))
print("Extracting...")
z.extractall(temp_dest)

# Checks if we already have existing files
if os.path.exists(final_dest) and os.listdir(final_dest):

    # Compares old files with new files
    comparison = filecmp.dircmp(temp_dest, final_dest)
    print("Comparing...")

    # If they are different sets of files, updates GTFS
    if comparison.diff_files:
        shutil.rmtree(final_dest)
        os.rename(temp_dest, final_dest)
        print("Updating GTFS...")

    # Otherwise discards new files
    else:
        shutil.rmtree(temp_dest)
        print("No need to update")

# First time downloading the zip file
else:
    os.rename(temp_dest, final_dest)
    print("No new files to check")