import AppUtils
import PhotosFetcher_Server

class Client(object):
    """description of class"""

    _buffer_size = 4096

    def __init__(self, clientSocket, clientAddress, clientLink = None):
        """
        __init__()

        Purpose:
            This method is responsible to construct a new Client object

        Parameters:
            [socket.socket] clientSocket - The socket which belongs to the current client.
            [tuple] - clientAddress - The address of the current client
            [str] - clientLink - The link which the client needs to handle. Default value is None.

        Return Value:
            [Client] <unnamed> - The object itself.
        """

        self._m_ClientSocket  = clientSocket
        self._m_ClientAddress = clientAddress
        self._m_ClientLink    = clientLink

    @property
    def ClientAddress(self):
        """
        ClientLink()

        Purpose:
            Getter of the property ClientAddress

        Parameters:
            None

        Return Value:
            [str] <unnamed> - The current address of the client
        """

        print('Getting address')
        return self._m_ClientAddress

    @ClientAddress.setter
    def ClientAddress(self, value):
        """
        ClientAddress()

        Purpose:
            Setter of the property ClientAddress

        Parameters:
            [str] value - The new address

        Return Value:
            None
        """

        print('Setting address to ' + value)
        self._m_ClientAddress = value

    @property
    def ClientLink(self):
        """
        ClientLink()

        Purpose:
            Getter of the property ClientLink

        Parameters:
            None

        Return Value:
            [str] <unnamed> - The current link
        """

        print('Getting link')
        return self._m_ClientLink

    @ClientLink.setter
    def ClientLink(self, value):
        """
        ClientLink()

        Purpose:
            Setter of the property ClientLink

        Parameters:
            [str] value - The new link

        Return Value:
            None
        """

        print('Setting link to ' + str(value))
        self._m_ClientLink = value


    def download_file(self, folderOfDestinationFile):
        """
        download_file()

        Purpose:
            This method is responsible to download a new file from the client.

        Parameters:
            [str] folderOfDestinationFile - The folder which the file should be saved in.

        Return Value:
            None
        """

        isReadFileProcess = True

        filedata = []

        while isReadFileProcess:
            currentChunk = self._m_ClientSocket.recv(self._buffer_size)

            if currentChunk == b"end of file": # REMEMBER TO CHANGE THIS TO b"end of file" INSTEAD OF b"\n"
                isReadFileProcess = False
            else:
                filedata += [currentChunk]

        # filedata = bytearray(filedata)
        filedata = b"".join(filedata)

        # Save the file's content to filesystem
        with open(folderOfDestinationFile + str(self.ClientAddress) + "_" + AppUtils.get_current_time() + ".png", "wb") as fileobj:
            fileobj.write(filedata)

        return

    def send_link(self, availableLink):
        """
        send_link()

        Purpose:
            This method is responsible to send a link that will be handled by the client.

        Parameters:
            [str] availableLink - The link that will be sent to the client.

        Return Value:
            None
        """

        self.ClientLink = availableLink.split(" ")[0]

        print(f"Sending the link {availableLink} to the client {self.ClientAddress}")

        self._m_ClientSocket.send(availableLink.encode())

    def get_command(self):
        """
        get_command()

        Purpose:
            This method is responsible to receive a new command from the client

        Parameters:
            None

        Return Value:
            [str] data - The command which has been received from the client
        """

        data = self._m_ClientSocket.recv(self._buffer_size)

        return data

    def release_link(self):
        """
        release_link()

        Purpose:
            This method is responsible to release the link which belongs to the current client.

        Parameters:
            None

        Return Value:
            None
        """

        try:

            self._m_ClientSocket.close()
        except Exception as err:
            pass
        finally:
            print(f"{self.ClientLink} is free to use again. {self.ClientAddress} is offline.")
            self.ClientLink = None
        
        return