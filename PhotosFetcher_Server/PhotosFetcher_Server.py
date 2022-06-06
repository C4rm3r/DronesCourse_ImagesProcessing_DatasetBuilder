###################
#                 #
#     Imports     #
#                 #
###################

from socket import *
import threading
import Client
import AppUtils

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

def read_links_file(path = ".\links.txt"):
    """
    read_links_file()

    Purpose:
        Read the file which contians all the links into a dictionary

    Parameters:
        [str] path - The path of the file with the links. Default path is ".\links.txt"

    Return Value:
        None
    """

    global LINKS

    with open(path, "r+") as fileobj:
        readLinks = [link.strip().rstrip() for link in fileobj.readlines()]
        LINKS = { currentLink: False for currentLink in readLinks }

    return

def create_server_socket():
    """
    handle_new_client()

    Purpose:
        Create the socket of the server

    Parameters:
        None

    Return Value:
        None
    """

    global SERVER_PORT

    serverSock = socket(AF_INET, SOCK_STREAM)
    # serverSock.bind((SERVER_IP, 0))
    # SERVER_PORT = serverSock.getsockname()[1]
    serverSock.bind((SERVER_IP, SERVER_PORT))
    serverSock.listen(len(LINKS))

    return serverSock

def handle_new_client(client):
    """
    handle_new_client()

    Purpose:
        Handle the communication with the new client

    Parameters:
        [socket.socket] client - The socket object which will be used to communicate with the current client

    Return Value:
        None
    """

    global LINKS
    global CLIENTS

    isCLientAlive = True

    # Get the first non-occupied link from the list of links
    availableLink = [link for link in LINKS.keys() if LINKS[link] == False][0]

    # Send the link to the current client
    client.send_link(availableLink + " " + str(BUFFER_SIZE))

    # Set the current link as occupied
    LINKS[availableLink] = True

    while isCLientAlive:

        try:
            currentCommand = client.get_command()
            currentCommand = currentCommand.decode("utf-8").rstrip()

            if "new file" in currentCommand:
                client.download_file(PATH_OF_GENERAL_OUTPUTS)
                
            elif "release" in currentCommand:
                raise Exception("Release has been requested")

            else:
                print(f"Some not supported command has been received. Command is: {currentCommand}")
        except Exception as err:

            if str(err) != "Release has been requested":
                print(err)

            LINKS[client.ClientLink] = False
            client.release_link()
            CLIENTS.remove(client)
            isCLientAlive = False

    return

def main():
    """
    main()

    Purpose:
        The main function of the program.
        This function handles keystrokes and launching the server's activity in a new deamon thread.

    Parameters:
        None

    Return Value:
        None
    """
    
    global CLIENTS
    global SERVER_IP

    AppUtils.create_programs_directories([PATH_OF_GENERAL_OUTPUTS])
    SERVER_IP = AppUtils.get_host_ip()

    print(f"server ip is: {SERVER_IP}")
    print(f"server port is: {SERVER_PORT}")
    read_links_file()

    serverSock = create_server_socket()

    while True:
        clientSock, clientAddr = serverSock.accept()

        if clientSock not in CLIENTS:

            currentClientObject = Client.Client(clientSock, clientAddr)

            CLIENTS += [currentClientObject]

            print(f"New Connection established. Client address is: {clientAddr}")

            thread = threading.Thread(target=handle_new_client, args = (currentClientObject,))
            thread.start()

    return

if __name__ == '__main__':
    main()