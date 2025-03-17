#!/usr/bin/env python3
import time

from nicegui import ui, events

import argparse # for command-line argument handling for thescript 
import os   # for directory operations
import csv  # to simplify creating csv files
import re # for regex

# file constants
abbreviationsFile = "./Abbreviations.csv"
testFile = "./midi-main/Roland/S-1.csv"

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

# table definition
columns = [
    {'name': 'type', 'label': 'Type', 'field': 'type','sortable': True, 'required': True},
    {'name': 'paramNameFull', 'label': 'Parameter Name (Full)', 'field': 'paramNameFull', 'sortable': True,'required': True},
    {'name': 'paramNameClean', 'label': 'Parameter Name (Cleaned)', 'field': 'paramNameClean', 'sortable': True,'required': True},
    {'name': 'cc', 'label': 'CC', 'field': 'cc', 'sortable': True},
    {'name': 'nrpnLsb', 'label': 'NRPN LSB', 'field': 'nrpnLsb', 'sortable': True,'required': True},
    {'name': 'nrpnMsb', 'label': 'NRPN MSB', 'field': 'nrpnMsb', 'sortable': True,'required': True},
]

column_defaults = {'align':'center'}

type_options = ['CC','NRPN']

rows = []

class MidiControl:
    def __init__(self, id, paramNameFull, type, cc, nrpnMsb, nrpnLsb):
        self.id = id
        self.paramNameFull = paramNameFull
        self.paramNameClean = cleanParameterName(paramNameFull)
        self.type = type
        self.cc = cc
        self.nrpnMsb = nrpnMsb
        self.nrpnLsb = nrpnLsb

    def __str__(self):
        if self.type == "CC":
            return f"{self.type} {self.paramNameClean} {self.cc}"
        elif self.type == "NRPN":
            return f"{self.type} {self.paramNameClean} {self.nrpnMsb} {self.nrpnMsb}"
        else:
            return False


def launchUI(synthName,controlList):

    # Add all controls to table
    rows = []
    for control in controlList:
        rows.append({'id':control.id,'type':control.type,'paramNameFull':control.paramNameFull, 'paramNameClean':control.paramNameClean,'cc':control.cc,'nrpnMsb':control.nrpnMsb,'nrpnLsb':control.nrpnLsb})


    """
    with ui.table(title=synthName, columns=columns, rows=rows, selection='multiple', column_defaults=column_defaults).classes('w-full') as table: # the w-NUMBER sets the width, maybe?
        with table.add_slot('top-right'):
            with ui.input(placeholder='Search').props('type=search').bind_value(table, 'filter').add_slot('append'):
                ui.icon('search')
        
        with table.add_slot('bottom-row'):
            with table.row():
                with table.cell():
                    ui.button(on_click=lambda: (
                        table.add_row({'id': time.time(), 'type': new_type.value, 'paramName': new_paramName.value, 'cc': new_cc.value, 'nrpnMsb': new_nrpnMsb.value, 'nrpnLsb': new_nrpnLsb.value}),
                        new_type.set_value(None),
                        new_paramName.set_value(None),
                        new_cc.set_value(None),
                        new_nrpnMsb.set_value(None),
                        new_nrpnLsb.set_value(None),
                    ), icon='add').props('flat fab-mini')
                with table.cell():
                    new_type = ui.input('Type')
                with table.cell():
                    new_paramName = ui.input('Parameter Name')
                with table.cell():
                    new_cc = ui.number("CC")
                with table.cell():
                    new_nrpnMsb = ui.number("NRPN MSB")
                with table.cell():
                    new_nrpnLsb = ui.number("NRPN LSB")



    ui.label().bind_text_from(table, 'selected', lambda val: f'Current selection: {val}')
    ui.button('Remove', on_click=lambda: table.remove_rows(table.selected)) \
        .bind_visibility_from(table, 'selected', backward=lambda val: bool(val))
    """


    def add_row() -> None:
        new_id = max((dx['id'] for dx in rows), default=-1) + 1
        rows.append({'id':new_id,'type':"",'paramNameFull':"", 'paramNameClean':"",'cc':"",'nrpnMsb':"",'nrpnLsb':""})
        ui.notify(f'Added new row with ID {new_id}')
        table.update()


    def rename(e: events.GenericEventArguments) -> None:
        for row in rows:
            if row['id'] == e.args['id']:
                row.update(e.args)
        ui.notify(f'Updated rows to: {table.rows}')
        table.update()


    def delete(e: events.GenericEventArguments) -> None:
        rows[:] = [row for row in rows if row['id'] != e.args['id']]
        ui.notify(f'Deleted row with ID {e.args["id"]}')
        table.update()



    table = ui.table(title=synthName, columns=columns, rows=rows, column_defaults=column_defaults, row_key='id').classes('w-full')

    table.add_slot('body', r'''
        <q-tr :props="props">
            <q-td key="id" :props="props">
                {{ props.row.id }}
                <q-popup-edit v-model="props.row.id" v-slot="scope"
                    @update:model-value="() => $parent.$emit('rename', props.row)"
                >
                    <q-input v-model.number="scope.value" type="number" dense autofocus counter @keyup.enter="scope.set" />
                </q-popup-edit>
            </q-td>
            <q-td key="type" :props="props">
                {{ props.row.type }}
                <q-popup-edit v-model="props.row.type" v-slot="scope"
                    @update:model-value="() => $parent.$emit('rename', props.row)"
                >
                    <q-input v-model="scope.value" dense autofocus counter @keyup.enter="scope.set" />
                </q-popup-edit>
            </q-td>
            <q-td key="paramNameFull" :props="props">
                {{ props.row.paramNameFull }}
                <q-popup-edit v-model="props.row.paramNameFull" v-slot="scope"
                    @update:model-value="() => $parent.$emit('rename', props.row)"
                >
                    <q-input v-model="scope.value" dense autofocus counter @keyup.enter="scope.set" />
                </q-popup-edit>
            </q-td>
            <q-td key="paramNameClean" :props="props">
                {{ props.row.paramNameClean }}
                <q-popup-edit v-model="props.row.paramNameClean" v-slot="scope"
                    @update:model-value="() => $parent.$emit('rename', props.row)"
                >
                    <q-input v-model="scope.value" dense autofocus counter @keyup.enter="scope.set" />
                </q-popup-edit>
            </q-td>
            <q-td key="cc" :props="props">
                {{ props.row.cc }}
                <q-popup-edit v-model="props.row.cc" v-slot="scope"
                    @update:model-value="() => $parent.$emit('rename', props.row)"
                >
                    <q-input v-model.number="scope.value" type="number" dense autofocus counter @keyup.enter="scope.set" />
                </q-popup-edit>
            </q-td>
            <q-td key="nrpnMsb" :props="props">
                {{ props.row.nrpnMsb }}
                <q-popup-edit v-model="props.row.nrpnMsb" v-slot="scope"
                    @update:model-value="() => $parent.$emit('rename', props.row)"
                >
                    <q-input v-model.number="scope.value" type="number" dense autofocus counter @keyup.enter="scope.set" />
                </q-popup-edit>
            </q-td>
            <q-td key="nrpnLsb" :props="props">
                {{ props.row.nrpnLsb }}
                <q-popup-edit v-model="props.row.nrpnLsb" v-slot="scope"
                    @update:model-value="() => $parent.$emit('rename', props.row)"
                >
                    <q-input v-model.number="scope.value" type="number" dense autofocus counter @keyup.enter="scope.set" />
                </q-popup-edit>
            </q-td>
            <q-td auto-width >
                <q-btn size="sm" color="primary" round dense icon="add"
                    @click="() => $parent.$emit('add', props.row)"
                />
            </q-td>
            <q-td auto-width >
                <q-btn size="sm" color="primary" round dense icon="remove"
                    @click="() => $parent.$emit('delete', props.row)"
                />
            </q-td>
            <q-td auto-width >
                <q-btn size="sm" color="deep-orange" round dense icon="delete"
                    @click="() => $parent.$emit('delete', props.row)"
                />
            </q-td>
        </q-tr>
    ''')
    with table.add_slot('bottom-row'):
        with table.cell().props('colspan=9'):
            ui.button('Add row', icon='add', color='accent', on_click=add_row).classes('w-full')

    with table.add_slot('top-right'):
        with ui.input(placeholder='Search').props('type=search').bind_value(table, 'filter').add_slot('append'):
            ui.icon('search')
    table.on('rename', rename)
    table.on('delete', delete)

    ui.run()



