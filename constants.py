import os
from math import tan, radians
from screeninfo import get_monitors

# This block of code gets info about the subject's monitor
# =======================================================================
# =======================================================================

screen_width_in_centimeters = 31.5
distance_from_screen_in_centimeters = 69

# get screen size for each monitor in the syste m
winfo = get_monitors()
if len(winfo) > 1:
    winX = winfo[1].x
    winY = winfo[1].y
    winWidth = winfo[1].width
    winHeight = winfo[1].height

else:
    winX = winfo[0].x
    winY = winfo[0].y
    winWidth = winfo[0].width
    winHeight = winfo[0].height


os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (winX, winY)

# Get the size in pixels for 2 degrees of visual angle
def deg2pix():
    
    
    # Calculate the total visual angle width in cm
    width_in_cm = 2 * distance_from_screen_in_centimeters * tan(radians(1))
    
    # Calculate the number of pixels per degree as
    pixels_per_cm = winWidth / screen_width_in_centimeters

    # total pixel width
    total_width_in_pixels = width_in_cm * pixels_per_cm

    return total_width_in_pixels

# gives us the size we must scale the images by
stimSize = round(deg2pix())

# screen center for drawing images
screenCenter = ((winWidth // 2) - (stimSize // 2), (winHeight // 2) - (stimSize // 2))


# define some font sizes and colors for easy access

# == Font sizes ==
extraLargeFont = winHeight // 5
largeFont = winHeight // 10
mediumFont = winHeight // 20
smallFont = winHeight // 30

# == Greyscale ==
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREY = [128, 128, 128]
SLATEGREY = [112, 128, 144]
DARKSLATEGREY = [47, 79, 79]


# == Yellows ==
YELLOW = [255, 255, 0]
OLIVE = [128,128,0]
DARKKHAKI = [189,183,107]

# == Greens ==
GREEN = [0, 128, 0]
GREENYELLOW = [173, 255, 47]

RED = [255, 50, 50]


backgroundColor = GREY # background color for screen
textColor = BLACK # text color

# =======================================================================
# =======================================================================

# This block of code defines the valid characters and numbers for text entry
# =======================================================================
# =======================================================================

# getting the valid letters and numbers for user info.
def getValidChars():
    validLetters = []
    validNumbers = []
    
    # valid digits (0 - 9)
    for i in range(48, 58):
        validNumbers.append(chr(i))
        
    # valid lowercase letters (a - z)
    for i in range(97, 123):
        validLetters.append(chr(i))
        
    # valid uppercase letters (A - Z)
    for i in range(65, 91):
        validLetters.append(chr(i))
    
    return validLetters, validNumbers

validLetters, validNumbers = getValidChars()

# =======================================================================
# =======================================================================


# This block of code contains the text for explanation screens
# =======================================================================
# =======================================================================

explanationText = 'In this task you will be shown a series of squares which contain a pattern of black and white dots. \
In half of the trials, a black H will be present in the pattern. You will be asked to determine whether or not the H is in the image. \
It will be very difficult to make this determination, but please trust your intuition. \
You will be stretching the limits of your perception, but previous research shows that people are quite good at this task, even when they feel like they do not think they are doing well.\
The H will not be obvious, but it is always centered, and you will be shown an image of the H for reference before you begin.\n\n\
For each image, please press "Y" if you believe that you see the H and \
press "N" if you do not believe that you see the H.\n\n\
Remember, you will be better at this task than you think.\n\n\
Thank you for participating and please let your experimenter know if you encounter any issues or if you would like to terminate your participation in the experiment.\n\n\
Press the spacebar to continue.\n\n\n'
                
realText = 'Remember to press "Y" if you believe that you see an H.\n\n\
Remember to press "N" if you do not believe that you see an H.\n\n\
You will now be shown the template H that will be in half of the stimuli.\n\n\
You will have 10 seconds to view the template H.\n\n\
After those 10 seconds, the first image will automatically appear and you will begin making your selections.\n\n\
Press the spacebar to continue when you are ready.'

breakScreenText = 'You have earned a break.\n\nPlease let the experimenter know.\n\n\
When you are ready you will be shown the template again and resume your task.\n\n'

exitScreenText = 'Thank you for participating in this study!\n\n'\
'Please notify the experimenter that you have completed the study.\n\n'\

questionnairesIntroText = 'You will now respond to some questionnaires.\n\nPlease read each question carefully and respond truthfully.\n\nPress the spacebar to begin.'
telleganScaleText = 'Please respond True or False to the following questions.\n\nPress the spacebar to begin.'
launeyScaleText = 'Please indicate the degree to which the following statements describe you on a scale from 1 (not at all like me) to 8 (extremely like me).\n\nPress the spacebar to begin.'
dissociativeExperiencesText = 'This questionnaire consists of twenty-eight questions about experiences that you may have in your daily life. We are interested in how often you have these experiences. It is important, however, that your answers show how often these experiences happen to you when you are not under the influence of alcohol or drugs.\n\nTo answer the questions, please determine to what degree the experience described in the question applies to you and click the box corresponding to what percentage of the time you have the experience.\n\n Press the spacebar to begin.'
experimentIntroText = 'You have now completed the questionnaires.\n\nYou will now begin the main experiment.\n\nPress the spacebar to continue'
# =======================================================================
# =======================================================================



# map the weighting scheme/correlation scheme pair to the actual path to the images
ImageFolderPathDict = {
        ('unweighted', 'icorrelated', 'target'): 'unweightedICorrelatedH',
        ('unweighted', 'icorrelated', 'distractor'): 'unweightedI',
        ('unweighted', 'uncorrelated', 'target'): 'unweightedUncorrelatedH',
        ('unweighted', 'uncorrelated', 'distractor'): 'unweightedUncorrelated',
        ('gaussian', 'icorrelated', 'target'): 'gaussianICorrelatedH',
        ('gaussian', 'icorrelated', 'distractor'): 'gaussianI',
        ('gaussian', 'uncorrelated', 'target'): 'gaussianUncorrelatedH',
        ('gaussian', 'uncorrelated', 'distractor'): 'gaussianUncorrelated',
    }                
    

 