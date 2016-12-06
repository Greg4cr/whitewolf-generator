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

        if len(classSelect) < 100:
            raise Exception("Sum of weights " + str(len(classSelect)) + "is less than 100")
        else:
            return classSelect[random.randint(0,99)]
    
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

    # Select derangements.
    # Can assign up to three, with odds weighted towards none.
    def selectDerangements(self):
        myDerangements = []

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
            derangements.append("severe dysmenorrheic psychosis")

        # TODO: Add discipline-specific derangements
        
        # Choose number of derangements
        choice = random.random()
        if choice > 0.95:
            numDer = 3
        elif choice > 0.85:
            numDer = 2
        elif choice > 0.75:
            numDer = 1
        else:
            numDer = 0

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
