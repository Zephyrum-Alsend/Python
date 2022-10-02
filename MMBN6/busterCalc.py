'''
Daric Leland
22/10/02

Calculates buster DPS at various distances and speeds, as well as various forms.
As it's small, most values are hardcoded.
'''

import os
import sys

#Calculates buster damage per second, given damage and frames for charging, start up, and cooldown.
#If the flashing flag is set, will account for waiting for flashing to run out.
def busterCalc(dmg, chg, sta, cld = 20, fls = False):
    if fls and (chg + sta + cld) < 120:
        return dmg/2
    return round((dmg / ((chg + sta + cld)/60)), 1)

#Calculates bugged buster damage per second, given damage, frames for start up and cooldown, and misfire chance.
def busterBugCalc(dmg, sta, cld, mis):
    return round((dmg+(dmg*9*mis)) / (((sta+(sta*mis))+cld)/60), 1)

#Creates a table of chargeshot DPS for Attack Lv1-5 and Charge Lv1-5.
def attackChargeTable(base, mult, chgArr, sta, cld = 20, fls = False):
    table = []
    for c in range(5):
        sub = []
        for a in range(1, 6):
            damage = base + (a * mult)
            item = str(busterCalc(damage, chgArr[c], sta, cld))+' ('+str(busterCalc(damage, chgArr[c], sta, cld, fls))+')'
            sub.append(item)
        table.append(sub)

    return table

#Converts a data table into a string table with labeled axes.
def makeTable(arr, x, y, tabs = 1):
    table = '\t'
    for i in range(len(arr[0])):
        table += str(i+1)
        for i in range(tabs):
            table += '\t'
    table += x

    for j in range(len(arr)):
        table += '\n' + str(j+1)
        for i in arr[j]:
            table += '\t' + str(i)
    table += '\n' + y
    
    return table

