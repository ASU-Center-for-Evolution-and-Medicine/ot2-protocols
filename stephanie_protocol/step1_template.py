### start
import profile
import sys
import os
import pandas as pd
from opentrons import protocol_api, simulate, execute
import json
import argparse
### end

"""
step1_tepmplate.py 

Description: Generates python protocol file that can be uploaded directly to Opentrons app

General Protocol Steps: 
1.) Make master mix
2.) Add 15uL master mix to each reaction well
3.) Run thermocycler 
4.) Hold thermocycler plate at 4C until human intervention
"""

# HELPER METHODS ------------------------------------------------------------------
def write_protocol(num_rxns, mm_volumes_dict, file_name):  
    """ write_protocol

    Description: Copies anything between '### start' and '### end' comments in this file to new protocol file
                 Writes num_rxns and mm_volumes dict variables into output protocol at '### VARIABLES' location.
                 Output protocol will be in same directory with name specified by file_name variable (user provided)

    Parameters: 
        num_rxns: (int) number of rxns to perform (1-96)
        mm_volumes_dict: dictionatry of master mix source wells to volumes
        file_name: (str) user specifiec output file name (ex. 'protocol_02.py')
    
    """  
    current_file_path = __file__ 
    output_filepath = os.path.join(os.path.split(current_file_path)[0], file_name)

    try: 
        with open(current_file_path, 'r') as open_this: 
            with open(output_filepath, 'w+') as open_that: 
                contents_this = open_this.readlines()
                for i in range(len(contents_this)): 
                    if contents_this[i].startswith("### start"):
                        j = i
                        while not contents_this[j].startswith("### end"): 
                            j+=1
                        open_that.writelines(contents_this[i+1:j])

                    if contents_this[i].startswith("### VARIABLES"):
                        open_that.write(f"\nnum_rxns = {str(num_rxns)}")
                        open_that.write(f"\nmm_volumes_dict = {str(mm_volumes_dict)}\n\n")
                        
        return(f"Protocol created = {output_filepath} ")
    except: 
        return(f"Error: Could not write to protocol file\n{current_file_path}\n{output_filepath}")


def calculate_mm_volumes(num_rxns): 
    """ calculate_mm_volumes

    Description: Calculates volumes of reagents needed to make master mix depending on number of reactions (num_rxns)

    Parameters: 
        num_rxns: (int) number of rxns to perform (1-96) 

    Output: 
        mm_volumes_dict: dictionatry of master mix source wells to volumes
            NOTE: reagent source rack contains 5 1.5mL tubes 
                A1 - RP Primer
                A2 - 5x Multimodal RT Buffer
                A3 - Nuclease-free Water
                A4 - Rnase Inhibitor
                A5 - EZ Reverse Transcriptase

    """
    rp_primer_vol = (num_rxns * 1) * 1.1
    multi_buff_5x_vol = (num_rxns * 4) * 1.1
    nuc_free_water_volume = (num_rxns * 8) * 1.1
    rnase_inhibitor_vol = (num_rxns * 1) * 1.1
    ez_rev_trans_vol = (num_rxns * 1) * 1.1

    mm_volumes_dict = {
        'A1': rp_primer_vol,
        'A2': multi_buff_5x_vol,
        'A3': nuc_free_water_volume,
        'A4': rnase_inhibitor_vol,
        'A5': ez_rev_trans_vol,
    }

    return mm_volumes_dict


# MAIN METHOD --------------------------------------------------------------------
def generate_step1_from_template(num_rxns, file_name): 
    """ generate_step1_from_template

    Description: Handles num_rxns variable checking and pass to calculate_mm_volumes dict

    Paramerers:
        num_rxns: (int) number of rxns to perform (1-96). 
        file_name: (str) user specifiec output file name (ex. 'protocol_02.py')

    """
    if num_rxns > 96 or num_rxns < 1: 
        print("number of reactions must be between 1 and 96")
        exit

    mm_volumes_dict = calculate_mm_volumes(num_rxns)

    try: 
        print(write_protocol(num_rxns, mm_volumes_dict, file_name))
    except OSError as e:  
        raise

    return 


