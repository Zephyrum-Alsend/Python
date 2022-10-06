'''
Daric Leland
Created: 22/10/02
Edited:  22/10/05

Calculates buster DPS at various distances and speeds, as well as various forms.
'''

import os
import sys

#Time in frames from when a button is pressed to the corresponding action starting
inputDelay = 3
fps = 60

#Calculates buster damage per second, given damage and frames for charging, start up, and cooldown.
#If the flashing flag is set, will account for waiting for flashing to run out.
def busterCalc(dmg, chrg, strt, cldn = 20, flsh = False):
    if flsh and (chrg + strt + cldn) < 120:
        return dmg/2
    return round((dmg / ((chrg + strt + cldn)/fps)), 1)


#Calculates bugged buster damage per second, given damage, frames for start up and cooldown, and misfire chance.
def busterBugCalc(dmg, chrg, strt, cldn, misf):
    return round((dmg+(dmg*9*misf)) / (((chrg+strt+(strt*misf))+cldn)/fps), 1)


#Creates a table of chargeshot DPS for Attack Lv1-5 and Charge Lv1-5.
def attackChargeTable(base, mult, chrgArr, strt, cldn = 20, flsh = False, DPSf = True):
    table = []
    for chrgLv in range(5):
        row = []
        for atkLv in range(1, 6):
            damage = base + (atkLv * mult)
            item = str(busterCalc(damage, chrgArr[chrgLv], strt, cldn))
            if DPSf:
                item += ' ('+str(busterCalc(damage, chrgArr[chrgLv], strt, cldn, flsh))+')'
            row.append(item)
        table.append(row)

    return table


#Converts a data table into a string table with labeled axes.
def makeTable(arr, x, y, tabs = 1):
    #Number and label X axis.
    table = '\t'
    for i in range(len(arr[0])):
        table += str(i+1)
        for i in range(tabs):
            table += '\t'
    table += x

    for j in range(len(arr)):
        #Number Y axis.
        table += '\n' + str(j+1)
        #Fill out table row.
        for i in arr[j]:
            table += '\t' + str(i)
    #Label Y axis.
    table += '\n' + y
    
    return table


#Given an Attack Lv, Peashot stats, and misfire rate, create and return a table of AVG buster bug DPS at every Speed Lv and distance.
def bugBusterSubBlock(atk, Pea, misf):
    DPS = []
    for spd in range(len(Pea['cldn'])):
        subDPS = []
        for dst in range(len(Pea['cldn'][spd])):
            subDPS.append(busterBugCalc(Pea['dmg'][atk], Pea['chrg'], Pea['strt'], Pea['cldn'][spd][dst], Pea['misf'][misf]))
        DPS.append(subDPS)
    return makeTable(DPS, 'Panels', 'Speed')


#Given an Attack Lv and Peashot stats, create and return tables of buster bug DPS at every bug Lv.
def bugBusterBlock(atk, Pea):
    Output = ''

    Output += 'Buster Bug MAX DPS:\n'
    Output += bugBusterSubBlock(atk, Pea, 3)

    Output += '\n\nBuster Bug Lv3 AVG DPS:\n'
    Output += bugBusterSubBlock(atk, Pea, 2)

    Output += '\n\nBuster Bug Lv2 AVG DPS:\n'
    Output += bugBusterSubBlock(atk, Pea, 1)

    Output += '\n\nBuster Bug Lv1 AVG DPS:\n'
    Output += bugBusterSubBlock(atk, Pea, 0)

    return Output


#Output overview of all buster DPS.
def busterDPS(Pea, Base, Cross, BRS, BDT):
    Output = ''

    #Base buster
    Output += 'Peashot DPS:\n'
    DPS = []
    for s in range(len(Pea['cldn'])):
        subDPS = []
        for f in range(len(Pea['cldn'][s])):
            subDPS.append(busterCalc(Pea['dmg'][-1], Pea['chrg'], Pea['strt'], Pea['cldn'][s][f]))
        DPS.append(subDPS)
    Output += makeTable(DPS, 'Panels', 'Speed')

    Output += '\n\nChargeshot DPS:\n'
    DPS = []
    for s in range(len(Base['cldn'])):
        subDPS = []
        for f in range(len(Base['cldn'][s])):
            subDPS.append(busterCalc(Base['base']+Base['mult']*5, Base['chrg'][-1], Base['strt'], Base['cldn'][s][f]))
        DPS.append(subDPS)
    Output += makeTable(DPS, 'Panels', 'Speed')

    #Bugged buster
    Output += '\n\n' + bugBusterBlock(4, Pea)

    #Cross busters
    Output += '\n\n' + busterCrossDPS(Cross)

    #Beast and giga chip busters
    Output += '\n\n' + busterMiscDPS(Pea, BRS, BDT)

    Output += '\n\nSpecial thanks to HonorNite for getting the missing frame data!'

    return Output


