"""
Outline
-------

Characters must be generated multiple at once (to prevent duplicate items etc. across characters)
Stats can be 1d20//2 then +/- incrementally from other characters

make text files with all the random things to choose from:
read said text files, splitlines to get choices based on random

characters as classes
"""
file_paths = {
    'Standard Equipment' : '',
    'Silly Equipment' : '',
    'Service Group' : '',
    'Mutant Powers' : '',
    'Secret Societies' : '',
    'Secret Skills' : '',
    'Character Quirks' : '',
    }


equip_file = open('sillyequipment.txt','r')
equips = equip_file.read()

print(equips.splitlines())