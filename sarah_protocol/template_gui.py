from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import os
from template import *

root = Tk()
root.title("Generate Transfer Protocol")

# *CREATE WIDGETS -----------------------------------------------------------------------------
# Labels
csv_filename_label = Label(root, text="CSV FILENAME")
deck_location_label = Label(root, text="DECK LOCATION")
plate_type_label = Label(root, text="PLATE TYPE")

source1_label = Label(root, text="Source 1: ")
source2_label = Label(root, text="Source 2: ")
source3_label = Label(root, text="Source 3: ")
source4_label = Label(root, text="Source 4: ")
source5_label = Label(root, text="Source 5: ")
separator = ttk.Separator(root, orient='horizontal')
write_loc_label = Label(root, text="Output Folder: ")
file_name_label = Label(root, text="File Name (without extension): ")

output_label = Label(root, text = "")
deck_info_label = Label(root, text= "", anchor=W)

# Text Entry Boxes
source1_text_entry = Entry(root, width=75)
source2_text_entry = Entry(root, width=75)
source3_text_entry = Entry(root, width=75)
source4_text_entry = Entry(root, width=75)
source5_text_entry = Entry(root, width=75)

write_loc_text_entry = Entry(root, width=75)
write_loc_text_entry.insert(END, '/Users/stephanie/Desktop/OT2_Protocols')
#write_loc_text_entry.insert(END, '/Users/cstone/Desktop/SarahTest') # LOCAL TESTING

file_name_text_entry = Entry(root, width=75)
file_name_text_entry.insert(END, "Protocol1")

# Drop down boxes 
drop1_loc = StringVar()  # set variable type
drop2_loc = StringVar()
drop3_loc = StringVar()
drop4_loc = StringVar()
drop5_loc = StringVar()

drop1_loc.set(None)  # set default value
drop2_loc.set(None)
drop3_loc.set(None)
drop4_loc.set(None)
drop5_loc.set(None)

drop1 = OptionMenu(root, drop1_loc, None,2,3,4,5,6)  # create drop downs
drop2 = OptionMenu(root, drop2_loc, None,2,3,4,5,6)
drop3 = OptionMenu(root, drop3_loc, None,2,3,4,5,6)
drop4 = OptionMenu(root, drop4_loc, None,2,3,4,5,6)
drop5 = OptionMenu(root, drop5_loc, None,2,3,4,5,6)



# *HELPER METHODS ---------------------------------------------------------------------------
def browse_csv_click(browse_text_entry): 
    csv_filename = filedialog.askopenfile(title = "Select File",filetypes = (("CSV Files","*.csv"),))
    browse_text_entry.delete(0,"end")
    browse_text_entry.insert(0, csv_filename.name)

def browse_folder_click(browse_text_entry): 
    output_folder = filedialog.askdirectory(title="Select Folder")  # todo: add a default folfer opening location
    browse_text_entry.delete(0,"end")
    browse_text_entry.insert(0, output_folder)

def check_box_click(box1, box2): 
    if box1: 
        print("box 1 is checked")
    if box2:
        print("box 2 is checked")

