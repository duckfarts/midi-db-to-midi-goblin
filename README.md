# Overview of MIDI DB to MIDI Goblin
This is a utility to convert .csv MIDI definitions from the [pencilresearch/midi MIDI CC & NRPN Database](https://github.com/pencilresearch/midi) into [MIDI Goblin](https://www.midigoblin.com/) `MIDI_INFO.txt` files already placed in synth definition folders you can copy to its microSD card.

This means you can create definitions without having to manually enter all the parameter names and CC/NRPN values. If the database doesn't have your synth in it, consider helping out and [contributing](https://github.com/pencilresearch/midi#contributing) to the database!

**Note:** There is no warranty for using this utility, and I can't guarantee it won't break your PC or MIDI Goblin somehow. Have fun!

## What it does
- Processes a single .csv MIDI definition, or a directory of them
- Cleans parameter names (up to 14 alphanumeric characters, only `-` and `_` symbols allowed)
- If there is a duplicate parameter name, prompts you for a replacement name
- Uses the `Abbreviations.csv` file to auto-abbreviate parameter names to help them fit in the 14 character limit

## What it doesn't do
- It doesn't check to see if there are duplicate CC/NRPN definitions (e.g. 2 controls with the same CC)
    - It assumes the provided definition is correct
    - Keep in mind that some devices may use the same CC to control different things, depending on the mode the device is in
- Your laundry
## Other notes
- I've only tested this in Windows, but I *think* the script should work in other environments
- Feel free to submit an issue or pull request, but keep in mind I barely know what I'm doing in Github

# Using MIDI DB to MIDI Goblin
## Before you get started
- Download the .csv MIDI definitions you want to use from the [pencilresearch/midi repo](https://github.com/pencilresearch/midi)
### Windows users
- Download the files for Windows from the [Releases](https://github.com/duckfarts/midi-db-to-midi-goblin/releases) page
### Everybody else, or if the exe doesn't work
- Download the files for Python from the [Releases](https://github.com/duckfarts/midi-db-to-midi-goblin/releases) page
- Make sure you have Python installed (I like using [Chocolatey](https://chocolatey.org/) to handle this in Windows)
## Running the utility
### Command line options
- `-f YOURFILE.csv` runs the script on a single .csv MIDI definition
- `-d /Path/To/MIDIDefinitions` runs the script on a directory of .csv MIDI definitions
- `-nospaces` will remove spaces from parameter names, which helps bring some names under the 14 character limit
### Examples
#### Using the exe file in Windows
- `MidiDefToGoblin -f YourMIDIDefinition.csv`
- `MidiDefToGoblin -d ./Path/To/MIDIFiles -nospaces`
#### Running the script using Python
- `python MidiDefToGoblin.py -f YourMIDIDefinition.csv`
- `python MidiDefToGoblin.py -d ./Path/To/MIDIFiles -nospaces`

## After running the script
- You can preview and edit the MIDI Goblin definition files, which are in `YOURSYNTHNAME/CONFIG/MIDI_INFO.txt` for each synth
    - Keep in mind that when editing the file, parameter names are alphanumeric only, can't have spaces or symbols other than `-` and `_`, and need to be 14 characters or less
- If you don't like how parameter names are shortened, feel free to edit the `Abbreviations.csv` file however you want
- Copy the synth folders to your MIDI Goblin microSD card's root folder
    - To get to the microSD card, remove the screws on the bottom of the device and lift off the plate