### start
import sys
import os
import pandas as pd
from opentrons import protocol_api, simulate, execute
import json
### end


# HELPER METHODS ------------------------------------------------------------------
def write_protocol(protocol_path, wells_dict, volumes_dict, destinations_dict, plate_types_dict): 
    #current_file_path = os.path.abspath("template.py")   # TODO: For some reason this downs't work on mac 
    current_file_path = "/Users/cstone/Desktop/OT-2/ot2-protocols/sarah_protocol/template.py"

    try: 
        with open(current_file_path, 'r') as open_this: 
            with open(protocol_path, 'w+') as open_that: 
                contents_this = open_this.readlines()
                for i in range(len(contents_this)): 
                    if contents_this[i].startswith("### start"):
                        j = i
                        while not contents_this[j].startswith("### end"): 
                            j+=1
                        open_that.writelines(contents_this[i+1:j])

                    if contents_this[i].startswith("### TD"):
                        open_that.write(f"\nsource_wells = {str(wells_dict)}")
                        open_that.write(f"\nsource_volumes = {str(volumes_dict)}\n")
                        open_that.write(f"\nsource_destinations = {str(destinations_dict)}\n")
                        open_that.write(f"\nsource_plate_types = {str(plate_types_dict)}\n")

        return(f"Protocol created = {protocol_path} ")
    except: 
        return(f"Error: Could not write to protocol file\n{current_file_path}\n{protocol_path}")

# MAIN METHOD --------------------------------------------------------------------

def generate_from_template(source_csv_list, output_folder, file_name): 
    source_csvs = source_csv_list
    source_wells = {}
    source_volumes = {} 
    source_destinations = {}
    source_plate_types = {}
    output = ""
  
    # extract data from csvs
    tips = 0
    for loc, path, plate_type in source_csvs:  # this should still work
        df = pd.read_csv(path, encoding='utf-8-sig')
        wells = []
        volumes = []
        destinations = []
        for each in df["Source"]: 
            wells.append(each)
        for each in df["Volume"]: 
            volumes.append(each)
        for each in df["Destination"]:
            each = "A" + (str(each)).strip()
            destinations.append(each)
        source_wells[loc] = wells
        source_volumes[loc] = volumes
        source_destinations[loc] = destinations
        source_plate_types[loc] = plate_type

        tips += len(source_wells[loc]) # keep track of number of tips needed

    # determine the number of tips needed 
    num_boxes = int(tips/96)+1 if not tips%96 == 0 else int(tips/96)
    tip_box_loc = [7,8,9,10,11]

    # add deck layout to output string -----
    # output += "DECK LAYOUT: "
    # output += "1: DESTINATION PLATE"
    # output += "SOURCE PLATES: "
    # for loc, path in source_csvs: 
    #     output += f"{loc}: {path}"
    # output += "TIP BOXES: "
    # for i in range(num_boxes): 
    #     output += f"{tip_box_loc[i]}: 20uL tip box"
    # --------------------------------------

    # where to write the protocol? # TODO: make this another GUI option
    try: 
        file_to_create = os.path.join(output_folder, file_name)
        write_output = write_protocol(file_to_create, source_wells, source_volumes, source_destinations, source_plate_types)
        output += write_output
    except Error as e:  
        output += f"\nError: Coud not resolve output protocol file path"

    return output
    


### start  ------------------------------------------------------------------------------------------------------

# metadata
metadata = {
'protocolName': 'Volume Transfer Protocol',
'author': 'Casey Stone <cstone@anl.gov>',
'description': 'Simple protocol to transfer a given set of volumes into a tube.',
'apiLevel': '2.8'
}

### end


### TD  <--- DO NOT DELETE THIS


### start

