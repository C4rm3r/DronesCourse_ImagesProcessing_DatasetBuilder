# Drones Course - Image Processing Team - Dataset Builder

This GitHub repository contains a Client-Server based system that allows data scientists to photos from youtube videos.
This system was developed to allow the creation of an Images Dataset without an actual need to purchase a camera and take photos manually.

The server side contains a text file that all the desired videos to capture images from should be placed in it. System Administrators should add links to the videos (either live or not) and the system will use them.

The system was developed by Aviv Aharon from the Image Processing Team (Drones Course) in H.i.T (2022)

## How to run it?

1. Clone the GitHub repository to your local machine

2. In the server directory, go to the links.txt file and fulfill it to contain the desired videos.

3. Prepare as many PCs (which will behave as Clients) as you want
   
   **Note:** The maximum number of clients which can be launched equals the number of the links in the file `links.txt` on the server side.

4. Install the required dependencies in the client's PCs. Run the following: `pip install -r requirements.txt`

5. Run the server
   Note: you can open the project with the .sln file and run the server from there or from the command line...)

6. Run the clients
   Note: in order to run the client correctly, use the following command template:

   `PhotosFetcher_Client.py -t <server_ip_addr> -p <server_port> -d <duration>`, where "duration" means "how many seconds to wait between 2 photos that being taken from the current video?".

   **Alternative:** You can run the client with the `ClientLauncher.bat`, but you will have to change the hardcoded IP address for every client.
