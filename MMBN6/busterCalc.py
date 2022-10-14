'''
Daric Leland
Created: 22/10/02
Edited:  22/10/14

Calculates buster DPS at various distances and speeds, as well as various forms.

Naming conventions:
constant =          EXAMPLE_NAME
1D list arg =       ExampleNameArr
2D list arg =       ExampleNameTbl
map arg =           ExampleNameMap
list/map local =    _ExampleName
var arg =           exampleName
var local =         _exampleName
function =          exampleName
'''

#For outputting files to a dynamic directory path.
import os
import sys

FPS = 60 #Frames Per Second
FLASHING = 120 #Duration of flashing state in frames.
INPUT_DELAY = 3 #Delay from button press until action starts in frames.
SPEED = [ #Cooldown values for base buster at each panel distance by Speed Lv.
        [5, 9, 13, 17, 21, 25], #Lv1
        [4, 8, 11, 15, 18, 21], #Lv2
        [4, 7, 10, 13, 16, 18], #Lv3
        [3, 5,  7,  9, 11, 13], #Lv4
        [3, 4,  5,  6,  7,  8]  #Lv5
        ]

    
    
#Calculates buster damage per second, given damage and frames for charging, start up, and cooldown.
#If the flashing flag is set, will account for waiting for flashing to run out.
def busterCalc(dmg, chrg, strt, cldn = 20, flsh = False):
    if flsh and (chrg + strt + cldn) < FLASHING:
        return dmg/2
    return round((dmg / ((chrg + strt + cldn)/FPS)), 1)

#Calculates bugged buster damage per second, given damage, frames for start up and cooldown, misfire chance, and jam chance.
def busterBugCalc(dmg, chrg, strt, SpeedArr, dst, misf, jam):
    #Jam cooldown is peashot cooldown +1 tier.
    _jDst = dst + 1
    #Prevent out of bounds index
    if (_jDst >= len(SpeedArr)):
        _jDst = len(SpeedArr) - 1
    #Peashot chance
    _pea = 1 - (misf + jam)
    
    #Calculate average damage per frame.
    _dJam = 0
    _fJam = (chrg + strt + SpeedArr[_jDst]) * jam

    _dPea = dmg * _pea
    _fPea = (chrg + strt + SpeedArr[dst]) * _pea

    _dMis = dmg * 10 * misf
    _fMis = (chrg + strt + strt + SpeedArr[dst]) * misf

    #Combine them and convert to damage per second.
    _dpf = (_dJam + _dPea + _dMis) / (_fJam + _fPea + _fMis)
    _dps = _dpf * FPS

    return round(_dps, 1)

#Creates a table of chargeshot DPS for Attack Lv1-AtkLv and Charge Lv1-5.
def attackChargeTable(base, mult, ChrgArr, strt, cldn = 20, flsh = False, dpsf = True, atkLv = 5):
    _table = []
    for _chrgLv in range(5):
        _row = []
        for _atk in range(1, (atkLv+1)):
            _damage = base + (_atk * mult)
            _item = str(busterCalc(_damage, ChrgArr[_chrgLv], strt, cldn))
            if dpsf: #Calculate DPS accounting for waiting for flashing to end.
                _item += ' ('+str(busterCalc(_damage, ChrgArr[_chrgLv], strt, cldn, flsh))+')'
            _row.append(_item)
        _table.append(_row)

    return _table

#Creates a table of normal buster DPS for all panel ranges and Speed levels.
def rangeSpeedTable(dmg, chrg, strt, CldnTbl, xAxis = 'Panels', yAxis = 'Speed'):
    _dps = []
    for _s in range(len(CldnTbl)):
        _subDps = []
        for _f in range(len(CldnTbl[_s])):
            _subDps.append(busterCalc(dmg, chrg, strt, CldnTbl[_s][_f]))
        _dps.append(_subDps)
    return makeTable(_dps, xAxis, yAxis)

#Converts a data table into a string table with labeled axes.
#Assumes table has square dimensions.
def makeTable(ArgTbl, xAxis, yAxis, tabs = 1):
    #Number and label X axis.
    _table = '\t'
    for _i in range(len(ArgTbl[0])):
        _table += str(_i+1)
        for _i in range(tabs):
            _table += '\t'
    _table += xAxis

    for _j in range(len(ArgTbl)):
        #Number Y axis.
        _table += '\n' + str(_j+1)
        #Fill out table row.
        for _i in ArgTbl[_j]:
            _table += '\t' + str(_i)
    #Label Y axis.
    _table += '\n' + yAxis
    
    return _table

