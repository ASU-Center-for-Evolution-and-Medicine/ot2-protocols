### start
import sys
import os
import pandas as pd
from opentrons import protocol_api, simulate, execute
### end


# HELPER METHODS ------------------------------------------------------------------
def write_protocol(protocol_path, wells, volumes): 
    current_file_path = "/Users/cstone/Desktop/CodingPractice/sarah_protocol/template.py"

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

    quit()    