# *GENERATE PROTOCOL METHOD -----------------------------------------------------------------
def generate_button_click(): 
    global output_label
    global deck_info_label
    output_label.destroy()  # destroy the old output label 
    deck_info_label.destroy()

    output_label = Label(root, text="")  # instantiate new output label 
    deck_info_label = Label(root, text="", anchor=W)  # instantiate new deck information label
    is_error = False 
    info_text = ""
    error_text = ""
    deck_text= ""
    final_csv_list = []

    # extract deck locations from drop downs
    deck_locs = []
    verified_deck_locs = []
    repeats = False
    deck_locs.append(drop1_loc.get())
    deck_locs.append(drop2_loc.get())
    deck_locs.append(drop3_loc.get())
    deck_locs.append(drop4_loc.get())
    deck_locs.append(drop5_loc.get())

    # ensure no repeated deck locations
    for i in range(len(deck_locs)): 
        if not deck_locs[i] == "None":  
            if len(verified_deck_locs) == 0: 
                verified_deck_locs.append(deck_locs[i])
            else: 
                if not deck_locs[i] in verified_deck_locs: 
                    verified_deck_locs.append(deck_locs[i])
                else: 
                    repeats=True

    if repeats: 
        is_error = True
        error_text += "\nError: Please use a different deck location for each csv"

    # extract plate types from radio buttons
    plate_types = []
    plate_types.append(plate1_type.get())
    plate_types.append(plate2_type.get())
    plate_types.append(plate3_type.get())
    plate_types.append(plate4_type.get())
    plate_types.append(plate5_type.get())

    # extract all csv filenames from text entry boxes
    csv_filenames = []
    num_csv = 0
    csv_filenames.append(source1_text_entry.get())
    csv_filenames.append(source2_text_entry.get())
    csv_filenames.append(source3_text_entry.get())
    csv_filenames.append(source4_text_entry.get())
    csv_filenames.append(source5_text_entry.get())

    # check which entries are csv files
    for i in range(0,5):
        if csv_filenames[i]: 
            csv_filenames[i] = csv_filenames[i].strip()
            if len(csv_filenames[i]) == 0: 
                csv_filenames[i] = None
        else: 
            csv_filenames[i] = None

    # check csv paths exist
    for i in range(len(csv_filenames)):  
        if csv_filenames[i]: 
            if os.path.exists(csv_filenames[i]): 
                num_csv += 1    
            else: 
                is_error = True
                error_text += f"\npath dees not exist: {csv_filenames[i]}"

            if not is_error: 
                if not deck_locs[i] == "None":
                    csv_tuple = (deck_locs[i], csv_filenames[i], plate_types[i])
                    final_csv_list.append(csv_tuple)   # add to final list if all correct
                else: 
                    is_error = True
                    error_text += f"\n Please enter a deck location for Source {i+1}"

    # check that there are entries in final list 
    if num_csv > 0: 
        info_text += f"\nNumber of CSVs processed = {num_csv}"
    else: 
        is_error = True
        error_text += f"\nNumber of CSVs processed = {num_csv}\nPlease enter a csv file and try again"

    # check that output folder location exists 
    output_loc = (write_loc_text_entry.get()).strip()
    if not os.path.isdir(output_loc): 
        is_error = True
        error_text += "\nOutput Folder path does not exist"

    # check that file name provided could be used to create valid file path # TODO: figure out how to do this
    output_file_name = (file_name_text_entry.get()).strip() + str(".py")

    # check that you won't need more tip boxes than there are alloted tip deck locations
    tips_20 = 0
    tips_300 = 0
    for loc, path, plate_type in final_csv_list:
        df = pd.read_csv(path, encoding='utf-8-sig')
        volumes = []
        for well_volume in df["Volume"]: 
            volumes.append(well_volume)
            # keep count of how many tips needed (20uL vs 300uL)
            if well_volume > 0 and well_volume <= 20: 
                tips_20 += 1
            elif well_volume > 20 and well_volume <= 300: 
                tips_300 += 1
    num_20_tip_boxes = int(tips_20/96)+1 if not tips_20%96 == 0 else int(tips_20/96)
    num_300_tip_boxes = int(tips_300/96)+1 if not tips_300%96 == 0 else int(tips_300/96)
    if num_20_tip_boxes + num_300_tip_boxes > 5: 
        is_error = True
        error_text += f"20uL tip boxes needed: {num_20_tip_boxes}\n300uL tip boxes needed: {num_300_tip_boxes}\n"
        error_text += "\nToo many tip boxes required (only 5 deck locations availible)\nPlease try again with one less csv. Run this pool in batches"


    # Decide whether or not to generate protocol 
    if not is_error: 
        # generate the protocol
        more_info = generate_from_template(
            final_csv_list, num_20_tip_boxes, 
            num_300_tip_boxes, 
            output_loc, 
            output_file_name
        )  

        # format display text 
        deck_text += f"20uL tip boxes needed: {num_20_tip_boxes}\n300uL tip boxes needed: {num_300_tip_boxes}\n"
        deck_text += more_info
        output_label["text"] = info_text 
        deck_info_label["text"] = deck_text

    else: 
        # format display text 
        output_label["text"] = error_text  
        
    # display ouptut label from current click
    output_label.grid(row=10, column=1,pady=3)
    deck_info_label.grid(row=11, column=1, pady=3, padx=3)
    

