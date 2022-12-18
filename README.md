# futbot22
A basic reddit bot designed to scrap football player stats from Transfermarkt.com

# Use

Right now it only works on r/test because the account doesnt have karma so reddit limits posts to one every 10 minutes

to retrieve the basic stats of the current season of a player using this command structure

**-stats [player name]**

examples:

**-stats messi**

**-stats mbappe**

the bot will first make a search in transfermarkt to try to retrieve the URL from the first player on the list then access the player page and get the basic stats

you can also compare players by using the following structure

**-stats [player name] -v [player name]**

example:

**-stats messi -v erling haaland**

Haven't tested how it works with retired players yet