def processDefinition(inputFile,noSpaces):
    print("=============================")
    print("Processing ",inputFile,"...\n")

    midiArray = loadCsv(inputFile)

# Choose to use abbreviations
    abbreviationsArray = loadCsv(abbreviationsFile)
    midiArray = applyAbbreviations(midiArray,abbreviationsArray)
    midiArray = midiArray[1:] # Remove first entry, which is the column names

    # deduplicateParameterNames(midiArray,noSpaces)
    synthName = cleanParameterName(midiArray[1][device]).replace(" ","_")

   # createFolderStructure(synthName)
   # createPanelFile(synthName)

    controlList = createControlList(midiArray)

    for control in controlList:
        print(control)
   #  createMGDefinition(midiArray,synthName,noSpaces)
   # print("Finished making MIDI Goblin folder for "+synthName)


    launchUI(synthName, controlList)


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
            if midiArray[i][cc_msb] != "": # prioritize processing controls for CC over NRPN
                file.write("CC "+cleanParameterName(midiArray[i][parameter_name],noSpaces)+" "+midiArray[i][cc_msb]+"\n")
            elif midiArray[i][nrpn_msb] != "": # process if there's an NRPN value, but no CC value
                file.write("NRPN "+cleanParameterName(midiArray[i][parameter_name],noSpaces)+" "+midiArray[i][nrpn_msb]+" "+midiArray[i][nrpn_lsb]+"\n")

def createControlList(midiArray, noSpaces=False):
    controlList = []
    for i in range(len(midiArray)-1):
            if midiArray[i][cc_msb] != "": # prioritize processing controls for CC over NRPN
                controlList.append(MidiControl(i,midiArray[i][parameter_name],"CC",midiArray[i][cc_msb],"",""))
            elif midiArray[i][nrpn_msb] != "": # process if there's an NRPN value, but no CC value
                controlList.append(MidiControl(i,midiArray[i][parameter_name],"NRPN","",midiArray[i][nrpn_msb],midiArray[i][nrpn_lsb]))
    return controlList



# ========MAIN CODE===========================

processDefinition(testFile,False)
  