# Gregory Gay (greg@greggay.com)
# Classes that represent character sheets

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

class Vampire():
    # Character Clan
    clan = "Brujah"
    # Character Generation
    generation = 13
    # Derangements
    derangements = []
    # Dusciplines
    disciplines = []

    # Pretty printing (to screen)
    def printToScreen(self):
        print "Clan: " + self.clan
        print "Generation: " + str(self.generation)
        dis = "Disciplines: "

        for entry in self.disciplines:
            dis = dis + entry + ", "
        dis = dis[:len(dis) - 2]

        print dis

        der = "Derangements: "

        if len(self.derangements) == 0:
            der = der + "(none)"
        else:
            for entry in self.derangements:
                der = der + entry + ", "
            der = der[:len(der)-2]
        print der

    # Pretty printing (to file)
    def printToFile(self, outFile):
        if outFile != "":
            output = open(outFile, "w")
            output.write("Clan: " + self.clan + "\n")
            output.write("Generation: " + str(self.generation) + "\n")
          
            dis = "Disciplines: "
   
            for entry in self.disciplines:
                dis = dis + entry + ", "

            dis = dis[:len(dis) - 2]

            output.write(dis + "\n")

            der = "Derangements: "
            if len(self.derangements) == 0:
                der = der + "(none)"
            else:
                for entry in self.derangements:
                    der = der + entry + ", "
                der = der[:len(der)-2]

            output.write(der + "\n")
            output.close()