#Output tables of all stat combinations for base charge shot.
def busterChargeShotDPS(Base):
    Output = ''
    for spd in range(len(Base['cldn'])):
        for dst in range(len(Base['cldn'][spd])):
            Output += 'Speed Lv'+str(spd+1)+' @ '+str(dst+1)+' panels\n'+makeTable(attackChargeTable(Base['base'], Base['mult'], Base['chrg'], Base['strt'], Base['cldn'][spd][dst], Base['flsh'], DPSf = False), 'Attack', 'Charge')+'\n\n' 
    return Output


#Output tables of all stat combinations for buster bug.
def busterBugDPS(Pea):
    Output = ''
    for atk in range(len(Pea['dmg'])):
        Output += 'Attack Lv'+str(Pea['dmg'][atk])+':\n\n'
        Output += bugBusterBlock(atk, Pea)
        Output += '\n\n\n'
    return Output


#Output tables of all stat combinations for cross charge shots.
def busterCrossDPS(Cross):
    Heat, Elec, Slash, Erase, Charge, Spout, Toma, Tengu, Ground, Dust = Cross
    Output = 'DPS (w/ Flashing)'

    Output += '\n\nGregar cross DPS:'
    Output += '\n\nHeat:\n'+makeTable(attackChargeTable(Heat['base'], Heat['mult'], Heat['chrg'], Heat['strt'], Heat['cldn'], Heat['flsh']), 'Attack', 'Charge', 2)
    Output += '\n\nElec:\n'+makeTable(attackChargeTable(Elec['base'], Elec['mult'], Elec['chrg'], Elec['strt'], Elec['cldn'], Elec['flsh']), 'Attack', 'Charge', 2)
    Output += '\n\nSlash:\n'+makeTable(attackChargeTable(Slash['base'], Slash['mult'], Slash['chrg'], Slash['strt'], Slash['cldn'], Slash['flsh']), 'Attack', 'Charge', 2)
    Output += '\n\nErase:\n'+makeTable(attackChargeTable(Erase['base'], Erase['mult'], Erase['chrg'], Erase['strt'], Erase['cldn'], Erase['flsh']), 'Attack', 'Charge', 2)
    Output += '\n\nCharge (1 panel):\n'+makeTable(attackChargeTable(Charge['base'], Charge['mult'], Charge['chrg'], Charge['strt'], Charge['cldnHit'][0], Charge['flsh']), 'Attack', 'Charge', 2)
    Output += '\n\nCharge (2 panels):\n'+makeTable(attackChargeTable(Charge['base'], Charge['mult'], Charge['chrg'], Charge['strt'], Charge['cldnHit'][1], Charge['flsh']), 'Attack', 'Charge', 2)
    Output += '\n\nCharge (3 panels):\n'+makeTable(attackChargeTable(Charge['base'], Charge['mult'], Charge['chrg'], Charge['strt'], Charge['cldnHit'][2], Charge['flsh']), 'Attack', 'Charge', 2)

    Output += '\n\nFalzar cross DPS:'
    Output += '\n\nSpout:\n'+makeTable(attackChargeTable(Spout['base'], Spout['mult'], Spout['chrg'], Spout['strt'], Spout['cldn'], Spout['flsh']), 'Attack', 'Charge', 2)
    Output += '\n\nTomahawk:\n'+makeTable(attackChargeTable(Toma['base'], Toma['mult'], Toma['chrg'], Toma['strt'], Toma['cldn'], Toma['flsh']), 'Attack', 'Charge', 2)
    Output += '\n\nTengu:\n'+makeTable(attackChargeTable(Tengu['base'], Tengu['mult'], Tengu['chrg'], Tengu['strt'], Tengu['cldn'], Tengu['flsh']), 'Attack', 'Charge', 2)
    Output += '\n\nGround:\n'+makeTable(attackChargeTable(Ground['base'], Ground['mult'], Ground['chrg'], Ground['strt'], Ground['cldn'], Ground['flsh']), 'Attack', 'Charge', 2)
    Output += '\n\nDust:\n'+makeTable(attackChargeTable(Dust['base'], Dust['mult'], Dust['chrg'], Dust['strt'], Dust['cldn'], Dust['flsh']), 'Attack', 'Charge', 2)

    return Output