def run(protocol):
    
    #Defining the labware types and locations.
    
    PIPETTE_TYPE = "p20_single_gen2"
    PIPETTE_MOUNT = "right"
    
    DESTINATION_PLATE_TYPE = 'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap' #idk what plate you have, I just temp it up here.
    DESTINATION_PLATE_SLOT = "1"
    
    SOURCE_PLATE_TYPE_FULL = "nest_96_wellplate_100ul_pcr_full_skirt" # same as above.
    SOURCE_PLATE_TYPE_SEMI = 'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap'   # TODO: REPLACE WITH NEW PLATE DEF

    # SOURCE_PLATE_SLOT = "4"
    
    TIPRACK_TYPE = "opentrons_96_tiprack_20ul"
    TIPRACK_SLOT1 = 7
    TIPRACK_SLOT2 = 8
    TIPRACK_SLOT3 = 9
    TIPRACK_SLOT4 = 10
    TIPRACK_SLOT5 = 11
    
    # TIPRACK_TYPE = "opentrons_96_tiprack_20ul"
    # TIPRACK_SLOT = "5" #this is the slot you put the tiprack in.
    INITIAL_TIP = "A1" #picks up the first tip from the upper left of rack. 

    # TEST SEMI SKIRTED LABWARE   #!
    LABWARE_DEF_JSON = """{"ordering":[["A1","B1","C1","D1","E1","F1","G1","H1"],["A2","B2","C2","D2","E2","F2","G2","H2"],["A3","B3","C3","D3","E3","F3","G3","H3"],["A4","B4","C4","D4","E4","F4","G4","H4"],["A5","B5","C5","D5","E5","F5","G5","H5"],["A6","B6","C6","D6","E6","F6","G6","H6"],["A7","B7","C7","D7","E7","F7","G7","H7"],["A8","B8","C8","D8","E8","F8","G8","H8"],["A9","B9","C9","D9","E9","F9","G9","H9"],["A10","B10","C10","D10","E10","F10","G10","H10"],["A11","B11","C11","D11","E11","F11","G11","H11"],["A12","B12","C12","D12","E12","F12","G12","H12"]],"brand":{"brand":"PCR_semi_skirt_wAdapter","brandId":[]},"metadata":{"displayName":"PCR_semi_skirt_wAdapter 96 Well Plate 200 µL","displayCategory":"wellPlate","displayVolumeUnits":"µL","tags":[]},"dimensions":{"xDimension":127.76,"yDimension":85.48,"zDimension":24},"wells":{"A1":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":14.38,"y":74.24,"z":3.2},"B1":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":14.38,"y":65.24,"z":3.2},"C1":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":14.38,"y":56.24,"z":3.2},"D1":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":14.38,"y":47.24,"z":3.2},"E1":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":14.38,"y":38.24,"z":3.2},"F1":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":14.38,"y":29.24,"z":3.2},"G1":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":14.38,"y":20.24,"z":3.2},"H1":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":14.38,"y":11.24,"z":3.2},"A2":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":23.38,"y":74.24,"z":3.2},"B2":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":23.38,"y":65.24,"z":3.2},"C2":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":23.38,"y":56.24,"z":3.2},"D2":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":23.38,"y":47.24,"z":3.2},"E2":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":23.38,"y":38.24,"z":3.2},"F2":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":23.38,"y":29.24,"z":3.2},"G2":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":23.38,"y":20.24,"z":3.2},"H2":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":23.38,"y":11.24,"z":3.2},"A3":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":32.38,"y":74.24,"z":3.2},"B3":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":32.38,"y":65.24,"z":3.2},"C3":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":32.38,"y":56.24,"z":3.2},"D3":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":32.38,"y":47.24,"z":3.2},"E3":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":32.38,"y":38.24,"z":3.2},"F3":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":32.38,"y":29.24,"z":3.2},"G3":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":32.38,"y":20.24,"z":3.2},"H3":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":32.38,"y":11.24,"z":3.2},"A4":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":41.38,"y":74.24,"z":3.2},"B4":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":41.38,"y":65.24,"z":3.2},"C4":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":41.38,"y":56.24,"z":3.2},"D4":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":41.38,"y":47.24,"z":3.2},"E4":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":41.38,"y":38.24,"z":3.2},"F4":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":41.38,"y":29.24,"z":3.2},"G4":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":41.38,"y":20.24,"z":3.2},"H4":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":41.38,"y":11.24,"z":3.2},"A5":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":50.38,"y":74.24,"z":3.2},"B5":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":50.38,"y":65.24,"z":3.2},"C5":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":50.38,"y":56.24,"z":3.2},"D5":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":50.38,"y":47.24,"z":3.2},"E5":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":50.38,"y":38.24,"z":3.2},"F5":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":50.38,"y":29.24,"z":3.2},"G5":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":50.38,"y":20.24,"z":3.2},"H5":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":50.38,"y":11.24,"z":3.2},"A6":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":59.38,"y":74.24,"z":3.2},"B6":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":59.38,"y":65.24,"z":3.2},"C6":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":59.38,"y":56.24,"z":3.2},"D6":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":59.38,"y":47.24,"z":3.2},"E6":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":59.38,"y":38.24,"z":3.2},"F6":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":59.38,"y":29.24,"z":3.2},"G6":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":59.38,"y":20.24,"z":3.2},"H6":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":59.38,"y":11.24,"z":3.2},"A7":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":68.38,"y":74.24,"z":3.2},"B7":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":68.38,"y":65.24,"z":3.2},"C7":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":68.38,"y":56.24,"z":3.2},"D7":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":68.38,"y":47.24,"z":3.2},"E7":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":68.38,"y":38.24,"z":3.2},"F7":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":68.38,"y":29.24,"z":3.2},"G7":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":68.38,"y":20.24,"z":3.2},"H7":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":68.38,"y":11.24,"z":3.2},"A8":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":77.38,"y":74.24,"z":3.2},"B8":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":77.38,"y":65.24,"z":3.2},"C8":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":77.38,"y":56.24,"z":3.2},"D8":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":77.38,"y":47.24,"z":3.2},"E8":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":77.38,"y":38.24,"z":3.2},"F8":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":77.38,"y":29.24,"z":3.2},"G8":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":77.38,"y":20.24,"z":3.2},"H8":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":77.38,"y":11.24,"z":3.2},"A9":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":86.38,"y":74.24,"z":3.2},"B9":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":86.38,"y":65.24,"z":3.2},"C9":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":86.38,"y":56.24,"z":3.2},"D9":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":86.38,"y":47.24,"z":3.2},"E9":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":86.38,"y":38.24,"z":3.2},"F9":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":86.38,"y":29.24,"z":3.2},"G9":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":86.38,"y":20.24,"z":3.2},"H9":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":86.38,"y":11.24,"z":3.2},"A10":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":95.38,"y":74.24,"z":3.2},"B10":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":95.38,"y":65.24,"z":3.2},"C10":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":95.38,"y":56.24,"z":3.2},"D10":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":95.38,"y":47.24,"z":3.2},"E10":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":95.38,"y":38.24,"z":3.2},"F10":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":95.38,"y":29.24,"z":3.2},"G10":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":95.38,"y":20.24,"z":3.2},"H10":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":95.38,"y":11.24,"z":3.2},"A11":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":104.38,"y":74.24,"z":3.2},"B11":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":104.38,"y":65.24,"z":3.2},"C11":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":104.38,"y":56.24,"z":3.2},"D11":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":104.38,"y":47.24,"z":3.2},"E11":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":104.38,"y":38.24,"z":3.2},"F11":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":104.38,"y":29.24,"z":3.2},"G11":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":104.38,"y":20.24,"z":3.2},"H11":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":104.38,"y":11.24,"z":3.2},"A12":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":113.38,"y":74.24,"z":3.2},"B12":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":113.38,"y":65.24,"z":3.2},"C12":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":113.38,"y":56.24,"z":3.2},"D12":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":113.38,"y":47.24,"z":3.2},"E12":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":113.38,"y":38.24,"z":3.2},"F12":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":113.38,"y":29.24,"z":3.2},"G12":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":113.38,"y":20.24,"z":3.2},"H12":{"depth":20.8,"totalLiquidVolume":200,"shape":"circular","diameter":5.38,"x":113.38,"y":11.24,"z":3.2}},"groups":[{"metadata":{"wellBottomShape":"v"},"wells":["A1","B1","C1","D1","E1","F1","G1","H1","A2","B2","C2","D2","E2","F2","G2","H2","A3","B3","C3","D3","E3","F3","G3","H3","A4","B4","C4","D4","E4","F4","G4","H4","A5","B5","C5","D5","E5","F5","G5","H5","A6","B6","C6","D6","E6","F6","G6","H6","A7","B7","C7","D7","E7","F7","G7","H7","A8","B8","C8","D8","E8","F8","G8","H8","A9","B9","C9","D9","E9","F9","G9","H9","A10","B10","C10","D10","E10","F10","G10","H10","A11","B11","C11","D11","E11","F11","G11","H11","A12","B12","C12","D12","E12","F12","G12","H12"]}],"parameters":{"format":"irregular","quirks":[],"isTiprack":false,"isMagneticModuleCompatible":false,"loadName":"pcrsemiskirtwadapter_96_wellplate_200ul"},"namespace":"custom_beta","version":1,"schemaVersion":2,"cornerOffsetFromSlot":{"x":0,"y":0,"z":0}}"""
    LABWARE_DEF = json.loads(LABWARE_DEF_JSON)
    LABWARE_LABEL = LABWARE_DEF.get('metadata', {}).get('displayName', 'test labware')
    LABWARE_DIMENSIONS = LABWARE_DEF.get('wells', {}).get('A1', {}).get('yDimension')
    
    
    def transfer_volumes(source_wells, volumes):

        #load tip racks at all possible locations (don't need to actually use all these tip locations)
        tiprack1 = protocol.load_labware(TIPRACK_TYPE, TIPRACK_SLOT1)
        tiprack2 = protocol.load_labware(TIPRACK_TYPE, TIPRACK_SLOT2)
        tiprack3 = protocol.load_labware(TIPRACK_TYPE, TIPRACK_SLOT3)
        tiprack4 = protocol.load_labware(TIPRACK_TYPE, TIPRACK_SLOT4)
        tiprack5 = protocol.load_labware(TIPRACK_TYPE, TIPRACK_SLOT5)

        #load the pipette and point to location
        pipette = protocol.load_instrument(PIPETTE_TYPE, mount=PIPETTE_MOUNT, tip_racks=[tiprack1, tiprack2, tiprack3, tiprack4, tiprack5])
        pipette.well_bottom_clearance.aspirate = 0

        print("PIPETTE TYPE:")
        print(PIPETTE_TYPE)
        print("TIP RACKS SLOTS:")
        print(TIPRACK_SLOT1)
        print(TIPRACK_SLOT2)
        print(TIPRACK_SLOT3)
        print(TIPRACK_SLOT4)
        print(TIPRACK_SLOT5)
        print("LOADED TIP RACKS")
        print(tiprack1)
        print(tiprack2)
        print(tiprack3)
        print(tiprack4)
        print(tiprack5)

        
        # format arrays of source names and locations
        source_locs = []
        for key in source_wells.keys(): 
            source_locs.append(key)
        # source_names = source_locs.copy()  # might not need this??
        # source_names = [f"source{x}" for x in source_names]

        source1 = None 
        source2 = None
        source3 = None 
        source4 = None
        source5 = None

        source1_wells = None
        source2_wells = None
        source3_wells = None
        source4_wells = None
        source5_wells = None

        source1_volumes = None
        source2_volumes = None
        source3_volumes = None 
        source4_volumes = None 
        source5_volumes = None 

        source1_dest = None
        source2_dest = None
        source3_dest = None 
        source4_dest = None 
        source5_dest = None

        source1_type = None
        source2_type = None 
        source3_type = None
        source4_type = None
        source5_type = None

        #load the destination plate (a 2ml tuberack in this case).
        destination_plate = protocol.load_labware(DESTINATION_PLATE_TYPE, DESTINATION_PLATE_SLOT)

        # load the source plates and source wells
        if len(source_locs) >= 1: 
            #source1 = protocol.load_labware(SOURCE_PLATE_TYPE, source_locs[0])
            source1_type = source_plate_types[source_locs[0]]
            if source1_type == "semi": 
                source1 = protocol.load_labware_from_definition(LABWARE_DEF, source_locs[0], LABWARE_LABEL)  #!
                #source1 = protocol.load_labware(SOURCE_PLATE_TYPE_SEMI, source_locs[0])
            elif source1_type == "full": 
                source1 = protocol.load_labware(SOURCE_PLATE_TYPE_FULL, source_locs[0])
            else: 
                print("Cannot load labware - plate 1")
            source1_wells = [source1.wells_by_name()[well] for well in source_wells[source_locs[0]]]
            source1_volumes = source_volumes[source_locs[0]]   # should be a list already :) 
            source1_dest = [destination_plate.wells_by_name()[well] for well in source_destinations[source_locs[0]]]
            
            
            if len(source_locs) >= 2: 
                source2_type = source_plate_types[source_locs[1]]
                if source2_type == "semi": 
                    source2 = protocol.load_labware_from_definition(LABWARE_DEF, source_locs[1], LABWARE_LABEL)  #!
                    #source2 = protocol.load_labware(SOURCE_PLATE_TYPE_SEMI, source_locs[1])
                elif source2_type == "full": 
                    source2 = protocol.load_labware(SOURCE_PLATE_TYPE_FULL, source_locs[1])
                else: 
                    print("Cannot load labware - plate 2")
                source2_wells = [source2.wells_by_name()[well] for well in source_wells[source_locs[1]]]
                source2_volumes = source_volumes[source_locs[1]]
                source2_dest = [destination_plate.wells_by_name()[well] for well in source_destinations[source_locs[1]]]
                source2_type = source_plate_types[source_locs[1]]

                if len(source_locs) >= 3: 
                    source3_type = source_plate_types[source_locs[2]]
                    if source3_type == "semi": 
                        source3 = protocol.load_labware_from_definition(LABWARE_DEF, source_locs[2], LABWARE_LABEL) #!
                        #source3 = protocol.load_labware(SOURCE_PLATE_TYPE_SEMI, source_locs[2])
                    elif source3_type == "full": 
                        source3 = protocol.load_labware(SOURCE_PLATE_TYPE_FULL, source_locs[2])
                    else: 
                        print("Cannot load labware - plate 3")
                    source3_wells = [source3.wells_by_name()[well] for well in source_wells[source_locs[2]]]
                    source3_volumes = source_volumes[source_locs[2]]
                    source3_dest = [destination_plate.wells_by_name()[well] for well in source_destinations[source_locs[2]]]
                    source3_type = source_plate_types[source_locs[2]]

                    if len(source_locs) >= 4: 
                        source4_type = source_plate_types[source_locs[3]]
                        if source4_type == "semi": 
                            source4 = protocol.load_labware_from_definition(LABWARE_DEF, source_locs[3], LABWARE_LABEL)  #!
                            #source4 = protocol.load_labware(SOURCE_PLATE_TYPE_SEMI, source_locs[3])
                        elif source4_type == "full": 
                            source4 = protocol.load_labware(SOURCE_PLATE_TYPE_FULL, source_locs[3])
                        else: 
                            print("Cannot load labware - plate 4")
                        source4_wells = [source4.wells_by_name()[well] for well in source_wells[source_locs[3]]]
                        source4_volumes = source_volumes[source_locs[3]]
                        source4_dest = [destination_plate.wells_by_name()[well] for well in source_destinations[source_locs[3]]]
                        source4_type = source_plate_types[source_locs[3]]

                        if len(source_locs) == 5: 
                            source5_type = source_plate_types[source_locs[4]]
                            if source5_type == "semi": 
                                source5 = protocol.load_labware_from_definition(LABWARE_DEF, source_locs[4], LABWARE_LABEL) #!
                                #source5 = protocol.load_labware(SOURCE_PLATE_TYPE_SEMI, source_locs[4])
                            elif source5_type == "full": 
                                source5 = protocol.load_labware(SOURCE_PLATE_TYPE_FULL, source_locs[4])
                            else: 
                                print("Cannot load labware - plate 5")
                            source5_wells = [source5.wells_by_name()[well] for well in source_wells[source_locs[4]]]
                            source5_volumes = source_volumes[source_locs[4]]
                            source5_dest = [destination_plate.wells_by_name()[well] for well in source_destinations[source_locs[4]]]
                            source5_type = source_plate_types[source_locs[4]]

                        elif len(source_locs) > 5: 
                            print("Error: cannot load more than 5 source plates")
                            raise
        else: 
            print("Error: there are no source locations to initialize")
            raise

        print("SOURCE PLATE TYPES: ")
        print(source1_type)
        print(source2_type)
        print(source3_type)
        print(source4_type)
        print(source5_type)

        print("LOADED SOURCE PLATES")
        print(source1)
        print(f"\t{source1_wells}")
        print(source2)
        print(f"\t{source2_wells}")
        print(source3)
        print(f"\t{source3_wells}")
        print(source4)
        print(f"\t{source4_wells}")
        print(source5)
        print(f"\t{source5_wells}")

        #read in the destination wells on the destination plate(tuberack), in this case, just the first well since all volume goes into one well.
        destination_well = destination_plate.wells()[0] #'A1'

        #start the transfers, home the robot when transfers are complete
        pipette.flow_rate.aspirate = 3
        if source1: 
            for i in range(len(source1_wells)): 
                pipette.transfer(source1_volumes[i], source1_wells[i], source1_dest[i], blowout=False, new_tip='always') 
            # pipette.transfer(source1_volumes, source1_wells, destination_well, blowout=False, new_tip="always")
        if source2: 
            for i in range(len(source2_wells)): 
                pipette.transfer(source2_volumes[i], source2_wells[i], source2_dest[i], blowout=False, new_tip='always') 
            #pipette.transfer(source2_volumes, source2_wells, destination_well, blowout=False, new_tip="always")
        if source3: 
            for i in range(len(source3_wells)): 
                pipette.transfer(source3_volumes[i], source3_wells[i], source3_dest[i], blowout=False, new_tip='always') 
            #pipette.transfer(source3_volumes, source3_wells, destination_well, blowout=False, new_tip="always")
        if source4: 
            for i in range(len(source4_wells)): 
                pipette.transfer(source4_volumes[i], source4_wells[i], source4_dest[i], blowout=False, new_tip='always') 
            #pipette.transfer(source4_volumes, source4_wells, destination_well, blowout=False, new_tip="always")
        if source5: 
            for i in range(len(source5_wells)): 
                pipette.transfer(source5_volumes[i], source5_wells[i], source5_dest[i], blowout=False, new_tip='always') 
            #pipette.transfer(source5_volumes, source5_wells, destination_well, blowout=False, new_tip="always")
        pipette.home()
    
    transfer_volumes(source_wells=source_wells, volumes=source_volumes)

# run(protocol)

# for line in protocol.commands():
#     print(line)

### end
        
