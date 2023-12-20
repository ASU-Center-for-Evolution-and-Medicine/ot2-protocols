import pandas as pd

def parse_csv(input_csv_path):
    """ parse_input_csv
    Description: 
        Parses the information contained within the csv at the specified file path (input_csv_path)
        and compiles the information into lists that can be used to later generate the OT-2 protocol 

    Parameters: 
        input_csv_path: full path to input csv file
        
    Returns: 
        source_plate_wells: list of source wells to aspirate from in order
        dest_plate_wells: list of destination wells to dispense into in order 
        transf_volumes: list of transfer volumes (uL) to aspirate from specified source plate
            well and dispense into destination plate well in order

    """
    source_plate_wells = []
    transf_volumes = []
    dest_plate_wells = []

    try: 
        # read csv into data frame
        df = pd.read_csv(input_csv_path, encoding='utf-8-sig')

        # collect data from csv into lists
        try: 
            for source_well in df["Source Well"]: 
                source_well = str(source_well)  # make sure contents of csv are a string
                source_plate_wells.append(source_well)
        except KeyError as e:
            print("'Source Well' column cannot be parsed from input csv")
            raise e

        try: 
            for dest_well in df["Destination Well"]: 
                dest_well = str(source_well)  # make sure contents of csv are a string
                dest_plate_wells.append(dest_well)
        except KeyError as e:
            print("'Destination Well' column cannot be parsed from input csv")
            raise e

        try: 
            for volume in df["Volume"]: 
                volume = int(volume)  # make sure contents of csv are integers for volume column
                transf_volumes.append(volume)
        except KeyError as e: 
            print("'Volume' column cannot be parsed from input csv")
            raise e
        
    except OSError as e: 
        print("ERROR: Input CSV could not be parsed")
        raise e

    return source_plate_wells, dest_plate_wells, transf_volumes



def write_protocol_from_template(template_path, output_filename, source_plate_wells, dest_plate_wells, transf_volumes): 
    """
    write_protocol_from_template

    Description: Writes all variables parsed from csv into template protocol and outputs to python file

    Parameters: 
        template_path:
        output_filename:
        source_plate_wells:  
        dest_plate_wells:
        transf_volumes:   
         
    Returns: 
        None 
    """  
    try: 
        with open(template_path, 'r') as open_template: 
            with open(output_filename, 'w+') as open_protocol: 
                template_contents = open_template.readlines()
                for i in range(len(template_contents)): 
                    if template_contents[i].startswith("### start"):
                        j = i
                        while not template_contents[j].startswith("### end"): 
                            j+=1
                        open_protocol.writelines(template_contents[i+1:j])

                    if template_contents[i].startswith("### VAR"):
                        open_protocol.write(f"\nsource_wells = {str(source_plate_wells)}")
                        open_protocol.write(f"\ndest_wells = {str(dest_plate_wells)}")
                        open_protocol.write(f"\ntransf_volumes = {str(transf_volumes)}\n")

        print(f"Protocol created: {output_filename}" )
    
    except Exception as e: 
        print(f"\nError: Could not write to protocol file: {output_filename}")
        raise e
    

