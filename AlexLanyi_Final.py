# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 15:08:23 2020

@author: Alexander L

@data: MIT Election Data and Science Lab, 2018, "countypres_2000-2016.tab",
County Presidential Election Returns 2000-2016, doi.org/10.7910/DVN/VOQCHQ/HEIJCQ,
Harvard Dataverse, V6, UNF:6:ZZe1xuZ5H2l4NUiSRcRf8Q== [fileUNF]
"""
import numpy as np # Numpy
import pandas as pd # Pandas
import matplotlib.pyplot as plt # matplotlib
import scipy.stats # Scipy

# Read file as pandas data frame (election data from outside class research)
df = pd.read_csv('countypres_2000-2016.csv')

# Define colorize function for parties
def partyColorize(party):
    pC=[];
    for x in party:
        if x =='democrat':
            c='b'
        elif x =='republican':
            c='r'               
        elif x =='green':
            c='g'
        else:
            c='y'
        pC.append(c)
    return pC

df['partyColor']=partyColorize(df['party']) # Call colorize function
# Plot data using matplotlib
ax1 = plt.figure().add_subplot(111, projection='3d')
ax1.scatter(
    df['FIPS'],
    df['candidatevotes'],
    df['year'],
    c=df['partyColor'],
    s=1, 
    depthshade=True)
ax1.set_xlabel('FIPS')
ax1.set_ylabel('Votes')
ax1.set_zlabel('Year')
ax1.set_title("Voting Data")

# Statistical analysis
CI=0.999999
df['votePercent']=df['candidatevotes']/df['totalvotes']
df.drop(df[df['votePercent'].isna()==True].index, inplace = True) # Drop nan vote totals
vPCI=scipy.stats.t.interval(CI, len(df['votePercent'])-1, loc=np.mean(df['votePercent']), scale=scipy.stats.sem(df['votePercent']))
print("Vote percent confidence interval",CI,"% :")
print(vPCI)

# Leave behind outliers for analysis
df.drop(df[df['votePercent'].between(vPCI[0], vPCI[1], inclusive=True)].index, inplace = True)

# Plot florida data using matplotlib
fldf = df[df['state']=="Florida"]
ax2 = plt.figure().add_subplot(111, projection='3d')
ax2.scatter(
    fldf['FIPS'],
    fldf['candidatevotes'],
    fldf['year'],
    c=fldf['partyColor'],
    s=1, 
    depthshade=True)
ax2.set_xlabel('FIPS')
ax2.set_ylabel('Votes')
ax2.set_zlabel('Year')
ax2.set_title("Florida Voting Data Outside Vote% CI")

# Export year 2000 from florida
fldf[fldf['year']==2000].to_csv('FilteredFlorida2000.csv')
