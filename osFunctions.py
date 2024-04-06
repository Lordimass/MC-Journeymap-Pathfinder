import os

# Check whether dir exists, if not create it and prompt user to upload files
def check_for_directory(dir, 
                        success_response = None, 
                        fail_response = None):
    directoryExists = False
    for fileName in os.listdir(): # Checking Directory
        if fileName == dir:
            directoryExists = True
            print(success_response)
            return True

    if not directoryExists: # Creating directory given that it doesn't already exist
        os.mkdir(dir)
        print(fail_response)
        return False

