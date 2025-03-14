# Overview of MIDI DB to MIDI Goblin
This is a utility to convert MIDI definitions from the pencilresearch/midi database into MIDI Goblin device definitions.
## What it can do
- It can process a single .csv MIDI definition, or a directory of them
- It creates the file and folder structure for each MIDI definition, which you then copy to the MIDI Goblin microSD card
- It processes the name of the parameter to shorten it to 14 characters and remove invalid characters
- If there is a duplicate parameter name, you will be prompted to enter a replacement name
  - Please note some definitions may mean you have to enter *lots* of replacement names...
## What it doesn't do
- It doesn't check to see if there are duplicate definitions (e.g. 2 controls with the same CC); it assumes the provided definition is correct
## What's planned
- Option to remove spaces from parameter names to shorten them
- Option to use a .txt file of term abbreviations (e.g. Oscillator:Osc)
# Using MIDI DB to MIDI Goblin
## For single files
Run `python MidiDefToGoblin.py -f YourMIDIDefinition.csv`
## For a directory of files
Run `python MidiDefToGoblin.py -d ./Path/To/MIDIFiles`