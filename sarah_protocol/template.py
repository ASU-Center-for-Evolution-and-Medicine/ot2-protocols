### start
import sys
import os
import pandas as pd
from opentrons import protocol_api, simulate, execute
### end


# HELPER METHODS ------------------------------------------------------------------
def write_protocol(protocol_path, wells, volumes): 
    current_file_path = os.path.abspath("template.py")

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
                        open_that.write(f"\nsource_wells = {str(wells)}")
                        open_that.write(f"\nsource_volumes = {str(volumes)}\n")
        
        return(f"Protocol created = {protocol_path} ")
    except: 
        return("Error: Could not write to protocol file")

# MAIN METHOD --------------------------------------------------------------------

def generate_from_template(source_csv_list, output_folder, file_name): 
    source_csvs = source_csv_list
    source_wells = {}
    source_volumes = {} 
    output = ""
  
    # extract data from csvs
    tips = 0
    for loc, path in source_csvs:  # this should still work
        df = pd.read_csv(path, encoding='utf-8-sig')
        wells = []
        volumes = []
        for each in df["Source"]: 
            wells.append(each)
        for each in df["Volume"]: 
            volumes.append(each)
        source_wells[loc] = wells
        source_volumes[loc] = volumes

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
        write_output = write_protocol(file_to_create, source_wells, source_volumes)
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
    
    DESTINATION_PLATE_TYPE = "nest_96_wellplate_2ml_deep" #idk what plate you have, I just temp it up here.
    DESTINATION_PLATE_SLOT = "1"
    
    SOURCE_PLATE_TYPE = "nest_96_wellplate_100ul_pcr_full_skirt" # same as above.
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
    
    
    def transfer_volumes(source_wells, volumes):
        
        #load tip racks at all possible locations (don't need to actually use all these tip locations)
        tiprack1 = protocol.load_labware(TIPRACK_TYPE, TIPRACK_SLOT1)
        tiprack2 = protocol.load_labware(TIPRACK_TYPE, TIPRACK_SLOT2)
        tiprack3 = protocol.load_labware(TIPRACK_TYPE, TIPRACK_SLOT3)
        tiprack4 = protocol.load_labware(TIPRACK_TYPE, TIPRACK_SLOT4)
        tiprack5 = protocol.load_labware(TIPRACK_TYPE, TIPRACK_SLOT5)

        #load the pipette and point to location
        pipette = protocol.load_instrument(PIPETTE_TYPE, mount=PIPETTE_MOUNT, tip_racks=[tiprack1, tiprack2, tiprack3, tiprack4, tiprack5])

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

        # load the source plates and source wells
        if len(source_locs) >= 1: 
            source1 = protocol.load_labware(SOURCE_PLATE_TYPE, source_locs[0])
            source1_wells = [source1.wells_by_name()[well] for well in source_wells[source_locs[0]]]
            source1_volumes = source_volumes[source_locs[0]]   # should be a list already :) 
            
            if len(source_locs) >= 2: 
                source2 = protocol.load_labware(SOURCE_PLATE_TYPE, source_locs[1])
                source2_wells = [source2.wells_by_name()[well] for well in source_wells[source_locs[1]]]
                source2_volumes = source_volumes[source_locs[1]]

                if len(source_locs) >= 3: 
                    source3 = protocol.load_labware(SOURCE_PLATE_TYPE, source_locs[2])
                    source3_wells = [source3.wells_by_name()[well] for well in source_wells[source_locs[2]]]
                    source3_volumes = source_volumes[source_locs[2]]

                    if len(source_locs) >= 4: 
                        source4 = protocol.load_labware(SOURCE_PLATE_TYPE, source_locs[3])
                        source4_wells = [source4.wells_by_name()[well] for well in source_wells[source_locs[3]]]
                        source4_volumes = source_volumes[source_locs[3]]

                        if len(source_locs) == 5: 
                            source5 = protocol.load_labware(SOURCE_PLATE_TYPE, source_locs[4])
                            source5_wells = [source5.wells_by_name()[well] for well in source_wells[source_locs[4]]]
                            source5_volumes = source_volumes[source_locs[4]]

                        elif len(source_locs) > 5: 
                            print("Error: cannot load more than 5 source plates")
                            raise
        else: 
            print("Error: there are no source locations to initialize")
            raise

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

        #load the destination plate (a 2ml tuberack in this case).
        destination_plate = protocol.load_labware(DESTINATION_PLATE_TYPE, DESTINATION_PLATE_SLOT)
        
        #read in the destination wells on the destination plate(tuberack), in this case, just the first well since all volume goes into one well.
        destination_well = destination_plate.wells()[0] #'A1'

        #start the transfers, home the robot when transfers are complete
        if source1: 
            pipette.transfer(source1_volumes, source1_wells, destination_well, blowout=False, new_tip="always")
        if source2: 
            pipette.transfer(source2_volumes, source2_wells, destination_well, blowout=False, new_tip="always")
        if source3: 
            pipette.transfer(source3_volumes, source3_wells, destination_well, blowout=False, new_tip="always")
        if source4: 
            pipette.transfer(source4_volumes, source4_wells, destination_well, blowout=False, new_tip="always")
        if source5: 
            pipette.transfer(source5_volumes, source5_wells, destination_well, blowout=False, new_tip="always")
        pipette.home()
    
    transfer_volumes(source_wells=source_wells, volumes=source_volumes)

# run(protocol)

# for line in protocol.commands():
#     print(line)

### end
        