# Buttons ------------------------------------------------------------------------------------
generate_protocol_button = Button(root, text="Generate Protocol", command=generate_button_click)

browse1 = Button(root, text="Browse", command=lambda:browse_csv_click(source1_text_entry))
browse2 = Button(root, text="Browse", command=lambda:browse_csv_click(source2_text_entry))
browse3 = Button(root, text="Browse", command=lambda:browse_csv_click(source3_text_entry))
browse4 = Button(root, text="Browse", command=lambda:browse_csv_click(source4_text_entry))
browse5 = Button(root, text="Browse", command=lambda:browse_csv_click(source5_text_entry))
write_loc_button = Button(root, text="Browse", command=lambda:browse_folder_click(write_loc_text_entry))

# Check boxes
plate1_type = StringVar()
plate2_type = StringVar()
plate3_type = StringVar()
plate4_type = StringVar()
plate5_type = StringVar()

plate1_type.set('full')  # initialize radio buttons
plate2_type.set('full')
plate3_type.set('full')
plate4_type.set('full')
plate5_type.set('full')

semi1 = Radiobutton(root, text = "semi", variable=plate1_type, value="semi")
full1 = Radiobutton(root, text = "full", variable=plate1_type, value="full")

semi2 = Radiobutton(root, text = "semi", variable=plate2_type, value="semi")
full2 = Radiobutton(root, text = "full", variable=plate2_type, value="full")

semi3 = Radiobutton(root, text = "semi", variable=plate3_type, value="semi")
full3 = Radiobutton(root, text = "full", variable=plate3_type, value="full")

semi4 = Radiobutton(root, text = "semi", variable=plate4_type, value="semi")
full4 = Radiobutton(root, text = "full", variable=plate4_type, value="full")

semi5 = Radiobutton(root, text = "semi", variable=plate5_type, value="semi")
full5 = Radiobutton(root, text = "full", variable=plate5_type, value="full")

# Load labels onto root 
csv_filename_label.grid(row=0, column=1, pady=3)
deck_location_label.grid(row=0, column=3, padx=3, pady=3)
plate_type_label.grid(row=0, column=4, columnspan=2)

source1_label.grid(row=1, column=0)
source2_label.grid(row=2, column=0)
source3_label.grid(row=3, column=0)
source4_label.grid(row=4, column=0)
source5_label.grid(row=5, column=0)

separator.grid(row=6, columnspan=4, sticky=EW, pady=10)

write_loc_label.grid(row=7, column=0)
file_name_label.grid(row=8, column=0, padx=3)

# Load buttons onto root 
generate_protocol_button.grid(row=9, column=1, pady=5) 

browse1.grid(row=1, column=2)
browse2.grid(row=2, column=2)
browse3.grid(row=3, column=2)
browse4.grid(row=4, column=2)
browse5.grid(row=5, column=2)

write_loc_button.grid(row=7, column=2)

# Load text entry boxes onto root
source1_text_entry.grid(row=1, column=1)
source2_text_entry.grid(row=2, column=1)
source3_text_entry.grid(row=3, column=1)
source4_text_entry.grid(row=4, column=1)
source5_text_entry.grid(row=5, column=1)

write_loc_text_entry.grid(row=7, column=1)
file_name_text_entry.grid(row=8, column=1)

# Load drop down boxes onto root
drop1.grid(row=1, column=3)
drop2.grid(row=2, column=3)
drop3.grid(row=3, column=3)
drop4.grid(row=4, column=3)
drop5.grid(row=5, column=3)

# Load check boxes onto root
semi1.grid(row=1, column=4)
full1.grid(row=1, column=5, padx=(0,5))
semi2.grid(row=2, column=4)
full2.grid(row=2, column=5, padx=(0,5))
semi3.grid(row=3, column=4)
full3.grid(row=3, column=5, padx=(0,5))
semi4.grid(row=4, column=4)
full4.grid(row=4, column=5, padx=(0,5))
semi5.grid(row=5, column=4)
full5.grid(row=5, column=5, padx=(0,5))

root.mainloop()

