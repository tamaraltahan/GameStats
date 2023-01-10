# %%
import requests
import json
import time

# %%
my_id = 1986753
url = 'https://api.opendota.com/api/players/{}/matches?limit=100'.format(my_id)

# %%
# Get the data from the API
r = requests.get(url)

# Convert the data to a JSON object
data = r.json()

# %%
match_ids = []
# Loop through the matches and add the match ids to the list
for match in data:
    match_ids.append(match['match_id'])

# %%
players = []
# Loop through the match ids and get the player ids
for match in match_ids:
    url = 'https://api.opendota.com/api/matches/{}'.format(match)
    time.sleep(1)
    r = requests.get(url)
    data = r.json()
    players.append(data['players'])

# %%
pIDs = []
privatePlayers = 0
# Loop through the player ids and add them to the list
for player in players:
    for p in player:
        if not p['account_id']:
            privatePlayers += 1
        if p['account_id'] and p['account_id'] != my_id and p['account_id'] not in pIDs:
            pIDs.append(p['account_id'])

# %%
WL = {}
#counter = 0
limit = len(pIDs)//4
# Loop through the player ids and get the win/loss
for pID in pIDs:
    #counter += 1
    time.sleep(1)
    # if counter == limit:
    #     counter = 0
    #     time.sleep(20)
    if pID in WL:
        print('{} already in WL'.format(pID))
    url = 'https://api.opendota.com/api/players/{}/wl'.format(pID)
    r = requests.get(url)
    data = r.json()    
    WL[pID] = data


# %%
matchCount = len(match_ids)
playerCount = len(pIDs)
WLcount = len(WL)

# %%
privatePlayers + playerCount

# %%
print(str(matchCount) + ' matches')
print(str(playerCount) + ' player ID\'s')
print(str(WLcount) + ' player ID\'s with win/loss')

# %%
# adds the win/loss to the WL dictionary
for player in WL:
    WL[player]['total'] = WL[player]['win'] + WL[player]['lose']

playerData = WL


# %%
# adds the win percent to the WL dictionary
for player in playerData:
    playerData[player]['winPercent'] = round((playerData[player]['win']/playerData[player]['total'])*100,2)

# %% [markdown]
# playerdata { 
#     win : n,
#     lose: n,
#     total : n,
#     winPercent : n
# }

# %%
accountBuyers = 0
ABList = []

smurfCount = 0
smurfList = []

# %%
avgGames = 0
for player in playerData:
    avgGames += playerData[player]['total']

avgGames //= len(playerData)

print(avgGames)
    

# %%
totalThreshold = avgGames//4.5
winThreshold = 55

for player in playerData:
    if playerData[player]['total'] <= totalThreshold:
        accountBuyers += 1
        ABList.append(player)
        if playerData[player]['winPercent'] >= winThreshold:
            smurfCount += 1
            smurfList.append(player)

# %%
print(totalThreshold)

# %%
print('Suspected number of account buyers: ' + str(accountBuyers))
print('Suspected number of smurfs: ' + str(smurfCount))

# %%
print(smurfList)

# %%
import matplotlib.pyplot as plt
%matplotlib inline

# %%
normal = playerCount - accountBuyers

normalPercent = round((normal/playerCount)*100,2)

explode1 = [0,0.1]
explode2 = [0.1,0]

# %%
actors = plt.pie([accountBuyers,normal],labels=['Account Buyers','Normal'],autopct='%1.1f%%',explode=explode1,shadow=True,startangle=90)

# %%
smurfs = plt.pie([accountBuyers,smurfCount],labels=['Account Buyers','Smurfs'],autopct='%1.1f%%',explode=explode2,shadow=True,startangle=90)

# %% [markdown]
# # Lower Bound

# %%
fig, (AB,SMF) = plt.subplots(1,2,figsize=(10,10)) #ax1,ax2 refer to your two pies
fig.set_facecolor('#f2f2f2')
fig.tight_layout()
fig.subplots_adjust(wspace=0.5)

# 1,2 denotes 1 row, 2 columns - if you want to stack vertically, it would be 2,1
AB.pie([accountBuyers,normal],labels=['Account Buyers','Normal'],autopct='%1.1f%%',explode=explode1,shadow=True,startangle=90)
AB.title.set_text('Account Buyers to normal players')


SMF.pie([accountBuyers,smurfCount],labels=['Account Buyers','Smurfs'],autopct='%1.1f%%',explode=explode2,shadow=True,startangle=90)
SMF.title.set_text('Account Buyers to smurfs')

# %% [markdown]
# # Upper Bound
# 
# Buyers:Smurf Ratio invalid here
# 
# reason is that we're no longer capable of analysis the winrates of all players. Since we're not including an assumption that 1 in four anonymous players are bad actors, we're adding in multiple players with no access to their win rate. The judgement on who is a *smurf* is strictly on winrate, and access to this data does not exist for private profiles, giving us an incomplete dataset

# %%
fig, (ABanon,SMFanon) = plt.subplots(1,2,figsize=(10,10)) #ax1,ax2 refer to your two pies
fig.set_facecolor('#f2f2f2')
fig.tight_layout()
fig.subplots_adjust(wspace=0.5)

# 1,2 denotes 1 row, 2 columns - if you want to stack vertically, it would be 2,1
ABanon.pie([(accountBuyers+privatePlayers)/4,normal],labels=['Account Buyers','Normal'],autopct='%1.1f%%',explode=explode1,shadow=True,startangle=90)
ABanon.title.set_text('Account Buyers to normal players')


SMFanon.pie([accountBuyers+privatePlayers,smurfCount],labels=['Account Buyers','Smurfs'],autopct='%1.1f%%',explode=explode2,shadow=True,startangle=90)
SMFanon.title.set_text('Account Buyers to smurfs')


