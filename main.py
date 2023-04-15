import csv
import logging as logger
import sys

#Config options
skipMasterTier = True
skipMob = False
skipRec = False
skipRes = False
skipDis = False
skipInt = False
skipStr = False

class armorPiece:
    def __init__(self, info):
        #Set variables
        try:
            self.name = info[0]
            self.hash = info[1]
            self.id = info[2]
            self.tier = info[4]
            self.type = info[5]
            self.equippable = info[7]
            self.power = int(info[8])

            #Armor 1.0 exotics have no masterwork so this is required.
            try:
                self.masterTier = int(info[10])

            except Exception as e:
                self.masterTier = 0

            self.mob = int(info[24])
            self.res = int(info[25])
            self.rec = int(info[26])
            self.dis = int(info[27])
            self.int = int(info[28])
            self.str = int(info[29])
            self.total = int(info[30])

        except Exception as e:
            print(e)
            print("Something went wrong with " + self.name)

    #Determine if stats of two pieces are identical
    def identicalStats(self, test):
        return self.mob == test.mob and self.res == test.res and self.rec == test.rec and self.dis == test.dis and self.int == test.int and self.str == test.str

    #Determine if stats of a piece are better than stats of another piece
    def isBetter(self, test):
        #Skip comparing piece to self and exotics
        if self == test or self.tier == "Exotic" or test.tier == "Exotic":
            return False
        #Check classes and slot are the same
        if self.equippable == test.equippable and self.type == test.type:
            #Skip if stats are completely identical
            if self.identicalStats(test):
                return False
            #Check if all stats are equal to or better than test piece, respecting config options
            return (self.mob >= test.mob or skipMob) and (self.res >= test.res or skipRes) and (
                    self.rec >= test.rec or skipRec) and (self.dis >= test.dis or skipDis) and (
                           self.int >= test.int or skipInt) and (self.str >= test.str or skipStr) and (
                           self.masterTier >= test.masterTier or skipMasterTier)
        return False

    #Simpler way to print armor piece
    def shortStr(self):
        return str(self.name) + "," + str(self.equippable) + "," + str(self.type) + "," + str(self.power) + "," + str(
            self.total) + "," + str(self.masterTier)

def run():
    #Prompting and config
    print("Setup: Decide what parameters to use. Press Y for yes, any other key for no.")
    global skipMasterTier, skipMob, skipRec, skipRes, skipDis, skipInt, skipStr
    skipMasterTier = input("Ignore Masterwork Tier? Y/N (Default: Yes)\n") in ['Y', 'y', 'yes', 'Yes', 'YES']
    skipMob = input("Ignore Mobility? Y/N (Default: No)\n") in ['Y', 'y', 'yes', 'Yes', 'YES']
    skipRec = input("Ignore Recovery? Y/N (Default: No)\n") in ['Y', 'y', 'yes', 'Yes', 'YES']
    skipRes = input("Ignore Resilience? Y/N (Default: No)\n") in ['Y', 'y', 'yes', 'Yes', 'YES']
    skipDis = input("Ignore Discipline? Y/N (Default: No)\n") in ['Y', 'y', 'yes', 'Yes', 'YES']
    skipInt = input("Ignore Intellect? Y/N (Default: No)\n") in ['Y', 'y', 'yes', 'Yes', 'YES']
    skipStr = input("Ignore Strength? Y/N (Default: No)\n") in ['Y', 'y', 'yes', 'Yes', 'YES']

    #Open CSV from DIM
    rawArmorList = []
    armorList = []
    
    try:
        with open('resources/destinyArmor.csv', newline='') as f:
            reader = csv.reader(f)
            rawArmorList = list(reader)
    except Exception as e:
        logger.error("Caught exception when opening csv file\n" + str(e))
    
    if len(rawArmorList) == 0:
        logger.info("raw armor list was found empty, closing")
        sys.exit(1)
         
        
    #List of all pieces
    for currentArmor in rawArmorList[2:]:
        armorList.append(armorPiece(currentArmor))

    #Create list of comparisons
    superiorityList = []
    for currentArmor in armorList:
        for testArmor in armorList:
            if currentArmor.isBetter(testArmor):
                superiorityList.append((currentArmor.shortStr(), testArmor.shortStr()))

    #Lists of armor to keep and shard
    bestArmor = set([armor[0] for armor in superiorityList])
    worstArmor = set([armor[1] for armor in superiorityList])

    simpleSuperiorityList = []

    #Formatting the list so that each piece to keep is listed next to which pieces it supersedes
    for currentArmor in bestArmor:
        badArmorList = [armor[1] for armor in superiorityList if armor[0] == currentArmor]
        simpleSuperiorityList.append([currentArmor, badArmorList])

    #Display
    for element in simpleSuperiorityList:
        print(element[0] + " is better than: " + str(element[1]) + "\n")
    
    logger.info("Vault Spaces Saveable: " + str(len(worstArmor)))


if __name__ == "__main__":
    run()
