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

explanationText = 'Welcome to this fascinating visual perception task! As part of this experiment, you will encounter a series of images filled with a mix of black and white dots. Within half of these images, a black "H" will be subtly embedded. Your challenge is to identify whether the "H" is present in each image. This task will test the limits of your perception, urging you to trust the subtle hints and the instincts that might suggest the presence of the "H".\n\n\
Even though spotting the "H" might seem daunting at first, believe in your intuitive abilities. Research has consistently shown that people can perform remarkably well on such tasks, often exceeding their own expectations. The "H" will be centered but obscured, and we will provide you with a reference image of the "H" before you start, to help guide your observations.\n\n\
When you are ready to make a decision for each image, press "Y" if you feel the "H" is there, or press "N" if you think it is absent. Remember, more often than not, your first impression might be more accurate than you realize.\n\n\
We thank you for participating and value your contributions to this study. Should you have any questions, or if you decide to stop participating, please inform your experimenter immediately.\n\n\
Press the spacebar when you are ready to begin the experiment. Good luck, and trust in the power of your perception!'

                
realText = 'Remember, you are looking for the template "H", which will always be black, centered, and on a white background. It will always appear in the same place if it is present, and it is present in half of the images.\n\n\
After viewing the template "H" for 20 seconds, you will begin assessing each image. Press "Y" if you believe the "H" is in the image, and press "N" if you do not see it. The task consists of four rounds, and you will receive a short break between each round to rest.\n\n\
Press the spacebar when you are ready to proceed and start making your selections.\n\n\
Good luck, and believe in yourself! It is normal to feel unsure, as many participants think they are not doing well, but you will likely perform better than you expect!'

realTextAlt = 'Remember, you are looking for the template "H", which will always be black, centered, and on a white background. It will always appear in the same place if it is present, and it is present in half of the images.\n\n\
After viewing the template "H" for 20 seconds, you will begin assessing each image. Press "Y" if you believe the "H" is in the image, and press "N" if you do not see it. \n\n\
Press the spacebar when you are ready to proceed and start making your selections.\n\n\
Good luck, and believe in yourself! It is normal to feel unsure, as many participants think they are not doing well, but you will likely perform better than you expect!'

def breakScreenText(i):
    return f'You have now completed {i} out of 4 rounds.\n\n You have earned a break.\n\n Please let the experimenter know.\n\n\
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
    

 