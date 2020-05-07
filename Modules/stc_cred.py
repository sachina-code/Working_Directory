# Module which can be re-used to retrieve Device Credentials

#!/usr/bin/env python

from dotenv import load_dotenv 
load_dotenv()  
import os

# Function to return the stored STC Username and Password
def return_cred():
    user_name = os.environ.get('USER_STC')
    password = os.environ.get('PASSWORD_STC')
    return user_name, password
