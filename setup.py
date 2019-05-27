import os
import requests
import zipfile

facenet_url = 'https://github.com/davidsandberg/facenet'
file_id = '1EXPBSXwTaqrSC0OhUdXNmKSh9qJUQ55-'

def download_file_from_google_drive(id, destination):
    default_model_url = "https://drive.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(default_model_url, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)
    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(default_model_url, params = params, stream = True)
    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

if __name__ == '__main__': 
    print("Cloning the facenet from git...")
    os.system("git clone " + facenet_url)
    print("Downloading the model from google drive...")
    destination = os.path.join(os.getcwd(), 'model.zip')
    download_file_from_google_drive(file_id, destination)
    os.makedirs(os.path.join(os.getcwd(), 'models'))
    zip_file = zipfile.ZipFile(destination)
    for names in zip_file.namelist():
        zip_file.extract(names, os.path.join(os.getcwd(), 'models'))
    zip_file.close()

