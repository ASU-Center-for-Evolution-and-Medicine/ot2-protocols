from tkinter import *
from tkinter import filedialog

root = Tk()
root.title("Generate Transfer Protocol")

# Labels
csv_filename_label = Label(root, text="CSV FILENAME")
deck_location_label = Label(root, text="DECK LOCATION")

source1_label = Label(root, text="Source 1: ")
source2_label = Label(root, text="Source 2: ")
source3_label = Label(root, text="Source 3: ")
source4_label = Label(root, text="Source 4: ")
source5_label = Label(root, text="Source 5: ")

# Text Entry Boxes
source1_text_entry = Entry(root, width=75)
source2_text_entry = Entry(root, width=75)
source3_text_entry = Entry(root, width=75)
source4_text_entry = Entry(root, width=75)
source5_text_entry = Entry(root, width=75)

# Drop down boxes 
drop1_loc = StringVar()
drop2_loc = StringVar()
drop3_loc = StringVar()
drop4_loc = StringVar()
drop5_loc = StringVar()

drop1_loc.set(None)
drop2_loc.set(None)
drop3_loc.set(None)
drop4_loc.set(None)
drop5_loc.set(None)

drop1 = OptionMenu(root, drop1_loc, None,2,3,4,5,6)
drop2 = OptionMenu(root, drop2_loc, None,2,3,4,5,6)
drop3 = OptionMenu(root, drop3_loc, None,2,3,4,5,6)
drop4 = OptionMenu(root, drop4_loc, None,2,3,4,5,6)
drop5 = OptionMenu(root, drop5_loc, None,2,3,4,5,6)


#METHODS 
def browse_click(browse_text_entry): 

    csv_filename = filedialog.askopenfile(title = "Select file",filetypes = (("CSV Files","*.csv"),))

    browse_text_entry.delete(0,"end")
    browse_text_entry.insert(0, csv_filename.name)

def generate_button_click():
    output_info_text = ""
    output_error_text = ""
    is_error = False

    # test section!
    
    # extract all deck locations from drop down boxes

    deck_locs = []
    verified_deck_locs = []
    repeats = False
    deck_locs.append(drop1_loc.get())
    deck_locs.append(drop2_loc.get())
    deck_locs.append(drop3_loc.get())
    deck_locs.append(drop4_loc.get())
    deck_locs.append(drop5_loc.get())

    for i in range(len(deck_locs)): 
        if not deck_locs[i] == "None":  
            if len(verified_deck_locs) == 0: 
                verified_deck_locs.append(deck_locs[i])
            else: 
                if not deck_locs[i] in verified_deck_locs: 
                    verified_deck_locs.append(deck_locs[i])
                else: 
                    repeats=True
    print(deck_locs)
    print(verified_deck_locs)
    
    if repeats: 
        is_error = True
        output_error_text = "Error: Please use a different deck location for each csv"
    



    

    


    



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
                

                num_csv += 1
        else: 
            csv_filenames[i] = None

    output_info_text += f"\nNumber of CSVs processed = {num_csv}"

    generate_error_label = Label(root, text=output_error_text)
    generate_info_label = Label(root, text=output_info_text)

    if is_error: 
        generate_error_label.grid(row=7, column=1, sticky=W)
    else: 
        generate_info_label.grid(row=7, column=1, sticky=W)

    
    
    #print(f"Source {i+1}: {csv_filenames[i]}")
         



    # check that the input is correct



    # pass to template to make the protocol 



    # output the location of the generated protoco (and instructions how to use it? )





# Buttons
generate_protocol_button = Button(root, text="Generate Protocol", command=generate_button_click)

browse1 = Button(root, text="Browse", command=lambda:browse_click(source1_text_entry))
browse2 = Button(root, text="Browse", command=lambda:browse_click(source2_text_entry))
browse3 = Button(root, text="Browse", command=lambda:browse_click(source3_text_entry))
browse4 = Button(root, text="Browse", command=lambda:browse_click(source4_text_entry))
browse5 = Button(root, text="Browse", command=lambda:browse_click(source5_text_entry))


# Load labels onto root 
csv_filename_label.grid(row=0, column=1)
deck_location_label.grid(row=0, column=3)

source1_label.grid(row=1, column=0)
source2_label.grid(row=2, column=0)
source3_label.grid(row=3, column=0)
source4_label.grid(row=4, column=0)
source5_label.grid(row=5, column=0)

# Load buttons onto root 
generate_protocol_button.grid(row=6, column=1) 

browse1.grid(row=1, column=2)
browse2.grid(row=2, column=2)
browse3.grid(row=3, column=2)
browse4.grid(row=4, column=2)
browse5.grid(row=5, column=2)

# Load text entry boxes onto root
source1_text_entry.grid(row=1, column=1)
source2_text_entry.grid(row=2, column=1)
source3_text_entry.grid(row=3, column=1)
source4_text_entry.grid(row=4, column=1)
source5_text_entry.grid(row=5, column=1)

# Load drop down boxes onto root
drop1.grid(row=1, column=3)
drop2.grid(row=2, column=3)
drop3.grid(row=3, column=3)
drop4.grid(row=4, column=3)
drop5.grid(row=5, column=3)

root.mainloop()