#Given an Attack Lv, Peashot stats, and misfire rate, create and return a table of AVG buster bug DPS at every Speed Lv and distance.
def bugBusterSubBlock(atk, PeaMap, lv, jam = False):
    _dps = []
    for _spd in range(len(PeaMap['cldn'])):
        _subDps = []
        for _dst in range(len(PeaMap['cldn'][_spd])):
            _jamChance = 0
            if jam:
                _jamChance = PeaMap['jam'][lv]
            _subDps.append(busterBugCalc(PeaMap['dmg'][atk], PeaMap['chrg'], PeaMap['strt'], PeaMap['cldn'][_spd], _dst, PeaMap['misf'][lv], _jamChance))
        _dps.append(_subDps)
    return makeTable(_dps, 'Panels', 'Speed')

#Given an Attack Lv and Peashot stats, create and return tables of buster bug DPS at every bug Lv.
def bugBusterBlock(atk, PeaMap, jam = False):
    _output = ''

    _output += 'Buster Bug MAX DPS:\n'
    _output += bugBusterSubBlock(atk, PeaMap, 3, jam)

    _output += '\n\nBuster Bug Lv3 AVG DPS:\n'
    _output += bugBusterSubBlock(atk, PeaMap, 2, jam)

    _output += '\n\nBuster Bug Lv2 AVG DPS:\n'
    _output += bugBusterSubBlock(atk, PeaMap, 1, jam)

    _output += '\n\nBuster Bug Lv1 AVG DPS:\n'
    _output += bugBusterSubBlock(atk, PeaMap, 0, jam)

    return _output

#Output overview of all buster DPS.
def busterDPS(PeaMap, BaseMap, CrossArr, BugRSwrdMap, BgDthThdMap):
    _output = ''

    #Base buster
    _output += 'Peashot DPS:\n'
    _output += rangeSpeedTable(PeaMap['dmg'][4], PeaMap['chrg'], PeaMap['strt'], PeaMap['cldn'])

    _output += '\n\nChargeshot DPS:\n'
    _output += rangeSpeedTable(BaseMap['base']+BaseMap['mult']*5, BaseMap['chrg'][-1], BaseMap['strt'], BaseMap['cldn'])

    #Bugged buster
    _output += '\n\n' + bugBusterBlock(4, PeaMap)

    #Cross busters
    _output += '\n\n' + busterCrossDPS(CrossArr)

    #Beast and giga chip busters
    _output += '\n\n' + busterMiscDPS(PeaMap, BugRSwrdMap, BgDthThdMap)

    _output += '\n\nSpecial thanks to HonorNite for getting the missing frame data!'

    return _output

#Output tables of all stat combinations for peashot.
def busterPeaShotDPS(PeaMap):
    _output = ''
    for _atk in range(len(PeaMap['dmg'])):
        _output += 'Attack Lv'+str(PeaMap['dmg'][_atk])+':\n'
        _output += rangeSpeedTable(PeaMap['dmg'][_atk], PeaMap['chrg'], PeaMap['strt'], PeaMap['cldn'])
        _output += '\n\n'
    return _output

#Output tables of all stat combinations for base charge shot.
def busterChargeShotDPS(BaseMap, byRange = False):
    _output = ''
    if byRange:
        for _spd in range(len(BaseMap['cldn'])):
            for _dst in range(len(BaseMap['cldn'][_spd])):
                _output += 'Speed Lv'+str(_spd+1)+' @ '+str(_dst+1)+' panels\n'+makeTable(attackChargeTable(BaseMap['base'], BaseMap['mult'], BaseMap['chrg'], BaseMap['strt'], BaseMap['cldn'][_spd][_dst], BaseMap['flsh'], dpsf = False, atkLv = 10), 'Attack', 'Charge')+'\n\n' 
        return _output

    for _atk in range(1, 11):
        for _chg in range(len(BaseMap['chrg'])):
            _output += 'Attack Lv'+str(_atk)+' @ Charge Lv'+str(_chg+1)+':\n'
            _output += rangeSpeedTable(BaseMap['base']+BaseMap['mult']*_atk, BaseMap['chrg'][_chg], BaseMap['strt'], BaseMap['cldn'])
            _output += '\n\n'
    return _output

