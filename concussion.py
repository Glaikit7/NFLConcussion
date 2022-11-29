
# Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import re

# Read in the data
dfconc = pd.read_csv(r'C:\Users\crae1\Documents\GWG\NFL Concussion\NFL_concussion\concussionNFL.csv')

# Search for missing data
def missing_data_search():
    for col in dfconc.columns:
        percentage_missing = np.mean(dfconc[col].isnull())
        print('{} - {}%'.format(col, percentage_missing))
missing_data_search()

# Drop rows with incomplete data
dfconc = dfconc[dfconc['Reported Injury Type'].notna()]
dfconc = dfconc[dfconc['Games Missed'].notna()]
dfconc = dfconc[dfconc['Play Time After Injury'].notna()]
dfconc = dfconc[dfconc['Average Playtime Before Injury'].notna()]

missing_data_search()

# Filter data only for players that suffered a concussion
dfconc = dfconc[dfconc['Reported Injury Type'] == 'Concussion']


# List all positions in df
print(dfconc.Position.unique())

# Replace position names with abbreviations
dfconc = dfconc.replace('Wide Receiver', 'WR')
dfconc = dfconc.replace('Offensive Tackle', 'OT')
dfconc = dfconc.replace('Center', 'C')
dfconc = dfconc.replace('Guard', 'OG')
dfconc = dfconc.replace('Tight End', 'TE')
dfconc = dfconc.replace('Defensive End', 'DE')
dfconc = dfconc.replace('Running Back', 'RB')
dfconc = dfconc.replace('Safety', 'S')
dfconc = dfconc.replace('Comerback', 'CB')
dfconc = dfconc.replace('Linebacker', 'LB')
dfconc = dfconc.replace('Defensive Tackle', 'DT')
dfconc = dfconc.replace('Quarterback', 'QB')
dfconc = dfconc.replace('Full Back', 'FB')

# Change dtypes of play time columns and rename them, 'Did not return from injury' now has a value of 1000
dfconc['Play Time After Injury'] = dfconc['Play Time After Injury'].str.replace(r'Did not return from injury', '1000')
dfconc['Play Time After Injury'] = dfconc['Play Time After Injury'].str.replace(r' downs', '').astype(int)
dfconc['Average Playtime Before Injury'] = dfconc['Average Playtime Before Injury'].str.replace(r' downs', '').astype(float)

dfconc.rename(columns={'Play Time After Injury' : 'downs_after_injury', 'Average Playtime Before Injury' : 'mean_downs_before_injury', 'Player' : 'nameFull'}, inplace=True, errors='raise')

# Read in the data
dfcomb = pd.read_csv(r'C:\Users\crae1\Documents\GWG\NFL Concussion\NFL_concussion\combine.csv')

# Search for missing data
def missing_data_search():
    for col in dfcomb.columns:
        percentage_missing = np.mean(dfcomb[col].isnull())
        print('{} - {}%'.format(col, percentage_missing))
missing_data_search()


# Drop rows with missing data
dfcomb = dfcomb[dfcomb['nameFirst'].notna()]
dfcomb = dfcomb[dfcomb['nameLast'].notna()]
dfcomb = dfcomb[dfcomb['nameFull'].notna()]
dfcomb = dfcomb[dfcomb['position'].notna()]
dfcomb = dfcomb[dfcomb['collegeId'].notna()]
dfcomb = dfcomb[dfcomb['nflId'].notna()]
dfcomb = dfcomb[dfcomb['college'].notna()]
dfcomb = dfcomb[dfcomb['heightInches'].notna()]
dfcomb = dfcomb[dfcomb['weight'].notna()]
dfcomb = dfcomb[dfcomb['dob'].notna()]
dfcomb = dfcomb[dfcomb['ageAtDraft'].notna()]
missing_data_search()

# List all positions in df
print(dfcomb.position.unique())

# Refactor position ids to match concussion.csv
dfcomb = dfcomb.replace('DB', 'CB')
dfcomb = dfcomb.replace('LS', 'C')
dfcomb = dfcomb.replace('OLB', 'LB')
dfcomb = dfcomb.replace('OL', 'OG')
dfcomb = dfcomb.replace('DL', 'DT')


dfcomb.to_excel(r'C:\Users\crae1\Documents\GWG\NFL Concussion\NFL_concussion\comb.xlsx', index=False)

# Create a merged df with players that are concussed on dfconc and players that are on dfcomb and sort values
dfcommon = dfcomb.merge(dfconc, on=['nameFull'])
dfcommon = pd.read_csv(r'C:\Users\crae1\Documents\GWG\NFL Concussion\NFL_concussion\common.csv')

dfcommon = dfcommon.sort_values(by='position', ascending=True)
dfcomb = dfcomb.sort_values(by='position', ascending=True)

# Initialise list of pos
positions = ['C', 'RB', 'CB', 'LB', 'OG', 'OT', 'QB', 'DT', 'S', 'FB', 'WR', 'TE']

# Iterate through list and compare height and weight 
for pos in positions:
    avgh = np.mean(dfcomb['heightInches'].where(dfcomb['position'] == pos))
    avgconch = np.mean(dfcommon['heightInches'].where(dfcommon['position'] == pos))
    avgw = np.mean(dfcomb['weight'].where(dfcomb['position'] == pos))
    avgconcw = np.mean(dfcommon['weight'].where(dfcommon['position'] == pos))
    print('mean weight in the NFL for {}s is {} lbs mean weight of concussed players {} lbs'.format(pos + '\'', avgw, avgconcw))
    print('mean height in the NFL for {}s is {} in mean height of concussed players {} in'.format(pos + '\'', avgh, avgconch))

# Create summary df for concussion and NFL groups
heightavgNFL = dfcomb.groupby('position')['heightInches'].mean
heightavgdf = dfcommon.groupby('position')['heightInches'].mean
weightavgNFL = dfcomb.groupby('position')['weight'].mean
weightavgdf = dfcommon.groupby('position')['weight'].mean


# Plot height
bar_width = 0.10
ax = heightavgNFL().plot(kind='bar', align='edge', title='Mean NFL Height vs Mean Concussed Height', ylabel='Height (in)', xlabel='Position', width=bar_width, figsize=(16,8), color='r',label='NFL')
heightavgdf().plot(kind='bar', ax=ax, align='edge', title='Mean NFL Height vs Mean Concussed Height', ylabel='Height (in)', xlabel='Position', width=-bar_width, figsize=(16,8), color='b',label='Concussion Group')
plt.legend(loc='lower right')

# Plot weight
bar_width = 0.10
ax = weightavgNFL().plot(kind='bar', align='edge', title='Mean NFL Weight vs Mean Concussed Weight', ylabel='Weight (lbs)', xlabel='Position', width=bar_width, figsize=(16,8), color='r',label='NFL')
weightavgdf().plot(kind='bar', ax=ax, align='edge', title='Mean NFL Weight vs Mean Concussed Weight', ylabel='Weight (lbs)', xlabel='Position', width=-bar_width, figsize=(16,8), color='b',label='Concussion Group')
plt.legend(loc='lower right')