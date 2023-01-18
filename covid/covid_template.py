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
    PIPETTE_MOUNT_1 = "left"

    PLATE_TYPE_FULL = "nest_96_wellplate_100ul_pcr_full_skirt"
    #PLATE_TYPE_SEMI = "nest_96_wellplate_100ul_pcr_full_skirt" #TODO update this with new def from other pooling protocol!

    TIPRACK_TYPE_20 = "opentrons_96_tiprack_20ul"
    TIPRACK_SLOT1 = 7
    TIPRACK_SLOT2 = 8
    TIPRACK_SLOT3 = 9

    # TEST SEMI SKIRTED LABWARE  
    LABWARE_DEF_JSON = """{"ordering":[["A1","B1","C1","D1","E1","F1","G1","H1"],["A2","B2","C2","D2","E2","F2","G2","H2"],["A3","B3","C3","D3","E3","F3","G3","H3"],["A4","B4","C4","D4","E4","F4","G4","H4"],["A5","B5","C5","D5","E5","F5","G5","H5"],["A6","B6","C6","D6","E6","F6","G6","H6"],["A7","B7","C7","D7","E7","F7","G7","H7"],["A8","B8","C8","D8","E8","F8","G8","H8"],["A9","B9","C9","D9","E9","F9","G9","H9"],["A10","B10","C10","D10","E10","F10","G10","H10"],["A11","B11","C11","D11","E11","F11","G11","H11"],["A12","B12","C12","D12","E12","F12","G12","H12"]],"brand":{"brand":"PCR_semi_skirt_wAdapter","brandId":[]},"metadata":{"displayName":"PCR_semi_skirt_wAdapter 96 Well Plate 200 µL","displayCategory":"wellPlate","displayVolumeUnits":"µL","tags":[]},"dimensions":{"xDimension":127.76,"yDimension":85.48,"zDimension":24},"wells":{"A1":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":14.38,"y":74.24,"z":3.2},"B1":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":14.38,"y":65.24,"z":3.2},"C1":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":14.38,"y":56.24,"z":3.2},"D1":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":14.38,"y":47.24,"z":3.2},"E1":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":14.38,"y":38.24,"z":3.2},"F1":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":14.38,"y":29.24,"z":3.2},"G1":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":14.38,"y":20.24,"z":3.2},"H1":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":14.38,"y":11.24,"z":3.2},"A2":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":23.38,"y":74.24,"z":3.2},"B2":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":23.38,"y":65.24,"z":3.2},"C2":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":23.38,"y":56.24,"z":3.2},"D2":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":23.38,"y":47.24,"z":3.2},"E2":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":23.38,"y":38.24,"z":3.2},"F2":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":23.38,"y":29.24,"z":3.2},"G2":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":23.38,"y":20.24,"z":3.2},"H2":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":23.38,"y":11.24,"z":3.2},"A3":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":32.38,"y":74.24,"z":3.2},"B3":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":32.38,"y":65.24,"z":3.2},"C3":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":32.38,"y":56.24,"z":3.2},"D3":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":32.38,"y":47.24,"z":3.2},"E3":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":32.38,"y":38.24,"z":3.2},"F3":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":32.38,"y":29.24,"z":3.2},"G3":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":32.38,"y":20.24,"z":3.2},"H3":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":32.38,"y":11.24,"z":3.2},"A4":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":41.38,"y":74.24,"z":3.2},"B4":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":41.38,"y":65.24,"z":3.2},"C4":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":41.38,"y":56.24,"z":3.2},"D4":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":41.38,"y":47.24,"z":3.2},"E4":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":41.38,"y":38.24,"z":3.2},"F4":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":41.38,"y":29.24,"z":3.2},"G4":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":41.38,"y":20.24,"z":3.2},"H4":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":41.38,"y":11.24,"z":3.2},"A5":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":50.38,"y":74.24,"z":3.2},"B5":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":50.38,"y":65.24,"z":3.2},"C5":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":50.38,"y":56.24,"z":3.2},"D5":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":50.38,"y":47.24,"z":3.2},"E5":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":50.38,"y":38.24,"z":3.2},"F5":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":50.38,"y":29.24,"z":3.2},"G5":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":50.38,"y":20.24,"z":3.2},"H5":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":50.38,"y":11.24,"z":3.2},"A6":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":59.38,"y":74.24,"z":3.2},"B6":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":59.38,"y":65.24,"z":3.2},"C6":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":59.38,"y":56.24,"z":3.2},"D6":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":59.38,"y":47.24,"z":3.2},"E6":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":59.38,"y":38.24,"z":3.2},"F6":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":59.38,"y":29.24,"z":3.2},"G6":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":59.38,"y":20.24,"z":3.2},"H6":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":59.38,"y":11.24,"z":3.2},"A7":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":68.38,"y":74.24,"z":3.2},"B7":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":68.38,"y":65.24,"z":3.2},"C7":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":68.38,"y":56.24,"z":3.2},"D7":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":68.38,"y":47.24,"z":3.2},"E7":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":68.38,"y":38.24,"z":3.2},"F7":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":68.38,"y":29.24,"z":3.2},"G7":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":68.38,"y":20.24,"z":3.2},"H7":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":68.38,"y":11.24,"z":3.2},"A8":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":77.38,"y":74.24,"z":3.2},"B8":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":77.38,"y":65.24,"z":3.2},"C8":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":77.38,"y":56.24,"z":3.2},"D8":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":77.38,"y":47.24,"z":3.2},"E8":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":77.38,"y":38.24,"z":3.2},"F8":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":77.38,"y":29.24,"z":3.2},"G8":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":77.38,"y":20.24,"z":3.2},"H8":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":77.38,"y":11.24,"z":3.2},"A9":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":86.38,"y":74.24,"z":3.2},"B9":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":86.38,"y":65.24,"z":3.2},"C9":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":86.38,"y":56.24,"z":3.2},"D9":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":86.38,"y":47.24,"z":3.2},"E9":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":86.38,"y":38.24,"z":3.2},"F9":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":86.38,"y":29.24,"z":3.2},"G9":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":86.38,"y":20.24,"z":3.2},"H9":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":86.38,"y":11.24,"z":3.2},"A10":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":95.38,"y":74.24,"z":3.2},"B10":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":95.38,"y":65.24,"z":3.2},"C10":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":95.38,"y":56.24,"z":3.2},"D10":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":95.38,"y":47.24,"z":3.2},"E10":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":95.38,"y":38.24,"z":3.2},"F10":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":95.38,"y":29.24,"z":3.2},"G10":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":95.38,"y":20.24,"z":3.2},"H10":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":95.38,"y":11.24,"z":3.2},"A11":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":104.38,"y":74.24,"z":3.2},"B11":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":104.38,"y":65.24,"z":3.2},"C11":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":104.38,"y":56.24,"z":3.2},"D11":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":104.38,"y":47.24,"z":3.2},"E11":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":104.38,"y":38.24,"z":3.2},"F11":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":104.38,"y":29.24,"z":3.2},"G11":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":104.38,"y":20.24,"z":3.2},"H11":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":104.38,"y":11.24,"z":3.2},"A12":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":113.38,"y":74.24,"z":3.2},"B12":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":113.38,"y":65.24,"z":3.2},"C12":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":113.38,"y":56.24,"z":3.2},"D12":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":113.38,"y":47.24,"z":3.2},"E12":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":113.38,"y":38.24,"z":3.2},"F12":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":113.38,"y":29.24,"z":3.2},"G12":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":113.38,"y":20.24,"z":3.2},"H12":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":113.38,"y":11.24,"z":3.2}},"groups":[{"metadata":{"wellBottomShape":"v"},"wells":["A1","B1","C1","D1","E1","F1","G1","H1","A2","B2","C2","D2","E2","F2","G2","H2","A3","B3","C3","D3","E3","F3","G3","H3","A4","B4","C4","D4","E4","F4","G4","H4","A5","B5","C5","D5","E5","F5","G5","H5","A6","B6","C6","D6","E6","F6","G6","H6","A7","B7","C7","D7","E7","F7","G7","H7","A8","B8","C8","D8","E8","F8","G8","H8","A9","B9","C9","D9","E9","F9","G9","H9","A10","B10","C10","D10","E10","F10","G10","H10","A11","B11","C11","D11","E11","F11","G11","H11","A12","B12","C12","D12","E12","F12","G12","H12"]}],"parameters":{"format":"irregular","quirks":[],"isTiprack":false,"isMagneticModuleCompatible":false,"loadName":"pcrsemiskirtwadapter_96_wellplate_200ul"},"namespace":"custom_beta","version":1,"schemaVersion":2,"cornerOffsetFromSlot":{"x":0,"y":0,"z":0}}"""
    LABWARE_DEF = json.loads(LABWARE_DEF_JSON)
    LABWARE_LABEL = LABWARE_DEF.get('metadata', {}).get('displayName', 'test labware')
    LABWARE_DIMENSIONS = LABWARE_DEF.get('wells', {}).get('A1', {}).get('yDimension')
    
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
            # if plate_type == "full":   # labware types
            #     plate_types.append
            #     #plate_types.append(PLATE_TYPE_FULL)
            #     plate_labels.append(PLATE_TYPE_FULL)
            # elif plate_type == "semi": 
            #     plate_types.append(LABWARE_DEF)
            #     plate_labels.append(LABWARE_LABEL)

        # define labware 
        if len(plate_names) >= 1: 
            if plate_types[0] == "semi": 
                plate1 = protocol.load_labware_from_definition(LABWARE_DEF, plate_locations[0], LABWARE_LABEL)  #!
            elif plate_types[0] == "full": 
                plate1 = protocol.load_labware(PLATE_TYPE_FULL, plate_locations[0])
            else: 
                print("Cannot load labware - plate 1")
        
            if len(plate_names) >= 2: 
                #plate2 = protocol.load_labware(plate_types[1], plate_locations[1], plate_labels[1])
                if plate_types[1] == "semi": 
                    plate2 = protocol.load_labware_from_definition(LABWARE_DEF, plate_locations[1], LABWARE_LABEL)  #!
                elif plate_types[1] == "full": 
                    plate2 = protocol.load_labware(PLATE_TYPE_FULL, plate_locations[1])
                else: 
                    print("Cannot load labware - plate 2")

                if len(plate_names) >= 3: 
                    #plate3 = protocol.load_labware(plate_types[2], plate_locations[2], plate_labels[2])
                    if plate_types[2] == "semi": 
                        plate3 = protocol.load_labware_from_definition(LABWARE_DEF, plate_locations[2], LABWARE_LABEL)  #!
                    elif plate_types[2] == "full": 
                        plate3 = protocol.load_labware(PLATE_TYPE_FULL, plate_locations[2])
                    else: 
                        print("Cannot load labware - plate 3")
                    
                    if len(plate_names) >= 4: 
                        #plate4 = protocol.load_labware(plate_types[3], plate_locations[3], plate_labels[3])
                        if plate_types[3] == "semi": 
                            plate4 = protocol.load_labware_from_definition(LABWARE_DEF, plate_locations[3], LABWARE_LABEL)  #!
                        elif plate_types[3] == "full": 
                            plate4 = protocol.load_labware(PLATE_TYPE_FULL, plate_locations[3])
                        else: 
                            print("Cannot load labware - plate 4")

                        if len(plate_names) >= 5: 
                            #plate5 = protocol.load_labware(plate_types[4], plate_locations[4], plate_labels[4])
                            if plate_types[4] == "semi": 
                                plate5 = protocol.load_labware_from_definition(LABWARE_DEF, plate_locations[4], LABWARE_LABEL) 
                            elif plate_types[4] == "full": 
                                plate5 = protocol.load_labware(PLATE_TYPE_FULL, plate_locations[4])
                            else: 
                                print("Cannot load labware - plate 5")

        else: 
            print("Error: there are no source locations to initialize")
            raise  # what does this do? 

        # define plate name to plate def dictionary
        naming_dict = {} 
        # TODO: should these if statements be stacked?
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

        # TESTING
        print(naming_dict)

        # START THE TRANSFERS, home the robot when transfers are complete
        pipette_20uL.flow_rate.aspirate = 3  # TODO: think about making this faster

        for i in range(len(source_names)):   # TODO: this should accomplish all the transfers ( test this!)
            pipette_20uL.transfer(
                transf_volumes[i], 
                naming_dict[source_names[i]].wells(source_wells[i]), 
                naming_dict[dest_names[i]].wells(dest_wells[i]),
            )
            
        pipette_20uL.home() 
    
    transfer_volumes()

### end