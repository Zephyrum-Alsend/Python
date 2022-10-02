'''
Daric Leland
22/10/02

Calculates buster DPS at various distances and speeds, as well as various forms.
As it's small, most values are hardcoded.
'''

import os
import sys

#Calculates buster damage per second, given damage and frames for charging, start up, and cooldown.
def busterCalc(dmg, chg, sta, cld = 20):
    return round((dmg / ((chg + sta + cld)/60)), 1)

#Calculates bugged buster damage per second, given damage, frames for start up and cooldown, and misfire chance.
def busterBugCalc(dmg, sta, cld, mis):
    return round((dmg+(dmg*9*mis)) / (((sta+(sta*mis))+cld)/60), 1)

#Converts a data table into a string table with labeled axes.
def makeTable(arr):
    table = '\t'
    for i in range(len(arr[0])):
        table += str(i+1) + '\t'
    table += 'Panels'

    for j in range(len(arr)):
        table += '\n' + str(j+1)
        for i in arr[j]:
            table += '\t' + str(i)
    table += '\nSpeed'
    
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

    DPSTable = ''


    #Base buster
    DPSTable += 'Peashot DPS:\n'
    DPS = []
    for s in range(len(speed)):
        subDPS = []
        for f in range(len(speed[s])):
            subDPS.append(busterCalc(5, 0, 5, speed[s][f]))
        DPS.append(subDPS)
    DPSTable += makeTable(DPS)

    DPSTable += '\n\nChargeshot DPS:\n'
    DPS = []
    for s in range(len(speed)):
        subDPS = []
        for f in range(len(speed[s])):
            subDPS.append(busterCalc(50, 60, 10, speed[s][f]))
        DPS.append(subDPS)
    DPSTable += makeTable(DPS)


    #Buster bug
    DPSTable += '\n\nBuster Bug MAX DPS:\n'
    DPS = []
    for s in range(len(speed)):
        subDPS = []
        for f in range(len(speed[s])):
            subDPS.append(busterCalc(50, 0, 10, speed[s][f]))
        DPS.append(subDPS)
    DPSTable += makeTable(DPS)

    DPSTable += '\n\nBuster Bug Lv3 AVG DPS:\n'
    DPS = []
    for s in range(len(speed)):
        subDPS = []
        for f in range(len(speed[s])):
            subDPS.append(busterBugCalc(5, 5, speed[s][f], 3/16))
        DPS.append(subDPS)
    DPSTable += makeTable(DPS)

    DPSTable += '\n\nBuster Bug Lv2 AVG DPS:\n'
    DPS = []
    for s in range(len(speed)):
        subDPS = []
        for f in range(len(speed[s])):
            subDPS.append(busterBugCalc(5, 5, speed[s][f], 2/16))
        DPS.append(subDPS)
    DPSTable += makeTable(DPS)

    DPSTable += '\n\nBuster Bug Lv1 AVG DPS:\n'
    DPS = []
    for s in range(len(speed)):
        subDPS = []
        for f in range(len(speed[s])):
            subDPS.append(busterBugCalc(5, 5, speed[s][f], 1/16))
        DPS.append(subDPS)
    DPSTable += makeTable(DPS)


    #Beast buster
    DPSTable += '\n\nGregar vulcan:\t'+str(busterCalc(5, 0, 5, 0))
    DPSTable += '\nFalzar feather:\t'+str(busterCalc(5, 0, 5, 3))+' >'+str(busterCalc(5, 0, 5, 3)*2/3)+'<'


    #Cross charge shots
    DPSTable += '\n\nDPS (w/ Flashing)*unknown cooldown, assume 20f'
    
    DPSTable += '\n\nGregar cross DPS:'
    DPSTable += '\nHeat:\t'+str(busterCalc(130, 40, 1, 61))+' ('+str(130/2)+')'
    DPSTable += '\nElec:\t'+str(busterCalc(140, 60, 12, 26))+' ('+str(140/2)+')'
    DPSTable += '\nSlash:\t'+str(busterCalc(160, 50, 12))+' ('+str(160/2)+')*'
    DPSTable += '\nErase:\t'+str(busterCalc(140, 80, 7, 70))+' ('+str(busterCalc(140, 80, 7, 70))+')'
    DPSTable += '\nCharge:\t'+str(busterCalc(130, 60, 12, 34))+' ('+str(130/2)+')'

    DPSTable += '\n\nFalzar cross DPS:'
    DPSTable += '\nSpout:\t'+str(busterCalc(70, 20, 3))+' ('+str(70/2)+')*'
    DPSTable += '\nToma:\t'+str(busterCalc(140, 90, 26))+' ('+str(busterCalc(140, 90, 26))+')*'
    DPSTable += '\nTengu:\t'+str(busterCalc(140, 70, 12))+' ('+str(busterCalc(140, 70, 12))+')*'
    DPSTable += '\nGround:\t'+str(busterCalc(180, 70, 40, 23))+' ('+str(busterCalc(180, 70, 40, 23))+')'
    DPSTable += '\nDust:\t'+str(busterCalc(100, 50, 9))+' ('+str(100/2)+')*'


    #Giga charge shots
    DPSTable += '\n\nGiga chip DPS:'
    DPSTable += '\nBugRSwrd:\t'+str(busterCalc(200, 120, 12))+'*'
    DPSTable += '\nBgDthThd:\t'+str(busterCalc(200, 200, 1))+'*'


    #Write to file and print to console for debug
    with open(os.path.join(sys.path[0], "BusterDPS.txt"), "w") as f:
            f.write(DPSTable)
    print(DPSTable)

if __name__ == '__main__':
    main()