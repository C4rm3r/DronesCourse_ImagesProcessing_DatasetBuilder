###################
#                 #
#     Imports     #
#                 #
###################

from socket import *
import threading
import AppUtils
import pyautogui
import argparse
import os
import time
import msvcrt
import threading
import sys

###################
#                 #
#    Constants    #
#                 #
###################

USER_AGENT              = { 'User-agent' : 'Mozilla/5.0' }
PATH_OF_GENERAL_OUTPUTS = ".\\outputs\\"
SERVER_IP               = None
SERVER_PORT             = 5000
LINKS                   = {}
CLIENTS                 = []
BUFFER_SIZE             = 4096

###################
#                 #
#     Methods     #
#                 #
###################

def get_script_arguments():

    """
    get_script_arguments()

    Purpose:
        Retrieve the script's arguemnts from the command line.

    Parameters:
        None

    Return Value:
        [dict] args - The argument which contains all the given arguments.
    """

    parser = argparse.ArgumentParser(description='PhotosFetcher_Client.py')
    parser.add_argument('-t','--target-ip', help='The IP address of the server', required=True)
    parser.add_argument('-p','--target-port', help='The port of the server', required=True, type=int)
    parser.add_argument('-d','--duration', help='The duration to take photos from the given url', required=True, type=int)
    args = vars(parser.parse_args())

    return args

def launch_client_activity(sock, target_ip, target_port, duration):
    """
    launch_client_activity()

    Purpose:
        Launch the activity of the client against the server

    Parameters:
        [socket.socket] sock - The socket object which will be used to communicate with the server
        [str] target_ip      - The ip address of the remote server
        [int] target_port    - The port of the remote server
        [int] duration       - The duration for taking screenshots

    Return Value:
        None
    """

    global BUFFER_SIZE

    sock.connect((target_ip, target_port))
    initializationParts = sock.recv(BUFFER_SIZE).decode("utf-8").split(" ")
    linkToHandle, BUFFER_SIZE = initializationParts[0], int(initializationParts[1])

    os.system("start " + linkToHandle)
    time.sleep(10)
    pyautogui.press('m')
    pyautogui.press('f')
    time.sleep(5)

    while True:
        currentTime = AppUtils.get_current_time()
        pyautogui.screenshot(f'image_{currentTime}.png')

        # Get the size of the file (Source: https://stackoverflow.com/a/6591957/2196301)
        fileSize = os.path.getsize(f'image_{currentTime}.png')

        # Send the file to the server
        # Source for logic of reading file in chunks: https://stackoverflow.com/a/19802839/2196301
        with open(f'image_{currentTime}.png', 'rb') as fileobj:

            print(f"Sending the file: \"image_{currentTime}.png\"")

            lastIndex = 0
            isUploadProcessOn = True

            sock.send("new file".encode())

            while isUploadProcessOn:
                piece = fileobj.read(BUFFER_SIZE)
                if piece:
                    print(f"Length of current piece: {len(piece)} bytes")
                    print(f"Sending bytes {lastIndex}-{lastIndex + len(piece)}")
                    lastIndex += len(piece)
                    sock.send(piece)
                else:
                    time.sleep(1)
                    sock.send(b"end of file")
                    isUploadProcessOn = False

            print("*" * 60)

        time.sleep(duration)

    return

def main():
    """
    main()

    Purpose:
        The main function of the program.
        This function handles keystrokes and launching the client's activity in a new deamon thread.

    Parameters:
        None

    Return Value:
        None
    """

    global BUFFER_SIZE

    args = get_script_arguments()

    print(args)

    target_ip   = args["target_ip"]
    target_port = args["target_port"]
    duration    = args["duration"]

    sock = socket(AF_INET, SOCK_STREAM)
    thread = threading.Thread(target = launch_client_activity, args = (sock, target_ip, target_port, duration))

    # Set the thread to be a deamon thread, which means it will be killed when the main thread will be killed too.
    # (Source: https://stackoverflow.com/a/1667825/2196301)
    thread.setDaemon(True)
    thread.start()

    while True:
        key = msvcrt.getch()
        if key == b'r':
            print("Release requested. Exiting ...")
            sock.send(b"release")
            print("Command \"release\" has been successfully sent.")
            sys.exit(0)

    return

if __name__ == '__main__':
    main()