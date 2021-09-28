OVERVIEW --------------------------------------------------

This program allows the user to create an Opentrons OT-2 APIv2 protocol for transfering 
from wells (source wells) in up to 5 96-well plates into up to 5 destination 
1.5 mL microcentrifuge tubes (destinations). 

Notes: Destination tubes must be placed in top row of tube rack (A1-A5)

DIRECTIONS ------------------------------------------------

- set up OT-2 environment (see environment setup section below)

Create Protocol: 
- Open the GUI by double clicking on the desktop icon entitled 'ICON TITLE'
- Select source plate csv's:  (repeat for up to 5 source plates)
    - click 'Browse' to locate a source csv in your file structure
    - select the deck location corresponding to the source plate's location on the OT-2 deck
- Specify output folder: 
    - click 'Browse' to locate a folder in your file structure
    - The final generated protocol will be stored in this folder
    - NOTE: The folder must already exist inorder to be chosen 
- Specify the desired output protocol name
    - What do you want the name of your protocol's file to be? 
        Ex. Enter 'Protocol1' if you want the resulting protocol file to be named 'Protocol1.py'
            (the protocol will be a python file)
- Click 'Generate Protocol' to create the protocol file

** (optional) ** 
Simulate your protocol with opentrons simulator through command line
...on windows 
    opentrons_simulate.exe <path to protocol file>
...on mac 
    opentrons_simulate <path to protocol file> 

Run Protocol in Opentrons app: 
- Open the Opentrons app and connect to the OT-2
- Select the protocol tab on the left
- Browse your file structure and select the protocol file you just created
- Ensure that all deck locations look correct and set up the deck accordingly
- Follow the OT-2's prompts to calibrate all labware
- Run your protocol


ENVIRONMENT SETUP -----------------------------------------

Make sure to gave anaconda installed (command line compatible)
(check if conda is already installed with 'which conda') <-- this will only work on mac? 
https://docs.anaconda.com/anaconda/install/index.html

# Create a conda environment for the OT-2 protocols (with correct verison of python)
conda create -n ot2 python=3.9
    NOTE: If you change the environment name to something other than 'ot2' 
          then you'll also need ot change the env name in the .bat and .sh files

# Activate the conde environment
conda activate ot2

# install pip (required to install opentrons package)
conda install pip

# install the necessary packages
conda install pandas
pip install opentrons

# check that packages installed correctly
conda list

You should be good to go now :) 

----------------------------------------------------------------


