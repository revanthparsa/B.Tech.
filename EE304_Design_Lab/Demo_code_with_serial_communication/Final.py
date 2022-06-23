import sys
import numpy as np
import fileinput
import serial
import csv
import math
####################       Modifying the gerber fileand Generating a text file       ##################################
with open("copper_top_rand1.gbr","r") as input:
    with open("rand_2.txt","w") as output: 
        for line in input:
            for p in line:
                if p =='X':
                    output.write(line)
                else:
                    break            
for i, line in enumerate(fileinput.input('rand_2.txt', inplace=1)):
    sys.stdout.write(line.replace('D02*', ' 0'))  
for i,line in enumerate(fileinput.input('rand_2.txt',inplace=1)):
    sys.stdout.write(line.replace('D01*',' 1'))
for i, line in enumerate(fileinput.input('rand_2.txt', inplace=1)):
    sys.stdout.write(line.replace('X', ''))  
for i,line in enumerate(fileinput.input('rand_2.txt',inplace=1)):
    sys.stdout.write(line.replace('Y',' '))
xco=[]
yco=[]
zco=[]
with open('rand_2.txt','r') as f:
    reader = csv.reader(f,delimiter=' ')
    for row in reader:
        xco.append(row[0])
        yco.append(row[1])
        zco.append(row[2])

arduino= serial.Serial('/dev/ttyACM0',9600)   #This line should be updated every time after checking the Arduino port  

