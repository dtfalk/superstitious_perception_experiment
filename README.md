# **Superstitious Perception Experiment**
Hello everyone, my name is David Falk. I work at the University of Chicago and this is a document explaining how to run the code associated with the Superstitious Perception Experiment. 

## Contact Info
**email #1:** dtfalk@uchicago.edu
**email #2:** davidtobiasfalk@gmail.com

# Software you should download
The goal of this section is to give you a place where you can run python code and create Anaconda Virtual Environments using the **.yml** file in this github. If you already have a way of doing that, then you may skip this section and proceed to the next section. Otherwise, here is how to do this...

First, you will need to install Python on your device. If you already have it, then great! Otherwise, or if you do not know if you have it installed, follow the instructions in this link: https://wiki.python.org/moin/BeginnersGuide/Download

Second, you want to install VS Code. You can install it from the following link: https://code.visualstudio.com/download

Follow the link above and select the version of VS Code that matches your operating system. If it asks to create a **Desktop Icon** or **Desktop Shortcut** during installation, then please select this option.

Once this is downloaded, open up VS Code. Then search around for the **Extensions** tab. It will either be located on the left side of your screen or the top of your screen. Mine is located on the left side of my screen and it looks like 4 squares. Three of the squares are connected to each other and the top-right square looks like it is floating away from the other three. Open the **Extensions** tab and use the search bar and enter **Python**. It is published by Microsoft. Download this extension. Once it is downloaded, exit out of VS Code.

Third, you will want to install Anaconda. This is for managing our virtual environments. You may download it from this link: https://www.anaconda.com/download/success

Once it is downloaded and installed, follow the instructions in this link to get anaconda and vs code working together: https://docs.anaconda.com/working-with-conda/ide-tutorials/vscode/


# Downloading and running the code
Now we need to download the code for the experiment. Start by going to the github respository that contains the code (https://github.com/dtfalk/superstitious_perception_experiment). 

Scroll to the top of the page and you should see a green "<> Code" button. Click on this button and a drop down menu will appear. Click on the "Download Zip" option and this will download the code for you as a zip file. 

Once the download finishes, unzip the folder and extract the **superstitious_perception_experiment-master** file to your desktop.

Then, open VS code and select the **File** button, followed by **Open Folder...** and open the **superstitious_perception_experiment-master** folder. This should open all of the files for the experiment in your VS Code window. 

Then open a VS Code terminal and enter the following command to download all necessary packages for the experiment...

```
conda env create -f superstitious_perception_experiment.yml
```

After that finishes, enter the following command into the terminal...

```
conda activate superstitious_perception_experiment
```

Great! Now enter the following command to run the experiment...
```
python runExperiment.py
```

# Things you need to modify
This experiment has a requirement that the images that the user sees occupy 2-degrees of their visual field. Ensuring this happens is a function of how big the monitor is, how far the user is sitting from the screen, and the resolution of the computer. 

All you will need is a measuring tape and you can change the two lines of code to ensure we adhere to this 2-degrees requirement.

First, measure the width of your screen in **centimeters**. You do not need the height. You do not need the diagonal size of the screen. **You only need the width of the monitor the subject will be looking at. You need this in centimeters.** 

Second, you need some idea of how far the subject will be sitting from the screen. Try to simulate the situation by pretending that you are the subject sitting in the chair. Take a measurement from your eyes to the screen. You can either do this once, or you can let the subject decide how they want to sit and then measure the distance from them to the screen. **You need this distance in centimeters.**

Next, open up the **constants.py** file. This is what you will see...
```
import os
from math import tan, radians
from screeninfo import get_monitors

# This block of code gets info about the subject's monitor
# =======================================================================
# =======================================================================

screen_width_in_centimeters = 31.5
distance_from_screen_in_centimeters = 69
```

Change the the **screen_width_in_centimeters** variable to the width of the screen that you measured earlier. Then change the **distance_from_screen_in_centimeters** variable to the distance that the subject is sitting from the screen. For example, if the screen is 50 cm wide and the subject is sitting 100 cm away from the screen, then your code should look like this...
```
import os
from math import tan, radians
from screeninfo import get_monitors

# This block of code gets info about the subject's monitor
# =======================================================================
# =======================================================================

screen_width_in_centimeters = 50
distance_from_screen_in_centimeters = 100
```

**That is all that you should need to change!!**

# Data Outputs
The experiment typically takes 90 minutes to run. When the experiment first starts you will be asked to enter a **Subject Name** and a **Subject Number**. Once the subject completes the experiment, their results will be located in the **results** folder. The sub-folder containing their results will be named according to their subject number. So if your subject has subject number **1122334455**, then their results will be in a folder that is named **1122334455**. Within each folder there will be the following files:

**dissociative_experiences.csv:** The subject's responses to the dissociative experiences questionnaire.

**launay_slade.csv:** The subject's responses to the Launay-Slade questionnaire.

**tellegen.csv:** The subject's responses to the tellegen absorption questionnaire.

**gaussian_icorrelated.csv:** The subject's responses to the gaussian-weighted with i-correlated distractors block.

**gaussian_uncorrelated.csv:** The subject's responses to the gaussian-weighted with uncorrelated distractors block.

**unweighted_icorrelated.csv:** The subject's responses to the unweighted with i-correlated distractors block.

**unweighted_uncorrelated.csv:** The subject's responses to the unweighted with uncorrelated distractors block.

**summaryData.csv:** A file containing summary data of the subject's performance over the four blocks. This includes dprime scores and the order in which the subjects received the blocks.