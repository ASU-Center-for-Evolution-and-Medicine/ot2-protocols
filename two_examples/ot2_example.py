from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'OT-2 code example',
    'author': 'Name <email@address.com>',
    'description': 'ot2 code example',
    'apiLevel': '2.12'  # apiLevel is the only part of the metadata that matters
}

def run(protocol: protocol_api.ProtocolContext):   # must have a run method if executing the protocol with opentrons_execute (from opentrons package)

    #* Load items onto deck
    #labware
    plate1 = protocol.load_labware('corning_96_wellplate_360ul_flat', '1')  # (plate_type, deck_location)
    plate2 = protocol.load_labware('corning_96_wellplate_360ul_flat', '2')

    # tip racks
    tiprack1 = protocol.load_labware('opentrons_96_tiprack_300uL', '4')   # 300 uL tip rack at position 4
    tiprack2 = protocol.load_labware('opentrons_96_tiprack_300uL', '5')   # 300 uL tip rack at position 5
    tiprack3 = protocol.load_labware('opentrons_96_tiprack_1000uL', '6')  # 1000 uL tip rack at position 6

    # pipettes
    pipette_300uL_multi = protocol.load_instrument('p300_multi_gen2', 'right', tip_racks=[tiprack1, tiprack2])  # (pipette_type, location, availible_tip_racks)
    pipette_1000uL_single = protocol.load_instrument('p1000_single_gen2', 'left', tip_racks=[tiprack3])  

    #* Other protocol variables
    transfer_volume = 150

    #* Protocol Commands
    #Transfer 150uL from each well in plate1 to each well in plate2 (using an 8 channel pipette)
    for column in plate1.columns_by_name(): 
        top_well = f"A{column}"  # there should be an easier way to do this but it wasn't working for me
        pipette_300uL_multi.pick_up_tip()
        pipette_300uL_multi.aspirate(transfer_volume, plate1[top_well])
        pipette_300uL_multi.dispense(transfer_volume, plate2[top_well])
        pipette_300uL_multi.drop_tip()

    # Transfer 150uL from each well in plate2 to each well in plate1 (using a single pipette channel)
    pipette_1000uL_single.pick_up_tip()
    for well in plate2.wells_by_name(): 
        pipette_1000uL_single.aspirate(transfer_volume, plate2[well])
        pipette_1000uL_single.dispense(transfer_volume, plate1[well])
    pipette_1000uL_single.drop_tip()




