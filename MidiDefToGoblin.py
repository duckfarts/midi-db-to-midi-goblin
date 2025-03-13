import csv

# Run the application
if __name__ == "__main__":

# enumerations
    manufacturer = 0
    device = 1
    section = 2
    parameter_name = 3
    parameter_description = 4
    cc_msb = 5
    cc_lsb = 6
    cc_min_value = 7
    cc_max_value = 8
    nrpn_msb = 9
    nrpn_lsb = 10
    nrpn_min_value = 11
    nrpn_max_value = 12
    orientation = 13
    notes = 14
    usage = 15

    # Load csv file into an array
    with open('./Elektron/Digitakt II.csv', newline='') as csvfile:
        midiDefinition = csv.reader(csvfile, delimiter=',', quotechar='|')
        midiArray = list(midiDefinition)

    # Create MIDI Goblin definition
    for midiControl in midiArray:
        if midiControl[manufacturer] != "manufacturer":
            if midiControl[cc_msb] != "": # prioritize processing controls for CC over NRPN
                print("CC",midiControl[parameter_name][:14],midiControl[cc_msb])
            elif midiContro[nrpn_msb] != "": # process if there's an NRPN value, but no CC value
                print("NRPN",midiControl[parameter_name][:14],midiControl[nrpn_msb],midiControl[nrpn_lsb])

