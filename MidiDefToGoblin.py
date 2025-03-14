import argparse # for command-line argument handling for thescript 
import os   # for directory operations
import csv  # to simplify creating csv files
import re # for regex

# file constants
abbreviationsFile = "./Abbreviations.csv"

# enumerations based on MIDI DB template definition
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

def processDefinition(inputFile,noSpaces):
    print("=============================")
    print("Processing ",inputFile,"...\n")

    midiArray = loadCsv(inputFile)

# Choose to use abbreviations
    abbreviationsArray = loadCsv(abbreviationsFile)
    midiArray = applyAbbreviations(midiArray,abbreviationsArray)

    deduplicateParameterNames(midiArray,noSpaces)
    synthName = cleanParameterName(midiArray[1][device]).replace(" ","_")

    createFolderStructure(synthName)
    createPanelFile(synthName)

    createMGDefinition(midiArray,synthName,noSpaces)
    print("Finished making MIDI Goblin folder for "+synthName)


def createFolderStructure(synthName):
    createFolder("./"+synthName)
    createFolder("./"+synthName+"/"+"PATCHES")
    createFolder("./"+synthName+"/"+"CONFIG")
    createFolder("./"+synthName+"/"+"REMAPS")

def createPanelFile(synthName):
    file_path = "./"+synthName+"/"+"PATCHES"+"/PANEL.txt"
    with open(file_path, 'w') as file:
        print("")

def loadCsv(inputFile):    
    if os.path.isfile(inputFile) and ".csv" in inputFile:
        myFile = open(inputFile, encoding='utf8')
    else:
        print("Not a valid file for processing: " + inputFile)
        quit()

    # Load csv file into an array
    with open(inputFile, newline='') as csvfile:
        midiDefinition = csv.reader(csvfile, delimiter=',', quotechar='|')
        midiArray = list(midiDefinition)

    return midiArray

def applyAbbreviations(targetArray,abbreviationsArray):
    for item in targetArray:
        for abbreviation in abbreviationsArray:
            item[parameter_name] = re.sub(r'(?i)'+abbreviation[0],abbreviation[1],item[parameter_name])
    return targetArray

def cleanParameterName(parameterName,noSpaces=False):
    # Removes characters that aren't alphanumeric or underscore, replaces spaces with underscore, and shortens name to 14 characters spaces
    if noSpaces:
        newName = re.sub('[ ]+', '', parameterName) # Removes spaces
    else:    
        newName = re.sub('[ ]+', '_', parameterName) # Changes spaces to underscore

    newName = re.sub('[^0-9a-zA-Z_]+', '', newName) # Get rid of invalid characters
    newName = newName[:14]
    return newName

def deduplicateParameterNames(midiArray,noSpaces):
    parNames = []

    for i in range(1, len(midiArray)-1):
        newName = cleanParameterName(midiArray[i][parameter_name],noSpaces)
        while newName in parNames:
            print("---------------------------------------")
            print("\nThere is already a parameter called\n     ",newName)
            print("Enter a different name to use for the \n     ",midiArray[i][parameter_name],"\n parameter.")
            newName = input("> ")
            cleanParameterName(newName,noSpaces)
        parNames.append(newName)
        midiArray[i][parameter_name] = newName
       
def createFolder(directory_name):
    try:
        os.mkdir(directory_name)
        print(f"Directory '{directory_name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_name}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{directory_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")


def createMGDefinition(midiArray,synthName,noSpaces=False):
    # Create MIDI Goblin definition arrays
    file_path = "./"+synthName+"/"+"CONFIG"+"/MIDI_INFO.txt"
    with open(file_path, 'w') as file:
        for i in range(1,len(midiArray)-1):
            if midiArray[i][manufacturer] != "manufacturer":
                if midiArray[i][cc_msb] != "": # prioritize processing controls for CC over NRPN
                    file.write("CC "+cleanParameterName(midiArray[i][parameter_name],noSpaces)+" "+midiArray[i][cc_msb]+"\n")
                elif midiArray[i][nrpn_msb] != "": # process if there's an NRPN value, but no CC value
                    file.write("NRPN "+cleanParameterName(midiArray[i][parameter_name],noSpaces)+" "+midiArray[i][nrpn_msb]+" "+midiArray[i][nrpn_lsb]+"\n")

# ========MAIN CODE===========================

if __name__ == "__main__":

    # Handle command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", metavar="FILE", help="Process a single file")
    parser.add_argument("-d", metavar="DIRECTORY", help="Process an entire directory of files")
    parser.add_argument("-nospaces", action='store_true', help="Removes spaces from parameter names")

    args = parser.parse_args()


    if args.d != None and args.f != None:
        print("")
        print("Please use the -f file option or the -d directory option, not both.")
        print("")
    else:
        if args.d != None:
            print("Processing a directory")
            if os.path.isdir(args.d):
                for inputFile in os.listdir(args.d): # Loop through all files in directory
                    processDefinition(args.d + "\\" + inputFile,args.nospaces)
            else:
                print("Invalid directory")

        elif args.f != None:
            if os.path.isfile(args.f):
                processDefinition(args.f,args.nospaces)
            else:
                print("Invalid file")

        else: # If no flags or invalid flags entered, show help
            print("Use the following syntax to run the MIDI to MIDI Goblin utility:")
            print("")
            print("To process a single file:")
            print("python MidiDefToGoblin.py -f FILETOPROCESS.csv")
            print("")
            print("To process all files in a directory:")
            print("python MidiDefToGoblin.py -d /PATHTODIRECTORY/")
            print("")
            print("Adding -nospaces will remove spaces from parameter names")