#Output tables of all stat combinations for buster bug.
def busterBugDPS(PeaMap):
    _output = ''
    for _atk in range(len(PeaMap['dmg'])):
        _output += 'Attack Lv'+str(PeaMap['dmg'][_atk])+':\n\n'
        _output += bugBusterBlock(_atk, PeaMap)
        _output += '\n\n\n'
    return _output

#Output tables of all stat combinations for buster bug.
def busterBugJamDPS(PeaMap):
    _output = ''
    for _atk in range(len(PeaMap['dmg'])):
        _output += 'Attack Lv'+str(PeaMap['dmg'][_atk])+':\n\n'
        _output += bugBusterBlock(_atk, PeaMap, True)
        _output += '\n\n\n'
    return _output

#Output tables of all stat combinations for cross charge shots.
def busterCrossDPS(CrossArr):
    _Heat, _Elec, _Slash, _Erase, _Charge, _Spout, _Toma, _Tengu, _Ground, _Dust = CrossArr
    _output = 'DPS (w/ Flashing)'

    _output += '\n\nGregar cross DPS:'
    _output += '\n\nHeat:\n'+makeTable(attackChargeTable(_Heat['base'], _Heat['mult'], _Heat['chrg'], _Heat['strt'], _Heat['cldn'], _Heat['flsh']), 'Attack', 'Charge', 2)
    _output += '\n\nElec:\n'+makeTable(attackChargeTable(_Elec['base'], _Elec['mult'], _Elec['chrg'], _Elec['strt'], _Elec['cldn'], _Elec['flsh']), 'Attack', 'Charge', 2)
    _output += '\n\nSlash:\n'+makeTable(attackChargeTable(_Slash['base'], _Slash['mult'], _Slash['chrg'], _Slash['strt'], _Slash['cldn'], _Slash['flsh']), 'Attack', 'Charge', 2)
    _output += '\n\nErase:\n'+makeTable(attackChargeTable(_Erase['base'], _Erase['mult'], _Erase['chrg'], _Erase['strt'], _Erase['cldn'], _Erase['flsh']), 'Attack', 'Charge', 2)
    _output += '\n\nCharge (1 panel):\n'+makeTable(attackChargeTable(_Charge['base'], _Charge['mult'], _Charge['chrg'], _Charge['strt'], _Charge['cldnHit'][0], _Charge['flsh']), 'Attack', 'Charge', 2)
    _output += '\n\nCharge (2 panels):\n'+makeTable(attackChargeTable(_Charge['base'], _Charge['mult'], _Charge['chrg'], _Charge['strt'], _Charge['cldnHit'][1], _Charge['flsh']), 'Attack', 'Charge', 2)
    _output += '\n\nCharge (3 panels):\n'+makeTable(attackChargeTable(_Charge['base'], _Charge['mult'], _Charge['chrg'], _Charge['strt'], _Charge['cldnHit'][2], _Charge['flsh']), 'Attack', 'Charge', 2)

    _output += '\n\nFalzar cross DPS:'
    _output += '\n\nSpout:\n'+makeTable(attackChargeTable(_Spout['base'], _Spout['mult'], _Spout['chrg'], _Spout['strt'], _Spout['cldn'], _Spout['flsh']), 'Attack', 'Charge', 2)
    _output += '\n\nTomahawk:\n'+makeTable(attackChargeTable(_Toma['base'], _Toma['mult'], _Toma['chrg'], _Toma['strt'], _Toma['cldn'], _Toma['flsh']), 'Attack', 'Charge', 2)
    _output += '\n\nTengu:\n'+makeTable(attackChargeTable(_Tengu['base'], _Tengu['mult'], _Tengu['chrg'], _Tengu['strt'], _Tengu['cldn'], _Tengu['flsh']), 'Attack', 'Charge', 2)
    _output += '\n\nGround:\n'+makeTable(attackChargeTable(_Ground['base'], _Ground['mult'], _Ground['chrg'], _Ground['strt'], _Ground['cldn'], _Ground['flsh']), 'Attack', 'Charge', 2)
    _output += '\n\nDust:\n'+makeTable(attackChargeTable(_Dust['base'], _Dust['mult'], _Dust['chrg'], _Dust['strt'], _Dust['cldn'], _Dust['flsh']), 'Attack', 'Charge', 2)

    return _output

