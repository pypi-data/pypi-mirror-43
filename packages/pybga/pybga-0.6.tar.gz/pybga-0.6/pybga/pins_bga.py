# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 13:32:11 2019

@author: kuzin.n
"""

import os
from enum import Enum

_ainput =[]
_counter_call = {} #"1...len(grp)": current Y pos
_grp_x = {} #"1...len(grp)": current X pos

class _package(Enum):
    PACKAGE_EMPTY=1
    PACKAGE_FILL=2

def _fill_bga(_pack):
#empty ball array
    if(_pack == _package.PACKAGE_EMPTY):
        _f0 = open("./package.csv")
    else:
        if(_pack == _package.PACKAGE_FILL):
            _f0 = open("./package_out.csv")
    global _ainput 
    _ainput = [_row.split(',') for _row in _f0] 
    _f0.close()
    
def _in_str(_str,_grp,gs,ggs,holdy): #проверка что строки списка _grp входят в начало строки _str  
    global _counter_call
    global _grp_x
    for idx0, _lst in enumerate(_grp):
        try:
            if(_str.index(_lst)==0):
                if(_counter_call.get(idx0+1)==None):
                    _counter_call[idx0+1]=0
                    if(len(_grp_x)==0):
                        _grp_x[idx0+1]=1
                    else:
                        _grp_x[idx0+1]=max(_grp_x.values())+1
                else:
                    if(_counter_call[idx0+1]>holdy):
                        _grp_x[idx0+1]+= (ggs/gs) 
                        _counter_call[idx0+1]=0
                    else:    
                        _counter_call[idx0+1]+=1
                return _grp_x[idx0+1],_counter_call[idx0+1]
        except:
            pass
    if(_counter_call.get(0)==None):
        _counter_call[0]=0
    else:
        _counter_call[0]+=1
    return 0,_counter_call[0] # вхождение не найдено

#xs -> begin X pos
#ys -> begin Y pos
#gs -> gap betweeen group   
#ggs -> gap in group     
#holdy -> max pins by Y
#_pack -> type of input file: package.csv or package_out.csv    
def pins_bga(_folder,_dict0,_group0,xs,ys,gs,ggs,holdy,_pack):
        
    global _ainput
    global _counter_call
    global _grp_x
    
    _ainput=[]
    _counter_call = {}
    _grp_x = {}     
    
    print("Starting... change current dir to: "+_folder+"\n")
    os.chdir(_folder)
    _fill_bga(_pack)
    
    if(_pack.PACKAGE_EMPTY):
        for idx0, _row in enumerate(_ainput):
            for idx1, _i1 in enumerate(_row):
                if((idx0>0) and (idx0<(len(_ainput)-1))):
                    if((idx1>3) and (idx1<(len(_row)-1))):
                        _des = _row[3]+_ainput[0][idx1] #des
                        _ainput[idx0][idx1] =  _dict0.get(_des)
                

        _f0 = open('./package_out.csv', 'w')            
        for idx0 in range(len(_ainput)):
            _str = ','.join(str(item) for item in _ainput[idx0])
            _f0.writelines(_str)
        _f0.close()


    print ("Starting the Altium pins to out\n")
    _f0 = open('./package_out.csv')

    _out_list=[]
    for idx0, _row in enumerate(_ainput):
        for idx1, _i1 in enumerate(_row):
            if((idx0>0) and (idx0<(len(_ainput)-1))):
                if((idx1>3) and (idx1<(len(_row)-1))):
                    _des = _row[3]+_ainput[0][idx1] #des
                    _res0,_res1=_in_str(str(_ainput[idx0][idx1]),_group0,gs,ggs,holdy)
                    _out_list.append(str(_ainput[idx0][idx1])+','+_des+",Passive,Default,180 Degrees,"+str(int(xs+_res0*gs))+","+str(ys+_res1*10))            
    _f0.close()
    _i0=0
    _f0 = open('./pins_out.csv', 'w')
    _f0.writelines("display name,designator,electrical type,description,orientation,Location X,Location Y\n")
    for _item in _out_list:
        _f0.writelines(_item+"\n")
        #print(_item+str(_i0*20))
        _i0 += 1
    
    _f0.close()

    
    print("finished\n")
   
    
"""
test
""" 
#список групп, каждая группа в начале имени содержит соответствующий эл-т списка групп 
#_group = {"A","D","Ucc","GND","NC","DP"}

#dictionary {"des": "name"}
#_dict = {"A3": "A0", 
#          "B3": "A1",
#          "A4": "A2",
#          "B4": "A3",
#          "A5": "A4",
#          "B5": "A5",
#          "A6": "A6",
#          "B6": "A7",
#          "A7": "A8",
#          "B7": "A9",
#          "A8": "A10",
#          "B8": "A11",
#          "A9": "A12",
#          "B9": "A13",
#          "B10": "A14",
#          "A10": "A15",
#          "M5": "A16",
#          "M4": "A17",
#          "L4": "A18",
#          "L3": "A19",
#          "M3": "A20",
#          "L9": "nBW0",
#          "M9": "nBW1",
#          "L10": "nBW2",
#          "M10": "nBW3",
#          "L5": "ADV/nLD",
#          "L6": "nWE",
#          "L7": "CLK",
#          "L8": "nCE1",
#          "M8": "CE2",
#          "K8": "nCE3",
#          "M6": "nОE",
#          "M7": "nCEN",
#          "F1": "D0",
#          "F2": "D1",
#          "E1": "D2",
#          "E2": "D3",
#          "D1": "D4",
#          "D2": "D5",
#          "C2": "D6",
#          "C1": "D7",
#          "G2": "D8",
#          "G1": "D9",
#          "H2": "D10",
#          "H1": "D11",
#          "J2": "D12",
#          "J1": "D13",
#          "K2": "D14",
#          "K1": "D15",
#          "F11": "D16",
#          "F12": "D17",
#          "E11": "D18",
#          "E12": "D19",
#          "D11": "D20",
#          "D12": "D21",
#          "C11": "D22",
#          "C12": "D23",
#          "G12": "D24",
#          "G11": "D25",
#          "H12": "D26",
#          "H11": "D27",
#          "J12": "D28",
#          "J11": "D29",
#          "K11": "D30",
#          "K12": "D31",
#          "D3": "DP0",
#          "K3": "DP1",
#          "C10": "DP2",
#          "J10": "DP3",
#          "K5": "MODE",
#          "C9": "TDO",
#          "C8": "TDI",
#          "C4": "TMS",
#          "C5": "TCK",
#          "K9": "SHDN",
#          "B1": "Ucc",
#          "B12": "Ucc",
#          "C6": "Ucc",
#          "C7": "Ucc",
#          "D6": "Ucc",
#          "E4": "Ucc",
#          "E10": "Ucc",
#          "F4": "Ucc",
#          "F9": "Ucc",
#          "F10": "Ucc",
#          "G3": "Ucc",
#          "G4": "Ucc",
#          "G9": "Ucc",
#          "H3": "Ucc",
#          "H9": "Ucc",
#          "J7": "Ucc",
#          "K6": "Ucc",
#          "K7": "Ucc",
#          "L1": "Ucc",
#          "L12": "Ucc",
#          "A1": "GND",
#          "A2": "GND",
#          "A11": "GND",
#          "B2": "GND",
#          "B11": "GND",
#          "D4": "GND",
#          "D5": "GND",
#          "D7": "GND",
#          "D8": "GND",
#          "D9": "GND",
#          "D10": "GND",
#          "E3": "GND",
#          "E5": "GND",
#          "E6": "GND",
#          "E7": "GND",
#          "E8": "GND",
#          "E9": "GND",
#          "F3": "GND",
#          "F5": "GND",
#          "F6": "GND",
#          "F7": "GND",
#          "F8": "GND",
#          "G5": "GND",
#          "G6": "GND",
#          "G7": "GND",
#          "G8": "GND",
#          "G10": "GND",
#          "H4": "GND",
#          "H5": "GND",
#          "H6": "GND",
#          "H7": "GND",
#          "H8": "GND",
#          "H10": "GND",
#          "J3": "GND",
#          "J4": "GND",
#          "J5": "GND",
#          "J6": "GND",
#          "J8": "GND",
#          "J9": "GND",
#          "K4": "GND",
#          "L2": "GND",
#          "L11": "GND",
#          "M2": "GND",
#          "M11": "GND",
#          "M12": "GND",
#          "A12": "NC",
#          "C3": "NC",
#          "K10": "NC",
#          "M1": "NC"
#         }


#work folder
#IC dictionary
#list items of group
#xs -> begin X pos
#ys -> begin Y pos
#gs -> gap betweeen group   
#ggs -> gap in group     
#holdy -> max pins by Y
#_pack -> type of input file: package.csv or package_out.csv 
#pins_bga("d:/_temp",_dict,_group,-900,-900,400,100,10,_package.PACKAGE_FILL)


