import pygame as pg
from random import shuffle
from time import sleep
from helperFunctions import *
from questionnaires import main as questions
from questionnaires import flow_state_scale, stanford_sleepiness_scale


# The experiment itself
def experiment(subjectName, subjectNumber, block, targetStimuli, distractorStimuli, saveFolder, win):


    # various variables for handling the game
    pg.event.clear()
    reset = False
    startTime = pg.time.get_ticks()
    
    # select an initial image
    image, stimulusNumber, stimulusType = selectStimulus(targetStimuli, distractorStimuli)

    # Loop for handling events
    while True:
        
        # handles key presses
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:

                # quit the experiment key
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

                # handles response keys (y for "yes, the stimulus is here". "n" otherwise)
                elif event.key == pg.K_y or event.key == pg.K_n:
                
                    # indicates we will reset the experiment once a response is selected
                    reset = True

                    # user's response to a stimulus
                    if event.key == pg.K_y:
                        response = 'target'
                    else:
                        response = 'distractor'

                    # saves user's response
                    responseTime = pg.time.get_ticks() - startTime
                    recordResponse(subjectName, subjectNumber, block, stimulusNumber, stimulusType, response, responseTime, saveFolder)
                    
                    # 2 second rest between each stimulus
                    win.fill(backgroundColor)
                    pg.display.flip()
                    #sleep(2)
                    pg.event.clear()
            
        # while the trial continues on just keep the image on the screen until they give a response
        if not reset:
            win.fill(backgroundColor)
            win.blit(image, screenCenter)
            pg.display.flip()
    
        # end of a trial
        else:

            # update the restart variables 
            reset = False
            
            # end experiment if we have shown all of the images
            if (len(targetStimuli) == 0 and len(distractorStimuli) == 0):
                return
            
            # otherwise select a new image
            image, stimulusNumber, stimulusType = selectStimulus(targetStimuli, distractorStimuli)
            
            # reset the trial timer
            startTime = pg.time.get_ticks()

            # clear events so spamming keys doesn't mess things up
            pg.event.clear()


# handles the overall experiment flow
def main():

    # Initializing Pygame
    # =================================================================

    # == Initiate pygame and collect user information ==
    pg.init()
    pg.mixer.init()

    # == Set window ==
    win = pg.display.set_mode((winWidth, winHeight), pg.FULLSCREEN)

    # make mouse invisible
    pg.mouse.set_visible(False)

    # =================================================================


    
    # Collects user info and preps the stimuli and the rest of the experiment
    # ============================================================================================

    # get user info and where to store their results
    subjectName = getSubjectInfo('subject name', win)
    subjectNumber = getSubjectInfo('subject number', win)
    subjectEmail = getSubjectInfo('subject email', win)
    experimenterName = getSubjectInfo('experimenter name', win)

    saveFolder = os.path.join(os.path.dirname(__file__), 'results', subjectNumber)
    while os.path.exists(saveFolder):
        subjectNumber = subjectNumber + '0'
        saveFolder = os.path.join(os.path.dirname(__file__), 'results', subjectNumber)
    os.makedirs(saveFolder, exist_ok = True)

    # gets the top rated Hs, top rated Is and noisy images
    gaussianHStimuli_uncorrelated,  gaussianHStimuli_vcorrelated, gaussianVStimuli, gaussianNoCorrelationStimuli, \
    unweightedHStimuli_uncorrelated, unweightedHStimuli_vcorrelated, unweightedVStimuli, unweightedNoCorrelationStimuli = getStimuli()

    # map the weighting scheme/correlation scheme pair to the actual lists of images
    # (weighting scheme, correlation scheme) ---> (target images, distractor images)
    stimuliDictionary = {
        'unweighted_vcorrelated': (unweightedHStimuli_vcorrelated, unweightedVStimuli),
        'unweighted_uncorrelated': (unweightedHStimuli_uncorrelated, unweightedNoCorrelationStimuli),
        'gaussian_vcorrelated': (gaussianHStimuli_vcorrelated, gaussianVStimuli),
        'gaussian_uncorrelated': (gaussianHStimuli_uncorrelated, gaussianNoCorrelationStimuli)
    }
    
    # shuffle the blocks randomly, preserving gaussian with gaussian and unweighted with unweighted
    shuffledBlocks = [['unweighted_vcorrelated', 'unweighted_uncorrelated'],
                    ['gaussian_vcorrelated', 'gaussian_uncorrelated']]   
    for block in shuffledBlocks:
        shuffle(block)
    shuffle(shuffledBlocks)

    blocks = shuffledBlocks[0] + shuffledBlocks[1]

    # ============================================================================================

    
    # showing the user the experiment
    consented = consentScreen(subjectNumber, subjectEmail, experimenterName, win)
    if not consented:
        nonConsentScreen(win)
    sleepiness_responses = []
    experimentExplanation(win)
    stanford_sleepiness_scale(sleepiness_responses, win)
    pg.event.clear()

    # give users all four blocks
    for i, block in enumerate(blocks):
        print(f'block {i + 1}: {block}')

        # extract weighting scheme (gaussian vs unweighted) and correlation scheme (uncorrelated vs i-correlated)
        targetImages, distractorImages = stimuliDictionary[block]

        # show template image and display stimuli
        showTemplate(win)
        experiment(subjectName = subjectName, subjectNumber = subjectNumber, 
                   block = block, 
                   targetStimuli = targetImages, distractorStimuli = distractorImages, 
                   saveFolder = saveFolder, win = win)
        
        # give break screen betweeen blocks
        if i < len(blocks) - 1:
            if i == 1:
                stanford_sleepiness_scale(sleepiness_responses, win)
            breakScreen(i + 1, win)
            realInstructionsAlt(win)
    
    pg.mouse.set_visible(True)
    stanford_sleepiness_scale(sleepiness_responses, win)
    subjectExplanation_methodology = getSubjectInfo('selfReflect_explanation', win)
    with open(os.path.join(os.path.dirname(__file__), 'results', subjectNumber, 'selfReflect_methodology.txt'), mode = 'w') as f:
        f.write(subjectExplanation_methodology)

    subjectExplanation_changes = getSubjectInfo('selfReflect_changes', win)
    with open(os.path.join(os.path.dirname(__file__), 'results', subjectNumber, 'selfReflect_changes.txt'), mode = 'w') as f:
        f.write(subjectExplanation_changes)
    
    # display questionnaires
    questions(subjectNumber, win)

    # write the responses to a csv file with the questionnaire's name
    with open(os.path.join(os.path.dirname(__file__), 'results', subjectNumber, 'stanford_sleepiness.csv'), mode = 'w', newline = '') as f:
        writer = csv.writer(f)
        header = ['Pre-Experiment', 'During Experiment', 'Post-Experiment']
        writer.writerow(header)
        writer.writerow([''.join([ch for ch in response if ch.isdigit()]) for response in sleepiness_responses])

    # exit screen thanking participants
    exitScreen(subjectNumber, win)

    # calculate overall data and write to a user-specific data file
    writeSummaryData(subjectName, subjectNumber, blocks, saveFolder)

if __name__ == '__main__':
    main()