#Output damage per second for busters which don't fall under normal, bugged, or crosses.
#Namely Beast Out and giga chips.
def busterMiscDPS(PeaMap, BugRSwrdMap, BgDthThdMap):
    _output = ''

    #Beast buster
    _output += 'Gregar vulcan:\t'+str(busterCalc(PeaMap['dmg'][4], 0, PeaMap['strt'], 0))
    _output += '\nFalzar feather:\t'+str(busterCalc(PeaMap['dmg'][4], 0, PeaMap['strt'], 3))+' >'+str(busterCalc(PeaMap['dmg'][4], 0, PeaMap['strt'], 3)*2/3)+'<'

    #Giga charge shots
    _output += '\n\nGiga chip DPS:'
    _output += '\nBugRSwrd:\t'+str(busterCalc(BugRSwrdMap['dmg'], BugRSwrdMap['chrg'], BugRSwrdMap['strt'], BugRSwrdMap['cldn']))+' ('+str(busterCalc(BugRSwrdMap['dmg'], BugRSwrdMap['chrg'], BugRSwrdMap['strt'], BugRSwrdMap['cldn'], BugRSwrdMap['flsh']))+')'
    _output += '\nBgDthThd:\t'+str(busterCalc(BgDthThdMap['dmg'], BgDthThdMap['chrg'], BgDthThdMap['strt'], BgDthThdMap['cldn']))+' ('+str(busterCalc(BgDthThdMap['dmg'], BgDthThdMap['chrg'], BgDthThdMap['strt'], BgDthThdMap['cldn'], BgDthThdMap['flsh']))+')'

    return _output

#Calculate how much a buster would win against BDT in a head-on trade, accounting for paralysis.
def vsBDT(BgDthThdMap, dmg, chrg, strt, cldn, flsh, mash = False):
    #Paralysis lasts this many frames.
    _paralysis = 120
    _time = chrg + strt + cldn
    _hit = chrg + strt
    #How long you are free from paralysis before the next shot hits.
    _limit = BgDthThdMap['chrg'] + BgDthThdMap['strt'] + BgDthThdMap['cldn']
    if mash:
        _limit -= _paralysis/2
    else:
        _limit -= _paralysis
    
    #Too slow to land even a single hit.
    if _hit > _limit:
        return -(BgDthThdMap['dmg'])

    #Able to land 1 hit, either barely or because of flashing.
    if _time > _limit or flsh:
        return dmg - BgDthThdMap['dmg']

    #Able to land multiple hits between BDT shots.
    return (dmg * int(_limit/_time)) - BgDthThdMap['dmg']
    
