# KBB Outline

-----

This document outlines the processes of the KBB discord bot.
It contains the following sections:

 1. Interface Programming
    1. Class Object
    2. On Events
    3. Class Functions
 2. Modules for the Bot
    1. Message Building
    2. Tasks and Multithreading
    3. Database Interfaces
 3. Commands

-----

## 1. Interface Programming

*i. Class Object*

The bot is programmed using a main interface that controls all other actions.
The file `main.py` is used for this.
A class object is created and used to run all aspects of the bot.
By using `discord.py`, a module to help with bot APIs, KBB is written with fewer functions.
The KBB object shall have the following variables to aid in all functions.
These are public and can be modified.

 + `tasks` - for any tasks created by commands.
 + `data_access_locks` - to prevent over stepping within database access.
 + `database` - allows access to the DynamoDB database.

*ii. On Events*

After the bot has been logged into discord, initialization occurs.
Static files such as items and texts are loaded in and stored in variables for quick access.
Certain actions shall execute a function in the bot's class.
For example, when a message is send, it will check for a user issued command in the text.
If found it parses and executes that command.
More on this in the Commands (3) section.
When a reaction is added to a message, it checks the message ID for matches in the `tasks` variable.
If such a task does exist it will try to add that reaction to the task.

*iii. Class Functions*

Certain functions are done within the class object as they are used through out multiple commands.
The following functions are available for commands to use.
For more information about each function, examine the `main.py` file.

 + `draw_boyfriend`
 + `draw_girlfriend`
 + `draw_relationship`
 + `_add_hearts`
 + `random_item`
 + `_add_item`

-----

## 2. Modules for the Bot

*i. Message Building*

An embedded discord message may be built by using the `bot_utils.Message` class object.
It takes in the following parameters: `title, user, content, task, fields, image_path, footer, footer_icon`.
Only the title, user, and content are required fields.
This message object is created and then returned to the bot's main interface where it will assemble the message and send it through the discord channel.
If fields need to be added, one should use the `MessageFields` class object.
This object takes in a tuples or lists with a size of 2 for each field in the message.
The first index (0) is the name of the field, while the second (1) is the value.

*ii. Tasks and Multithreading*

A message may need to have user interaction to be successful.
To aid in this, there are tasks.
Tasks allow reactions to be added to the embedded message send in discord and execute certain code based on what reaction was added.
A message may contain only one task, however, a task may contain multiple conditions, or reactions.
The following are parameters of the Task class object: `self, conditions, users_list, whitelist, expires`.
A task condition is an instance of the `TaskCondition` object.
Task conditions contain the following parameters: `self, emoji, callback`.
Everything after this is either an argument or key word argument that is passed to the callback on a successful condition.
A callback shall take in a message object which is the specified message that the task is attached to.
Everything after that is the arguments and keyword arguments passed in from the initialization of the task condition.

*iii. Database Interfaces*

To store data about each user there is a DynamoDB setup.
Connection to this database is done through the `database_manager.py` file.
Indexed by `user_id` as an Integer, each user contains the values `relationships`, and `inventory`.
The following commands can be used from the DatabaseManager class.

 + `get_user(user_id)`
 + `new_user(user_id)`
 + `put_user(user_id, user=None, relationships=None, inventory=None)`

-----

## 3. Commands

The following is a list of commands with a short description of what it does.
If the command is highlighted in green it is complete and fully implemented.
Orange commands are being worked on, but not completed.
Red is for commands that have not been started but are planned.

 + <fin>help</fin> - shows a short help message with each available command.
 + <fin>bf</fin> - draws a k-pop boyfriend to give the user if it has been at least 24 hours since the last given relationship.
 + <fin>gf</fin> - draws a k-pop girlfriend to give the user if it has been at least 24 hours since the last given relationship.
 + <fin>view [person]</fin> - views the user's current relationship; if a person is specified, view their current relationship.
 + <fin>flirt</fin> - flirt with your current relationship for a chance at 0-3 hearts.
 + <fin>marry [hearts]</fin> - ask your current relationship to marry you; at least 25 hearts must be given up to attempt this.
 + <fin>talk</fin> - your relationship will tell you a pickup line.
 + <fin>time</fin> - displays how much time is left until you can flirt and claim a new relationship.
 + <fin>pickup [line]</fin> - try to gain hearts based on a pickup line you write, the community votes on how it is.
 + <fin>items</fin> - display your current inventory.
 + <fin>open</fin> - open a mystery box if you currently have one.
 + <fin>vote</fin> - vote for KBB and earn rewards!
 + <nst>prefix [prefix]</nst> - change the command prefix for KBB

<style>
li>ol>li{
    list-style-type:lower-roman;
}
fin{
    color:green;
}
inc{
    color:orange;
}
nst{
    color:red;
}
</style>