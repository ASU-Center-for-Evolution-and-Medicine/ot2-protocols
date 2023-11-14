### start  ------------------------------------------------------------------------------------------------------
import sys
import os
import pandas as pd
from opentrons import protocol_api, simulate, execute
import json

# metadata
# metadata
metadata = {
### end

### PROTOCOL NAME  <--- DO NOT DELETE THIS

### start
'author': 'Casey Stone <cstone@anl.gov>',
'description': 'Simple protocol to transfer a given set of volumes into a tube.',
'apiLevel': '2.8'
}

### end

### VAR  <--- DO NOT DELETE THIS

### start


def run(protocol):

    # Define labware types and locations.
    PIPETTE_TYPE_1 = "p20_single_gen2"
    PIPETTE_MOUNT_1 = "right"

    PLATE_TYPE_FULL = "nest_96_wellplate_100ul_pcr_full_skirt"
    SEMI_w_ADAPTER_TYPE = "pcrsemiskirtwadapter_96_wellplate_200ul"
    SEMI_ICE_TYPE = "pcrsemiskirtwiceblock_96_wellplate_200ul"
    #PLATE_TYPE_SEMI = "nest_96_wellplate_100ul_pcr_full_skirt" #TODO update this with new def from other pooling protocol!

    TIPRACK_TYPE_20 = "opentrons_96_tiprack_20ul"
    TIPRACK_SLOT1 = 7
    TIPRACK_SLOT2 = 8
    TIPRACK_SLOT3 = 9
    
    def transfer_volumes():
        
        print("TRANSFER VOLUMES METHOD CALLED")

        #load tip racks at all possible locations (don't need to actually use all these tip locations)
        tiprack1 = protocol.load_labware(TIPRACK_TYPE_20, TIPRACK_SLOT1)
        tiprack2 = protocol.load_labware(TIPRACK_TYPE_20, TIPRACK_SLOT2)
        tiprack3 = protocol.load_labware(TIPRACK_TYPE_20, TIPRACK_SLOT3)

        #load the pipette and point to location
        # TODO: check that this is consistent with the updated version of the new protocol
        pipette_20uL = protocol.load_instrument(PIPETTE_TYPE_1, mount=PIPETTE_MOUNT_1, tip_racks=[tiprack1, tiprack2, tiprack3])
        pipette_20uL.well_bottom_clearance.aspirate = 0.4
        
        # format arrays of source names and locations
        plate1 = None
        plate2 = None 
        plate3 = None
        plate4 = None
        plate5 = None

        plate1_type = None
        plate2_type = None
        plate3_type = None 
        plate4_type = None
        plate5_type = None

        # assign plate types from plate dictionary
        plate_names = []
        plate_types = []
        plate_locations = []
        plate_labels = []
        for plate in plates_dict: 
            deck_loc, plate_type = plates_dict[plate]  # unpack variables from plates_dict
            plate_names.append(plate)  # user defined plate names
            plate_locations.append(int(deck_loc.strip()))  # user defined deck locations
            plate_types.append(plate_type)

        # define labware 
        if len(plate_names) >= 1: 
            if plate_types[0] == "semi": 
                plate1 = protocol.load_labware(SEMI_w_ADAPTER_TYPE, plate_locations[0])
            elif plate_types[0] == "full": 
                plate1 = protocol.load_labware(PLATE_TYPE_FULL, plate_locations[0])
            elif plate_types[0] == "semi_ice": 
                plate1 = protocol.load_labware(SEMI_ICE_TYPE, plate_locations[0])
            else: 
                print("Cannot load labware - plate 1")
        
            if len(plate_names) >= 2: 
                if plate_types[1] == "semi": 
                    plate2 = protocol.load_labware(SEMI_w_ADAPTER_TYPE, plate_locations[1])
                elif plate_types[1] == "full": 
                    plate2 = protocol.load_labware(PLATE_TYPE_FULL, plate_locations[1])
                elif plate_types[1] == "semi_ice": 
                    plate2 = protocol.load_labware(SEMI_ICE_TYPE, plate_locations[1])
                else: 
                    print("Cannot load labware - plate 2")

                if len(plate_names) >= 3: 
                    if plate_types[2] == "semi": 
                        plate3 = protocol.load_labware(SEMI_w_ADAPTER_TYPE, plate_locations[2])
                    elif plate_types[2] == "full": 
                        plate3 = protocol.load_labware(PLATE_TYPE_FULL, plate_locations[2])
                    elif plate_types[2] == "semi_ice": 
                        plate3 = protocol.load_labware(SEMI_ICE_TYPE, plate_locations[2])
                    else: 
                        print("Cannot load labware - plate 3")
                    
                    if len(plate_names) >= 4: 
                        if plate_types[3] == "semi": 
                            plate4 = protocol.load_labware(SEMI_w_ADAPTER_TYPE, plate_locations[3])
                        elif plate_types[3] == "full": 
                            plate4 = protocol.load_labware(PLATE_TYPE_FULL, plate_locations[3])
                        elif plate_types[3] == "semi_ice": 
                            plate4 = protocol.load_labware(SEMI_ICE_TYPE, plate_locations[3])
                        else: 
                            print("Cannot load labware - plate 4")

                        if len(plate_names) >= 5: 
                            if plate_types[4] == "semi": 
                                plate5 = protocol.load_labware(SEMI_w_ADAPTER_TYPE, plate_locations[4]) 
                            elif plate_types[4] == "full": 
                                plate5 = protocol.load_labware(PLATE_TYPE_FULL, plate_locations[4])
                            elif plate_types[4] == "semi_ice": 
                                plate5 = protocol.load_labware(SEMI_ICE_TYPE, plate_locations[4])
                            else: 
                                print("Cannot load labware - plate 5")

        else: 
            print("Error: there are no source locations to initialize")
            raise  # what does this do? 

        # define plate name to plate def dictionary
        naming_dict = {} 
        if plate1: 
            naming_dict[plate_names[0]] = plate1
        if plate2: 
            naming_dict[plate_names[1]] = plate2
        if plate3: 
            naming_dict[plate_names[2]] = plate3
        if plate4: 
            naming_dict[plate_names[3]] = plate4
        if plate5: 
            naming_dict[plate_names[4]] = plate5

        # START THE TRANSFERS, home the robot when transfers are complete
        for i in range(len(source_names)):   # TODO: this should accomplish all the transfers ( test this!)

            # Set pipette speed to slow for aspirate/dispense
            pipette_20uL.flow_rate.aspirate = 3  # TODO: think about making this faster
            pipette_20uL.flow_rate.dispense = 3
            
            # extract source and dest plate defs
            source_plate = naming_dict[source_names[i]]
            dest_plate = naming_dict[dest_names[i]]
            
            # complete transfer with mixing
            pipette_20uL.pick_up_tip()
            pipette_20uL.aspirate(transf_volumes[i], source_plate[source_wells[i]])
            pipette_20uL.dispense(transf_volumes[i], dest_plate[dest_wells[i]])

            # Set pipette speed to faster for mixing (mixing no longer included)
            # pipette_20uL.flow_rate.aspirate = 5  
            # pipette_20uL.flow_rate.dispense = 5

            #pipette_20uL.mix(5, 10)   # mixing removed for time sake 

            pipette_20uL.drop_tip()
            
        pipette_20uL.home() 
    
    transfer_volumes()

### end