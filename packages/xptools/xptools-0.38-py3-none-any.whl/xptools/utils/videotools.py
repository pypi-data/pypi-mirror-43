import av
import numpy as np
from skimage import img_as_ubyte
from skimage.color import rgb2gray
from skimage.filters import threshold_minimum

def open_video(file):
    """
    Opens a video file and returns a list of numpy arrays corresponding to each frame.
    The images in the stack are converted to ubyte and gray scale for further processing.
    
    Parameters
    ----------
    file : string
        path of the file to open

    Returns
    -------
    list
        a list of numpy arrays each containing a frame of the video
    """

    v = av.open(file)
    stack = []
    for frame in v.decode(video=0):
        img = frame.to_image()
        #Convert the img to a numpy array, convert to grayscale and ubyte.
        img_gray = img_as_ubyte(rgb2gray(np.asarray(img)))
        stack.append(img_gray)
    return stack

def determine_threshold(stack):
    """Determines the threshold to use for a video based on the minimum threshold algorithm.
    Returns the value obtained by running a minimum threshold algorithm on the median image of the stack.

    Parameters
    ----------
    stack : list
        list of numpy arrays each containing a frame of a video

    Returns
    -------
    int
        threshold value for the video

    TODO: increase robustness by comparing thresholds obtained on different images and choosing the best one.
    """
    img = stack[int(len(stack)*0.25)]
    return threshold_minimum(img)

def obtain_cropping_boxes(file_list):
    """Prompts the user to select the region of interest for each video file.

    Parameters
    ----------
    file_list : list (str)
        list of path of the video files to process

    Returns
    -------
    Dictionary {'Name', 'CroppingBox'}
        A dictionary containing the selected region for each file.
        Name (str): name of the file without the extension
        CroppingBox (tuple (int)): rectangle coordinates following the numpy array convention (minRow, minCol, maxRow, maxCol).
    """
    #Imports
    from xptools.utils import select_roi
    #Create a dictionary to hold the cropping boxes
    dict_crop = {}
    #Determine the bounding boxes
    for file in file_list:
        #Extract experiment name from filename
        name = file.split('.')[0].split('/')[-1]
        #Open the file and get a stack of grayscale images
        stack = open_video(file)
        #Select the region of interest
        rectangle = None
        while rectangle == None:
            rectangle = select_roi.select_rectangle(stack[len(stack) - 10])
        dict_crop[name]=rectangle
    return dict_crop