def main():
    #Hardcoded cooldown values for base buster at each Speed Lv and panel distance.
    speed = [
            [5, 9, 13, 17, 21, 25],
            [4, 8, 11, 15, 18, 21],
            [4, 7, 10, 13, 16, 18],
            [3, 5, 7, 9, 11, 13],
            [3, 4, 5, 6, 7, 8]
            ]

    #Frame data for cross charge shots at all charge levels.
    Heat = [70, 60, 50, 45, 40]
    Elec = [90, 80, 70, 65, 60]
    Slash = [80, 70, 60, 55, 50]
    Erase = [110, 100, 90, 85, 80]
    Charge = [90, 80, 70, 65, 60]
    Spout = [60, 50, 40, 30, 20]
    Toma = [120, 110, 100, 95, 90]
    Tengu = [100, 90, 80, 75, 70]
    Ground = [100, 90, 80, 75, 70]
    Dust = [80, 70, 60, 55, 50]

    DPSTable = ''


    #Base buster
    DPSTable += 'Peashot DPS:\n'
    DPS = []
    for s in range(len(speed)):
        subDPS = []
        for f in range(len(speed[s])):
            subDPS.append(busterCalc(5, 0, 5, speed[s][f]))
        DPS.append(subDPS)
    DPSTable += makeTable(DPS, 'Panels', 'Speed')

    DPSTable += '\n\nChargeshot DPS:\n'
    DPS = []
    for s in range(len(speed)):
        subDPS = []
        for f in range(len(speed[s])):
            subDPS.append(busterCalc(50, 60, 10, speed[s][f]))
        DPS.append(subDPS)
    DPSTable += makeTable(DPS, 'Panels', 'Speed')


    #Buster bug
    DPSTable += '\n\nBuster Bug MAX DPS:\n'
    DPS = []
    for s in range(len(speed)):
        subDPS = []
        for f in range(len(speed[s])):
            subDPS.append(busterCalc(50, 0, 10, speed[s][f]))
        DPS.append(subDPS)
    DPSTable += makeTable(DPS, 'Panels', 'Speed')

    DPSTable += '\n\nBuster Bug Lv3 AVG DPS:\n'
    DPS = []
    for s in range(len(speed)):
        subDPS = []
        for f in range(len(speed[s])):
            subDPS.append(busterBugCalc(5, 5, speed[s][f], 3/16))
        DPS.append(subDPS)
    DPSTable += makeTable(DPS, 'Panels', 'Speed')

    DPSTable += '\n\nBuster Bug Lv2 AVG DPS:\n'
    DPS = []
    for s in range(len(speed)):
        subDPS = []
        for f in range(len(speed[s])):
            subDPS.append(busterBugCalc(5, 5, speed[s][f], 2/16))
        DPS.append(subDPS)
    DPSTable += makeTable(DPS, 'Panels', 'Speed')

    DPSTable += '\n\nBuster Bug Lv1 AVG DPS:\n'
    DPS = []
    for s in range(len(speed)):
        subDPS = []
        for f in range(len(speed[s])):
            subDPS.append(busterBugCalc(5, 5, speed[s][f], 1/16))
        DPS.append(subDPS)
    DPSTable += makeTable(DPS, 'Panels', 'Speed')


    #Beast buster
    DPSTable += '\n\nGregar vulcan:\t'+str(busterCalc(5, 0, 5, 0))
    DPSTable += '\nFalzar feather:\t'+str(busterCalc(5, 0, 5, 3))+' >'+str(busterCalc(5, 0, 5, 3)*2/3)+'<'

    #Cross charge shots
    DPSTable += '\n\nDPS (w/ Flashing)\n*unknown cooldown, assume 20f'

    DPSTable += '\n\nGregar cross DPS:'
    DPSTable += '\n\nHeat:\n'+makeTable(attackChargeTable(30, 20, Heat, 1, 61, fls = True), 'Attack', 'Charge', 2)
    DPSTable += '\n\nElec:\n'+makeTable(attackChargeTable(40, 20, Elec, 12, 26, fls = True), 'Attack', 'Charge', 2)
    DPSTable += '\n\nSlash*:\n'+makeTable(attackChargeTable(60, 20, Slash, 12, fls = True), 'Attack', 'Charge', 2)
    DPSTable += '\n\nErase:\n'+makeTable(attackChargeTable(40, 20, Erase, 7, 70, fls = False), 'Attack', 'Charge', 2)
    DPSTable += '\n\nCharge:\n'+makeTable(attackChargeTable(30, 20, Charge, 12, 34, fls = True), 'Attack', 'Charge', 2)

    DPSTable += '\n\nFalzar cross DPS:'
    DPSTable += '\n\nSpout*:\n'+makeTable(attackChargeTable(20, 10, Spout, 3, fls = True), 'Attack', 'Charge', 2)
    DPSTable += '\n\nToma*:\n'+makeTable(attackChargeTable(40, 20, Toma, 26, fls = False), 'Attack', 'Charge', 2)
    DPSTable += '\n\nTengu*:\n'+makeTable(attackChargeTable(40, 20, Tengu, 12, fls = False), 'Attack', 'Charge', 2)
    DPSTable += '\n\nGround:\n'+makeTable(attackChargeTable(30, 30, Ground, 40, 23, fls = False), 'Attack', 'Charge', 2)
    DPSTable += '\n\nDust*:\n'+makeTable(attackChargeTable(50, 10, Dust, 9, fls = True), 'Attack', 'Charge', 2)

    #Giga charge shots
    DPSTable += '\n\nGiga chip DPS:'
    DPSTable += '\nBugRSwrd*:\t'+str(busterCalc(200, 120, 12))+' ('+str(busterCalc(200, 120, 12, fls = True))+')'
    DPSTable += '\nBgDthThd*:\t'+str(busterCalc(200, 200, 1))+' ('+str(busterCalc(200, 200, 1, fls = False))+')'

    
    #Write to file and print to console for debug
    with open(os.path.join(sys.path[0], "BusterDPS.txt"), "w") as f:
            f.write(DPSTable)
    print(DPSTable)

if __name__ == '__main__':
    main()