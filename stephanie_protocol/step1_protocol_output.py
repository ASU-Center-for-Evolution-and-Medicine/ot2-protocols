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


num_rxns = 48
mm_volumes_dict = {'A1': 52.800000000000004, 'A2': 211.20000000000002, 'A3': 422.40000000000003, 'A4': 52.800000000000004, 'A5': 52.800000000000004}


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


