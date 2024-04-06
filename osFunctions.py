import os
import sys

# Check whether dir exists, if not create it and prompt user to upload files
def check_for_directory(dir, 
                        success_response = None, 
                        fail_response = None):
    directoryExists = False
    for fileName in os.listdir(): # Checking Directory
        if fileName == dir:
            directoryExists = True
            if success_response != None:
                print(success_response)
            return True

    if not directoryExists: # Creating directory given that it doesn't already exist
        os.mkdir(dir)
        if fail_response != None:
            print(fail_response)
        return False

def quit(custom_message = "Press any key to continue..."):
    input(custom_message)
    sys.exit()