#Creates a table comparing many busters to BDT in a head-on trade. Calls vsBDT.
def vsBDTBlock(BaseMap, CrossArr, BugRSwrdMap, BgDthThdMap):
    _Heat, _Elec, _Slash, _Erase, _Charge, _Spout, _Toma, _Tengu, _Ground, _Dust = CrossArr
    _output = ''

    _output += 'Normal:\t'+str(vsBDT(BgDthThdMap, BaseMap['base']+BaseMap['mult']*5, BaseMap['chrg'][4], BaseMap['strt'], BaseMap['cldn'][4][0], BaseMap['flsh']))
    _output += '\t- '+str(vsBDT(BgDthThdMap, BaseMap['base']+BaseMap['mult']*5, BaseMap['chrg'][4], BaseMap['strt'], BaseMap['cldn'][4][0], BaseMap['flsh'], True))+'\n'

    _output += 'Heat:\t'+str(vsBDT(BgDthThdMap, _Heat['base']+_Heat['mult']*5, _Heat['chrg'][4], _Heat['strt'], _Heat['cldn'], _Heat['flsh']))
    _output += '\t- '+str(vsBDT(BgDthThdMap, _Heat['base']+_Heat['mult']*5, _Heat['chrg'][4], _Heat['strt'], _Heat['cldn'], _Heat['flsh'], True))+'\n'

    _output += 'Elec:\t'+str(vsBDT(BgDthThdMap, _Elec['base']+_Elec['mult']*5, _Elec['chrg'][4], _Elec['strt'], _Elec['cldn'], _Elec['flsh']))
    _output += '\t- '+str(vsBDT(BgDthThdMap, _Elec['base']+_Elec['mult']*5, _Elec['chrg'][4], _Elec['strt'], _Elec['cldn'], _Elec['flsh'], True))+'\n'

    _output += 'Slash:\t'+str(vsBDT(BgDthThdMap, _Slash['base']+_Slash['mult']*5, _Slash['chrg'][4], _Slash['strt'], _Slash['cldn'], _Slash['flsh']))
    _output += '\t- '+str(vsBDT(BgDthThdMap, _Slash['base']+_Slash['mult']*5, _Slash['chrg'][4], _Slash['strt'], _Slash['cldn'], _Slash['flsh'], True))+'\n'

    _output += 'Erase:\t'+str(vsBDT(BgDthThdMap, _Erase['base']+_Erase['mult']*5, _Erase['chrg'][4], _Erase['strt'], _Erase['cldn'], _Erase['flsh']))
    _output += '\t- '+str(vsBDT(BgDthThdMap, _Erase['base']+_Erase['mult']*5, _Erase['chrg'][4], _Erase['strt'], _Erase['cldn'], _Erase['flsh'], True))+'\n'

    _output += 'Charge:\t'+str(vsBDT(BgDthThdMap, _Charge['base']+_Charge['mult']*5, _Charge['chrg'][4], _Charge['strt'], _Charge['cldnHit'][0], _Charge['flsh']))
    _output += '\t- '+str(vsBDT(BgDthThdMap, _Charge['base']+_Charge['mult']*5, _Charge['chrg'][4], _Charge['strt'], _Charge['cldnHit'][0], _Charge['flsh'], True))+'\n'

    _output += 'Spout:\t'+str(vsBDT(BgDthThdMap, _Spout['base']+_Spout['mult']*5, _Spout['chrg'][4], _Spout['strt'], _Spout['cldn'], _Spout['flsh']))
    _output += '\t- '+str(vsBDT(BgDthThdMap, _Spout['base']+_Spout['mult']*5, _Spout['chrg'][4], _Spout['strt'], _Spout['cldn'], _Spout['flsh'], True))+'\n'

    _output += 'Toma:\t'+str(round(busterCalc(_Toma['base']+_Toma['mult']*5, _Toma['chrg'][4], _Toma['strt'], _Toma['cldn']) - busterCalc(BgDthThdMap['dmg'], BgDthThdMap['chrg'], BgDthThdMap['strt'], BgDthThdMap['cldn']), 1))+'\n'
    
    _output += 'Tengu:\t'+str(vsBDT(BgDthThdMap, _Tengu['base']+_Tengu['mult']*5, _Tengu['chrg'][4], _Tengu['strt'], _Tengu['cldn'], _Tengu['flsh']))
    _output += '\t- '+str(vsBDT(BgDthThdMap, _Tengu['base']+_Tengu['mult']*5, _Tengu['chrg'][4], _Tengu['strt'], _Tengu['cldn'], _Tengu['flsh'], True))+'\n'

    _output += 'Ground:\t'+str(vsBDT(BgDthThdMap, _Ground['base']+_Ground['mult']*5, _Ground['chrg'][4], _Ground['strt'], _Ground['cldn'], _Ground['flsh']))
    _output += '\t- '+str(vsBDT(BgDthThdMap, _Ground['base']+_Ground['mult']*5, _Ground['chrg'][4], _Ground['strt'], _Ground['cldn'], _Ground['flsh'], True))+'\n'

    _output += 'Dust:\t'+str(vsBDT(BgDthThdMap, _Dust['base']+_Dust['mult']*5, _Dust['chrg'][4], _Dust['strt'], _Dust['cldn'], _Dust['flsh']))
    _output += '\t- '+str(vsBDT(BgDthThdMap, _Dust['base']+_Dust['mult']*5, _Dust['chrg'][4], _Dust['strt'], _Dust['cldn'], _Dust['flsh'], True))+'\n'

    _output += 'BRS:\t'+str(vsBDT(BgDthThdMap, BugRSwrdMap['dmg'], BugRSwrdMap['chrg'], BugRSwrdMap['strt'], BugRSwrdMap['cldn'], BugRSwrdMap['flsh']))
    _output += '\t- '+str(vsBDT(BgDthThdMap, BugRSwrdMap['dmg'], BugRSwrdMap['chrg'], BugRSwrdMap['strt'], BugRSwrdMap['cldn'], BugRSwrdMap['flsh'], True))+'\n'

    return _output
    

