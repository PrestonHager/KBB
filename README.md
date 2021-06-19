# KBB - K-pop Boyfriend Bot

[![Discord Bots](https://top.gg/api/widget/status/812894609289510952.svg)](https://top.gg/bot/812894609289510952)

-----

A discord bot that adds K-pop boyfriends to your server.
Flirt, chat, and create your own pickup lines to make your way into an idol's heart!
This bot features groups such as BTS, NCT, ITZY, Red Velvet, and many more!
Rely on your luck and flirtatious skills to get all your favorite K-Pop idols!

## Commands

 + ;help - shows a help message
 + ;bf - give me a boyfriend
 + ;gf - give me a girlfriend
 + ;xf - give me someone
 + ;view [person] - view the current relationship of someone
 + ;flirt - flirt with your relationship for hearts
 + ;marry [hearts] - ask your relationship to marry you
 + ;talk - talk to your relationship
 + ;time - how much time until the next...
 + ;pickup [line] - try to gain hearts based on the pickup line you wrote (community votes)
 + ;items - view the items in your inventory
 + ;open - open a mystery box if you have one
 + ;vote - vote for KBB and earn rewards!

-----

## Install

Create a `BOT_KEY.txt` file and put your bot key in there.
Set the environment variables for an AWS private and public key to run the DynamoDB table.
This table may need to be set up before it can be used.
Install `discord.py` with `python -m pip install discord.py`.
Then, run the `main.py` file with `python main.py`

## Notes

If you wish to run your own instance of the bot, voting will not work as it is tied to a seperate webhook running through AWS Lambdas.
This lambda is included in the repository but will use a database seperate from the databases being used in the script.
Create your own instance of a DynamoDB before running the bot.
Additionally, set the AWS keys to environment variables otherwise the bot will not be able to access the database.
