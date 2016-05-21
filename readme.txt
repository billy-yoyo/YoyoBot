
%
% CREATED BY:
%      Billyoyo (Will)
% Verion:
%      1.0.1
%
% Recent changes:
%     * fixed the command-checking function as it was slightly broken before
%

Yoyobot's Readme!
Created with discord.py, asyncio, youtube_dl and requests
discord.py is amazing, it was a lot of fun making this bot and this library was incredibly easy to use.

Key features:
    * Fully customizable roles, allowing any combination of commands to be allowed.
    * Easily set up and personalized radio, including custom playlists and a song queue, all using youtube links.
    * Customizable rewards system, to automatically reward users who contribute to the server a lot (or who buy them).
    * Highly versatile Money and XP systems (see !money and !activity)
    * Completely customizable shop for spending money (ties in with rewards system)
    * Plenty of other commands (over 30 base commands, with a grand total of over 75 individual commands)
    * Everything is easily manageable through discord commands, no need to edit any files!
    * Custom commands able to do a variety of things
    * Customizable command names and command prefix (you don't have to use !)
    * Plugin support!

Setting up a bot:

    Before you install it, you need to actually make your bot, so go to
    https://discordapp.com/developers/applications/me
    and click on "new application",
    Then type in your bot name (You can call it something else if you want), add an image if you want and click the create button in the bottom right hand corner.
    Now click the convert to bot button in the application page, and keep your App Bot User Bot ID and Token. You'll need this when you run setup.py

Installation (for windows):
   
    Yoyobot runs on a few things, so I'll try and explain best how to get them.
    First things first, yoyobot makes quite a lot of files and in general presumes it's in its own folder.

    Firstly, install Python 3.4: https://www.python.org/downloads/release/python-343/
    scroll down to the bottom and install the relevant one.

    Yoyobot specifically needs Python 3.4, if you already have another one just install this one and I'll explain how to make it work anyway
    From now on, we're going to be installing things using pip, to make sure you have pip installed open up command prompt (search cmd) and type
        pip -V
    if it errors or nothing comes up, pip isn't installed correctly. It should install with python, so try reinstalling python.
    If pip -V (notice the capital) shows you that you're not running on python 3.4, then you need to use cd to go to where pip is installed, for example:
        cd C:/python34/scripts/
    if you've installed it somewhere else just go to the same scripts folder whever you installed it, if you had to do this then whenever I say do
        pip install x
    instead do
        pip3.4.exe install x

    One more thing before we start, make sure you have git installed (just type git in to cmd)
    if it isn't, download it here https://git-scm.com/download/win

    Now we need to use pip to install a few things:
        pip install git+https://github.com/Rapptz/discord.py@async
        pip install asyncio
        pip install youtube_dl
        pip install requests

    Now you're done with pip there's just one more thing left to install, ffmpeg. First download the package here: (click on your OS first)
    https://ffmpeg.org/download.html (Here's a more direct link for windows: https://ffmpeg.zeranoe.com/builds/)
    Now extract it somewhere convenient (though it doesn't really matter)
    Now we need to add an environment variable for ffmpeg, so search for your system environment variable editor,
    Note how you do this may depend on your windows version so you may have to look up how to do it on yours if it doesn't seem to be working (I'm running win10)
    then click on the environment variables in the bottom right hand corner, then double click on the User variable named PATH,
    then click the new button and paste the directory to your ffmpeg/bin/ folder, for example C:\Code\ffmpeg\bin, and click ok on the 3 windows you've opened.

    Now you're done! As long as everything worked properly, you should be good to go now, just run run.py and follow the instructions to setup yoyo!
    One last thing to note though, you want to make sure you're running run.py with python 3.4 if you have other versions installed, if it
    isn't working and you followed the steps above this is likely the problem. If you don't use .py files for anything else, you can look up
    changing the file association for python (fairly simple), otherwise you're going to want to set up a script which runs run.py with python 3.4 specifically.

USAGE:
    !help [page]                                    - you already know this one, page numbers also work for all help pages in the same way
    !rng                                            - random number generator, do !rng help for usage
    !yoyo <message>                                 - makes yoyo say the message
    !yoyosay <message>                              - makes yoyo tts the message
    !history                                        - shows who's been making yoyo say what (newest to oldest)
    !poke <user>                                    - makes yoyo poke the user
    !uptime                                         - tells you how long yoyo's been alive for
    !song | !radio                                  - song suggestions and radio, do !song help for usage
    !flip | !coin                                   - flips a coin
    !8ball [message]                                - magic 8 ball
    !dice | !die | !roll                            - rolls a 6-sided die
    !nick <user|nickname> [nickname]                - sets the users nickname (for tag), if only one parameter given user is you
    !nickname [user]                                - tells you that user's nickname, if no user given it tells you your nickname
    !tagged                                         - functions for information about the tag-game (see !tag help)
    !msg                                            - lightweight email-type system, see !msg help for help
    !invite                                         - creates an invite to the channel (if yoyobot is allowed to)
    !hangman | !hman                                - !hangman to check progress, !hangman new [word] create new game, random word if none given, !hangman [letter|word] guess a word or a letter, !hangman end to give up
    !activity                                       - see !activity help for commands
    !xkcd [number]                                  - gives the xkcd comic corresponding to that number, chooses a random number if none given
    !cah | !c&h [number]                            - gives the cyanide and happiness comic corersponding to that number, chooses a random number if none given
    !humblebundle | !humble | !hb [bundle-suffix]   - tells you what the current humble bundle is, with the suffix added to the end of the link if supplied
    !img [number]                                   - gets a random image from themetapicture
    !code                                           - links to a pastebin of my code
    !status <gamename> [idle]                       - changes the bots status
    !role                                           - see !role help
    !reward                                         - see !reward help
    !bind add|set|del|get <command> <bind>          - see !bind usage
    !settings set|get <setting> [value]             - used to change yoyobot settings, see !settings get to see a list of settings.
    !custom set|get|del <command> [reward]          - allows you to create custom commands which give whoever uses them the reward. Work with roles, to give access to a command do '+_custom commandname' or '+_custom' for all
    !shop                                           - see !shop usage
    !decide [decision] or [decision] or ...         - randomly chooses a decision for you
    !plugin                                         - see !plugin usage
    !purge <limit> <parameters>                     - purges chat up to the limit of messages, see reward for information on purge parameters


    !rng usage:
        !rng                                        - generates number between 0 and 1
        !rng <number>                               - generates an integer between 0 and number, add f for non-integer
        !rng <lower> <upper>                        - generates integer between lower and upper, add f for non-integer

    BIG NOTE: radio looks for a channel called radio_channel, where it dumps the songs it's currently playing.
              Nothing bad happens (it shouldn't, anyway) if this channel doesn't exist, but it's useful functionality either way.
    !song usage (can sub !radio for !song):
        !song add <songlink>                        - adds a song to the default playlist
        !song add <playlist> <songlink>             - adds a song to that playlist, automatically creates the playlist if it doesn't already exist
        !song del|delete <songlink>                 - deletes a song from the default playlist
        !song del|delete <playlist> <songlink>      - deletes a song from that playlist
        !song [playlists]                           - gives a random song from the given playlists, default if none given, if 'all' given, all playlists selected
        !song playlists                            - gives a list of playlists
        !song connect <channel>                     - makes yoyo join a channel
        !song radio <playlists>                     - starts a radio which randomly plays songs from those playlists, all for all playlists
        !song stop                                  - disconnects yoyo from channel and stops the radio
        !song link                                  - links to the current song playing
        !song skip                                  - votes to skip the current song, need 50% of users listening, rounded up, to skip
        !song q|queue <songlink>                    - queue a song
        !song pause                                 - pause the current song
        !song resume                                - resume the current song
            > example radio:
            >   !song connect general - connects yoyo to the general voice channel, note you should always do this before starting radio, even if yoyo is already in the channel
            >   !song radio all - starts the radio, picking its songs from every playlist
            >   !song radio - changes the radio's playlist to just the default playlist
            >   !song stop - stops the radio and disconnects yoyo from the voice channel
            >   !song connect League of - connects yoyo to the League of Legends voice channel (auto-complete)
            >   !song radio wills random - starts the radio, picking its songs from the "wills" and "random" playlists
            >
            > A note about radio, if multiple links to the same song are in a playlist or collection of playlists, its probability
            > won't be weighted.

    !msg usage:
        !msg send <user> <message> - sends that user a message
        !msg check - checks your messages
        !msg del|delete [indexs] - deletes the given messages, deletes all messages if indexs is left empty, a>b can be given as an index, meaning integers from a to b inclusive
    !tagged usage:
        How tagged works: If you have a !nick nickname, then if whoever's tagged says your nickname (at all) in chat, you get tagged.
        !tagged - shows who's currently tagged (lies if you're tagged!)
        !tagged best - shows the record for the shortest time spend being tagged
        !tagges worst [username] - shows that users longest time spend being tagged, if no user given it shows the server record

    !role usage:",
        !role set <username> <role> - sets that users role
        !role new <role> - creates a new role
        !role check <username> - checks that user's role
        !role - tells you your role
        !role roles - shows you a list of all those roles
        !role get <role> - shows you what permissions that role has
        !role edit <role> <changes> - edits a role, changes are:
           >  +all whitelists all commands | -all presumes access to no commands
           >  +clear clear the whitlist    | -clear clear the blacklist
           >  +[cmd] add cmd to whitelist  | -[cmd] remove cmd from whitelist
           >  commands have there root (e.g. role) and also specific commands (e.g role set), so '+role -role set' will give access to all role commands except role set
           >  *rolename to make it inherit commands (only whitelist) from a role
           > example role: Regular = -all *Normal +song +hman +yoyo - this has access to all the commands Normal has access as well as !song, !hman and !yoyo
           > Also, in most cases where a command accepts no arguments the permission will be '+cmd check'

    !money usage:
        !money set <username> <amount> - sets that users money to that amount
        !money give <username> <amount> - gives that user that amount of money out of thin air
        !money trade <username> <amount> - gives that user that amount of money from their balance, if they can
        !money [username] - checks that users balance, your balance if no name given

    !activity usage:
        !activity add <username> <amount> - gives that username that amount of activity
        !activity set <username> <amount> - sets that username's activity to that amount
        !activity trigger <event> <activity_amount> <reward> - sets that reward to trigger if the user has that amount of activity
        !activity event <event> <amount> [cooldown] - sets the amount of activity rewarded for events
          > events: on_message, on_message_delete, on_member_join, on_member_remove, on_member_update, on_voice_state, on_ban, on_unban, on_typing
        !activity get <event> - checks the amount given and cooldown of an event
        !activity [username] - check that users activity, yours if no username given

    !reward usage:
        !reward set <reward> <commands> - sets that reward's commands (overrides already existing onces)
        !reward edit <reward> <commands> - adds those commands to that reward's commands
        !reward del|delete <reward> <commands> - deletes those commands (if they exist) from that reward's commands
        !reward get <reward> - gets the commands for that reward
        !reward give <username> <reward> - gives that username the given reward
            > reward commands:
            >    yoyo::role::[rolename]                                                             - sets the memebers role to rolename
            >        ::money::give::[amount]                                                        - gives the member that amount of money
            >               ::set::[amount]                                                         - sets that members balance to that amount
            >        ::say::[channel]::[message]                                                    - makes yoyo say that message
            > discord::role::add::[role]                                                            - gives that member that role
            >              ::remove::[role]                                                         - removes that role from that member
            >        ::nickname::[nickname]                                                         - sets the memeber's server nickname
            >        ::mute::[true|false]                                                           - mutes or unmutes the member
            >        ::deafen::[true|false]                                                         - deafens or undeafens the member
            >        ::purge::[channel]::[limit]::[checks]                                          - purges the channel, removing all messages that fulfill the checks up to a limit of limit messages
            >        ::invite::server::[max_age]::[max_uses]::[temporary(true|false)]               - creates a server invite with those settings, max_age is in seconds.
            >                ::channel::[channel]::[max_age]::[max_uses]::[temporary(true|false)]   - same as above to invites to channel instead
            > note: if . is given for [channel], it sets channel to the member's current channel
            >
            > purge checks: (note none of the strings can contain %, sorry!)
            >     %all% - removes all messages
            >     %c%string%c% - removes all messages that contain string, case sensitive
            >     %ic%string%ic% - removes all messages that contain string, not cast sensitive
            >     %nc%string%nc% - removes all messages that don't contain string, case sensitive
            >     %inc%string%inc% - removes all messages that don't contain string, not cast sensitive
            >     %u%string%u% - removes all messages sent by a user who's name matches string not case sensitive
            >     %nu%string%nu% - removes messages not sent by a user who's name matches string not case sensitive
            >
            > example rewards:
            >   discord::purge::.::100::%ic%bye%ic% %inc%hello%inc%  -  would remove all mesages that contain bye and don't contain hello
            >   yoyo::say::general::hello world!                     -  would make yoyobot say hello world!
            >   discord::nickname::YoyoFriend                        -  would set the member's nickname to YoyoFriend
            >   yoyo:money:set:100                                   -  would set the member's money to $100

    !reward shop usage: (used to setup the shop, note 'reward shop' is it's own root command for permissions
        !reward shop add <reward> <price> <category> <name> <short description> - creates and adds an item to a category, also makes the category if it doesn't exist
        !reward shop remove <category> [name] - removes that item from the shop, or that category if no name is given
        !reward shop price <category> <name> <price> - sets that item's price
        !reward shop move <name> <old_category> <new_category> - moves that item from old_category to new_category
        !reward shop hide <true|false> <category> [name] - hides or unhides and item or category from the shop
        !reward shop short <short description> - sets the short description for the item (one line)
        !reward shop long <long description> - sets the long description for the item to that line
        !reward shop long add <line> - adds a line to the long description
        !reward shop long delete|del [line number] - removes that line from the lone description, if no number given the last number is chosen, negative numbers count backwards from the end
        !reward shop info [category] [item] - works in the same way as !shop get [category] [item] except it shows hidden items in square brackets


    !bind usage:
        !bind set <command> <bind> - resets a commands bind so that ONLY this command will work (e.g. '!bind set yoyo say' means you can only do !say <message> instead of !yoyo <message>)
        !bind get <command> - gets all the binds for this command
        !bind add <command> <bind> - adds an extra bind to this command, (e.g. '!bind add yoyo say means' !say <message> and !yoyo <message> will work)
        !bend del|delete <command> <bind> - deletes a specific bind from this comand
        Note: while setting the command_prefix command in settings will update all the help lines, bind won't as a command can have multiple binds.
        So if you've removed a command or rebound it, it will still show up as the base command name. So if you plan on doing that, make sure your users are aware of !bind get <command>

    !shop usage:
        !shop get [collection] [item] - tells you information about that item, or collection if no item given, or returns list of all collections if no collection given
        !shop buy <collection> <item> - buys this item (if you can afford it)

    !plugin usage:
        !plugin install <name> <link> - installs a plugin, link is a raw pastebin link, name is what it will be saved as
        !plugin uninstall <name> - uninstalls a plugin
        !plugin update <name> - updates a plugin if it can (if you use !plugin install it remembers the link used to install it)
        !plugin enable <name> - enabled the plugin
        !plugin disable <name> - disabled the plugin without uninstalling it
        !plugin check <name> - checks whether or not the plugin is enabled or disabled
        !plugin list - lists all the plugins currently loaded
        !plugin reload - reloads all plugins

Other:

    A few things, the code was a bit of a hack-job and so is a bit messy. I'm too far gone to re-do it so I'm making do,
    if you plan on making any changes and want any help feel free to contact me (through github or reddit or whatever) and I'll try give you a hand.
    The same goes for if you have any issues / find any bugs. My friends have tried to stress test this thing but obviously things get through the cracks.

    The hangman file is really weird. I just ripped 3000 words of some random list of words I found. I have some code to ignore certain cases
    so that some of the weird song don't come up, so if you plan on adding some words to it, they must be at least 4 letters long and cannot start with a capital letter.
    also don't put punctuation in the words. It technically shouldn't break it, but it looks confusing. Spaces are fine though.

    If you have any ideas or feedback or you think this is the worst bot ever, please leave me some message somewhere.

    I want to add a plugin-type system and I think it would be fairly simple to do so, except for the fact that it's hard for
    me to pass the data on to a plugin. I store almost everything as global variables. I honestly have no idea how a plugin would interact with them,
    and even if they could interact with them I'd rather they didn't, for a few reasons. If anyone has any good ideas for how I could fix this without
    rewriting my code, I'm all ears.

    Also, tag is a fun game. The fact that you need a nickname means that you can limit it to only people who are commonly on the server.
    The rules that are set in stone are as follows:
        the tagging message cannot be in a private channel
        the user you're tagging must be currently connected to the channel to tag them
        your message must contain their entire tag, though it does not need to be its own word
        your message cannot start with !
        yoyo cannot participate in the game
        messages can't be over 300 characters long
    The extra rules we play by:
        stick to the main chat channel
        don't delete messages
    Also, if you're tagged, !tagged will show you the last person who was tagged, so they won't realise the tag has changed just from that.
    Other than that, it's a free game. We set our nicknames to normal words that don't come up too commonly (like monitor or clutch), the fun
    comes from being creative with your tagging :D

    As a side note, in case anyone is interested how I got the radio to work, here is the list, in order, of problems I ran into:
        > First things first, I didn't install ffmpeg correctly. But that didn't take long to fix
        > Next up, create_ytdl_player kept coming up with a "generator has no module start" or something like that,
        this turns out to be because it was a coroutine despite the docs not listing it as one (I was using outdated docs, the proper ones are hard to find)
        (here's a link to the ones I'm using now https://discordpy.readthedocs.io/en/latest/api.html)
        > Now because ytdl is a coroutine, I have to yield from it, in order for this to work in another function (in my case next_song()),
        this song also has to be yielded from (if you look in !song radio I do yield from start_radio(), which in turn does yield from next_song()).
        > So this was the first turning point, because now a song was actually playing. However now because next_song required to be yielded from,
        if I set after in create_ytdl_player to be next_song it simply wouldn't do anything. I couldn't (and still haven't) found a way to directly solve this.
        > My final solution was to create a seperate loop on start, which checks every 3 seconds to see if the radio is on,
        if it is on then it checks if the song has finished (song_finished variable), if it is then it does yield from next_song().
        I then set after to be finish_song which basically just set song_finished to True.
        So there's a maximum 3 second gap after a song finishing before the next one starts (at least starts downloading).
    Also, I haven't put anything in place to stop it, but if someone adds a youtube playlist to one of the song playlists,
    even if it's a link to a specific song in that playlist, then it downloads and plays every single song in the playlist.
    So use with caution!

    Also, with the xkcd, cyanide and happinness, themetapicture and humblebundle commands they could very easily stop working at any point.
    My method for those commands is to download the webpage, broken up in to lines, then go line by line looking for keywords and finding the
    key information (with xkcd or c&h it's just looking for the img url, with humblebundle it looks for a lot more information). If any of these
    websites significantly change their websites layout these commands could become entirely disfunctional and return gibberish (or more likely, not much at all)
    If they do stop working, I'll try and fix it but it may take me a while to realize, so if you could message me that would be great.

Creating plugins:

    creating a plugin is fairly easy, once you've setup yoyobot just create a python file in the plugins folder with the name of your plugin,
    now your plugin has only one requirement: it must have a setup function, which takes a plugin manager as its only argument.
    Here's an example of a plugin you could make:
        from pluglib import Plugin
        import main

        class MyPlugin(Plugin):
            def __init__(self, plugin_manager, file_name):      #
                self.name = "example_plugin"                    # these four lines
                self.file_name = file_name                      # are very important
                self.plugin_manager = plugin_manager            #
                self.plugin_manager.register_event(self, "on_message")

            def on_message(self, message):
                print(" recieved message " + message.content + ", current command-prefix is " + main.cfix() )
                if "plugin_test" in message.content:
                    yield from self.plugin_manager.client.send_message(message.channel, ">>>PLUGIN TEST<<<")
                return False

        def setup(plugin_manager, file_name):      #  so are these two
            MyPlugin(plugin_manager, file_name)    #

    This would print the message and the command-prefix in to the console every time a message is sent which isn't picked up by yoyobot or another plugin
    Also, if the message contains plugin_test it would write >>>PLUGIN TEST<<< in channel.
    If you return True, it stops the any further plugins accessing the event.

    PluginManager has the following functions:
        plugin_manager.register(plugin, event_list) - calls plugin_manager.register_event for each event in event_list
        plugin_manager.register(plugin, event) - registers the plugin to the plugin_manager
        plugin_manager.plugin_list() - a list of all the loaded plugins
        plugin_manager.plugin_name_list() - a list of all the loaded plugin names
        plugin_manager.get_plugin(plugin_name) - gets a plugin from its name, None if no plugin found with that name (case sensitive)
        plugin_manager.uninstall(plugin_name) - installs that plugin
        plugin_manager.client - the bot's client
    PluginManager also shares all of the event functions with Plugin:
        plugin.on_message(message)
        plugin.on_message_delete(message)
        plugin.on_member_join(member)
        plugin.on_member_remove(member)
        plugin.on_member_update(before, after)
        plugin.on_voice_state_update(before, after)
        plugin.on_member_ban(member)
        plugin.on_member_unban(member)
        plugin.on_typing(channel, user, when)
    These follow the exact conditions and parameters of the corresponding events in the discord.py API (https://discordpy.readthedocs.io/en/latest/api.html)
    That's all there is to it, there are a lot of functions in main, some of which may be more obscure as to their user than others.
    At some point I'll try and document the useful ones but a few key things:

        changing any of the persistent things (for example money), requires you to do the corresponding save function, which should be easy to find as they all start with save_
        to integrate any of your commands with the bind system, do:

            is_command(message.content, "command_name"):

        to integerate any of your commands with the permissions system, do:

            if not check_command(message.author.name, "specific_command", "command_root"):
                yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
            else:
                # Your code

        A useful snippet of code to get the parameters of your command (so !cmd [paramters])

            params = [""]
            if " " in message.content:
                params = message.content[message.content.find(" ")+1:].split(" ")

        params will always contain a string, so if they did an empty command, e.g. !hello, params[0] = "", but if they did !hello world 2, params[0] = "world", params[1] = "2"

        To implement an auto-complete system:

            name = [string].lower()
            member = None
            for mem in message.author.server.members: (or any other list of members)
                if name in mem.name.lower():
                    member = mem
                    break

        returns the member corresponding to name, if they're online.
        You can very similarly construct one to look for channels, using server.channels instead being essentially the only difference!

        A very useful function is

            print_help(list_of_lines, page_number)

        example in use:

            page = 0
            if len(params) > 1:
                page = int(params[1]) - 1
            lines = print_help(shop_help_str, page)
            if lines is not None:
                for line in lines:
                    yield from client.send_message(message.author, line)
            else:
                yield from client.send_message(message.channel, "<SHOP> invalid page!")

         this is the code for !shop help [page].

         Also, a special case for interacting with my functions is add_activity or add_raw_activity (as well as some others but you're less likely to use those, like next_song)
         you muse use them as:
            yield from add_activity(member, origin_channel, act) - act is a activity event name
            yield form add_raw_activity(member, origin_channel, amount) - adds that amount of activity to the player's profile

    One more thing, just so you're aware if the discord.py says the function is a coroutine underneath it, you need to call
        yield from function()
    instead of
        function()

    This includes client.send_message(channel, text) and yield from client.delete_message(message)

