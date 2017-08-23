# Gregory Gay (greg@greggay.com)
# Generation of random White Wolf RPG character sheets

# Command line options:
# -c <class weight filename>
# CSV, where the first column is clan/class file and the second is percent of total.
# See demo directory for an example.
# If none is given, default Vampire Camirilla clans are used with equal probability.
# -o <output filename>
# File to print output to. If none is given, sheet is printed to screen.
# -t <game type>
# Game type to generate for. Default is Vampire: The Masquerade
# -m <minimum "level">
# Minimum power level for a character (i.e., generation in Vampire).
# Default is 8th generation for Vampire.
# -x <maximum level>
# Maximum power level for a character.
# Default is 13th generation for Vampire.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import getopt
import sys
import os
import random
import copy
from Sheets import *

class Generator(): 
    # System
    system = "vampire"
    # Weights
    weights = []
    # Minimum "level" (i.e., generation for Vampire)
    minLevel = 8
    # Maximum "level"
    maxLevel = 13
    # Character sheet
    sheet = Vampire()

    def generate(self, classWeightFile, outFile):
        if self.system == "vampire":
            self.sheet = Vampire()
            # Intialize the set of available clans and weights
            self.initializeWeights(classWeightFile)
            # Choose a clan
            self.sheet.clan = self.selectClass()
            # Choose disciplines
            self.sheet.disciplines = self.selectDisciplines() 
            # Choose a generation
            self.sheet.generation = self.selectPowerLevel()
            # Choose derangements
            self.sheet.derangements = self.selectDerangements()
            

            # Print to screen and file
            self.sheet.printToScreen()
            if outFile != "":
                self.sheet.printToFile(outFile)
        else:
            raise Exception("System " + self.system+" is not yet supported.")

    # Build set of weights
    def initializeWeights(self, classWeightFile):
        if classWeightFile == "" and self.system == "vampire":
            self.weights.append(["Brujah",14])
            self.weights.append(["Gangrel",14])
            self.weights.append(["Malkavian",14])
            self.weights.append(["Nosferatu",14])
            self.weights.append(["Toreador",15])
            self.weights.append(["Tremere",14])
            self.weights.append(["Ventrue",15])
        else:
            if os.path.isfile(classWeightFile):
                lines = open(classWeightFile, "r")
                for line in lines:
                    if line[:1] != "#":
                        self.weights.append(line.strip().split(","))
                lines.close()
            else:
                raise Exception("File " + classWeightFile + "does not exist")

    # Choose class from weighted list
    def selectClass(self):
        classSelect = []
        for entry in self.weights:
            for index in range(0,int(entry[1])):
                classSelect.append(entry[0])

        # Shuffle the list of classes
        newClassSelect = []
        while len(classSelect) > 0:
            choice = random.randint(0, len(classSelect) - 1)
            newClassSelect.append(classSelect[choice])
            del classSelect[choice]
        classSelect = copy.deepcopy(newClassSelect)

        return classSelect[random.randint(0,len(classSelect) - 1)]
    
    # Select character power level (i.e., generation in Vampire)
    # Power is weighted towards minimal level.
    def selectPowerLevel(self):
        if self.system == "vampire":
            minP = self.maxLevel
            maxP = self.minLevel
        else:
            minP = self.minLevel
            maxP = self.maxLevel

        difference = abs(maxP - minP) + 1
        genSelect = []
        for power in range(1, difference + 1):
             for entry in range(0, difference * power):
                 genSelect.append(maxP)
             
             if self.system == "vampire":
                 maxP+=1
             else:
                 maxP-=1

        return genSelect[random.randint(0,len(genSelect)-1)]

    # Select disciplines
    # This is generally pre-determined by clan, but randomly chooses for Caitiffs/Panders
    def selectDisciplines(self):
        myDisciplines = []

        # Pre-determined disciplines
        if "Assamite" in self.sheet.clan:
            if "Sorcerer" in self.sheet.clan:
                myDisciplines = ["Assamite Sorcery", "Obfuscate", "Quietus"]
            elif "Vizier" in self.sheet.clan:
                myDisciplines = ["Auspex", "Celerity", "Quietus"]
            else:
                myDisciplines = ["Celerity", "Obfuscate", "Quietus"]
        elif "Baali" in self.sheet.clan:
            myDisciplines = ["Daimonion", "Obfuscate", "Presence"]
        elif "Blood Brothers" == self.sheet.clan:
            myDisciplines = ["Fortitude", "Potence", "Sanguinus"]
        elif "Brujah" in self.sheet.clan:
            if "True" in self.sheet.clan:
                myDisciplines = ["Potence", "Presence", "Temporis"]
            else:
                myDisciplines = ["Celerity", "Potence", "Presence"]
        elif "Cappadocian" == self.sheet.clan:
            myDisciplines = ["Auspex", "Fortitude", "Mortis"]
        elif "Daughters of Cacophony" == self.sheet.clan:
            myDisciplines = ["Fortitude", "Melpominee", "Presence"]
        elif self.sheet.clan == "Followers of Set" or self.sheet.clan == "Serpents of the Light":
            myDisciplines = ["Obfuscate", "Presence", "Serpentis"]
        elif "Gangrel" in self.sheet.clan:
            if "City" in self.sheet.clan:
                myDisciplines = ["Celerity", "Obfuscate", "Protean"]
            else: 
                myDisciplines = ["Animalism", "Fortitude", "Protean"]
        elif "Gargoyle" == self.sheet.clan:
            myDisciplines = ["Flight", "Fortitude", "Potence", "Visceratika"]
        elif "Harbingers of Skulls" == self.sheet.clan:
            myDisciplines = ["Auspex", "Fortitude", "Necromancy"]
        elif self.sheet.clan == "Giovanni":
            myDisciplines = ["Dominate", "Necromancy", "Potence"]
        elif "Kiasyd" == self.sheet.clan:
            myDisciplines = ["Dominate", "Mytherceria", "Obtenebration"]
        elif "Lasombra" in self.sheet.clan:
            myDisciplines = ["Dominate", "Obtenebration", "Potence"]
        elif "Malkavian" in self.sheet.clan:
            myDisciplines = ["Auspex", "Dementation", "Obfuscate"]
        elif "Nagaraja" == self.sheet.clan:
            myDisciplines = ["Auspex", "Necromancy", "Nihilistics"]
        elif "Nosferatu" in self.sheet.clan:
            myDisciplines = ["Animalism", "Obfuscate", "Potence"]
        elif "Ravnos" in self.sheet.clan:
            myDisciplines = ["Animalism", "Chimerstry", "Fortitude"]
        elif "Salubri" in self.sheet.clan:
            if "Warrior" in self.sheet.clan or "Antitribu" in self.sheet.clan:
                myDisciplines = ["Auspex", "Fortitude", "Valeren"]
            else: 
                myDisciplines = ["Auspex", "Fortitude", "Obeah"]
        elif "Samedi" == self.sheet.clan:
            myDisciplines = ["Fortitude", "Obfuscate", "Thanatosis"]
        elif "Toreador" in self.sheet.clan:
            myDisciplines = ["Auspex", "Celerity", "Presence"]
        elif "Tremere" in self.sheet.clan:
            myDisciplines = ["Auspex", "Dominate", "Thaumaturgy"]
        elif "Tzimisce" in self.sheet.clan:
            if "Old Clan" in self.sheet.clan:
                myDisciplines = ["Auspex", "Animalism", "Dominate"]
            elif "Sorcerer" in self.sheet.clan:
                myDisciplines = ["Auspex", "Animalism", "Koldunic Sorcery"]
            else:
                myDisciplines = ["Auspex", "Animalism", "Vicissitude"]
        elif "Ventrue" in self.sheet.clan:
            myDisciplines = ["Dominate", "Fortitude", "Presence"]
        else:
            myDisciplines = ["(unknown)"]
 
        # If you are a Pander or Caitiff, you get random disciplines (fun!)
        if self.sheet.clan == "Pander" or self.sheet.clan == "Caitiff":
            myDisciplines = []
            common = []
            rare = []
            
            if self.sheet.clan == "Pander":
                common = ["Celerity", "Obfuscate", "Presence", "Potence", "Fortitude", "Auspex", "Obtenebration", "Dominate", "Animalism", "Vicissitude"]
                rare = ["Quietus", "Dementation", "Daimonion", "Serpentis", "Protean", "Necromancy", "Mytherceria", "Nihilistics", "Chimerstry", "Valeren", "Thanatosis"]
            elif self.sheet.clan == "Caitiff":
                common = ["Celerity", "Obfuscate", "Presence", "Potence", "Fortitude", "Auspex", "Dominate", "Animalism"]
                rare = ["Obeah", "Melpominee", "Mortis", "Quietus", "Dementation", "Daimonion", "Serpentis", "Protean", "Necromancy", "Chimerstry", "Valeren", "Thaumaturgy"]

            # Select three disciplines from the common/rare lists
            for choice in range(1,4):
               prob = random.randint(1,10)
               if prob <= 8:
                   # choose from common
                   selection = random.randint(0, len(common) - 1)
                   myDisciplines.append(common[selection])
                   del common[selection]
               else:
                   # choose from rare
                   selection = random.randint(0, len(rare) - 1)
                   myDisciplines.append(rare[selection])
                   del rare[selection]
    
        return myDisciplines


    # Select derangements.
    # Can assign up to three, with odds weighted towards none.
    def selectDerangements(self):
        myDerangements = []
        numDer = 0

        # Generic derangements
        derangements = ["agoraphobia", "amnesia", "antisocial personality disorder", "berserk", "bipolar affective disorder", "bulimia", "compulsion", "dependent personality disorder", "fugue", "histrionics", "hysteria", "klazomania", "megolomania", "memory lapses", "multiple-personality disorder", "obsessive-compulsive disorder", "overcompensation", "paranoia", "phobia", "power-object fixation", "post-traumatic stress disorder", "regression", "schizophrenia", "self-defeating personality disorder", "sexual dysfunction", "synesthesia"]

        # System-specific derangements
        if self.system == "werewolf":
            derangements.append("moon madness")
        elif self.system == "vampire":
            derangements.append("acute sanguinary aversion")
            derangements.append("blood sweats")
            derangements.append("hierarchical sociology disorder")
            derangements.append("desensitization")
            derangements.append("dissociate blood-spending")
            derangements.append("dissociate perceptions syndrome")
            derangements.append("sanguinary animism")
            derangements.append("sanguinary cryptophagy")
            derangements.append("self-annihilation impulse")
  
            if "Malkavian" in self.sheet.clan:
               numDer = 1

        # TODO: Add discipline-specific derangements
        
        # Choose number of derangements
        choice = random.random()
        if choice > 0.95:
            numDer += 3
        elif choice > 0.85:
            numDer += 2
        elif choice > 0.75:
            numDer += 1
        else:
            numDer += 0

        # Choose specific derangements
        for derangement in range(0,numDer):
            myDerangements.append(random.choice(derangements))

        return myDerangements

def main(argv):
    generator = Generator()
    classWeightFile= ""
    outFile = ""
    system = "vampire"
    minLevel = 8
    maxLevel = 13

    try:
        opts, args = getopt.getopt(argv,"hc:o:t:m:x:")
    except getopt.GetoptError:
        print 'Generator.py -c <class weight filename> -o <output filename> -t <character type> -m <minimum power level> -x <maximum power level>'
        sys.exit(2)
													  		
    for opt, arg in opts:
        if opt == "-h":
            print 'Generator.py -c <class weight filename> -o <output filename> -t <character type> -m <minimum power level> -x <maximum power level>'
            sys.exit()
        elif opt == "-c":
		    classWeightFile = arg
        elif opt == "-o":
            outFile = arg
        elif opt == "-t":
            system = arg
        elif opt == "-m":
            minLevel = int(arg)
        elif opt == "-x":
            maxLevel = int(arg)

    generator.system = system
    generator.minLevel = minLevel
    generator.maxLevel = maxLevel
    generator.generate(classWeightFile, outFile)

# Call into main
if __name__ == '__main__':
	main(sys.argv[1:])
