import os 
import shutil

def save_uploaded_file(uploaded_file,directory="temp_files"):
    """
    Saves an uploaded file to a temporary directory.
    Returns the file path.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    file_path = os.path.join(directory, uploaded_file.name)


    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    
    return file_path


def cleanup_temp_files(directory="temp_files"):
    """ 
    Deletes the temporary directory and all files inside it.
    """
    if  os.path.exists(directory):
        shutil.rmtree(directory)