def busterMiscDPS(Pea, BRS, BDT):
    Output = ''

    #Beast buster
    Output += 'Gregar vulcan:\t'+str(busterCalc(Pea['dmg'][4], 0, Pea['strt'], 0))
    Output += '\nFalzar feather:\t'+str(busterCalc(Pea['dmg'][4], 0, Pea['strt'], 3))+' >'+str(busterCalc(Pea['dmg'][4], 0, Pea['strt'], 3)*2/3)+'<'

    #Giga charge shots
    Output += '\n\nGiga chip DPS:'
    Output += '\nBugRSwrd:\t'+str(busterCalc(BRS['dmg'], BRS['chrg'], BRS['strt'], BRS['cldn']))+' ('+str(busterCalc(BRS['dmg'], BRS['chrg'], BRS['strt'], BRS['cldn'], BRS['flsh']))+')'
    Output += '\nBgDthThd:\t'+str(busterCalc(BDT['dmg'], BDT['chrg'], BDT['strt'], BDT['cldn']))+' ('+str(busterCalc(BDT['dmg'], BDT['chrg'], BDT['strt'], BDT['cldn'], BDT['flsh']))+')'

    return Output


def main():
    #Cooldown values for base buster at each Speed Lv and panel distance.
    speed = [
            [5, 9, 13, 17, 21, 25],
            [4, 8, 11, 15, 18, 21],
            [4, 7, 10, 13, 16, 18],
            [3, 5, 7, 9, 11, 13],
            [3, 4, 5, 6, 7, 8]
            ]

    #Normal buster data.
    Pea =       {'dmg':[1, 2, 3, 4, 5], 'chrg':inputDelay, 'strt':5, 'cldn':speed, 'flsh':False, 'misf':[1/16, 2/16, 3/16, 1]}
    Base =      {'chrg':[100, 90, 80, 70, 60], 'strt':10, 'cldn':speed, 'base':0, 'mult':10, 'flsh':False}

    #Cross charge shot data.
    Heat =      {'chrg':[70,  60,  50,  45, 40], 'strt':1,  'cldn':66, 'base':30, 'mult':20, 'flsh':True}
    Elec =      {'chrg':[90,  80,  70,  65, 60], 'strt':12, 'cldn':20, 'base':40, 'mult':20, 'flsh':True}
    Slash =     {'chrg':[80,  70,  60,  55, 50], 'strt':12, 'cldn':18, 'base':60, 'mult':20, 'flsh':True}
    Erase =     {'chrg':[110, 100, 90,  85, 80], 'strt':7,  'cldn':65, 'base':40, 'mult':20, 'flsh':False}
    Charge =    {'chrg':[90,  80,  70,  65, 60], 'strt':12, 'cldnHit':[35, 38, 42], 'cldnMis':[24, 28, 30], 'base':30, 'mult':20, 'flsh':True}
    Spout =     {'chrg':[60,  50,  40,  30, 20], 'strt':3,  'cldn':20, 'base':20, 'mult':10, 'flsh':True}
    Toma =      {'chrg':[120, 110, 100, 95, 90], 'strt':26, 'cldn':18, 'base':40, 'mult':20, 'flsh':False}
    Tengu =     {'chrg':[100, 90,  80,  75, 70], 'strt':12, 'cldn':16, 'base':40, 'mult':20, 'flsh':False}
    Ground =    {'chrg':[100, 90,  80,  75, 70], 'strt':40, 'cldn':46, 'base':30, 'mult':30, 'flsh':False}
    Dust =      {'chrg':[80,  70,  60,  55, 50], 'strt':9,  'cldn':27, 'base':50, 'mult':10, 'flsh':True}
    Cross = [Heat, Elec, Slash, Erase, Charge, Spout, Toma, Tengu, Ground, Dust]

    #Giga chip charge shot data.
    BRS = {'dmg':200, 'chrg':120, 'strt':12, 'cldn':18, 'flsh':True}
    BDT = {'dmg':200, 'chrg':200, 'strt':2,  'cldn':34, 'flsh':False}


    #Output master sheet.
    Output = busterDPS(Pea, Base, Cross, BRS, BDT)
    with open(os.path.join(sys.path[0], "BusterDPS.txt"), "w") as f:
            f.write(Output)
    print(Output)
    
    #Output base charge shot sheet.
    Output = busterChargeShotDPS(Base)
    with open(os.path.join(sys.path[0], "BusterChargeShotDPS.txt"), "w") as f:
            f.write(Output)
    print(Output)

    #Output bugged buster sheet.
    Output = busterBugDPS(Pea)
    with open(os.path.join(sys.path[0], "BusterBugDPS.txt"), "w") as f:
            f.write(Output)
    print(Output)

    #Output cross charge shot sheet.
    Output = busterCrossDPS(Cross)
    with open(os.path.join(sys.path[0], "BusterCrossDPS.txt"), "w") as f:
            f.write(Output)
    print(Output)


if __name__ == '__main__':
    main()