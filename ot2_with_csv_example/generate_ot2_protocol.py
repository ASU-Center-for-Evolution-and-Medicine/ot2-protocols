import argparse
import sys
import os
import pandas as pd
from helper_methods import parse_csv, write_protocol_from_template


def generate_ot2_protocol(input_file, output_file): 
    """
    Example usage: 

    python generate_ot2_protocol.py -i /Users/cstone/Documents/RapidPrototypingLab/GitRepos/ot2-protocols/ot2_with_csv_example/csv_input/one_plate.csv -o /Users/cstone/Documents/RapidPrototypingLab/GitRepos/ot2-protocols/ot2_with_csv_example/test_output/test1.py
    
    """

    protocol_template_path = "ot2_csv_template.py"  

    # parse input csv file
    source_wells_list, dest_wells_list, volumes_list = parse_csv(input_file) 

    # write the parsed information into a new OT-2 script
    write_protocol_from_template(
        protocol_template_path, 
        output_file, 
        source_wells_list, 
        dest_wells_list, 
        volumes_list,
    )



def main(args):
    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        help="path to input csv file",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="path to output ot2 protcol file",
        required=True,
        type=str,
    )

    # capture the command line arguments
    args = vars(parser.parse_args())

    # pass to method that generates the ot2 protocol (see above)
    generate_ot2_protocol(
        args["input"],
        args["output"],
    )


if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv)