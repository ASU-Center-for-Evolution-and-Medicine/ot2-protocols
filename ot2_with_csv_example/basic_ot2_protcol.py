from opentrons import protocol_api

# metadata
metadata = {
    "protocolName": "50 test one",
    "author": "Name <opentrons@example.com>",
    "description": "Simple protocol to get started using the Flex",
}

# requirements
requirements = {"robotType": "OT-2", "apiLevel": "2.14"}

# protocol run function
def run(protocol: protocol_api.ProtocolContext):
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
        "p300_single_gen2", mount="left", tip_racks=[tiprack]
    )

    # commands
    left_pipette.well_bottom_clearance.aspirate = 2
       
    left_pipette.pick_up_tip()
    left_pipette.aspirate(50, plate1["A1"])
    left_pipette.dispense(50, plate2["A2"])
    left_pipette.drop_tip()

    left_pipette.pick_up_tip()
    left_pipette.aspirate(50, plate1["C4"])
    left_pipette.dispense(50, plate2["C5"])
    left_pipette.drop_tip()

    left_pipette.pick_up_tip()
    left_pipette.aspirate(50, plate1["E8"])
    left_pipette.dispense(50, plate2["E9"])
    left_pipette.drop_tip()



