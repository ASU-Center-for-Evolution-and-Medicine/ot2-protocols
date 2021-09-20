OVERVIEW -------------------------------------------------



DIRECTIONS ------------------------------------------------





Simulate your protocol with opentrons simulator
...on windows 
    opentrons_simulate.exe <path to protocol file>

... on mac 
    opentrons_simulate <path to protocol file> 


ENVIRONMENT SETUP -----------------------------------------

Make sure to gave anaconda installed (command line compatible)
(check if conda is already installed with 'which conda')
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


