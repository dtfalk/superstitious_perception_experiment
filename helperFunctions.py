import os
import sys
import csv
from random import choice
from scipy.stats import norm
import pygame as pg
import pytz
from datetime import datetime
from constants import *


imageWidth, imageHeight = 50, 50
imageSize = imageWidth * imageHeight

# class for the buttons the user will see
class Button:

    # initializes an instance of a button
    def __init__(self, buttonType, questionnaireName, text, i, yPosQuestion):

         # creates a box to click and text for questionnaire options
        if buttonType == 'option':
            self.fontSize = mediumFont
            if questionnaireName == 'tellegen':
                scalar = 1.75
            elif questionnaireName == 'launay':
                scalar = 1.4
            elif questionnaireName == 'dissociative':
                scalar = 1.5
            spacing = scalar * i * self.fontSize 
            buffer = winHeight // 20
            maxY = (0.85 * winHeight) - self.fontSize
            self.coords = ((0.05 * winWidth) + (0.45 * winWidth) * ((yPosQuestion + spacing + buffer) // maxY), 
                           yPosQuestion + buffer + (spacing % (maxY - (yPosQuestion + buffer))), 
                           self.fontSize, 
                           self.fontSize)
            self.text_x = self.coords[0] + 1.5 * self.fontSize
            self.text_y = self.coords[1] - 0.1 * self.fontSize
            
        else: # creates the submit button so the user may submit their response
            self.fontSize = int(0.85 * mediumFont)
            self.coords = (0.45 * winWidth, 0.85 * winHeight, 0.1 * winWidth, 1.1 * self.fontSize)
            self.text_x = 0.46 * winWidth
            self.text_y = self.coords[1]
        
        self.color = WHITE
        self.text = text
        self.checkbox = pg.Rect(self.coords)
        self.checked = False # is the checkbox checked or not
        self.buttonType = buttonType # question option vs submit button
    
    # draw function for each button
    def draw(self, win):
        pg.draw.rect(win, self.color, self.checkbox)
        text_surface = pg.font.SysFont("times new roman", self.fontSize).render(self.text, True, BLACK)     
        win.blit(text_surface, (self.text_x, self.text_y))

    # handles button clicks
    def handleClick(self, buttons):
        if self.buttonType == 'option':
            self.checked = not self.checked # switch button state
            if self.checked: # if selected, change color to red
                self.color = RED
            else: # if unselected, change color to white
                self.color = WHITE 
            self.unselectOthers(buttons)
            return None
        else:
            for button in buttons:
                if button.checked and button != self:
                    self.checked = True
                    return button.text
            
    # unselects all other questions
    def unselectOthers(self, buttons):
        for button in buttons:

            # don't unclick button just clicked or "unclick" the submit button
            if button == self or button.buttonType != 'option':
                continue

            # if something is already checked, then uncheck it
            if button.checked:
                button.checked = False
                button.color = WHITE

# This block of code handles lab streaming layer functionality
# =======================================================================
# =======================================================================

# # Initializes lab streaming layer outlet
# def initializeOutlet():
#     infoEvents = StreamInfo('eventStream', 'events', 1, 0, 'string')
#     outlet = StreamOutlet(infoEvents)
#     return outlet

# # pushes a sample to the outlet
# def pushSample(outlet, tag):
#     outlet.push_sample([tag])

# =======================================================================
# =======================================================================



# These functions are for collecting/saving user/experiment data
# =======================================================================
# =======================================================================

# stops game execution until a particular key is pressed
def waitKey(key):

    # just keep waiting until the relevant key is pressed
    while True:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == key:
                    return
                elif event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

# function to draw/fit a multiline message to the screen
def multiLineMessage(text, textsize, win, xPos_start = 0.05 * winWidth, yPos_start = 0.05 * winHeight, xMax = 0.95 * winWidth, yMax = 0.95 * winHeight):

    # set font and text color
    font = pg.font.SysFont("times new roman", textsize)
    color = BLACK

    # Function to calculate if the text fits within the designated area
    def fitsWithinArea(text, font):

        # starting x and y coordinate for the text
        xPos = xPos_start
        yPos = yPos_start

        # Get line height based on font size
        lineHeight = font.get_linesize() 
        lines = text.split('\n')
        for line in lines:

            # Handle empty lines for consecutive newlines
            if line == '':
                yPos += lineHeight
            
            # Handle non-empty lines
            else:
                words = line.split()
                for word in words:
                    word_surface = font.render(word, True, color)
                    wordWidth, _ = word_surface.get_size()

                    # Check if new word exceeds the line width
                    if xPos + wordWidth > xMax: 

                        # Reset to start of the line
                        xPos = xPos_start

                        # Move down by the height of the previous line
                        yPos += lineHeight

                    # Check if adding another line exceeds the page height
                    if yPos + lineHeight > yMax:
                        return False
                    
                    # Blit here for size calculation
                    win.blit(word_surface, (xPos, yPos))

                    # Move xPos for the next word, add space
                    xPos += wordWidth + font.size(" ")[0] 
                
                # reset x position and increment y position by height of text
                xPos = xPos_start
                yPos += lineHeight
        return True

    # Adjust font size until the text fits within the area
    while not fitsWithinArea(text, font) and textsize > 1:
        textsize -= 1
        font = pg.font.SysFont("times new roman", textsize)

    # Draw the background and boundaries only once
    win.fill(backgroundColor)

    # Now draw the text with the properly adjusted font size
    xPos = xPos_start
    yPos = yPos_start
    lineHeight = font.get_linesize()
    lines = text.split('\n')

    # iterate over each line
    for line in lines:

        # Handle empty lines for consecutive newlines
        if line == '':
            yPos += lineHeight

        # Handle non-empty lines
        else:

            # split the line into its constituent words
            words = line.split()

            # iterate over each words
            for word in words:

                # render the word and get the size of the word
                word_surface = font.render(word, True, color)
                wordWidth, _ = word_surface.get_size()

                # Check if word exceeds line width
                if xPos + wordWidth > xMax:

                    # reset x position and increment y position
                    xPos = xPos_start
                    yPos += lineHeight
                
                # draw word
                win.blit(word_surface, (xPos, yPos))

                # increment x position by word width
                xPos += wordWidth + font.size(" ")[0]
            
            # reset x position and increment y position
            xPos = xPos_start
            yPos += lineHeight

    return yPos

# returns true if user enters a valid key (a-z or 0-9 or spacebar)
def isValid(key, requestType):

    # response only allows a-z and spaces
    if 'name' in requestType:
        if 97 <= key <= 122 or key == 32:
            return True

    # subject number and level selection only allow digits
    elif requestType == 'subject number':
        if 48 <= key <= 57:
            return True
    
    # subejct email
    else:
        if (97 <= key <= 122) or (48 <= key <= 57) or key == 64 or key == 46 or key == 45:
            return True
        
    return False
    
# gets user's response and subject ID
def getSubjectInfo(requestType, win):

    response = "" 
    exit = False

    # event loop
    while True:
        for event in pg.event.get():

            # if user presses a key, then...
            if event.type == pg.KEYDOWN:

                # lets the user quit
                if event.key == pg.K_ESCAPE:
                    exit_key = pg.K_ESCAPE
                    exit = True
                    
                # if they press enter or return, then...
                if event.key == pg.K_KP_ENTER or event.key == pg.K_RETURN:
                    
                    if len(response) > 0:
                        
                        # set the exit key to the key they pressed and set the exit boolean to true
                        exit_key = event.key
                        exit = True
                
                # delete last character if they press backspace or delete
                elif event.key == pg.K_BACKSPACE or event.key == pg.K_DELETE:
                    response = response[:-1] 
                
                # if they enter a valid key (a-z, 0-9, or spacebar)
                elif isValid(event.key, requestType):
                    if (pg.key.get_mods() & pg.KMOD_CAPS) or (pg.key.get_mods() & pg.KMOD_SHIFT):
                        if event.key == 50:
                            response += '@'
                        else:
                            response = response + chr(event.key).upper()
                    else:
                        response = response + chr(event.key).lower()
        if exit == True:
            break
        win.fill(backgroundColor) 
        text = "Please enter the requested information. Then press Enter or Return to continue. Press ESC to exit or inform the observer of your decision. \n\n"
        multiLineMessage(text + f'\n{requestType}: ' + response, mediumFont, win)
        pg.display.flip()

    # if the user pressed either return or enter, then we continue
    if exit_key == pg.K_RETURN or exit_key == pg.K_KP_ENTER:
        return response 
    
    # otherwise, they pressed the exit key and we exit the game
    else:
        pg.quit()
        sys.exit()
        

# records a user's response to a given trial
def recordResponse(subjectName, subjectNumber, block, stimulusNumber, stimulusType, response, responseTime, saveFolder):
    
    # path to the save file
    filePath = os.path.join(saveFolder, f'{block}.csv')

    # prepare the header and the data
    header = ['Subject Name', 'Subject Number', 'Block Scheme', 'Stimulus Number', 'Stimulus Type', 'Subject Response', 'Response Time']
    data = [subjectName, subjectNumber, block, stimulusNumber, stimulusType, response, '%.5f'%(responseTime / 1000)]

    # if csv file does not exist, then write the header and the data
    if not os.path.exists(filePath):
        with open(filePath, mode = 'w', newline = '') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerow(data)

    # otherwise just write the data
    else:
        with open(filePath, mode = 'a', newline = '') as file:
            writer = csv.writer(file)
            writer.writerow(data)
    return

# calculates a dprime score
def calculateDprime(hits, misses, correctRejections, falseAlarms):
    
    try: 
        hitRate = hits / (hits + misses)
        falseAlarmRate = falseAlarms / (falseAlarms + correctRejections)
    except:
        return 'NaN'

    # values for fixing extreme d primes
    halfHit = 0.5 / (hits + misses)
    halfFalseAlarm = 0.5 / (falseAlarms + correctRejections)

    if hitRate == 1:
        hitRate = 1 - halfHit
    if hitRate == 0:
        hitRate = halfHit
    if falseAlarmRate == 1:
        falseAlarmRate = 1 - halfFalseAlarm
    if falseAlarmRate == 0:
        falseAlarmRate = halfFalseAlarm

    # calculate z values
    hitRateZScore = norm.ppf(hitRate)
    falseAlarmRateZScore = norm.ppf(falseAlarmRate)

    # calculate d prime
    dprime = hitRateZScore - falseAlarmRateZScore

    return dprime

# writes summary data about user's performance
def writeSummaryData(subjectName, subjectNumber, blocks, saveFolder):

    # Path to where we save the data
    filePath = os.path.join(saveFolder, 'summaryData.csv')

    # add files in correct order so we load and calculate data in correct order
    dataFiles = []
    for block in blocks:
        dataFiles.append(os.path.join(saveFolder, f'{block}.csv'))
    

    # caclulate dprimes for uncorrelated distractors
    dprimes = []
    for dataFile in dataFiles:
        with open(dataFile, mode = 'r', newline = '') as f:
            reader = csv.reader(f)
            lines = list(reader)
            header = lines[0]
            data = lines[1:]

            # create a dictionary to easily access data entries
            indices = {}
            for i, entry in enumerate(header):
                indices[entry] = i

            # collecting relevant data for calculating dprime
            hits = 0
            misses = 0
            falseAlarms = 0
            correctRejections = 0

            for entry in data:
                if entry[indices['Stimulus Type']] == 'target' and entry[indices['Subject Response']] == 'target':
                    hits += 1
                elif entry[indices['Stimulus Type']] == 'target' and entry[indices['Subject Response']] == 'distractor':
                    misses += 1
                elif entry[indices['Stimulus Type']] == 'distractor' and entry[indices['Subject Response']] == 'target':
                    falseAlarms += 1
                else:
                    correctRejections += 1
            print(dataFile)
            print(hits)
            print(misses)
            print(falseAlarms)
            print(correctRejections)
            dprime = calculateDprime(hits, misses, correctRejections, falseAlarms)
            dprimes.append(dprime)

    # prepare header and data for writing
    summaryDataHeader = ['Subject Name', 'Subject Number',  'Block 1', 'Block 1 D-Prime', 'Block 2', 'Block 2 D-Prime', 'Block 3', 'Block 3 D-Prime', 'Block 4', 'Block 4 D-Prime']
    summaryData = [subjectName, subjectNumber]
    for i, block in enumerate(blocks):
        summaryData.append(f'{block}')
        summaryData.append(dprimes[i])


    # write results to summary data file
    with open(filePath, mode = 'w', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(summaryDataHeader)
        writer.writerow(summaryData)
        

# =======================================================================
# =======================================================================
        
# a lists of the stimuli
def getStimuli():
    
    # get the current file's path
    stimuliDir = os.path.join(os.path.dirname(__file__), 'stimuli')

    # list of file names as paths (gaussian)
    gaussianHStimuli_uncorrelated = [os.path.join(stimuliDir, 'gaussianUncorrelatedH', fileName) for fileName in os.listdir(os.path.join(stimuliDir, 'gaussianUncorrelatedH'))]
    gaussianHStimuli_vcorrelated = [os.path.join(stimuliDir, 'gaussianVCorrelatedH', fileName) for fileName in os.listdir(os.path.join(stimuliDir,'gaussianVCorrelatedH'))]
    gaussianVStimuli = [os.path.join(stimuliDir, 'gaussianV', fileName) for fileName in os.listdir(os.path.join(stimuliDir,'gaussianV'))]
    gaussianNoCorrelationStimuli = [os.path.join(stimuliDir, 'gaussianUncorrelated', fileName) for fileName in os.listdir(os.path.join(stimuliDir,'gaussianUncorrelated'))]

    # list of file names as paths (unweighted)
    unweightedHStimuli_uncorrelated = [os.path.join(stimuliDir, 'unweightedUncorrelatedH', fileName) for fileName in os.listdir(os.path.join(stimuliDir, 'unweightedUncorrelatedH'))]
    unweightedHStimuli_vcorrelated = [os.path.join(stimuliDir, 'unweightedVCorrelatedH', fileName) for fileName in os.listdir(os.path.join(stimuliDir,'unweightedVCorrelatedH'))]
    unweightedVStimuli = [os.path.join(stimuliDir, 'unweightedV', fileName) for fileName in os.listdir(os.path.join(stimuliDir,'unweightedV'))]
    unweightedNoCorrelationStimuli = [os.path.join(stimuliDir, 'unweightedUncorrelated', fileName) for fileName in os.listdir(os.path.join(stimuliDir,'unweightedUncorrelated'))]

    return gaussianHStimuli_uncorrelated,  gaussianHStimuli_vcorrelated, gaussianVStimuli, gaussianNoCorrelationStimuli, \
    unweightedHStimuli_uncorrelated, unweightedHStimuli_vcorrelated, unweightedVStimuli, unweightedNoCorrelationStimuli 



# This code is for showing various message screens (e.g. experiment explanation)
# and functions that display images
# =======================================================================
# =======================================================================

# shows the template H
def showTemplate(win, text = ''):

    templateImagePath = os.path.join(os.path.dirname(__file__), 'templates', 'H.png')
    image = pg.transform.scale(pg.image.load(templateImagePath), (stimSize, stimSize))

    # display template to user for 10 seconds
    win.fill(backgroundColor)
    multiLineMessage(text, mediumFont, win, yMax = int(0.95 * (screenCenter[1] - (stimSize // 2))))
    win.blit(image, screenCenter)
    pg.display.flip()
    startTime = pg.time.get_ticks()
    while True:
        if text == '':
            if pg.time.get_ticks() - startTime >= int(20 * 1000):
                return
        
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                elif event.key == pg.K_SPACE:
                    return

# shows the example stimuli
def showExamples(win, text = ''):

    example_image_path = os.path.join(os.path.dirname(__file__), 'exampleStimuli', 'example.png')
    example_image = pg.transform.scale(pg.image.load(example_image_path), (stimSize, stimSize))

    nonexample_image_path = os.path.join(os.path.dirname(__file__), 'exampleStimuli', 'nonexample.png')
    nonexample_image = pg.transform.scale(pg.image.load(nonexample_image_path), (stimSize, stimSize))

    templateImagePath = os.path.join(os.path.dirname(__file__), 'templates', 'H.png')
    templateImage = pg.transform.scale(pg.image.load(templateImagePath), (stimSize, stimSize))

    # display template to user for 10 seconds
    win.fill(backgroundColor)
    multiLineMessage(text, mediumFont, win, yMax = int(0.95 * (screenCenter[1] - (stimSize // 2))))
    win.blit(templateImage, screenCenter)
    win.blit(example_image, (screenCenter[0] // 2, screenCenter[1]))
    win.blit(nonexample_image, (3 * (screenCenter[0] // 2), screenCenter[1]))
    pg.display.flip()
    while True:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                elif event.key == pg.K_SPACE:
                    return


# Tell the user that they are beginning the real experiment and have completed the questionnaires
def experimentIntro(win):
    win.fill(backgroundColor)
    multiLineMessage(experimentIntroText, mediumFont, win)
    pg.display.flip()
    waitKey(pg.K_SPACE)

# explains the experiment to the subject
def experimentExplanation(win):
    win.fill(backgroundColor)
    multiLineMessage(explanationText_1, mediumFont, win)
    pg.display.flip()
    waitKey(pg.K_SPACE)

    win.fill(backgroundColor)
    multiLineMessage(explanationText_2, mediumFont, win)
    pg.display.flip()
    waitKey(pg.K_SPACE)

    win.fill(backgroundColor)
    multiLineMessage(explanationText_3, mediumFont, win)
    pg.display.flip()
    waitKey(pg.K_SPACE)

    win.fill(backgroundColor)
    multiLineMessage(explanationText_4, mediumFont, win)
    pg.display.flip()
    waitKey(pg.K_SPACE)

    showTemplate(win, text = 'This is an image of the “H” that will be hidden within half of the images you will see.\n\nPress the spacebar to continue.')
    showExamples(win, text = showExamplesText)

    win.fill(backgroundColor)
    multiLineMessage(explanationText_5, mediumFont, win)
    pg.display.flip()
    waitKey(pg.K_SPACE)

# instructions for the real trials
def finalInstructions(win):
    win.fill(backgroundColor)
    multiLineMessage(realText, mediumFont, win)
    pg.display.flip()
    waitKey(pg.K_SPACE)

# instructions for the real trials
def realInstructionsAlt(win):
    win.fill(backgroundColor)
    multiLineMessage(realTextAlt, mediumFont, win)
    pg.display.flip()
    waitKey(pg.K_SPACE)

# break screen thanking the participant
def breakScreen(i, win):
    win.fill(backgroundColor)
    multiLineMessage(breakScreenText(i), mediumFont, win)
    pg.display.flip()
    waitKey(pg.K_f)

# exit screen thanking the participant
def exitScreen(win):
    win.fill(backgroundColor)
    multiLineMessage(exitScreenText, mediumFont, win)
    pg.display.flip()
    waitKey(pg.K_f)

# exit screen thanking the participant
def nonConsentScreen(win):
    win.fill(backgroundColor)
    multiLineMessage(nonConsentText, mediumFont, win)
    pg.display.flip()
    waitKey(pg.K_SPACE)
    pg.quit()
    sys.exit()


# contains questionnaire questions and displays questionnaire to the subject
def consentScreen(subjectNumber, subjectName, subjectEmail, experimenterName, win):

    win.fill(backgroundColor)
    multiLineMessage(studyInfoText, mediumFont, win)
    pg.display.flip()
    waitKey(pg.K_SPACE)

    win.fill(backgroundColor)
    multiLineMessage(risksAndBenefitsText, mediumFont, win)
    pg.display.flip()
    waitKey(pg.K_SPACE)

    win.fill(backgroundColor)
    multiLineMessage(confidentialityText, mediumFont, win)
    pg.display.flip()
    waitKey(pg.K_SPACE)

    win.fill(backgroundColor)
    multiLineMessage(contactsAndQuestionsText, mediumFont, win)
    pg.display.flip()
    waitKey(pg.K_SPACE)

    pg.mouse.set_visible(True)
    # variables to hold all of the questions and their associated response options
    questions = []

    # question 1 text and response options
    question1 = 'By clicking “I agree” below, you confirm that you have read the consent form, are at least 18 years old, and agree to participate in the research. Please print or save a copy of this page for your records. By selecting “I do NOT agree” you will not be able to participate in this research and we thank you for your consideration.'
    ResponseOptions1 = ['I agree to participate in the research', 'I do NOT agree to participate in the research ']
    questions.append([question1] + ResponseOptions1)

    submitButton = Button('submit', 'tellegen', 'Submit', -1, 0) # submit button
    responses = [] # for storing answers to each question

    # iterate over each question and display to user
    for i, question in enumerate(questions):

        response = None

        # draw the question and return how far down the screen the text goes
        yPos = multiLineMessage(question[0], mediumFont, win)

        # create all of the options for this particular questions
        buttons = [submitButton]
        for i, question_option in enumerate(question):
            if i == 0:
                continue
            buttons.append(Button('option', 'tellegen', question_option, i, yPos))

        while response == None:
            win.fill(backgroundColor)
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE: # escape will exit the study
                        pg.quit()
                        sys.exit()
                elif event.type == pg.MOUSEBUTTONUP:
                    for i, button in enumerate(buttons):
                        if (button.coords[0] <= pg.mouse.get_pos()[0] <= button.coords[0] + button.coords[2]) \
                            and (button.coords[1] <= pg.mouse.get_pos()[1] <= button.coords[1] + button.coords[3]):
                            response = button.handleClick(buttons)

            # draw the question and return how far down the screen the text goes
            multiLineMessage(question[0], mediumFont, win)

            # draw the submit button and the checkboxes for this questions
            submitButton.draw(win)
            for i, button in enumerate(buttons): 
                button.draw(win)
            pg.display.flip() 
        
        # add the user's response to the list of responses
        responses.append(response)
    if 'I agree' in responses[0]:
        consented = True
    else:
        consented = False
    
    # Create a timezone object for Central Time
    central_tz = pytz.timezone('America/Chicago')

    # Get the current time in UTC
    current_utc = datetime.now(pytz.utc)

    # Convert the current UTC time to Central Time
    current_central = current_utc.astimezone(central_tz)

    # Format the date and time in a specific format e.g., YYYY-MM-DD HH:MM:SS
    formatted_date = current_central.strftime('%Y-%m-%d %H:%M:%S')
    # write all of the responses to a csv file with the questionnaire's name as the file name. 
    with open(os.path.join(os.path.dirname(__file__), 'results', subjectNumber, 'consentInfo.csv'), mode = 'w', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(['Subject Number', 'Subject Name', 'Subject Email', 'Experimenter Name', 'Consented', 'Date'])
        writer.writerow([subjectNumber, subjectName, subjectEmail, experimenterName, str(consented), formatted_date])
    return consented

# =======================================================================
# =======================================================================

def selectStimulus(targetStimuli, distractorStimuli):

    # select a stimulus and remove it from its associated list
    masterList = targetStimuli + distractorStimuli
    stimulus = choice(masterList)
    if stimulus in targetStimuli:
        stimulusType = 'target'
        targetStimuli.remove(stimulus)
    else:
        stimulusType = 'distractor'
        distractorStimuli.remove(stimulus)

    # get the path to the image selected and load the image
    image = pg.image.load(stimulus)
    image = pg.transform.scale(image, (stimSize, stimSize))

    return image, os.path.basename(stimulus).replace('.png', ''), stimulusType
