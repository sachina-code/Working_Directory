# Module which can be re-used to retrieve Device Credentials

#!/usr/bin/env python

from dotenv import load_dotenv 
load_dotenv()  
import os

# To retrieve the stored STC Username and Password

user_name = os.environ.get('USER_STC')
password = os.environ.get('PASSWORD_STC')