def main():
    #Normal buster data.
    _Pea =       {'dmg':[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'chrg':INPUT_DELAY, 'strt':5, 'cldn':SPEED, 'flsh':False, 'misf':[1/16, 2/16, 3/16, 1], 'jam':[6/16, 10/16, 13/16, 0]}
    _Base =      {'chrg':[100, 90, 80, 70, 60], 'strt':10, 'cldn':SPEED, 'base':0, 'mult':10, 'flsh':False}

    #Cross charge shot data.
    _Heat =      {'chrg':[70,  60,  50,  45, 40], 'strt':1,  'cldn':66, 'base':30, 'mult':20, 'flsh':True}
    _Elec =      {'chrg':[90,  80,  70,  65, 60], 'strt':12, 'cldn':20, 'base':40, 'mult':20, 'flsh':True}
    _Slash =     {'chrg':[80,  70,  60,  55, 50], 'strt':12, 'cldn':18, 'base':60, 'mult':20, 'flsh':True}
    _Erase =     {'chrg':[110, 100, 90,  85, 80], 'strt':7,  'cldn':65, 'base':40, 'mult':20, 'flsh':False}
    _Charge =    {'chrg':[90,  80,  70,  65, 60], 'strt':12, 'cldnHit':[35, 38, 42], 'cldnMis':[24, 28, 30], 'base':30, 'mult':20, 'flsh':True}
    _Spout =     {'chrg':[60,  50,  40,  30, 20], 'strt':3,  'cldn':20, 'base':20, 'mult':10, 'flsh':True}
    _Toma =      {'chrg':[120, 110, 100, 95, 90], 'strt':26, 'cldn':18, 'base':40, 'mult':20, 'flsh':False}
    _Tengu =     {'chrg':[100, 90,  80,  75, 70], 'strt':10, 'cldn':18, 'base':40, 'mult':20, 'flsh':False}
    _Ground =    {'chrg':[100, 90,  80,  75, 70], 'strt':40, 'cldn':46, 'base':30, 'mult':30, 'flsh':False}
    _Dust =      {'chrg':[80,  70,  60,  55, 50], 'strt':9,  'cldn':27, 'base':50, 'mult':10, 'flsh':True}
    _Cross = [_Heat, _Elec, _Slash, _Erase, _Charge, _Spout, _Toma, _Tengu, _Ground, _Dust]

    #Giga chip charge shot data.
    _BugRSwrd = {'dmg':200, 'chrg':120, 'strt':12, 'cldn':18, 'flsh':True}
    _BgDthThd = {'dmg':200, 'chrg':200, 'strt':2,  'cldn':34, 'flsh':False}


    #Output master sheet.
    _output = busterDPS(_Pea, _Base, _Cross, _BugRSwrd, _BgDthThd)
    with open(os.path.join(sys.path[0], "BusterDPS.txt"), "w") as f:
            f.write(_output)
    print(_output)
    
    #Output peashot sheet.
    _output = busterPeaShotDPS(_Pea)
    with open(os.path.join(sys.path[0], "BusterPeaShotDPS.txt"), "w") as f:
            f.write(_output)
    print(_output)

    #Output base charge shot sheets.
    _output = busterChargeShotDPS(_Base)
    with open(os.path.join(sys.path[0], "BusterChargeShotDPSbyAttack@Charge.txt"), "w") as f:
            f.write(_output)
    print(_output)

    _output = busterChargeShotDPS(_Base, True)
    with open(os.path.join(sys.path[0], "BusterChargeShotDPSbySpeed@Distance.txt"), "w") as f:
            f.write(_output)
    print(_output)

    #Output bugged buster sheet.
    _output = busterBugDPS(_Pea)
    with open(os.path.join(sys.path[0], "BusterBugDPS.txt"), "w") as f:
            f.write(_output)
    print(_output)

    #Output jamming bugged buster sheet.
    _output = busterBugJamDPS(_Pea)
    with open(os.path.join(sys.path[0], "BusterBugJamDPS.txt"), "w") as f:
            f.write(_output)
    print(_output)

    #Output cross charge shot sheet.
    _output = busterCrossDPS(_Cross)
    with open(os.path.join(sys.path[0], "BusterCrossDPS.txt"), "w") as f:
            f.write(_output)
    print(_output)

    #Output vs BDT sheet.
    _output = vsBDTBlock(_Base, _Cross, _BugRSwrd, _BgDthThd)
    with open(os.path.join(sys.path[0], "BusterVsBDTDPS.txt"), "w") as f:
            f.write(_output)
    print(_output)


if __name__ == '__main__':
    main()