def main(args):
    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r",
        "--num_rxns",
        help="integer number of reactions to be completed in this step",
        required=True,
        type=int,
    )
    parser.add_argument(
        "-f",
        "--file_name", 
        help="output filename for the protocol. include .py extension. (ex. 'step1_protocol.py')",
        required=True,
        type=str,
    )
    args = vars(parser.parse_args())

    # pass to method
    generate_step1_from_template(
        args["num_rxns"],
        args["file_name"],
    )


if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv)


# ------------------------------------------ contents of protocol --------------------------------------------------
### start 

# metadata
metadata = {
    'protocolName': 'Step1',
    'author': 'Name <email@address.com>',
    'description': 'step1 of stephanies protocol',
    'apiLevel': '2.12'
}

### end

### VARIABLES

### start 

def run(protocol: protocol_api.ProtocolContext):

    # modules
    thermo_mod = protocol.load_module('thermocycler module')
    thermo_mod.open_lid()   # opens lid and sets to 4C when it turns on
    thermo_mod.set_block_temperature(4)
    
    mag_mod = protocol.load_module("magnetic module gen2", '4')
    mag_mod.calibrate()  # calibrate and disengage mag deck when it turns on
    mag_mod.disengage() 

    # labware
    thermo_plate = thermo_mod.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')  

    tiprack1 = protocol.load_labware('opentrons_96_tiprack_20ul', '9')
    tiprack2 = protocol.load_labware('opentrons_96_tiprack_20ul', '6')
    tiprack3 = protocol.load_labware('opentrons_96_tiprack_1000uL', '3')  

    tube_rack_1 = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '2')  # 1.5mL tubes for mm ingredients
    tube_rack_2 = protocol.load_labware('opentrons_15_tuberack_nest_15ml_conical', '5')  # 15 mL tubes to hold master mix

    # pipettes
    pipette_20uL_single = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=[tiprack1, tiprack2])
    pipette_1000uL_single = protocol.load_instrument('p1000_single_gen2', 'left', tip_racks=[tiprack3])  

    #* Protocol Commands

    # step 1: make master mix
    mm_total_volume = 0   # track volume in mm tube
    for mm_ingredient_well in mm_volumes_dict: 
        volume = round(mm_volumes_dict[mm_ingredient_well],2) 
        mm_total_volume += volume # track volume in mm tube
        pipette_1000uL_single.transfer(
            volume, 
            tube_rack_1[mm_ingredient_well], 
            tube_rack_2['A1'], 
            new_tip='always',
            mix_before=(3,volume))

    # mix master mix
    pipette_1000uL_single.pick_up_tip()
    pipette_1000uL_single.mix(3, max(500,mm_total_volume*0.6),tube_rack_2['A1'])  # mix with max of 500uL or 60% total mm volume in tube
    pipette_1000uL_single.drop_tip()
    
    # step 2: transfer 15uL mm to each rxn well on thermocycler 
    for i in range(num_rxns):  
        pipette_20uL_single.transfer(
            15, 
            tube_rack_2['A1'], 
            thermo_plate.wells(i), 
            new_tip='always', 
            mix_after=(3,10))

    # step 3: run thermocycler rounds 
    thermo_mod.close_lid()
    thermo_mod.set_lid_temperature(105)
    thermo_mod.set_block_temperature(25, hold_time_minutes=10, block_max_volume=20)
    thermo_mod.set_block_temperature(42, hold_time_minutes=50, block_max_volume=20)
    thermo_mod.set_block_temperature(85, hold_time_minutes=5, block_max_volume=20)

    thermo_mod.set_block_temperature(4) # hold at 4C until user opens thermocycler manually


### end 