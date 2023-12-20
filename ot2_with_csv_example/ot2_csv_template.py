### start  ------------------------------------------------------------------------------------------------------
import pandas as pd
from opentrons import protocol_api, simulate, execute

# metadata
metadata = {
    "protocolName": "OT-2 with csv input test",
    "author": "Casey Stone <opentrons@example.com>",
    "description": "Simple protocol to demonstrate using ot-2 protocols with csv input",
}

requirements = {"robotType": "OT-2", "apiLevel": "2.14"}

### end

### VAR  <--- DO NOT DELETE THIS

### start

def run(protocol):
        # labware
    plate1 = protocol.load_labware(
        "corning_96_wellplate_360ul_flat", location="6"
    )
    plate2 = protocol.load_labware(
        "corning_96_wellplate_360ul_flat", location="3"
    )

    tiprack = protocol.load_labware(
        "opentrons_96_tiprack_300ul", location="9"
    )

    # pipettes
    left_pipette = protocol.load_instrument(
        "p300_multi_gen2", mount="left", tip_racks=[tiprack]
    )

    # commands
    left_pipette.well_bottom_clearance.aspirate = 2

    for i in range(len(source_wells)): 
        left_pipette.pick_up_tip()
        left_pipette.aspirate(transf_volumes[i], plate1[source_wells[i]])
        left_pipette.dispense(transf_volumes[i], plate2[dest_wells[i]])
        left_pipette.drop_tip()

### end