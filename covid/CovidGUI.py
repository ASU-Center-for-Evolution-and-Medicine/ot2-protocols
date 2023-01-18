from genericpath import exists
from re import template
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import os
from covid_template import *
from button_click_methods import *
import pandas as pd


class CovidGUI:
    root = Tk()
    root.title("Covid Pooling Protocol")

    sources_label = Label(root, text="SOURCE(S)")
    destination_label = Label(root, text="DESTINATION(S)")

    source_plate_name_label = Label(root, text="Plate Name")
    source_deck_location_label = Label(root, text="Deck Location")
    source_plate_type_label = Label(root, text="Plate Type")

    destination_plate_name_label = Label(root, text="Plate Name")
    destination_deck_location_label = Label(root, text="Deck Location")
    destination_plate_type_label = Label(root, text="Plate Type")

    source1_label = Label(root, text="1: ")
    source2_label = Label(root, text="2: ")
    source3_label = Label(root, text="3: ")

    destination1_label = Label(root, text="1: ")
    destination2_label = Label(root, text="2: ")

    input_csv_label = Label(root, text="Input CSV filename: ")
    write_loc_label = Label(root, text="Output Folder: ")
    file_name_label = Label(root, text="File Name (without extension): ")

    # to display info to user
    output_label = Label(root, text = "")
    deck_info_label = Label(root, text= "", anchor=W)

    # Text Entry Boxes
    source_plate_name_1_entry = Entry(root, width=15)
    source_plate_name_2_entry = Entry(root, width=15)
    source_plate_name_3_entry = Entry(root, width=15)

    #global input_csv_text_entry
    input_csv_text_entry = Entry(root, width=65)

    #global write_loc_text_entry
    write_loc_text_entry = Entry(root, width=65)
    write_loc_text_entry.insert(END, '/Users/stephanie/Desktop/OT2_Protocols')

    #global file_name_text_entry
    file_name_text_entry = Entry(root, width=65)
    file_name_text_entry.insert(END, "Protocol1")

    # Text Entry Boxes
    destination_plate_name_1_entry = Entry(root, width=15)
    destination_plate_name_2_entry = Entry(root, width=15)

    # Drop Down Boxes 
    # source
    source_deck_drop1_loc = StringVar()  # set variable type
    source_deck_drop2_loc = StringVar()
    source_deck_drop3_loc = StringVar()

    source_deck_drop1_loc.set(None)  # set default value
    source_deck_drop2_loc.set(None)
    source_deck_drop3_loc.set(None)

    source_deck_drop1 = OptionMenu(root, source_deck_drop1_loc, None,4,5,6)  # create drop downs
    source_deck_drop2 = OptionMenu(root, source_deck_drop2_loc, None,4,5,6)
    source_deck_drop3 = OptionMenu(root, source_deck_drop3_loc, None,4,5,6)

    # destination
    destination_deck_drop1_loc = StringVar()  # set variable type
    destination_deck_drop2_loc = StringVar()

    destination_deck_drop1_loc.set(None)  # set default value
    destination_deck_drop2_loc.set(None)

    destination_deck_drop1 = OptionMenu(root, destination_deck_drop1_loc, None,1,2)  # create drop downs
    destination_deck_drop2 = OptionMenu(root, destination_deck_drop2_loc, None,1,2)

    # source radio buttons
    source_plate1_type = StringVar() # define variable type
    source_plate2_type = StringVar()
    source_plate3_type = StringVar()

    source_plate1_type.set('full')  # initialize radio buttons
    source_plate2_type.set('full')
    source_plate3_type.set('full')

    source_semi1 = Radiobutton(root, text = "semi", variable=source_plate1_type, value="semi")
    source_full1 = Radiobutton(root, text = "full", variable=source_plate1_type, value="full")

    source_semi2 = Radiobutton(root, text = "semi", variable=source_plate2_type, value="semi")
    source_full2 = Radiobutton(root, text = "full", variable=source_plate2_type, value="full")

    source_semi3 = Radiobutton(root, text = "semi", variable=source_plate3_type, value="semi")
    source_full3 = Radiobutton(root, text = "full", variable=source_plate3_type, value="full")

    # destination radio buttons  
    destination_plate1_type = StringVar() # define variable type
    destination_plate2_type = StringVar()

    destination_plate1_type.set('full')  # initialize radio buttons
    destination_plate2_type.set('full')

    destination_semi1 = Radiobutton(root, text = "semi", variable=destination_plate1_type, value="semi")
    destination_full1 = Radiobutton(root, text = "full", variable=destination_plate1_type, value="full")

    destination_semi2 = Radiobutton(root, text = "semi", variable=destination_plate2_type, value="semi")
    destination_full2 = Radiobutton(root, text = "full", variable=destination_plate2_type, value="full")

    # dividing lines
    separator_vertical = ttk.Separator(root, orient='vertical')
    separator_horizontal_1 = ttk.Separator(root, orient='horizontal')
    separator_horizontal_2 = ttk.Separator(root, orient='horizontal')

    input_csv_button = None
    write_loc_button = None
    generate_protocol_button = None
    


    # --------------------------------------------------------------------------------------------------------
    def __init__(self) -> None: 
        self.display_on_root()
    

    #* Create Buttons method ---------------------------------------------------------------------------------
    def create_buttons(self):
        self.input_csv_button = Button(self.root, text="Browse", command=lambda:self.browse_input_csv_click())
        self.write_loc_button = Button(self.root, text="Browse", command=lambda:self.browse_write_folder_click())
        self.generate_protocol_button = Button(self.root, text="Generate Protocol", command=lambda:self.generate_protocol_click())
    

    def display_on_root(self):
        # call to create buttons placed in display on root method
        self.create_buttons()
        self.sources_label.grid(row=0, column=1, padx=20, pady=3, columnspan=4)
        self.destination_label.grid(row=0, column=7, pady=3, columnspan=4)

        #* SOURCES SIDE -------
        # labels 
        self.source_plate_name_label.grid(row=1, column=1)
        self.source_deck_location_label.grid(row=1, column=2)
        self.source_plate_type_label.grid(row=1, column=3, columnspan=2)

        self.source1_label.grid(row=2, column=0)
        self.source2_label.grid(row=3, column=0)
        self.source3_label.grid(row=4, column=0)

        # text entry boxes
        self.source_plate_name_1_entry.grid(row=2, column=1)
        self.source_plate_name_2_entry.grid(row=3, column=1)
        self.source_plate_name_3_entry.grid(row=4, column=1)

        # drop down boxes
        self.source_deck_drop1.grid(row=2, column=2)
        self.source_deck_drop2.grid(row=3, column=2)
        self.source_deck_drop3.grid(row=4, column=2)

        # radio buttons
        self.source_semi1.grid(row=2, column=3)
        self.source_full1.grid(row=2, column=4, padx=(0,5))
        self.source_semi2.grid(row=3, column=3)
        self.source_full2.grid(row=3, column=4, padx=(0,5))
        self.source_semi3.grid(row=4, column=3)
        self.source_full3.grid(row=4, column=4, padx=(0,5))

        #* DESTINATION SIDE --------
        # labels
        self.destination_plate_name_label.grid(row=1, column=7)
        self.destination_deck_location_label.grid(row=1, column=8)
        self.destination_plate_type_label.grid(row=1, column=9, columnspan=2)

        self.destination1_label.grid(row=2, column=6)
        self.destination2_label.grid(row=3, column=6)

        # text entry boxes
        self.destination_plate_name_1_entry.grid(row=2, column=7)
        self.destination_plate_name_2_entry.grid(row=3, column=7)

        # drop down boxes
        self.destination_deck_drop1.grid(row=2, column=8)
        self.destination_deck_drop2.grid(row=3, column=8)

        # radio buttons
        self.destination_semi1.grid(row=2, column=9)
        self.destination_full1.grid(row=2, column=10, padx=(0,5))
        self.destination_semi2.grid(row=3, column=9)
        self.destination_full2.grid(row=3, column=10, padx=(0,5))

        # OTHER
        # dividing lines
        self.separator_vertical.grid(row=0, column=5, rowspan=5, sticky=NS)
        self.separator_horizontal_1.grid(row=5, columnspan=11, sticky=EW, pady=10)
        self.separator_horizontal_2.grid(row=7, columnspan=11, sticky=EW, pady=10)

        #* INPUT CSV
        self.input_csv_label.grid(row=6, column=0, columnspan=2)
        self.input_csv_text_entry.grid(row=6, column=2, columnspan=7)  # don't use self. with global variables
        self.input_csv_button.grid(row=6, column=9, columnspan=2)

        #* OUTPUT HANDLING
        self.write_loc_label.grid(row=8, column=0, columnspan=2)
        self.file_name_label.grid(row=9, column=0, columnspan=2)

        self.write_loc_text_entry.grid(row=8, column=2, columnspan=7)# don't use self. with global variables
        self.file_name_text_entry.grid(row=9, column=2, columnspan=7)# don't use self. with global variables

        self.write_loc_button.grid(row=8, column=9, columnspan=2)

        self.generate_protocol_button.grid(row=10, column=0, columnspan=11, pady=5) 

        # display the gui
        self.root.mainloop()

    #* Button click methods ----------------------------------------------------------------------------------
    def browse_input_csv_click(self): 
        """ 
        browse_input_csv_click

        Description: Handles actions after user clicks 'Browse' for input file name on GUI

        """
        csv_filename = filedialog.askopenfile(title = "Select File",filetypes = (("CSV Files","*.csv"),))
        self.input_csv_text_entry.delete(0,"end")
        if csv_filename: 
            self.input_csv_text_entry.insert(0, csv_filename.name)


    def browse_write_folder_click(self): 
        """ 
        browse_write_folder_click

        Description: Handles actions after user clicks 'Browse' for input file name on GUI

        """
        output_folder = filedialog.askdirectory(title="Select Folder")  # todo: add a default folder opening location
        self.write_loc_text_entry.delete(0,"end")
        if output_folder:
            self.write_loc_text_entry.insert(0, output_folder)


    #* GETTER & CHECKER METHODS ----------------------------------------------------------------------------------------
    def get_plate_input(self): 
        """ 
        get_plate_info

        Description: Gathers all plate info from GUI and checks for invalid user entries

        Parameters: 
            None
        
        Returns: 
            plates_dict: dictionary of plates 
                {
                    plate name: (plate location, plate type), 
                    plate name: (plate location, plate type, 
                    ...
                }
            is_error: Boolean flag, true if error was detected in user entry, false otherwise
            output_text: Text to display to user about any errors that were detected

        """
        output_text = ""
        is_error = False
        plates_dict = {}
        decks_used = []

        # collect all variables
        source_1_name = self.source_plate_name_1_entry.get() if self.source_plate_name_1_entry.get() else None
        source_2_name = self.source_plate_name_2_entry.get() if self.source_plate_name_2_entry.get() else None
        source_3_name = self.source_plate_name_3_entry.get() if self.source_plate_name_3_entry.get() else None
        dest_1_name = self.destination_plate_name_1_entry.get() if self.destination_plate_name_1_entry.get() else None
        dest_2_name = self.destination_plate_name_2_entry.get() if self.destination_plate_name_2_entry.get() else None
        source_name_list = [source_1_name, source_2_name, source_3_name]
        dest_name_list = [dest_1_name, dest_2_name]
        name_list = [source_1_name, source_2_name, source_3_name, dest_1_name, dest_2_name]

        source_1_loc = self.source_deck_drop1_loc.get()
        source_2_loc = self.source_deck_drop2_loc.get()
        source_3_loc = self.source_deck_drop3_loc.get()
        dest_1_loc = self.destination_deck_drop1_loc.get()
        dest_2_loc = self.destination_deck_drop2_loc.get()
        loc_list = [source_1_loc, source_2_loc, source_3_loc, dest_1_loc, dest_2_loc]

        source_1_type = self.source_plate1_type.get()
        source_2_type = self.source_plate2_type.get()
        source_3_type = self.source_plate3_type.get()
        dest_1_type = self.destination_plate1_type.get()
        dest_2_type = self.destination_plate2_type.get()
        type_list = [source_1_type, source_2_type, source_3_type, dest_1_type, dest_2_type]

        # check that there are source and destination plates entered
        if source_name_list == [None, None, None]: 
            output_text += "ERROR: Please enter source plate(s)\n"
            is_error = True
        if dest_name_list == [None, None]: 
            output_text += "ERROR: Please enter destination plate(s)\n"
            is_error = True
        
        # check for duplicate plate names and compile info
        if not is_error: 
            for i in range(len(name_list)): 

                if not name_list[i] == None:  # if name is not None

                    if name_list[i].strip() in plates_dict:  # error if name already recorded
                        output_text += "ERROR: All plate names must be unique\n"
                        is_error = True
                        break  

                    else: 
                        # check for duplicate deck locations 
                        if loc_list[i] == 'None': 
                            output_text += "ERROR: Please enter a deck location for all source plates\n"
                            is_error = True
                            break 

                        if loc_list[i] in decks_used: 
                            output_text += "ERROR: No two plates can be placed at the same deck location\n"
                            is_error = True
                            break 

                        else: # everything is good
                            plates_dict[name_list[i].strip()] = (loc_list[i], type_list[i])
                            decks_used.append(loc_list[i])

        return plates_dict, is_error, output_text


    def get_input_csv_input(self): 
        """
        get_input_csv

        Description: collects input csv details and checks for valid input

        Parameters: 
            None 

        Returns: 
            input_csv_filename: user input for input csv from GUI, checked for existence
            is_error: Boolean flag, true if error was detected in user entry, false otherwise
            output_text: Text to display to user about any errors that were detected

        """
        output_text = ""
        is_error = False

        # collect user input
        input_csv_filename = self.input_csv_text_entry.get()

        # check that filename not none and is actual file
        if input_csv_filename == "": 
            is_error = True
            output_text += "\nERROR: Please enter an input csv filename"

        else: # if input csv is entered
            if not os.path.isfile(input_csv_filename): # if the file doesn't exist
                is_error = True
                output_text += "/nERROR: input csv entered does not exist"

        return input_csv_filename, is_error, output_text
                
            
    def get_output_file_input(self): 
        """
        get_output_file_details

        Description: collects user output file details, formats output filename, and checks for correct user inputs

        Parameters: 
            None

        Returns: 
            output_filename: filename of the protocol to be created (as specified by user in GUI)
            is_error: Boolean flag, true if error was detected in user entry, false otherwise
            output_text: Text to display to user about any errors that were detected
        """
        is_error = False
        output_text = ""
        output_filename = ""

        # collect output folder and filename 
        output_folder = self.write_loc_text_entry.get()
        filename_wo_ext = self.file_name_text_entry.get()

        # run checks for user input correctness 
        if output_folder == "": 
            is_error = True
            output_text += "\nERROR: Please enter an output folder (without the extension)"
        else: 
            if not os.path.isdir(output_folder): # check that output folder exists
                is_error = True
                output_text += "\nERROR: The output folder entered does not exist"

        if filename_wo_ext == "":
            is_error = True
            output_text += "\nERROR: Please enter a output filename (without the extension)"
        
        # format output filename
        if not ".py" in filename_wo_ext: 
            filename = filename_wo_ext + ".py"
        else: 
            filename = filename_wo_ext

        if not is_error: 
            output_filename = os.path.join(output_folder, filename)
            #TODO: How to check if this filename is valid without it existing yet? try catch on file creation? 
    
        return output_filename, is_error, output_text
        
    

    #* HELPER METHODS -----------------------------------------------------------------------------------------------
    def display_output_text(self, display_text):
        """
        display_output_text

        Description: displays output text on GUI for the user

        Parameters: 
            is_error: Boolean flag, true if error was detected in user entry, false otherwise
            output_text: Text to display to user about any errors that were detected

        Returns: 
            None

        """
        # delete old text and instantiate new output labels
        self.output_label.destroy()
        self.output_label = Label(self.root, text="")  # instantiate new output label 

        # update label with new text
        self.output_label["text"] = display_text 
        
        # display on GUI
        self.output_label.grid(row=12, column=1,pady=3, columnspan=10)

    
    def parse_input_csv(self, input_csv_filename, plates_dict): 
        """
        parse_input_csv

        Description: 

        Parameters: 
            input_csv_filename: input csv filename after collected and checked in get_input_csv_input method
            plates_dict: 

        Returns: 

            is_error: Boolean flag, true if error was detected in user entry, false otherwise
            output_text: Text to display to user about any errors that were detected

        """
        is_error = False
        output_text = ""

        source_plate_names = []
        source_plate_wells = []
        transf_volumes = []
        dest_plate_names = []
        dest_plate_wells = []

        try: 
            # read csv into data frame
            df = pd.read_csv(input_csv_filename, encoding='utf-8-sig')

            # collect data frame contents into lists
            for source_name in df["Original Plate Number"]: 
                source_name = str(source_name)
                source_plate_names.append(source_name)
                if not source_name.strip() in plates_dict: 
                    is_error = True
                    output_text += "\nERROR: input csv source plate names do not match user input"
                    break # so only one of these error messages appears

            for source_well in df["Original Well Number"]: 
                source_plate_wells.append(source_well)

            for volume in df["Volume Needed (ul)"]: 
                transf_volumes.append(volume)
                if not (volume <= 20 and volume >= 0): 
                    is_error = True
                    output_text += "\nError: Transfer volumes must be between 0 and 20 inclusive"
                    break # so ony one of these error messages appears

            for dest_name in df["New Plate Number"]: 
                dest_plate_names.append(dest_name)
                if not dest_name.strip() in plates_dict: 
                    is_error = True
                    output_text += "\nERROR: input csv destination plate names do not match user input"
                    break # so only one of these error messages appears

            for dest_well in df["New Well Number"]: 
                dest_plate_wells.append(dest_well)

            # TODO: Check that all lists are the same length? necessary?
            # TODO: Check that well names are valid? necessary?



        except OSError as e: 
            is_error = True
            output_text += "\nERROR: Input CSV could not be parsed"

        return source_plate_names, source_plate_wells, transf_volumes, dest_plate_names, dest_plate_wells, is_error, output_text


    def write_protocol_from_template(
        self, 
        plates_dict,
        source_plate_names, 
        source_plate_wells, 
        transf_volumes, 
        dest_plate_names, 
        dest_plate_wells, 
        output_filename
    ): 
        """
        write_protocol_from_template

        Description: Writes all variables parsed from csv into template protocol and outputs to python file

        Parameters: 
            source_plate_names, 
            source_plate_wells, 
            transf_volumes, 
            dest_plate_names, 
            dest_plate_wells, 
            output_filename

        Returns: 
            is_error: Boolean flag, true if error was detected in user entry, false otherwise
            output_text: Text to display to user about any errors that were detected
        """
        is_error = False
        output_text = ""

        template_path = "/Users/stephanie/Desktop/OT2_repo/ot2-protocols/covid/covid_template.py"  

        # TESTING
        print("WRITE PROTOCOL METHOD CALLED")
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
                            open_protocol.write(f"\nplates_dict = {str(plates_dict)}")
                            open_protocol.write(f"\nsource_names = {str(source_plate_names)}")
                            open_protocol.write(f"\nsource_wells = {str(source_plate_wells)}")
                            open_protocol.write(f"\ntransf_volumes = {str(transf_volumes)}")
                            open_protocol.write(f"\ndest_names = {str(dest_plate_names)}")
                            open_protocol.write(f"\ndest_wells = {str(dest_plate_wells)}\n")

                        if template_contents[i].startswith("### PROTOCOL NAME"):

                            # TESTING 
                            print(output_filename)
                            
                            protocol_name = os.path.basename(output_filename).replace(".py", "")
                            open_protocol.write(f"\'protocolName\': \'{protocol_name}\',\n")

            output_text += f"\nProtocol created: {output_filename}"

        except: 
            is_error = True
            output_text += f"\nError: Could not write to protocol file: {output_filename}"
        
        return is_error, output_text


    #* GENERATE PROTOCOL CLICK METHOD ------------------------------------------------------------------------------
    def generate_protocol_click(self): 
        any_errors = False
        # TODO: check if overriding is_error each time is a problem... 

        output_text = ""
        # clear and reinitialize user output labels (each time generate protocol is clicked)

        self.output_label.destroy()
        self.deck_info_label.destroy()
        self.output_label = Label(self.root, text="")  # instantiate new output label 
        self.deck_info_label = Label(self.root, text="", anchor=W)  # instantiate new deck information label

        # collect plates info
        plates_dict, plate_is_error, plate_output_text = self.get_plate_input()
        output_text += plate_output_text
        any_errors = plate_is_error if plate_is_error else any_errors
        
        # TESTING
        print("PLATE DICT")
        print(plates_dict)
        
        # collect input csv info
        input_csv_filename, input_is_error, input_csv_output_text = self.get_input_csv_input()
        output_text += input_csv_output_text
        any_errors = input_is_error if input_is_error else any_errors

        # collect output file info
        output_filename, output_is_error, output_output_text = self.get_output_file_input()
        output_text += output_output_text
        any_errors = output_is_error if output_is_error else any_errors

        # parse input csv
        source_plate_names, source_plate_wells, transf_volumes, dest_plate_names, dest_plate_wells, parse_csv_is_error, parse_csv_output_text = self.parse_input_csv(input_csv_filename, plates_dict)
        output_text += parse_csv_output_text
        any_errors = parse_csv_is_error if parse_csv_is_error else any_errors


        # TESTING
        print("EXTRACTED VARIABLES")
        print(source_plate_names)
        print(source_plate_wells)
        print(transf_volumes)
        print(dest_plate_names)
        print(dest_plate_wells)

        # pass variables to write protocol from template method
        write_is_error, write_output_text = self.write_protocol_from_template(
            plates_dict,
            source_plate_names, 
            source_plate_wells, 
            transf_volumes, 
            dest_plate_names, 
            dest_plate_wells, 
            output_filename
        )
        output_text += write_output_text
        any_errors = write_is_error if write_is_error else any_errors

        


        # display output message to the user
        # if output_text == "": 
        #     output_text += "Protocol Generated"
        if not output_text == "": 
            self.display_output_text(output_text)

        if not any_errors: # continue to generating protocol
            pass

covidGUI = CovidGUI()

