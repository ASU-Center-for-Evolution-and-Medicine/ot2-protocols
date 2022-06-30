from liquidhandling import SoloSoft, SoftLinx
from liquidhandling import Plate_96_Corning_3635_ClearUVAssay

#* variables
transfer_volume = 150
default_z_height = 2
hso_count = 0
all_hso_files = []

# ------------------------------------------------------------------------------------------------------------------------------------------
#* Transfer 150uL from each well in plate 1 to each well in plate 2 (multi-channel transfer, new tips each time)
soloSoft = SoloSoft(
    filename=f"C:\\Users\\svcaibio\\Desktop\\Debug\\hudson_example_{hso_count}.hso",
    plateList=[
        "TipBox.50uL.Axygen-EV-50-R-S.tealbox",     # Deck position 1 = 50uL tip box
        "Empty",                                    # Deck position 2 = empty
        "TipBox.180uL.Axygen-EVF-180-R-S.bluebox",  # Deck position 3 = 180 uL tip box
        "Plate.96.Corning-3635.ClearUVAssay",       # Deck position 4 = flat bottom 96 well plate
        "Empty",                                    # Deck position 5 = empty 
        "Plate.96.Corning-3635.ClearUVAssay",       # Deck position 6 = flat bottom 96 well plate
        "TipBox.180uL.Axygen-EVF-180-R-S.bluebox",  # Deck position 7 = 180 uL tip box
        "Empty",                                    # Deck position 8 = empty 
    ],
)

for column in range(1,13):
    soloSoft.getTip(position="Position3")
    soloSoft.aspirate(
        position="Position4",
        aspirate_volumes=Plate_96_Corning_3635_ClearUVAssay().setColumn(column, transfer_volume),
        aspirate_shift = [0,0,default_z_height],
    )
    soloSoft.dispense(
        position="Position6",
        dispense_volumes=Plate_96_Corning_3635_ClearUVAssay().setColumn(column, transfer_volume),
        dispense_shift = [0,0,default_z_height]
    )
    soloSoft.shuckTip()
soloSoft.savePipeline()
all_hso_files.append(f"C:\\Users\\svcaibio\\Desktop\\Debug\\hudson_example_{hso_count}.hso")


# ------------------------------------------------------------------------------------------------------------------------------------------
#* Transfer 150uL from each well in plate 2 to each well in plate 1 (single-channel transfer, use the same tip for all transfers in the same row)

rows = ["A", "B", "C", "D", "E", "F", "G", "H"]
for row in rows:
    hso_count += 1

    # need to have a new hso file per row in this case to prevent going over the 72 step limit in soloSoft
    soloSoft = SoloSoft(
        filename=f"C:\\Users\\svcaibio\\Desktop\\Debug\\hudson_example_{hso_count}.hso",
        plateList=[
            "TipBox.50uL.Axygen-EV-50-R-S.tealbox",     # Deck position 1 = 50uL tip box
            "Empty",                                    # Deck position 2 = empty
            "TipBox.180uL.Axygen-EVF-180-R-S.bluebox",  # Deck position 3 = 180 uL tip box
            "Plate.96.Corning-3635.ClearUVAssay",       # Deck position 4 = flat bottom 96 well plate
            "Empty",                                    # Deck position 5 = empty 
            "Plate.96.Corning-3635.ClearUVAssay",       # Deck position 6 = flat bottom 96 well plate
            "TipBox.180uL.Axygen-EVF-180-R-S.bluebox",  # Deck position 7 = 180 uL tip box
            "Empty",                                    # Deck position 8 = empty 
        ],
    )

    soloSoft.getTip(position="Position3", num_tips=1)
    for column in range(1,13):
        soloSoft.aspirate(
            position="Position6",
            aspirate_volumes=Plate_96_Corning_3635_ClearUVAssay().setCell(row, column, transfer_volume),
            aspirate_shift=[0,0,default_z_height],
        )
        soloSoft.dispense(
            position="Position4",
            dispense_volumes=Plate_96_Corning_3635_ClearUVAssay().setCell(row, column, transfer_volume),
            dispense_shift=[0,0,default_z_height]
        )

    soloSoft.shuckTip()
    soloSoft.savePipeline()
    all_hso_files.append(f"C:\\Users\\svcaibio\\Desktop\\Debug\\hudson_example_{hso_count}.hso")


# ------------------------------------------------------------------------------------------------------------------------------------------
#* Collect all hso files into SoftLinx and create .slvp file
softLinx = SoftLinx("Hudson Example", "C:\\Users\\svcaibio\\Desktop\\Debug\\hudson_exampe.slvp")  # specify output .slvp file name
softLinx.setPlates({"SoftLinx.Solo.Position4":"Plate.96.Corning-3635.ClearUVAssay"})   # define starting plate layout, just as an example

# reset tip counts
softLinx.soloSoftResetTipCount(3)  # tips at position 3
softLinx.soloSoftResetTipCount(7)  # tips at position 7

# add all SoloSoft .hso files to SoftLinx .slvp file
for hso_file in all_hso_files:
    softLinx.soloSoftRun(hso_file)

# create output SoftLinx .slvp file
softLinx.saveProtocol()
