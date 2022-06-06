from datetime import datetime
import os
from socket import *

def print_all_object_attributes(object):
    """
    print_all_object_attributes()

    Purpose:
        This method is responsible to print all attributes names of a given object and the attributes values
        (Source: https://stackoverflow.com/a/53820171/2196301)

    Parameters:
        [object] object - The object which all his attributes should be printed

    Return Value:
        None
    """
    
    for attributeName in dir(object):
        attributeData = getattr(object, attributeName)
        print(f"[{attributeName}] --> {attributeData}")

    return

def is_folder_exists(path):
    """
    is_folder_exists()

    Purpose:
        This method is responsible to check if a given folder path exists or not.
    Parameters:
        [str] path - The path which should be checked
    Return Value:
        [bool] <unnamed> - True - if the folder exists, otherwise False.
    """

    return os.path.isdir(path)

def create_programs_directories(paths):
    """
    create_programs_directories()

    Purpose:
        This method is responsible to create all the neccessary directories for the program.
    Parameters:
        [lst] paths - A list which contains all the paths of the program
    Return Value:
        None
    """

    for path in paths:
        if (is_folder_exists(path) == False):
            os.makedirs(path)

    return

def get_current_time():
    """
    get_current_time()

    Purpose:
        This method is responsible to retrieve the currrent time as a formatted string.
        The format of the time's string is [YEAR-MONTH-DAY][HOURS..MINUTES..SECONDS]
    Parameters:
        None
    Return Value:
        [str] <unnamed> - The time as a formatted string.
    """

    return datetime.now().strftime('[%Y-%m-%d][%H..%M..%S]')

def get_host_ip():
    """
    get_host_ip()

    Purpose:
        This method is responsible to retrieve the ip address of the current host
    Parameters:
        None
    Return Value:
        [str] <unnamed> - The ip of the current host.
    """

    return gethostbyname(gethostname())
