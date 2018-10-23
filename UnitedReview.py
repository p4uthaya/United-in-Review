# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 22:49:12 2018

@author: Prabha
"""
###  United 17/18 Stats  ###
 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Read data
data=pd.read_csv('1718 United.csv', sep=',',header=None)
print(data)

# Data Frame to Arrays 
data = data.values
col = data[0]
data = data.transpose()

# Constants
num = len(data)        # number of columns 
col = col              # column names
print(col)

### Categories ####
var = {} # Dictionary of all columns 
for i in range(num):
    var[col[i]] = data[i][1:num]

# Converting the numeric column entries to floats
for i in range(5,num):
    # Skipping the Apps column due to its formatting : 25(3)
    if i == 7:
        continue
    else:
        var[col[i]] = [float(x) for x in var[col[i]]]
        
# Splitting Name into First and Last
        
ent = len(var['Name']) # number of entries (rows)        
var['Last'] = np.copy(var['Name']) # copied name to maintain same datatype

for i in range(ent): 
    fl = var['Name'][i].split()
    
    # The De Gea Clause
    if len(fl)>= 3:
        var['Last'][i] = fl[-2]+' '+fl[-1]
    else:
        var['Last'][i] = fl[-1]
    
# Splitting App data into starts and subs
        
var['Starts'] = np.copy(var['Name'])
var['Subs'] = np.copy(var['Name'])


for i in range(ent):
    temp = var['Apps'][i].split('(') # 25(3) ---> [25, 3)]
    
    if len(temp) == 1:
        var['Starts'][i] = int(temp[0])
        var['Subs'][i] = 0
    else:
        temp2 = temp[1].split(')')  # 3) ---> [3, ]
        var['Starts'][i] = int(temp[0]) 
        var['Subs'][i] = int(temp2[0])

var['Appstot'] = np.copy(var['Starts']) + np.copy(var['Subs'])

# Position Splitting

def countpos (array):
    temp = np.zeros(4) # [fwd, mid, def, gk]
    for i in range(len(array)):
        if array[i] == 'FW' :
            temp[0] += 1
        elif array[i] == 'GK':
            temp[3] += 1
        elif (array[i]== 'M(D)') or (array[i]== 'M(C)') or (array[i]== 'M(R)') or (array[i]== 'M(L)'):
            temp[1] +=1
        else:
            temp[2] +=1
    return temp


posno = countpos(var['Position'])

fwd = np.copy(var['Name'])[0:int(posno[0])]
mid = np.copy(var['Name'])[0:int(posno[1])]
dfn = np.copy(var['Name'])[0:int(posno[2])]
gkp = np.copy(var['Name'])[0:int(posno[3])]

c = np.zeros(4, dtype=int) # counter for each position [fwd, mid, def, gk]
for i in range(len(var['Last'])):
    if var['Position'][i] == 'FW':
        fwd[c[0]] = var['Last'][i]
        c[0] += 1
    elif var['Position'][i] == 'GK':
        gkp[c[3]] = var['Last'][i]
        c[3] += 1
    elif var['Position'][i] == 'M(D)' or var['Position'][i] == 'M(C)' or var['Position'][i] == 'M(L)' or var['Position'][i] == 'M(R)':
        mid[c[1]] = var['Last'][i]
        c[1] += 1
    else:
        dfn[c[2]] = var['Last'][i]
        c[2] += 1

print('Forwards:', fwd)
print('Midfielders:', mid)
print('Defender:', dfn)
print('Keepers:', gkp)

'''

Plots

'''

# Minutes 

#   Sorting by Minutes
dfmin = pd.DataFrame({'Players':var['Last'],
                     'Mins':var['Mins']}, index = var['Last'])
dfmin = dfmin.sort_values('Mins')

plt.figure(figsize=(11, 8))
ax=dfmin.Mins.plot(kind='barh', color='red', width=0.8)

for i in ax.patches:
    ax.text(i.get_width()+ 15, i.get_y()+ 0.19, str(int(i.get_width())))

plt.ylabel('Players')
plt.xlabel('Minutes')
plt.xlim(0,3500)
plt.title('Minutes Played')
plt.savefig('United Mins Played.png', dpi = 500)
plt.show()

# Games 

#   Sorting by Total Apps
dfgms = pd.DataFrame({'Players':var['Last'],
                      'Starts':var['Starts'],
                      'Subs':var['Subs'],
                      'Tot':var['Appstot'],
                      'Apps':var['Apps']},index = var['Last'])
dfgms = dfgms.sort_values('Tot')

plt.figure(figsize=(11, 8))
st = dfgms.Starts.plot(kind='barh', color='red', width=0.8, legend= True)
su = dfgms.Subs.plot(kind='barh', color= 'black', left=dfgms.Starts,
                     width=0.8, legend= True, stacked=True)


count = 0 
for i in st.patches:
    if count == 27:
        break
    else:
        st.text(i.get_width()+dfgms.Subs[count]+0.25 , i.get_y()+ 0.19, 
                dfgms.Apps[count], color='black',)
        count +=1

plt.title('Games Played')
plt.ylabel('Players')
plt.xlabel('Number of Games')
plt.xlim(0,40)
plt.savefig('United Games Played.png', dpi = 500)
plt.show()

# Goalscorers

dfgls = pd.DataFrame({'Players':var['Last'],
                      'Goals':var['Goals']}, index = var['Last'])
dfgls = dfgls.sort_values('Goals')

plt.figure()
gls = dfgls.iloc[13:27].Goals.plot(kind='barh', color='red',width=0.8)

for i in gls.patches:
    gls.text(i.get_width()+0.25 , i.get_y()+ 0.19, str(int(i.get_width())))
plt.title('Goals Scored by Player')
plt.ylabel('Players')
plt.xlabel('Number of Goals')
plt.xlim(0,18)
plt.savefig('United Goals.png', dpi = 500)
plt.show()

# Assists

dfast = pd.DataFrame({'Players':var['Last'],
                      'Assists':var['Assists']}, index = var['Last'])
dfast = dfast.sort_values('Assists')

plt.figure()
ast = dfast.iloc[15:27].Assists.plot(kind='barh', color='black',width=0.8)

for i in ast.patches:
    ast.text(i.get_width()+0.25 , i.get_y()+ 0.19, str(int(i.get_width())))

plt.title('Assists by Player')
plt.ylabel('Players')
plt.xlabel('Number of Assists')
plt.xlim(0,11)
plt.savefig('United Assists.png', dpi = 500)
plt.show()

# Dicipline

var['Cardtot'] = np.copy(var['Yellow Cards'])
for i in range(len(var['Cardtot'])):
    var['Cardtot'][i] = int(var['Yellow Cards'][i]) + int(var['Red Cards'][i])
dfdpl = pd.DataFrame({'Players':var['Last'],
                      'Yellows':var['Yellow Cards'],
                      'Reds':var['Red Cards'],
                      'Tot':var['Cardtot']}, index = var['Last'])

dfdpl = dfdpl.sort_values('Tot').iloc[7:27]

plt.figure(figsize=(8, 6))
yc = dfdpl.Yellows.plot(kind='barh', color='gold', 
                       width=0.8, legend= True)
rc = dfdpl.Reds.plot(kind='barh', color='red', left = dfdpl.Yellows,
                     width=0.8, legend= True, stacked=True)

count = 0 
for i in yc.patches:
    if count == 20:
        break
    else:
        if int(dfdpl.Reds[count]) == 0:
            yc.text(i.get_width()+dfdpl.Reds[count]+0.075 , i.get_y(),
                    str(int(dfdpl.Yellows[count])),color='black')
        else:
            yc.text(i.get_width()+dfdpl.Reds[count]+0.075, i.get_y(), 
                str(int(dfdpl.Yellows[count]))+'+'+str(int(dfdpl.Reds[count])), 
                color='black')
        count +=1

plt.title('Match Discipline: Card Totals')
plt.ylabel('Players')
plt.xlabel('Number of Cards')
plt.xlim(0,7.5)
plt.savefig('United Cards.png', dpi = 500)
plt.show()


# Forwards Stats  

nfwd = len(fwd)  # Number of forward players
fgls = np.zeros(nfwd)
fast = np.zeros(nfwd)
fsht = np.zeros(nfwd)
fkps = np.zeros(nfwd)
fdrb = np.zeros(nfwd)
ftrb = np.zeros(nfwd)

for i in range(len(fwd)):
    for j in range(num-1):
        if fwd[i] == var['Last'][j]:
            fgls[i] = round((var['Goals'][j]/var['Mins'][j])*90,2)   # goals per 90 min
            fast[i] = round((var['Assists'][j]/var['Mins'][j])*90,2) # assists per 90 min
            fsht[i] = var['Shots pG'][j]
            fkps[i] = var['Key Pass pG'][j]
            fdrb[i] = var['Dribbles pG'][j]
            ftrb[i] = var['Through Balls pG'][j]
        
        else:
            continue

# Plots

dfoff = pd.DataFrame({'Players':fwd,
                      'Goals':fgls,
                      'Shots':fsht,
                      'Assists':fast,
                      'Key_Passes':fkps,
                      'Dribbles':fdrb,
                      'Through_Balls':ftrb}, index = fwd)


# Goals and Assists per 90 min (same plot)
ga = dfoff.plot(kind ='bar',
                y=['Goals','Assists'],
                color=['red','black'],
                figsize=(10,8))

for tick in ga.get_xticklabels():
    tick.set_rotation(0)
for i in ga.patches:
    # The Ibra Clause
    if i.get_height() == 0.0:
        continue
    else:
        ga.text(i.get_x()+0.02, i.get_height()+0.002, str(i.get_height()))
plt.title('Goals and Assist per 90 minutes')
plt.xlabel('Players') 
plt.xticks()
plt.show()

#Shots per Game
plt.figure(figsize=(8, 6))
shots = dfoff.Shots.plot(kind='barh',
                         color = 'black')

for i in shots.patches:
    shots.text(i.get_width()+0.02 , i.get_y()+ 0.19, str(i.get_width()))
plt.title('Shots per Game')
plt.ylabel('Players')

#Key Passes per Game
plt.figure(figsize=(8, 6))
keyp = dfoff.Key_Passes.plot(kind='barh',
                              color = 'red')

for i in keyp.patches:
    keyp.text(i.get_width()+0.02 , i.get_y()+ 0.19, str(i.get_width()))
plt.title('Key Passes per Game')
plt.ylabel('Players')

# Dribbles per Game
plt.figure(figsize=(8, 6))
drib = dfoff.Dribbles.plot(kind='barh',
                              color = 'black')

for i in drib.patches:
    if i.get_width() == 0.0:
        continue
    else:
        drib.text(i.get_width()+0.02 , i.get_y()+ 0.19, str(i.get_width()))

plt.title('Dribbles per Game')
plt.ylabel('Players')

# Through Passes per Game
plt.figure(figsize=(8, 6))
thru = dfoff.Through_Balls.plot(kind='barh',
                              color = 'red')

for i in thru.patches:
    if i.get_width() == 0.0:
        continue
    else:
        thru.text(i.get_width()+0.002 , i.get_y()+ 0.19, str(i.get_width()))
plt.title('Through Balls per Game')
plt.ylabel('Players') 


# Defenders Stats 

ndfn = len(dfn)  # Number of forward players
dtkl = np.zeros(ndfn)
dint = np.zeros(ndfn)
dclr= np.zeros(ndfn)
dblk = np.zeros(ndfn)
dfls = np.zeros(ndfn)

for i in range(len(dfn)):
    for j in range(num-1):
        if dfn[i] == var['Last'][j]:
            dtkl[i] = var['Tackles pG'][j]
            dint[i] = var['Interceptions pG'][j]
            dclr[i] = var['Clearances pG'][j]
            dblk[i] = var['Blocks pG'][j]
            dfls[i] = var['Fouls pG'][j]
        
        else:
            continue

# Plots

dfdfn = pd.DataFrame({'Players':dfn,
                      'Tackles':dtkl,
                      'Interceptions':dint,
                      'Clearances':dclr,
                      'Blocks':dblk,
                      'Fouls':dfls}, index = dfn)

#Tackles per Game 
plt.figure(figsize=(8, 6))
sort = dfdfn.sort_values('Tackles')
tackles = sort.Tackles.plot(kind='barh',
                             color = 'black')

for i in tackles.patches:
    if i.get_width() == 0.0:
        continue
    else:
        tackles.text(i.get_width()+0.02 , i.get_y()+ 0.19, str(i.get_width()))
plt.title('Tackles per Game')
plt.ylabel('Players')

#Interceptions per Game 
plt.figure(figsize=(8, 6))
sort = dfdfn.sort_values('Interceptions')
inter = sort.Interceptions.plot(kind='barh',
                                 color = 'red')

for i in inter.patches:
    if i.get_width() == 0.0:
        continue
    else:
        inter.text(i.get_width()+0.02 , i.get_y()+ 0.19, str(i.get_width()))
plt.title('Interceptions per Game')
plt.ylabel('Players')

#Clearances per game 
plt.figure(figsize=(8, 6))
sort = dfdfn.sort_values('Clearances')
clear = sort.Clearances.plot(kind='barh',
                              color = 'black')

for i in clear.patches:
    if i.get_width() == 0.0:
        continue
    else:
        clear.text(i.get_width()+0.02 , i.get_y()+ 0.19, str(i.get_width()))
plt.title('Clearances per Game')
plt.ylabel('Players')

# Blocks per Game
plt.figure(figsize=(8, 6))
sort = dfdfn.sort_values('Blocks')
block = sort.Blocks.plot(kind='barh',
                          color = 'red')

for i in block.patches:
    if i.get_width() == 0.0:
        continue
    else:
        block.text(i.get_width()+0.02 , i.get_y()+ 0.19, str(i.get_width()))
plt.title('Blocks per Game')
plt.ylabel('Players')

# Fouls per Game
plt.figure(figsize=(8, 6))
sort = dfdfn.sort_values('Fouls')
foul = sort.Fouls.plot(kind='barh',
                                 color = 'black')

for i in foul.patches:
    if i.get_width() == 0.0:
        continue
    else:
        foul.text(i.get_width()+0.02 , i.get_y()+ 0.19, str(i.get_width()))
plt.title('Fouls per Game')
plt.ylabel('Players')

print (mid)





# 'Name' 'Squad Number' 'Date of Birth' 'Nationality' 'Position'
# 'Height (cm)' 'Weight (kg)' 'Apps' 'Mins' 'Goals' 'Assists'
# 'Yellow Cards' 'Red Cards' 'Shots pG' 'Key Pass pG' 'Dribbles pG'
# 'Passes pG' 'Pass Percentage' 'Crosses pG' 'Long Balls pG'
# 'Through Balls pG' 'Tackles pG' 'Interceptions pG' 'Fouls pG'
# 'Offsides pG' 'Clearances pG' 'Blocks pG' 'Own Goals'
'''
Things to do :
    
    Sorting bar plots (gotta use data frames godammit) DONE
    Data labels DONE
    Position Splitting DONE
    
    Plots to make
        goals DONE
        assists DONE
        Dicipline (red and yellow) DONE
        offensive stats (FW) shots, key pass, dribbles, offsides DONE
        Defensive stats (M) Fouls, intereceptions, tackles clearances DONE
          ---> sort these too 
'''

# trying to make a function for the plotting 
#def plotter(name, col):
#    plt.figure(figsize=(8, 6))
#    temp = dfdfn.name.plot(kind='barh',
#                             color = col)
#    for i in temp.patches:
#        if i.get_width() == 0.0:
#            continue
#        else:
#            tem.text(i.get_width()+0.02 , i.get_y()+ 0.19, str(i.get_width()))
#    plt.title(str(name),' per Game')
#    plt.ylabel('Players')
#
#plotter(Tackles,'red')