####################### Generating another text file in a way that a Robot can draw  ##################################
with open('rand_1.txt','w') as out:
    for s in range(0,len(xco)):
        xco[s]=float(xco[s])/1000.0
        yco[s]=float(yco[s])/1000.0
    for s in range(1,len(xco)):
        p = (float(xco[s])-float(xco[s-1]))
        q = (float(yco[s])-float(yco[s-1]))
        rxco = []
        ryco = []
        rzco = []
        # cheking wheather anyone is Zero or both are Zero  
        #Print is used to verify which loop code enters.In Print the first charcter represent wheather p >/< q.
        #second and third represent wheather p >/< 0(zero),similarly fourth and fifth for q.
        #remaining characters represent fractional part ratio(d) is zero(#d0) or not(#d!0)  
        if p != 0 and q != 0:#If both not are not zero enter this loop
                    #Here we get 'SIXTEEN(16)' cases with sign of p,q and largest among p,q and fractional part of the ratio of p,q#
                    if p >0 and q>0:
                        if p<q: 
                            e = float(q/p)
                            i=0
                            z = math.modf(e)
                            d = z[0]
                            if d!=0:######## case 1 ##########
                                while i <= (p-1):
                                    rzco = zco[s]
                                    out.write(str(int(rzco)))
                                    out.write(' ')
                                    rxco = 1
                                    out.write(str(int(rxco)))
                                    out.write(' ')
                                    ryco = math.floor(e)
                                    out.write(str(int(ryco)))
                                    out.write(' ')
                                    out.write('\n')
                                    arduino.write(str(int(rzco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(rxco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(ryco)))
                                    arduino.write('\n')
                                    d = d+z[0]
                                    if d > 1 :
                                        out.write(str(int(rzco)))
                                        out.write(' ')
                                        out.write('0 ')
                                        out.write('1 ')
                                        arduino.write(str(int(rzco)))
                                        arduino.write(' ')
                                        arduino.write(str(int(rxco)))
                                        arduino.write(' ')
                                        arduino.write(str(int(ryco)))
                                        arduino.write('\n')
                                        d = d-1
                                        out.write('\n')
                                    i = i+1
                                print(i)
                                print('<p>q>d!0')
                            else:######## case 2 ##########
                                    rzco = zco[s]
                                    out.write(str(int(rzco)))
                                    out.write(' ')
                                    rxco = 1
                                    out.write(str(int(rxco)))
                                    out.write(' ')
                                    ryco = math.floor(e)
                                    out.write(str(int(ryco)))
                                    out.write(' ')
                                    out.write('\n')
                                    arduino.write(str(int(rzco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(rxco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(ryco)))
                                    arduino.write('\n')
                                    print('<p>q>d0')
                        else:                              
                            e = float(p/q)
                            i=0
                            z = math.modf(e)
                            d = z[0]
                            if d!=0:######## case 3 ##########
                                while i <=(q-1):
                                    rzco = zco[s]
                                    out.write(str(int(rzco)))
                                    out.write(' ')
                                    rxco = math.floor(e)
                                    out.write(str(int(rxco)))
                                    out.write(' ')
                                    ryco = 1
                                    out.write(str(int(ryco)))
                                    out.write(' ')
                                    out.write('\n')
                                    d = d+z[0]
                                    arduino.write(str(int(rzco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(rxco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(ryco)))
                                    arduino.write('\n')
                                    if d > 1 :
                                        out.write(str(int(rzco)))
                                        out.write(' ')
                                        out.write('1 ')
                                        out.write('0 ')
                                        d = d-1
                                        arduino.write(str(int(rzco)))
                                        arduino.write(' ')
                                        arduino.write(str(int(rxco)))
                                        arduino.write(' ')
                                        arduino.write(str(int(ryco)))
                                        arduino.write('\n')
                                        out.write('\n')
                                    i = i+1
                                print(i)
                                print('>p>q>d!0')
                            else:   ######## case 4 ##########
                                    rzco = zco[s]
                                    out.write(str(int(rzco)))
                                    out.write(' ')
                                    rxco = math.floor(e)
                                    out.write(str(int(rxco)))
                                    out.write(' ')
                                    ryco = 1
                                    out.write(str(int(ryco)))
                                    out.write(' ')
                                    out.write('\n')
                                    arduino.write(str(int(rzco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(rxco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(ryco)))
                                    arduino.write('\n')
                                    print('>p>q>d0')
                    elif p >0 and q<0:
                        if p<abs(q):
                            e = float(abs(q/p))
                            i=0
                            z = math.modf(e)
                            d = z[0]
                            if d!=0:######## case 5 ##########
                                while i <= (p-1):
                                    rzco = zco[s]
                                    out.write(str(int(rzco)))
                                    out.write(' ')
                                    rxco = 1
                                    out.write(str(int(rxco)))
                                    out.write(' ')
                                    ryco = math.floor(e)
                                    out.write(str(int(-ryco)))
                                    out.write(' ')
                                    out.write('\n')
                                    d = d+z[0]
                                    arduino.write(str(int(rzco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(rxco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(ryco)))
                                    arduino.write('\n')
                                    if d > 1 :
                                        out.write(str(int(rzco)))
                                        out.write(' ')
                                        out.write('0 ')
                                        out.write('-1 ')
                                        d = d-1
                                        arduino.write(str(int(rzco)))
                                        arduino.write(' ')
                                        arduino.write(str(int(rxco)))
                                        arduino.write(' ')
                                        arduino.write(str(int(ryco)))
                                        arduino.write('\n')
                                        out.write('\n')
                                    i = i+1
                                print(i)
                                print('<p>q<d!0')
                            else:   ######## case 6 ##########
                                    rzco = zco[s]
                                    out.write(str(int(rzco)))
                                    out.write(' ')
                                    rxco = 1
                                    out.write(str(int(rxco)))
                                    out.write(' ')
                                    ryco = math.floor(e)
                                    out.write(str(int(-ryco)))
                                    out.write(' ')
                                    out.write('\n')
                                    arduino.write(str(int(rzco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(rxco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(ryco)))
                                    arduino.write('\n')
                                    print('<p>q<d0')
                        else:
                            e = float(p/abs(q))
                            i=0
                            z = math.modf(e)
                            d = z[0]
                            if d!=0:######## case 7 ##########
                                while i <= (abs(q)-1):
                                    rzco = zco[s]
                                    out.write(str(int(rzco)))
                                    out.write(' ')
                                    rxco = math.floor(e)
                                    out.write(str(int(rxco)))
                                    out.write(' ')
                                    ryco = -1
                                    out.write(str(int(ryco)))
                                    out.write(' ')
                                    out.write('\n')
                                    d = d+z[0]
                                    arduino.write(str(int(rzco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(rxco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(ryco)))
                                    arduino.write('\n')
                                    if d > 1 :
                                        out.write(str(int(rzco)))
                                        out.write(' ')
                                        out.write('1 ')
                                        out.write('0 ')
                                        d = d-1
                                        arduino.write(str(int(rzco)))
                                        arduino.write(' ')
                                        arduino.write(str(int(rxco)))
                                        arduino.write(' ')
                                        arduino.write(str(int(ryco)))
                                        arduino.write('\n')
                                        out.write('\n')
                                    i = i+1
                                print(i)
                                print('>p>q<d!0')
                            else:   ######## case 8 ##########
                                    rzco = zco[s]
                                    out.write(str(int(rzco)))
                                    out.write(' ')
                                    rxco = math.floor(e)
                                    out.write(str(int(rxco)))
                                    out.write(' ')
                                    ryco = -1
                                    out.write(str(int(ryco)))
                                    out.write(' ')
                                    out.write('\n')
                                    arduino.write(str(int(rzco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(rxco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(ryco)))
                                    arduino.write('\n')
                                    print('>p>q<d0')
                    elif p <0 and q>0:
                        if abs(p)<abs(q):
                            e = float(abs(q/p))
                            i=0
                            z = math.modf(e)
                            d = z[0]
                            if d!=0:######## case 9 ##########
                                while i <= (abs(p)-1):
                                    rzco = zco[s]
                                    out.write(str(int(rzco)))
                                    out.write(' ')
                                    rxco = -1
                                    out.write(str(int(rxco)))
                                    out.write(' ')
                                    ryco = math.floor(e)
                                    out.write(str(int(ryco)))
                                    out.write(' ')
                                    out.write('\n')
                                    d = d+z[0]
                                    arduino.write(str(int(rzco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(rxco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(ryco)))
                                    arduino.write('\n')
                                    if d > 1 :
                                        out.write(str(int(rzco)))
                                        out.write(' ')
                                        out.write('0 ')
                                        out.write('1 ')
                                        d = d-1
                                        arduino.write(str(int(rzco)))
                                        arduino.write(' ')
                                        arduino.write(str(int(rxco)))
                                        arduino.write(' ')
                                        arduino.write(str(int(ryco)))
                                        arduino.write('\n')
                                        out.write('\n')
                                    i = i+1
                                print(i)
                                print('<p<q>d!0')
                            else:   ######## case 10 ##########
                                while i <= (abs(p)-1):
                                    rzco = zco[s]
                                    out.write(str(int(rzco)))
                                    out.write(' ')
                                    rxco = -1
                                    out.write(str(int(rxco)))
                                    out.write(' ')
                                    ryco = math.floor(e)
                                    out.write(str(int(ryco)))
                                    out.write(' ')
                                    out.write('\n')
                                    d = d+z[0]
                                    #print(d)
                                    if d > 1 :
                                        out.write(str(int(rzco)))
                                        out.write(' ')
                                        out.write('0 ')
                                        out.write('1 ')
                                        d = d-1
                                        out.write('\n')
                                    i = i+1
                                print(i)
                                print('<p<q>d0')
                        else:       
                            e = float(abs(p)/abs(q))
                            i=0
                            z = math.modf(e)
                            d = z[0]
                            if d!=0:######### case 11 ##########
                                while i <= (q-1):
                                    rzco = zco[s]
                                    out.write(str(int(rzco)))
                                    out.write(' ')
                                    rxco = math.floor(e)
                                    out.write(str(int(-rxco)))
                                    out.write(' ')
                                    ryco = 1
                                    out.write(str(int(ryco)))
                                    out.write(' ')
                                    out.write('\n')
                                    d = d+z[0]
                                    arduino.write(str(int(rzco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(rxco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(ryco)))
                                    arduino.write('\n')
                                    if d > 1 :
                                        out.write(str(int(rzco)))
                                        out.write(' ')
                                        out.write('-1 ')
                                        out.write('0 ')
                                        d = d-1
                                        arduino.write(str(int(rzco)))
                                        arduino.write(' ')
                                        arduino.write(str(int(rxco)))
                                        arduino.write(' ')
                                        arduino.write(str(int(ryco)))
                                        arduino.write('\n')
                                        out.write('\n')
                                    i = i+1
                                print(i)
                                print('>p<q>d!0')
                            else:   ######## case 12 ##########
                                    rzco = zco[s]
                                    out.write(str(int(rzco)))
                                    out.write(' ')
                                    rxco = math.floor(e)
                                    out.write(str(int(-rxco)))
                                    out.write(' ')
                                    ryco = 1
                                    out.write(str(int(ryco)))
                                    out.write(' ')
                                    out.write('\n')
                                    arduino.write(str(int(rzco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(rxco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(ryco)))
                                    arduino.write('\n')
                                    print('>p<q>d0')
                    else:
                        if abs(p)<abs(q):
                            e = float(abs(q/p))
                            i=0
                            z = math.modf(e)
                            d = z[0]
                            if d!=0:######## case 13 ##########
                                while i <= (abs(p)-1):
                                    rzco = zco[s]
                                    out.write(str(int(rzco)))
                                    out.write(' ')
                                    rxco = -1
                                    out.write(str(int(rxco)))
                                    out.write(' ')
                                    ryco = math.floor(e)
                                    out.write(str(int(-ryco)))
                                    out.write(' ')
                                    out.write('\n')
                                    d = d+z[0]
                                    arduino.write(str(int(rzco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(rxco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(ryco)))
                                    arduino.write('\n')
                                    if d > 1 :
                                        out.write(str(int(rzco)))
                                        out.write(' ')
                                        out.write('0 ')
                                        out.write('-1 ')
                                        d = d-1
                                        out.write('\n')
                                        arduino.write(str(int(rzco)))
                                        arduino.write(' ')
                                        arduino.write(str(int(rxco)))
                                        arduino.write(' ')
                                        arduino.write(str(int(ryco)))
                                        arduino.write('\n')
                                    i = i+1
                                print(i)
                                print('<p<q<d!0')
                            else:   ######## case 14 ##########
                                    rzco = zco[s]
                                    out.write(str(int(rzco)))
                                    out.write(' ')
                                    rxco = -1
                                    out.write(str(int(rxco)))
                                    out.write(' ')
                                    ryco = math.floor(e)
                                    out.write(str(int(-ryco)))
                                    out.write(' ')
                                    out.write('\n')
                                    arduino.write(str(int(rzco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(rxco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(ryco)))
                                    arduino.write('\n')
                                    print('<p<q<d0')
                        else:
                            e = (abs(p)/abs(q))
                            i=0
                            z = math.modf(e)
                            d = z[0]
                            if d !=0:######## case 15 ##########
                                while i <= (abs(q)-1):
                                    rzco = zco[s]
                                    out.write(str(int(rzco)))
                                    out.write(' ')
                                    rxco = math.floor(e)
                                    out.write(str(int(-rxco)))
                                    out.write(' ')
                                    ryco = -1
                                    out.write(str(int(ryco)))
                                    out.write(' ')
                                    out.write('\n')
                                    d = d+z[0]
                                    arduino.write(str(int(rzco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(rxco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(ryco)))
                                    arduino.write('\n')
                                    if d > 1 :
                                        out.write(str(int(rzco)))
                                        out.write(' ')
                                        out.write('-1 ')
                                        out.write('0 ')
                                        d = d-1
                                        arduino.write(str(int(rzco)))
                                        arduino.write(' ')
                                        arduino.write(str(int(rxco)))
                                        arduino.write(' ')
                                        arduino.write(str(int(ryco)))
                                        arduino.write('\n')
                                        out.write('\n')
                                    i = i+1
                                print(i)
                                print('>p<q<d!0')
                            else:    ######## case 16 ##########
                                    rzco = zco[s]
                                    out.write(str(int(rzco)))
                                    out.write(' ')
                                    rxco = math.floor(e)
                                    out.write(str(int(-rxco)))
                                    out.write(' ')
                                    ryco = -1
                                    out.write(str(int(ryco)))
                                    out.write(' ')
                                    out.write('\n')
                                    arduino.write(str(int(rzco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(rxco)))
                                    arduino.write(' ')
                                    arduino.write(str(int(ryco)))
                                    arduino.write('\n')
                                    print('>p<q<d0')
        elif p==0 and q ==0:###if both are zeros enter this loop
            print('p0q0')
        else:##### if any one is Zero enter this loop
            i =0
            ### Here we get FOUR(4) cases any one is zero and sign of the other
            if p == 0:
                if q>0:######## case 1 #############
                    while i <= q:
                        rzco = zco[s]
                        out.write(str(int(rzco)))
                        out.write(' ')
                        rxco = 0
                        out.write(str(int(rxco)))
                        out.write(' ')
                        ryco = 1
                        out.write(str(int(ryco)))
                        out.write(' ')
                        out.write('\n')
                        i = i+1
                        arduino.write(str(int(rzco)))
                        arduino.write(' ')
                        arduino.write(str(int(rxco)))
                        arduino.write(' ')
                        arduino.write(str(int(ryco)))
                        arduino.write('\n')
                    print(i)
                    print('p0q>0')
                else:    ######## case 2 #############
                    while i <= abs(q):
                        rzco = zco[s]
                        out.write(str(int(rzco)))
                        out.write(' ')
                        rxco = 0
                        out.write(str(int(rxco)))
                        out.write(' ')
                        ryco = -1
                        out.write(str(int(ryco)))
                        out.write('\n')
                        i = i+1
                        arduino.write(str(int(rzco)))
                        arduino.write(' ')
                        arduino.write(str(int(rxco)))
                        arduino.write(' ')
                        arduino.write(str(int(ryco)))
                        arduino.write('\n')
                    print(i)
                    print('p0q<0')   
            else:
                if p>0:######## case 3 #############
                    while i <= p:
                        rzco = zco[s]
                        out.write(str(int(rzco)))
                        out.write(' ')
                        rxco = 1
                        out.write(str(int(rxco)))
                        out.write(' ')
                        ryco = 0
                        out.write(str(int(ryco)))
                        out.write(' ')
                        out.write('\n')
                        i = i+1
                        arduino.write(str(int(rzco)))
                        arduino.write(' ')
                        arduino.write(str(int(rxco)))
                        arduino.write(' ')
                        arduino.write(str(int(ryco)))
                        arduino.write('\n')
                    print(i)
                    print('p>0q0')
                else:    ######## case 4 #############
                    while i <= abs(p):
                        rzco = zco[s]
                        out.write(str(int(rzco)))
                        out.write(' ')
                        rxco = -1
                        out.write(str(int(rxco)))
                        out.write(' ')
                        ryco = 0
                        out.write(str(int(ryco)))
                        out.write('\n')
                        i = i+1
                        arduino.write(str(int(rzco)))
                        arduino.write(' ')
                        arduino.write(str(int(rxco)))
                        arduino.write(' ')
                        arduino.write(str(int(ryco)))
                        arduino.write('\n')
                    print(i)
                    print('p<0q0')   
    out.write('0 ')
    out.write('0 ')
    out.write('0 ')
    out.write('\n')
    arduino.write(str(int(rzco)))
    arduino.write(' ')
    arduino.write(str(int(rxco)))
    arduino.write(' ')
    arduino.write(str(int(ryco)))
    arduino.write('\n')
