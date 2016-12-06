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

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import getopt
import sys
import os
import random

class Generator(): 
    # System
    system = "vampire"
    # Weights
    weights = []

    def generate(self, classWeightFile, outFile):
        if self.system == "vampire":
            # Intialize the set of available clans and weights
            self.initializeWeights(classWeightFile)
            print self.weights
        else:
            raise Exception("System " + self.system+" is not yet supported.")

    def initializeWeights(self, classWeightFile):
        if classWeightFile == "":
            self.weights.append(["Brujah",0.143])
            self.weights.append(["Gangrel",0.143])
            self.weights.append(["Malkavian",0.143])
            self.weights.append(["Nosferatu",0.143])
            self.weights.append(["Toreador",0.143])
            self.weights.append(["Tremere",0.143])
            self.weights.append(["Ventrue",0.143])
        else:
            if os.path.isfile(classWeightFile):
                lines = open(classWeightFile, "r")
                for line in lines:
                    self.weights.append(line.strip().split(","))
                lines.close()
            else:
                raise Exception("File " + classWeightFile + "does not exist")

def main(argv):
    generator = Generator()
    classWeightFile= ""
    outFile = ""
    system = "vampire"

    try:
	    opts, args = getopt.getopt(argv,"hc:o:t:")
    except getopt.GetoptError:
        print 'Generator.py -c <class weight filename> -o <output filename> -t <character type>'
        sys.exit(2)
													  		
    for opt, arg in opts:
        if opt == "-h":
            print 'Generator.py -c <class weight filename> -o <output filename> -t <character type>'
            sys.exit()
        elif opt == "-c":
		    classWeightFile = arg
        elif opt == "-o":
            outFile = arg
        elif opt == "-t":
            system = arg

    generator.system = system
    generator.generate(classWeightFile, outFile)

# Call into main
if __name__ == '__main__':
	main(sys.argv[1:])
