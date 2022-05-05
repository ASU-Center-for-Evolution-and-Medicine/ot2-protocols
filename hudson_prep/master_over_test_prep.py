import profile
import sys
import os
import pandas as pd
from opentrons import protocol_api, simulate, execute
import json
import argparse

# metadata
metadata = {
    'protocolName': 'Step1',
    'author': 'Name <email@address.com>',
    'description': 'step1 of stephanies protocol',
    'apiLevel': '2.12'
}


num_rxns = 1
mm_volumes_dict = {'A1': 1.1, 'A2': 4.4, 'A3': 8.8, 'A4': 1.1, 'A5': 1.1}


def run(protocol: protocol_api.ProtocolContext):

    # modules
    #thermo_mod = protocol.load_module('thermocycler module')
    #thermo_mod.open_lid()   # opens lid and sets to 4C when it turns on
    #thermo_mod.set_block_temperature(4)
    
    #mag_mod = protocol.load_module("magnetic module gen2", '4')
    #mag_mod.calibrate()  # calibrate and disengage mag deck when it turns on
    #mag_mod.disengage() 

    # labware
    #thermo_plate = thermo_mod.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')  
    master_plate = protocol.load_labware('corning_96_wellplate_360ul_flat', '1')
    overnight_plate = protocol.load_labware('corning_96_wellplate_360ul_flat', '2')
    test_plate = protocol.load_labware('corning_96_wellplate_360ul_flat', '3')

    # tiprack1 = protocol.load_labware('opentrons_96_tiprack_20ul', '9')
    # tiprack2 = protocol.load_labware('opentrons_96_tiprack_20ul', '6')
    tiprack1 = protocol.load_labware('opentrons_96_tiprack_1000uL', '9')  

    #tube_rack_1 = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '2')  # 1.5mL tubes for mm ingredients
    tube_rack_2 = protocol.load_labware("opentrons_10_tuberack_nest_4x50ml_6x15ml_conical", '6')  # 15 mL tubes to hold master mix

    # pipettes
    #pipette_20uL_single = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=[tiprack1, tiprack2])
    pipette_1000uL_single = protocol.load_instrument('p1000_single_gen2', 'left', tip_racks=[tiprack1])  

    #* Protocol Commands

    # make master plate
    volume1 = 100
    pipette_1000uL_single.pick_up_tip()
    pipette_1000uL_single.distribute(
        volume1, 
        tube_rack_2['A3'], 
        master_plate.wells(),
        new_tip='never',
    )
    pipette_1000uL_single.drop_tip()

    # make overnight plate
    volume1 = 100
    pipette_1000uL_single.pick_up_tip()
    pipette_1000uL_single.distribute(
        volume1, 
        tube_rack_2['A3'], 
        overnight_plate.wells(),
        new_tip='never',
    )
    pipette_1000uL_single.drop_tip()

    # make test_plate
    volume1 = 180
    pipette_1000uL_single.pick_up_tip()
    pipette_1000uL_single.distribute(
        volume1, 
        tube_rack_2['A4'], 
        test_plate.wells(),
        new_tip='never',
    )
    pipette_1000uL_single.drop_tip()
    
