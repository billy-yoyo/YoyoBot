from os import listdir
from os.path import isfile, join

import asyncio
import discord
import math
import os
import random
import requests
import setup
import time

from pluglib import *

global plugin_manager
def load_plugins():
    global plugin_manager
    plugin_manager = PluginManager(client)

    onlyfiles = [f for f in listdir("plugins/") if isfile(join("plugins/", f))]
    loaded = 0
    for filename in onlyfiles:
        fname = filename[:-3]
        if "__init__" not in filename and ".py" in filename and not plugin_disabled(fname):
            print("importing " + filename + "...")
            try:
                test = __import__("plugins."+fname, fromlist=["plugins"])
                test.setup(plugin_manager, fname)
                loaded += 1
            except():
                print("ERROR: Failed to import " + filename)
    print("Done, loaded " + str(loaded) + " plugins!")

client = discord.Client()
client.voice = None

global poke_cooldowns, uptime_cooldown, uptime_start, left_messages, hangman_word, hangman_found, hangman_words, hangman_guessed_letters, hangman_tries
global activity, activity_events, activity_cds, activity_triggers, yoyo_code_link, command_binds, custom_commands, settings, plugin_disables
global permissions, command_swaps, user_roles, money_shop, user_money, ball_8, rewards
global msg_history, tag_stats, nickname, nick_players, songs, collections, tagged, old_tagged, radio_channel, current_music_player
global voice_chn, song_list, song_collection, song_finished, recent_songs, skip_votes, song_queue, song_paused, nicknames

def setup_variables():
    global poke_cooldowns, uptime_cooldown, uptime_start, left_messages, hangman_word, hangman_found, hangman_words, hangman_guessed_letters, hangman_tries
    global activity, activity_events, activity_cds, activity_triggers, yoyo_code_link, command_binds, custom_commands, settings, plugin_disables
    global permissions, command_swaps, user_roles, money_shop, user_money, ball_8, rewards
    global msg_history, tag_stats, nickname, nick_players, songs, collections, tagged, old_tagged, radio_channel, current_music_player
    global voice_chn, song_list, song_collection, song_finished, recent_songs, skip_votes, song_queue, song_paused, nicknames
    poke_cooldowns = {}
    uptime_cooldown = 0
    uptime_start = None

    left_messages = {}

    hangman_word = ""
    hangman_found = ""
    hangman_guess = 0
    hangman_guessed_letters = ""
    hangman_tries = 0

    hangman_words = []

    activity = {}
    activity_events = {}
    activity_cds = {}
    activity_triggers = {}

    yoyo_code_link = "http://pastebin.com/2PZARLXu"

    command_binds = {}
    custom_commands = {}

    plugin_disables = {}

    settings = {}

    permissions = {}
    command_swaps = {
        "radio": "song",
        "hangman": "hman",
        "coin": "flip",
        "dice": "roll",
        "die": "roll",
        "c&h": "cah",
        "humble": "hb",
        "humblebundle": "hb"
    }

    user_roles = {}

    money_shop = {}

    ball_8 = [
        "It is certain",
        "It is decidedly so",
        "Without a doubt",
        "Yes, definitely",
        "You may rely on it",
        "As I see it, yes",
        "Most likely",
        "Outlook good",
        "Yes",
        "Signs point to yes",
        "Reply hazy try again",
        "Ask again later",
        "Better not tell you now",
        "Cannot predict now",
        "Concentrate and ask again",
        "Don't count on it",
        "My reply is no",
        "My sources say no",
        "Outlook not so good",
        "Very doubtful"
    ]

    user_money = {}

    rewards = {}

    msg_history = [""] * 10

    tag_stats = {}

    nicknames = {}
    nick_players = []
    songs = {}
    collections = []

    tagged = ""
    old_tagged = ""

    radio_channel = None
    current_music_player = None
    voice_chn = None
    song_list = []
    song_collection = None
    song_finished = False
    recent_songs = []
    skip_votes = []
    song_queue = []
    song_paused = False

def load_plugin_disables():
    f = open("data/plugin_disables.txt", "r")
    for line in f:
        dat = line.replace("\n", "").split("/+++/")
        plugin_disables[dat[0]] = (dat[1].lower() == "true")
    f.close()

def save_plugin_disables():
    f = open("data/plugin_disables.txt", "w")
    for plugin_name in plugin_disables:
        f.write(plugin_name + "/+++/" + str(plugin_disables[plugin_name]) + "\n")
    f.close()

def plugin_disabled(plugin_name):
    if plugin_name in plugin_disables:
        return plugin_disables[plugin_name]
    return False

def load_custom_commands():
    f = open("data/custom_commands.txt", "r")
    for line in f:
        dat = line.replace("\n", "").split("/+++/")
        if dat[0] != "":
            custom_commands[dat[0]] = dat[1]
    f.close()

def save_custom_commands():
    f = open("data/custom_commands.txt", "w")
    for cmd in custom_commands:
        f.write(cmd + "/+++/" + custom_commands[cmd] + "\n")
    f.close()


#max_help_lines - the amount of lines shown in a help page
def mxlns():
    if "max_help_lines" in settings:
        return int(settings["max_help_lines"])
    return 5

#bot_name - the name of the bot in your channel
def botname():
    if "bot_name" in settings:
        return settings["bot_name"]
    return "yoyobot"

#command prefix - what signifies a message is a command
def cfix():
    if "command_prefix" in settings:
        return settings["command_prefix"]
    return "!"

#radio channel - the name of the channel to dump the radio links in
def rchn():
    if "radio_channel" in settings:
        return settings["radio_channel"]
    return "radio_channel"

#radio update rate - the rate at which you check if a song has finished (integer in seconds)
def ruprt():
    if "radio_update_rate" in settings:
        return int(settings["radio_update_rate"])
    return 3

#repeat cap - how many recent songs the radio tries to avoid
def rpcap():
    if "repeat_cap" in settings:
        return int(settings["repeat_cap"])
    return 10

#tag limit - the limit on the size of a message with someones tag in it
def taglimit():
    if "tag_limit" in settings:
        return int(settings["tag_limit"])
    return 300



def welcome(member):
    if get_role(member.name) is None:
        set_role(member.name, "DEFAULT")
        if "welcome_message" in settings:
            msg = settings["welcome_message"]
            if msg != "":
                msg.replace("%name%", member.name).replace("%c%", cfix())
                client.send_message(member, msg)

def load_settings():
    f = open("data/settings.txt", "r")
    for line in f:
        dat = line.replace("\n", "").split("=")
        if dat[0] != "":
            settings[dat[0]] = "=".join(dat[1:])
    f.close()

def save_settings():
    f = open("data/settings.txt", "w")
    for setting in settings:
        f.write(setting + "=" + settings[setting] + "\n")
    f.close()

def save_binds():
    f = open("data/bind.txt", "w")
    for basename in command_binds.keys():
        f.write(basename + "/+++/" + "/+++/".join(command_binds[basename]) + "\n")
    f.close()

def load_binds():
    f = open("data/bind.txt", "r")
    for line in f:
        dat = line.replace("\n", "").split("/+++/")
        if dat[0] != "":
            command_binds[dat[0]] = dat[1:]
    f.close()

def set_bind(basename, bind):
    command_binds[basename] = [bind]
    save_binds()

def add_bind(basename, bind):
    if basename not in command_binds:
        set_bind(basename, bind)
    else:
        command_binds[basename].append(bind)
        save_binds()

def remove_bind(basename, bind):
    if basename in command_binds:
        if bind in command_binds[basename]:
            command_binds[basename].remove(bind)
            return True
    return False

def get_binds(basename):
    if basename in command_binds:
        return ", ".join(command_binds[basename])
    return None

def is_command(msg, basename):
    if basename not in command_binds:
        set_bind(basename, basename)
    for bind in command_binds[basename]:
        cmdstr = cfix() + bind
        if msg.startswith(cmdstr) or msg == cmdstr:
            return True
    return False

def load_hangman_words():
    global hangman_words
    f = open("hangman.txt", "r")
    for line in f:
        line = line.replace("\n", "").replace("\t", "")
        if len(line) > 3:
            if line[0] == line[0].lower():
                line = line.lower()
                hangman_words.append(line)
    f.close()


class Role:
    def __init__(self, name, all, whitelist, blacklist, inher = []):
        self.name = name
        self.all = all
        self.whitelist = whitelist
        self.blacklist = blacklist
        self.inheritence = inher

    def update_inhers(self, roles):
        new_inheritence = []
        for rolename in self.inheritence:
            if rolename in roles:
                new_inheritence.append(roles[rolename])
        self.inheritence = new_inheritence

    def check_inher(self, command, command_root):
        for role in self.inheritence:
            if role.check(command, command_root):
                return True
        return False

    def check(self, command, command_root = ""):
        #print(self.name + " : " + str(self.all) + " : " + str(self.whitelist) + " : " + str(self.blacklist) + " : " + command + " : " + command_root)
        if self.all:
            if not command in self.blacklist and not command_root in self.blacklist or self.check_inher(command, command_root):
                return True
            return False
        else:
            if command in self.whitelist or (command_root in self.whitelist and command not in self.blacklist) or self.check_inher(command, command_root):
                return True
            return False

    def get_all_str(self):
        if self.all:
            return "+all"
        return "-all"

    def get_whitelist_str(self):
        line = ""
        for cmd in self.whitelist:
            line = line + ",+" + cmd
        return line

    def get_blacklist_str(self):
        line = ""
        for cmd in self.blacklist:
            line = line + ",-" + cmd
        return line

    def get_str(self):
        return self.get_all_str() + self.get_whitelist_str() + self.get_blacklist_str()




def load_permissions():
    f = open("data/permissions.txt", "r")
    for line in f:
        spl = line.replace("\n", "").split("=")
        rolename = spl[0]
        tabs = spl[1].split(",")
        role = Role(rolename, False, [], [])
        for tab in tabs:
            prefix = tab[0]
            cmd = tab[1:]
            if cmd in command_swaps:
                cmd = command_swaps[cmd]
            if prefix == "*":
                role.inheritence.append(cmd)
            else:
                if cmd == "all":
                    if prefix == "+":
                        role.all = True
                    elif prefix == "-":
                        role.all = False
                else:
                    if prefix == "+":
                        role.whitelist.append(cmd)
                    elif prefix == "-":
                        role.blacklist.append(cmd)
        permissions[rolename] = role
    f.close()
    for rolename in permissions.keys():
        permissions[rolename].update_inhers(permissions)

def save_permissions():
    f = open("data/permissions.txt", "w")
    for rolename in permissions.keys():
        role = permissions[rolename]
        line = rolename + "=" + role.get_str()
        f.write(line + "\n")
    f.close()

def create_permissions(rolename):
    if rolename not in permissions:
        permissions[rolename] = Role(False, [], [])
        return True
    return False

def change_permissions(rolename, changes):
    if rolename in permissions:
        role = permissions[rolename]
        for change in changes:
            prefix = change[0]
            cmd = change[1:]
            if cmd in command_swaps:
                cmd = command_swaps[cmd]
            if cmd == "all":
                if prefix == "+":
                    role.all = True
                elif prefix == "-":
                    role.all = False
            elif cmd == "clear":
                if prefix == "+":
                    role.whitelist = []
                elif prefix == "-":
                    role.blacklist = []
            else:
                if prefix == "+" and not cmd in role.whitelist:
                    role.whitelist.append(cmd)
                    if cmd in role.blacklist:
                        role.blacklist.remove(cmd)
                elif prefix == "-" and not cmd in role.blacklist:
                    role.blacklist.append(cmd)
                    if cmd in role.whitelist:
                        role.whitelist.remove(cmd)

        return True

    return False




def load_roles():
    f = open("data/roles.txt", "r")
    for line in f:
        spl = line.split("/+++/")
        user_roles[spl[0]] = spl[1].replace("\n", "")
    f.close()


def set_role(user, role):
    if role in permissions:
        user_roles[user] = role
        f = open("data/roles.txt", "w")
        for user in user_roles.keys():
            f.write(user+"/+++/"+user_roles[user]+"\n")
        f.close()
        return True
    return False


def get_role(user):
    role = "DEFAULT"
    if user not in user_roles:
        set_role(user, "DEFAULT")
    else:
        role = user_roles[user]
    if role in permissions:
        return permissions[role]
    return None


def check_command(user, command, command_root=""):
    role = get_role(user)
    if role is not None:
        return role.check(command, command_root)
    return False


global help_str, rng_help_str, song_help_str, msg_help_str, tag_help_str, role_help_str, money_help_str, activity_help_str, reward_help_str, shop_help_str, plugin_help_str
def load_help_str(target, filename):
    f = open(filename, "r")
    for line in f:
        target.append(line.replace("\n", "").replace("%c%", cfix()))
    f.close()


def load_help_strs():
    global help_str, rng_help_str, song_help_str, msg_help_str, tag_help_str, role_help_str, money_help_str, activity_help_str, reward_help_str, shop_help_str, plugin_help_str
    help_str = []
    load_help_str(help_str, "help/help.txt")

    rng_help_str = []
    load_help_str(rng_help_str, "help/rng.txt")

    song_help_str = []
    load_help_str(song_help_str, "help/song.txt")

    msg_help_str = []
    load_help_str(msg_help_str, "help/msg.txt")


    tag_help_str = []
    load_help_str(tag_help_str, "help/tag.txt")

    role_help_str = []
    load_help_str(role_help_str, "help/role.txt")

    money_help_str = []
    load_help_str(money_help_str, "help/money.txt")

    activity_help_str = []
    load_help_str(activity_help_str, "help/activity.txt")

    reward_help_str = []
    load_help_str(reward_help_str, "help/reward.txt")

    shop_help_str = []
    load_help_str(shop_help_str, "help/shop.txt")

    plugin_help_str = []
    load_help_str(plugin_help_str, "help/plugin.txt")



class ShopItem:
    def __init__(self, reward, price, name, short_desc, long_desc, hidden=False):
        self.reward = reward
        self.price = price
        self.name = name
        self.short_desc = short_desc
        self.long_desc = long_desc
        self.hidden = hidden
        if type(self.long_desc) is str:
            self.long_desc = [self.long_desc]

    def set_price(self, price):
        self.price = price

    def set_short(self, desc):
        self.short_desc = desc

    def set_long(self, long):
        self.long_desc = long
        if type(self.long_desc) is str:
            self.long_desc = [self.long_desc]

    def add_long(self, long):
        self.long_desc.append(long)

    def remove_long(self, line):
        if line < 0:
            line = len(self.long_desc) - line
        else:
            line -= 1
        if line < len(self.long_desc):
            del self.long_desc[line]
            return True
        return False

    def get_tagline(self):
        if self.hidden:
            return "["+self.name+"]" + " [$" + str(self.price) + "] - " + self.short_desc
        else:
            return self.name + " [$" + str(self.price) + "] - " + self.short_desc

    def get_long(self):
        return "\n".join(self.long_desc)

    def get_save_str(self):
        long_desc = "/+++/".join(self.long_desc)
        return str(self.hidden) + "/+++/" + self.reward + "/+++/" + str(self.price) + "/+++/" + self.name + "/+++/" + self.short_desc + "/+++/" + long_desc

class Category:
    def __init__(self, name, hidden=False):
        self.name = name
        self.items = {}
        self.hidden = hidden

    def set_hidden(self, hidden, itemname=""):
        if itemname == "":
            self.hidden = hidden
            return True
        else:
            item = self.get_item(itemname)
            if item is not None:
                item.hidden = hidden
                return True
        return False

    def add_item(self, item):
        self.items[item.name] = item

    def remove_item(self, item):
        if item is not None:
            if item.name in self.items:
                del self.items[item.name]
                return True
        return False

    def get_item(self, name):
        name = name.lower()
        for itemname in self.items.keys():
            if name == itemname.lower():
                return self.items[itemname]
        return None

    def move_item(self, item, dest):
        if self.remove_item(item):
            dest.add_item(item)
            return True
        return False

    def set_price(self, name, price):
        item = self.get_item(name)
        if item is not None:
            item.set_price(price)
            return True
        return False

    def set_short(self, name, short):
        item = self.get_item(name)
        if item is not None:
            item.set_short(short)
            return True
        return False

    def set_long(self, name, long):
        item = self.get_item(name)
        if item is not None:
            item.set_long(long)
            return True
        return False

    def add_long(self, name, long):
        item = self.get_item(name)
        if item is not None:
            item.add_long(long)
            return True
        return False

    def remove_long(self, name, line):
        item = self.get_item(name)
        if item is not None:
            return item.remove_long(line)
        return False

def get_item_desc(cat, itemname, show_hidden=False):
    if itemname in cat.items:
        item = cat.items[itemname]
        if item.hidden and not show_hidden:
            return ""
        line = item.get_tagline() + "\n"
        for desc in item.long_desc:
            line = line + "   " + desc + "\n"
        return line
    return None

def get_shop_items(catname, show_hidden = False):
    if catname in money_shop:
        line = ""
        cat = money_shop[catname]
        for itemname in cat.items.keys():
            if not cat.items[itemname].hidden or (cat.items[itemname].hidden and show_hidden):
                line = line + cat.items[itemname].get_tagline()
        return line
    return None

def get_cats(show_hidden=False):
    line = ""
    for catname in money_shop.keys():
        if not money_shop[catname].hidden or (money_shop[catname].hidden and show_hidden):
            cat = catname
            if money_shop[cat].hidden:
                cat = "[" + cat + "]"
            if line == "":
                line = cat
            else:
                line = line + ", " + cat
    return line

def get_items(catname, show_hidden=False):
    if catname in money_shop:
        line = ""
        cat = money_shop[catname]
        for itemname in cat.items.keys():
            if not cat.items[itemname].hidden or (cat.items[itemname].hidden and show_hidden):
                item = itemname
                if cat.items[itemname].hidden:
                    item = "[" + item + "]"
                if line == "":
                    line = item
                else:
                    line = line + ", " + item
        return catname + ": " + line
    return None

def add_item(catname, item):
    if catname not in money_shop:
        money_shop[catname] = Category(catname)
    money_shop[catname].add_item(item)

def load_shop():
    f = open("data/shop.txt", "r")
    for line in f:
        dat = line.replace("\n", "").split("/+++/")
        item = ShopItem(dat[3], int(dat[4]), dat[5], dat[6], dat[7:], dat[2].lower() == "true")
        add_item(dat[0], item)
        money_shop[dat[0]].hidden = (dat[1].lower() == "true")
    f.close()

def save_shop():
    f = open("data/shop.txt", "w")
    for catname in money_shop.keys():
        for itemname in money_shop[catname].items.keys():
            savestr = money_shop[catname].items[itemname].get_save_str()
            f.write(catname + "/+++/" + str(money_shop[catname].hidden) + "/+++/" + savestr + "\n")
    f.close()

def print_help(help_lines, page, max_lines=-1):
    if max_lines == -1:
        max_lines = mxlns()
    pages = math.ceil((len(help_lines) - 1) / max_lines) - 1
    if 0 <= page <= pages:
        lines = ""
        lines = lines + help_lines[0] + " (page " + str(page + 1) + " of " + str(pages + 1) + ")" + "\n"
        for i in range((page * max_lines) + 1, min(len(help_lines), (page * max_lines) + 1 + max_lines)):
            lines = lines + help_lines[i] + "\n"
        return [lines]
    return None




def load_money():
    f = open("data/money.txt", "r")
    for line in f:
        spl = line.replace("\n", "").split("=")
        if spl[0] != "":
            user_money[spl[0]] = int(spl[1])
    f.close()

def save_money():
    f = open("data/money.txt", "w")
    for user in user_money.keys():
        f.write(user+"="+str(user_money[user])+"\n")
    f.close()

def get_money(user):
    if user in user_money:
        return user_money[user]
    return 0

def give_money(user, amount):
    if user not in user_money:
        user_money[user] = amount
        save_money()
        return amount
    else:
        user_money[user] = user_money[user] + amount
        save_money()
        return user_money[user]


def set_money(user, amount):
    user_money[user] = amount
    save_money()

def trade_money(user_from, user_to, amount):
    if get_money(user_from) > amount:
        give_money(user_from, amount)
        give_money(user_to, amount)
        return True
    return False


class Purger:
    def __init__(self, const):
        self.all = False
        self.contains = []
        self.not_contains = []
        self.caps_contains = []
        self.not_caps_contains = []
        self.user = []
        self.not_user = []
        if const == "%all%":
            self.all = True
        else:
            while "%" in const:
                index = const.find("%")
                const = const[index+1:]
                index = const.find("%")
                check_type = const[:index]
                const = const[index+1:]
                index = const.find("%")
                check = const[:index]
                const = const[index+1:]
                index = const.find("%")
                const = const[index+1:]
                if check_type.lower() == "c":
                    self.contains.append(check)
                elif check_type.lower() == "nc":
                    self.not_contains.append(check)
                elif check_type.lower() == "ic":
                    self.caps_contains.append(check.lower())
                elif check_type.lower() == "inc":
                    self.not_caps_contains.append(check.lower())
                elif check_type.lower() == "u":
                    self.user.append(check.lower())
                elif check_type.lower() == "nu":
                    self.not_user.append(check.lower())


    def check(self, message):
        if self.all:
            return True
        for check in self.contains:
            if check in message.content:
                return True
        for check in self.caps_contains:
            if check.lower() in message.content.lower():
                return True
        for check in self.not_contains:
            if check in message.content:
                return False
        for check in self.not_caps_contains:
            if check in message.content.lower():
                return False
        for check in self.user:
            if message.author.name.lower() == check:
                return True
        for check in self.not_user:
            if message.author.name.lower() == check:
                return False
        return True


def load_rewards():
    f = open("data/rewards.txt")
    for line in f:
        dat = line.replace("\n", "").split("/+++/")
        if dat[0] != "":
            rewards[dat[0]] = dat[1:]
    f.close()

def save_rewards():
    f = open("data/rewards.txt", "w")
    for reward in rewards.keys():
        f.write(reward+"/+++/" + "/+++/".join(rewards[reward]) + "\n")
    f.close()

def set_reward(reward, commands):
    rewards[reward] = commands
    save_rewards()

def edit_reward(reward, commands, remove = False):
    result = False
    if remove:
        if reward in rewards:
            for command in commands:
                if command in rewards[reward]:
                    rewards[reward].remove(command)
            result = True
    else:
        if reward in rewards:
            rewards[reward] = rewards[reward] + commands
        else:
            rewards[reward] = commands
        result = True
    save_rewards()
    return result

def remove_reward(reward):
    result = False
    if reward in rewards:
        del rewards[reward]
        result = True
    save_rewards()
    return result

def get_reward(reward):
    if reward in rewards:
        return rewards[reward]
    return None

# C%hello %
global current_reward_checker
current_reward_checker = None
def reward_checker(message):
    if current_reward_checker is not None:
        return current_reward_checker.check(message)
    return False

def use_reward(member, origin_channel, reward_arr):
    if reward_arr is not None:
        for reward in reward_arr:
            data = reward.split("::")
            if data[0] == "yoyo":
                if data[1] == "role":
                    role = data[2]
                    set_role(member.author.name, role)
                elif data[1] == "money":
                    if data[2] == "give":
                        give_money(member.name, int(data[3]))
                    elif data[2] == "set":
                        set_money(member.name, int(data[3]))
                elif data[1] == "say":
                    channel_name = data[2].lower()
                    channel = None
                    if channel_name == ".":
                        channel = origin_channel
                    else:
                        for ch in member.server.channels:
                            if channel_name in ch.name.lower():
                                channel = ch
                                break
                    if channel is not None:
                        message = "::".join(data[3:])
                        yield from client.send_message(channel, message)
            elif data[0] == "discord":
                if data[1] == "role":
                    role = None
                    for r in member.server.roles:
                        if data[3].lower() == r.name.lower():
                            role = r
                            break
                    if role is not None:
                        if data[2] == "add":
                            yield from client.add_roles(member, role)
                        elif data[2] == "remove":
                            yield from client.remove_roles(member, role)
                elif data[1] == "nickname":
                    yield from client.change_nickname(member, " ".join(data[2:]))
                elif data[1] == "mute":
                    mute = False
                    if data[2] == "true":
                        mute = True
                    yield from client.server_voice_state(member, mute=mute)
                elif data[1] == "purge":
                    channel_name = data[2].lower()
                    channel = None
                    if channel_name == ".":
                        channel = origin_channel
                    else:
                        for ch in member.server.channels:
                            if channel_name in ch.name.lower():
                                channel = ch
                                break
                    if channel is not None:
                        limit = int(data[3])
                        global current_reward_checker
                        current_reward_checker = Purger("::".join(data[4:]))

                        yield from client.purge_from(channel, limit=limit, check=reward_checker)
                elif data[1] == "deafen":
                    deafen = False
                    if data[2] == "true":
                        deafen = True
                    yield from client.server_voice_state(member, deafen=deafen)
                elif data[1] == "invite":
                    if data[2] == "server":
                        max_age = 60
                        max_uses = 1
                        temporary = False
                        if len(data) >= 4:
                            max_age = int(data[3])
                        if len(data) >= 5:
                            max_uses = int(data[4])
                        if len(data) >= 6:
                            if data[5] == "true":
                                temporary = True
                        inv = yield from client.create_invite(member.server, max_age=max_age, max_uses=max_uses, temporary=temporary)
                        yield from client.send_message(member, inv.url)
                    elif data[2] == "channel":
                        channel_name = data[3].lower()
                        channel = None
                        if channel_name == ".":
                            channel = origin_channel
                        else:
                            for ch in member.server.channels:
                                if channel_name in ch.name.lower():
                                    channel = ch
                                break
                        if channel is not None:
                            max_age = 60
                            max_uses = 1
                            temporary = False
                            if len(data) >= 3:
                                max_age = int(data[3])
                            if len(data) >= 4:
                                max_uses = int(data[4])
                            if len(data) >= 5:
                                if data[5] == "true":
                                    temporary = True
                            inv = yield from client.create_invite(channel, max_age=max_age, max_uses=max_uses, temporary=temporary)
                            yield from client.send_message(member, inv.url)
    return True




def create_current_dat():
    ts = time.localtime()
    return DandT(ts.tm_yday, ts.tm_year, ts.tm_hour, ts.tm_min, ts.tm_sec)


class DandT:
    def __init__(self, d, y, h, m, s):
        self.day = int(d)
        self.year = int(y)
        self.hour = int(h)
        self.m = int(m)
        self.sec = int(s)

        self.user = None

    def get(self, i):
        if i == 0:
            return self.sec
        elif i == 1:
            return self.m
        elif i == 2:
            return self.hour
        elif i == 3:
            return self.day
        elif i == 4:
            return self.year
        else:
            return 0

    def set(self, i, v):
        if i == 0:
            self.sec = v
        elif i == 1:
            self.m = v
        elif i == 2:
            self.hour = v
        elif i == 3:
            self.day = v
        elif i == 4:
            self.year = v

    def max(self, i):
        if i == 0:
            return 60
        elif i == 1:
            return 60
        elif i == 2:
            return 24
        elif i == 3:
            return 365
        elif i == 4:
            return -1
        else:
            return 0

    def clone(self):
        return DandT(self.day, self.year, self.hour, self.m, self.sec)

    def greaterthan(self, dat):
        if self.year > dat.year:
            return True
        elif self.year == 0:
            if self.day > dat.dat:
                return True
            elif self.day == 0:
                if self.hour > dat.hour:
                    return True
                elif self.hour == 0:
                    if self.m > dat.min:
                        return True
                    elif self.m == 0:
                        if self.sec > dat.sec:
                            return True
        return False

    def minus(self, dat):

        temp = dat.clone()
        result = DandT(0, 0, 0, 0, 0)
        for i in range(5):
            v1, v2 = self.get(i), temp.get(i)
            if v2 > v1:
                if i == 4:
                    return None
                result.set(i, (self.max(i) - v2) + v1)
                temp.set(i + 1, temp.get(i + 1) + 1)
            else:
                result.set(i, v1 - v2)
        # print( "["+self.full_format() + "] : [" + dat.full_format() +"] : [" + result.full_format() + "]")
        return result

    def cformat(self, form):
        return form.replace("%Y", str(self.year)).replace("%d", str(self.day)).replace("%H", str(self.hour)).replace(
            "%M", str(self.m)).replace("%S", str(self.sec))

    def clever_format(self):
        form = ""
        if self.year > 0:
            form = form + str(self.year) + " years "
        if self.day > 0 or form != "":
            form = form + str(self.day) + " days "
        if self.hour > 0 or form != "":
            form = form + str(self.hour) + " hours "
        if self.m > 0 or form != "":
            form = form + str(self.m) + " minutes "
        if self.sec > 0 or form != "":
            form = form + str(self.sec) + " seconds "
        return form

    def full_format(self):
        form = str(self.year) + " years " + str(self.day) + " days " \
               + str(self.hour) + " hours " + str(self.m) + " minutes " + str(self.sec) + " seconds"
        return form

    def full_quick_format(self):
        return self.cformat("%d/%Y at %H:%M:%S")

    def save_format(self):
        return self.cformat("%Y/+++/%d/+++/%H/+++/%M/+++/%S")


def add_user_record(name, dat):
    if "user_record" not in tag_stats:
        tag_stats["user_record"] = {}
    tag_stats["user_record"][name.lower()] = dat


def get_user_record(name):
    if "user_record" in tag_stats:
        if name in tag_stats["user_record"]:
            return tag_stats["user_record"][name]
    return None


def load_tag_stats():
    f = open("data/tag_stats.tag", "r")
    for ln in f:
        line = ln.replace("\n", "")
        if line != "":
            sp = line.split("/+++/")
            if sp[0] == "last_tag":
                tag_stats["last_tag"] = DandT(sp[1], sp[2], sp[3], sp[4], sp[5])
            elif sp[0] == "record_longest":
                dat = DandT(sp[2], sp[3], sp[4], sp[5], sp[6])
                dat.user = sp[1]
                tag_stats["record_longest"] = dat
            elif sp[0] == "user_record":
                add_user_record(sp[1], DandT(sp[2], sp[3], sp[4], sp[5], sp[6]))
            elif sp[0] == "record_shortest":
                dat = DandT(sp[2], sp[3], sp[4], sp[5], sp[6])
                dat.user = sp[1]
                tag_stats["record_shortest"] = dat

    f.close()


def save_tag_stats():
    f = open("data/tag_stats.tag", "w")
    if "last_tag" in tag_stats:
        f.write("last_tag/+++/" + tag_stats["last_tag"].save_format() + "\n")
    if "record_longest" in tag_stats:
        dat = tag_stats["record_longest"]
        f.write("record_longest/+++/" + dat.user + "/+++/" + dat.save_format() + "\n")
    if "record_shortest" in tag_stats:
        dat = tag_stats["record_shortest"]
        f.write("record_shortest/+++/" + dat.user + "/+++/" + dat.save_format() + "\n")
    if "user_record" in tag_stats:
        urs = tag_stats["user_record"]
        for user in urs.keys():
            f.write("user_record/+++/" + user + "/+++/" + urs[user].save_format() + "\n")
    f.close()


def finish_song():
    global song_finished, skip_votes, song_list, song_collection
    song_finished = True
    skip_votes = []
    if song_collection is not None:
        song_list = get_songlist(song_collection)


def next_song():
    global song_list, current_music_player, voice_chn, radio_channel, song_finished, recent_songs, song_queue, song_paused

    print(str(song_list))
    if len(song_list) > 0:
        if voice_chn is not None:
            song = None
            if len(song_queue) > 0:
                song = song_queue[0]
                song_queue.remove(song)
            else:
                iter_cap = 0
                while song in recent_songs and iter_cap < 20:
                    song = song_list[random.randint(0, len(song_list) - 1)]
                    iter_cap += 1
                recent_songs.append(song)
                if len(recent_songs) > rpcap():
                    recent_songs.remove(recent_songs[0])
            if song is not None:
                current_music_player = yield from voice_chn.create_ytdl_player(song, after=finish_song)
                song_finished = False
                song_paused = False
                if radio_channel is not None:
                    secs = current_music_player.duration
                    mins = math.floor(secs / 60)
                    secs -= (mins * 60)
                    strsecs = str(secs)
                    if len(strsecs) == 1:
                        strsecs = "0" + strsecs
                    yield from client.send_message(radio_channel,
                                                   "<SONG> Playing song: " + current_music_player.title + " [" + str(
                                                       mins) + ":" + strsecs + "] ")
                    yield from client.send_message(radio_channel, song)
                else:
                    print(" no radio channel! ")
                game = discord.Game()
                game.name = current_music_player.title
                yield from client.change_status(game, False)
                current_music_player.start()
        else:
            current_music_player = None
            song_list = []
            print("failed")
    else:
        print("uber-failed")


def start_radio(colls):
    global song_list, voice_chn, song_collection
    if voice_chn is not None:
        song_collection = colls
        song_list = get_songlist(colls)
        yield from next_song()


def tag_player(name):
    global tagged, old_tagged
    old_tagged = tagged
    tagged = name
    f = open("data/tag.tag", "w")
    f.write(name + "\n")
    f.write(old_tagged)
    f.close()

    lt = None
    if "last_tag" in tag_stats:
        lt = tag_stats["last_tag"]
    if lt is None:
        tag_stats["last_tag"] = create_current_dat()
    else:
        newdt = create_current_dat()
        elap = newdt.minus(lt)
        elap.user = old_tagged
        record = get_user_record(old_tagged)
        if record is None:
            add_user_record(name, elap)
        elif elap.greaterthan(record):
            add_user_record(name, elap)
        if "record_longest" in tag_stats:
            longest = tag_stats["record_longest"]
            if elap.greaterthan(longest):
                tag_stats["record_longest"] = elap
        else:
            tag_stats["record_longest"] = elap
        if "record_shortest" in tag_stats:
            shortest = tag_stats["record_shortest"]
            if shortest.greaterthan(elap):
                tag_stats["record_shortest"] = elap
        else:
            tag_stats["record_shortest"] = elap
        tag_stats["last_tag"] = newdt
    save_tag_stats()


def load_tag():
    global tagged, old_tagged
    f = open("data/tag.tag", "r")
    for line in f:
        if line != "" and line != "\n":
            if tagged == "":
                tagged = line.replace("\n", "")
            elif old_tagged == "":
                old_tagged = line.replace("\n", "")
                break
    f.close()


def add_collection(collection):
    songs[collection] = []
    collections.append(collection)
    f = open("data/collections.txt", "w")
    for col in collections:
        f.write(col + "\n")
    f.close()


def add_song(collection, songname):
    if collection not in collections:
        add_collection(collection)
    songs[collection].append(songname)
    f = open("playlists/" + collection + ".sng", "w")
    for song in songs[collection]:
        f.write(song + "\n")
    f.close()


def remove_song(collection, songname):
    if collection in collections:
        if songname in songs[collection]:
            songs[collection].remove(songname)
            f = open("playlists/" + collection + ".sng", "w")
            for song in songs[collection]:
                f.write(song + "\n")
            f.close()
            return True
    return False


def get_songlist(colls):
    songlist = []
    for coll in colls:
        if coll in collections:
            for song in songs[coll]:
                cur = song.replace("\n", "")
                if cur not in songlist:
                    songlist.append(cur)
    return songlist


def get_song(colls):
    songlist = get_songlist(colls)
    if len(songlist) > 0:
        return songlist[random.randint(0, len(songlist) - 1)]
    return None


def add_history(username):
    for i in range(0, len(msg_history) - 1):
        j = len(msg_history) - (i + 1)
        msg_history[j] = msg_history[j - 1]
    msg_history[0] = username


def load_songs():
    f = open("data/collections.txt", "r")
    for line in f:
        if line != "" and line != "\n":
            collections.append(line.replace('\n', ''))
    f.close()
    for col in collections:
        songs[col] = []
        f = open("playlists/"+col + ".sng")
        for line in f:
            if line != "" and line != "\n":
                songs[col].append(line)
        f.close()


def add_nick(name, nick):
    name = name.lower()
    nick = nick.lower()
    if name not in nick_players:
        nick_players.append(name)
    nicknames[name] = nick
    f = open("data/nicknames.txt", "w")
    for player in nick_players:
        f.write(player.lower() + "=|=" + nicknames[player].lower() + "\n")
    f.close()


def load_nicks():
    f = open("data/nicknames.txt", "r")
    for line in f:
        spl = line.split("=|=")
        player = spl[0].replace("\n", "")
        nickname = spl[1].replace("\n", "")
        nick_players.append(player)
        nicknames[player] = nickname
    f.close()


xkcd_range = [100, 1600]


def get_xkcd_link(n):
    link = "http://xkcd.com/" + str(n) + "/"
    f = requests.get(link)
    lines = f.text.split('\n')
    imgurl = None
    for line in lines:
        if line.startswith("Image URL"):
            line = line.replace(" ", "")
            index = line.find("http")
            imgurl = line[index:]
            break
    return imgurl

def download_plugin(link, name):

    print("   [PLUGIN] sending request to " + link + "...")
    f = requests.get(link)
    print("   [PLUGIN] creating file "+name+".py ...")
    dest = open("plugins/"+name+".py", "w")
    print("   [PLUGIN] dumping data...")
    dest.write("#SOURCE/+++/"+link+"/+++/"+name+"\n")
    dest.write(f.text)
    dest.close()
    print("   [PLUGIN] done")

def update_plugin(name):
    if os.path.exists("plugins/"+name+".py"):
        f = open("plugins/"+name+".py")
        for line in f:
            if line.startswith("#SOURCE"):
                spl = line.replace("\n", "").split("/+++/")
                download_plugin(spl[1], spl[2])
                return True
    return False

def get_metapic(n=-1):
    link = "http://themetapicture.com/"
    f = requests.get(link)

    lines = f.text.split("\n")
    images = []

    for line in lines:
        if "<p><img src=" in line:
            index = line.find("img src=")
            imglink = line[index + 9:]
            index = imglink.find(" ")
            imglink = imglink[:index - 1]
            images.append(imglink)
    if n == -1:
        n = random.randint(0, len(images) - 1)
    else:
        n = min(len(images) - 1, max(0, n))
    return images[n]


cah_range = [100, 4300]


def get_cah_link(n):
    link = "http://explosm.net/comics/" + str(n) + "/"
    f = requests.get(link)
    lines = f.text.split('\n')
    imgurl = None
    for line in lines:
        if line.startswith("<meta property") and "og:image" in line:
            line = line.replace(" ", "")
            index = line.find("http")
            imgurl = line[index:]
            imgurl = imgurl[:-2]
            break
    return imgurl


def get_humblebundle(suffix=""):
    link = "https://www.humblebundle.com/" + suffix
    f = requests.get(link)

    lines = f.text.split('\n')
    base_games = ""
    average_games = ""
    average_price = "???"
    bonus_games = ""
    bonus_price = "???"

    game_index = 0
    last_line = None
    for line in lines:
        if "prepend section-heading price bta" in line and game_index == 0:
            game_index = 1
            index = line.find("$")
            average_price = line[index:]
            index = average_price.find(" ")
            average_price = average_price[:index]
        if "prepend section-heading price fixed" in line and game_index == 1:
            game_index = 2
            index = line.find("$")
            bonus_price = line[index:]
            index = bonus_price.find(" ")
            bonus_price = bonus_price[:index]
        if "section game-border prepend coupons" in line:
            break
        if "<h2>" in line and "game-description" in last_line:
            index = line.find("<h2>")
            gamename = line[index + 4:]
            gamename = gamename[:-5]
            if game_index == 0:
                base_games = base_games + "    - " + gamename + "\n"
            elif game_index == 1:
                average_games = average_games + "     - " + gamename + "\n"
            else:
                bonus_games = bonus_games + "     - " + gamename + "\n"
        last_line = line
    return "BASE GAMES ($1):\n" + base_games + "\n" + "AVERAGE GAMES (" + average_price + "):\n" + average_games + "\n" + "BONUS GAMES (" + bonus_price + "):\n" + bonus_games


def get_name(name):
    name = name.lower()
    for nm in nick_players:
        if nicknames[nm] == name:
            return nm
    return name

def add_raw_activity(member, origin_channel, amount):
    name = member.name.lower()
    old_activity = activity[name]
    activity[name] += amount
    for trigger in activity_triggers:
        if old_activity < trigger <= activity[name]:
            yield from use_reward(member, origin_channel, get_reward(activity_triggers[trigger]))
    save_activity()

def add_activity(member, origin_channel, act):
    global activity, activity_events, activity_cds
    save_acts = False
    name = member.name.lower()
    if name is not botname():
        if name not in activity:
            activity[name] = 0
            save_acts = True
        secs = time.time()
        if name not in activity_cds:
            activity_cds[name] = {}

        if act not in activity_cds[name]:
            activity_cds[name][act] = secs

        if activity_cds[name][act] <= secs:
            amount = 0
            cd = 0
            if act in activity_events:
                amount = activity_events[act][0]
                cd = activity_events[act][1]
            if amount > 0:
                yield from add_raw_activity(member, origin_channel, amount)
                activity_cds[name][act] = secs + cd
                save_acts = False

        if save_acts:
            save_activity()



def save_activity():
    f = open("data/activity.txt", "w")
    for name in activity.keys():
        f.write(name + "/+++/" + str(activity[name]) + "\n")
    f.close()


def load_activity():
    global activity
    f = open("data/activity.txt", "r")
    for line in f:
        tabs = line.replace("\n", "").split("/+++/")
        if tabs[0] != "":
            activity[tabs[0]] = int(tabs[1])
    f.close()

def load_activity_events():
    f = open("data/activity_events.txt", "r")
    for line in f:
        tabs = line.replace("\n", "").split(":")
        activity_events[tabs[0]] = [int(tabs[1]), int(tabs[2])]
    f.close()

def save_activity_events():
    f = open("data/activity_events.txt", "w")
    for act in activity_events:
        f.write(act+":"+str(activity_events[act][0])+":"+str(activity_events[act][1]) + "\n")
    f.close()

def load_activity_triggers():
    f = open("data/activity_triggers.txt", "r")
    for line in f:
        tabs = line.replace("\n", "").split("/+++/")
        activity_triggers[int(tabs[0])] = tabs[1]
    f.close()

def save_activity_triggers():
    f = open("data/activity_triggers.txt", "w")
    for trigger in activity_triggers.keys():
        f.write(str(trigger)+"/+++/"+activity_triggers[trigger] + "\n")
    f.close()

def save_messages():
    f = open("data/msgs.txt", "w")
    for name in left_messages.keys():
        if len(left_messages[name]) > 0:
            line = name + "/+++/" + left_messages[name][0]
            for i in range(1, len(left_messages[name])):
                line = line + "/+++/" + left_messages[name][i]
            f.write(line + "\n")
    f.close()


def load_messages():
    f = open("data/msgs.txt", "r")
    for line in f:
        if line != '' and line != '\n':
            spl = line.replace('\n', '').split("/+++/")
            name = spl[0]
            left_messages[name] = []
            for i in range(1, len(spl)):
                left_messages[name].append(spl[i])
    f.close()


def leave_message(name, msg):
    if name not in left_messages:
        left_messages[name] = []
    left_messages[name].append(msg)
    save_messages()


def get_messages(name):
    msgs = []
    if name in left_messages:
        msgs = left_messages[name]
    return msgs

@client.event
@asyncio.coroutine
def on_message_delete(message):
    yield from add_activity(message.author, message.channel, "on_message_delete")
    yield from plugin_manager.on_message_delete(message)

@client.event
@asyncio.coroutine
def on_member_join(member):
    yield from add_activity(member, member, "on_member_join")
    yield from plugin_manager.on_member_join(member)

@client.event
@asyncio.coroutine
def on_member_remove(member):
    yield from add_activity(member, member, "on_member_remove")
    yield from plugin_manager.on_member_remove(member)

@client.event
@asyncio.coroutine
def on_member_update(before, after):
    yield from add_activity(after, after, "on_member_update")
    yield from plugin_manager.on_member_update(before, after)

@client.event
@asyncio.coroutine
def on_voice_state_update(before, after):
    yield from add_activity(after, after, "on_voice_state")
    yield from plugin_manager.on_voice_state_update(before, after)

@client.event
@asyncio.coroutine
def on_member_ban(member):
    yield from add_activity(member, member, "on_ban")
    yield from plugin_manager.on_member_ban(member)

@client.event
@asyncio.coroutine
def on_member_unban(member):
    yield from add_activity(member, member, "on_unban")
    yield from plugin_manager.on_member_unban(member)

@client.event
@asyncio.coroutine
def on_typing(ch, user, when):
    yield from add_activity(user, ch, "on_typing")
    yield from plugin_manager.on_typing(ch, user, when)

@client.event
@asyncio.coroutine
def on_message(message):
    global tagged
    yield from add_activity(message.author, message.channel, "on_message")
    sucess = False
    if message.author.name.lower() != botname():
        if not message.content.startswith(cfix()) and not message.channel.is_private and len(message.content) < taglimit():
            if message.author.name.lower() == tagged:
                for member in message.author.server.members:
                    memname = member.name.lower()
                    if memname != message.author.name.lower():
                        if memname in nick_players:
                            if nicknames[memname] in message.content.lower():
                                tag_player(memname)
                                break
        welcome(message.author)
        global radio_channel
        if is_command(message.content, "yoyo"):
            if not check_command(message.author.name, "yoyo"):
                yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
            else:
                msg = message.content[message.content.find(" ")+1:]
                yield from client.send_message(message.channel, msg)
                add_history(message.author.name)
                sucess = True
        elif is_command(message.content, "yoyosay"):
            if not check_command(message.author.name, "yoyosay"):
                yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
            else:
                msg = message.content[message.content.find(" ")+1:]
                yield from client.send_message(message.channel, msg, tts=True)
                add_history(message.author.name)
                sucess = True
        elif is_command(message.content, "activity"):
            formatting = ": use "+cfix()+"activity to check | "+cfix()+"activity add/set <username> <amount> to add/set amount"
            try:
                params = [""]
                if " " in message.content:
                    params = message.content[message.content.find(" ")+1:].split(" ")
                if params[0] == "add":
                    formatting = ": "+cfix()+"activity add <username> <amount>"
                    if not check_command(message.author.name, "activity set", "activity"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        name = params[1].lower()
                        member = None
                        for mem in message.author.server.members:
                            if name in mem.name.lower():
                                member = mem
                                name = mem.name.lower()
                                break
                        if member is not None:
                            v = int(params[2])
                            yield from add_raw_activity(member, message.channel, v)
                            yield from client.send_message(message.channel, "<ACV> Added " + str(v) + " activity to " + name + "'s account")
                            sucess = True
                        else:
                            yield from client.send_message(message.channel, "<ACV> Could not find player " + params[1])
                elif params[0] == "set":
                    formatting = ": "+cfix()+"activity set <username> <amount>"
                    if not check_command(message.author.name, "activity set", "activity"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        name = params[1].lower()
                        member = None
                        for mem in message.author.server.members:
                            if name in mem.name.lower():
                                member = mem
                                name = mem.name.lower()
                                break

                        if member is not None:
                            v = 0
                            if name in activity:
                                v = activity[name]
                            yield from add_raw_activity(member, message.channel, int(params[2]) - v)
                            yield from client.send_message(message.channel, "<ACV> Set " + name + "'s activity to " + params[2])
                            sucess = True
                        else:
                            yield from client.send_message(message.channel, "<ACV> Could not find player " + params[1])
                elif params[0] == "trigger":
                    formatting = ": "+cfix()+"activity trigger [activity_amount|remove|get] [reward|activity_amount]"
                    if not check_command(message.author.name, "activity trigger", "activity"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        if len(params) == 1:
                            formatting = ": "+cfix()+"activity trigger"
                            joint = ""
                            if len(activity_triggers.keys()) > 0:
                                for activity_amount in activity_triggers.keys():
                                    if joint == "":
                                        joint = str(activity_amount)
                                    else:
                                        joint = joint + ", " + str(activity_amount)
                            yield from client.send_message(message.channel, "<ACV> Current triggers: " + joint)
                        elif params[1] == "get":
                            formatting = ": "+cfix()+"activity trigger get <activity_amount>"
                            amount = int(params[2])
                            if amount in activity_triggers:
                                yield from client.send_message(message.channel, "<ACV> Reward for " + str(amount) + " activity is " + activity_triggers[amount])
                            else:
                                yield from client.send_message(message.channel, "<ACV> Activity trigger for " + str(amount) + " doesn't exist!")
                        elif params[1] == "remove":
                            formatting = ": "+cfix()+"activity trigger remove <activity_amount>"
                            amount = int(params[2])
                            if amount in activity_triggers:
                                del activity_triggers[amount]
                                save_activity_triggers()
                                yield from client.send_message(message.channel, "<ACV> Removed activity trigger for " + str(amount))
                            else:
                                yield from client.send_message(message.channel, "<ACV> Activity trigger for " + str(amount) + " doesn't exist!")
                        else:
                            formatting = ": "+cfix()+"activity trigger <activity_amount> <reward>"
                            amount = int(params[1])
                            reward = params[2]
                            activity_triggers[amount] = reward
                            save_activity_triggers()
                            yield from client.send_message(message.channel, "<ACV> Added a new activity trigger!")
                            sucess = True
                elif params[0] == "event":
                    formatting = ": "+cfix()+"activity event <event> <activity_given> [cooldown]"
                    if not check_command(message.author.name, "activity event", "activity"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        event = params[1].lower()
                        amount = int(params[2])
                        cooldown = 0
                        if len(params) > 3:
                            cooldown = int(params[4])
                        if event in activity_events:
                            activity_events[event]
                            activity_events[event] = [amount, cooldown]
                            save_activity_events()
                            yield from client.send_message(message.channel, "<ACV> Set " + event + " to give " + str(amount) + " on a " + str(cooldown) + " second cooldown")
                            sucess = True
                        else:
                            yield from client.send_message(message.channel, "<ACV> Invalid event!")
                elif params[0] == "get":
                    formatting = ": "+cfix()+"activity get <event>"
                    if not check_command(message.author.name, "activity get", "activity"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        event = params[1].lower()
                        if event in activity_events:
                            info = activity_events[event]
                            yield from client.send_message(message.channel, "<ACV> Set " + event + " to give " + str(info[0]) + " on a " + str(info[1]) + " second cooldown")
                            sucess = True
                        else:
                            yield from client.send_message(message.channel, "<ACV> Invalid event!")
                elif params[0] == "help":
                    if not check_command(message.author.name, "activity help", "activity"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        formatting = ": "+cfix()+"activity help"
                        page = 0
                        if len(params) > 1:
                            page = int(params[1]) - 1
                        lines = print_help(activity_help_str, page)
                        if lines is not None:
                            for line in lines:
                                yield from client.send_message(message.author, line)
                            sucess = True
                        else:
                            yield from client.send_message(message.channel, "<ACV> invalid page!")
                else:
                    formatting = ": "+cfix()+"activity [username]"
                    if not check_command(message.author.name, "activity check", "activity"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        name = message.author.name.lower()
                        if params[0] != "":
                            name = params[0].lower()
                            for mem in message.author.server.members:
                                if name in mem.name.lower():
                                    name = mem.name.lower()
                                    break
                        v = 0
                        if name in activity:
                            v = activity[name]
                        yield from client.send_message(message.channel, "<ACV> " + name + "'s activity is " + str(v))
                    sucess = True
            except:
                yield from client.send_message(message.channel, "<ACV> Failed" + formatting)
        elif is_command(message.content, "tagged"):
            formatting = ": see "+cfix()+"tagged help"
            try:
                params = [""]
                if " " in message.content:
                    params = message.content[message.content.find(" ")+1:].split(" ")
                if params[0] == "":
                    formatting = ": "+cfix()+"tagged"
                    if not check_command(message.author.name, "tagged check", "tagged"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        cur = tagged
                        if message.author.name.lower() == tagged:
                            cur = old_tagged
                        yield from client.send_message(message.author, "<TAG> " + cur + " is currently tagged, shhh")
                        sucess = True
                elif params[0] == "best":
                    if not check_command(message.author.name, "tagged best", "tagged"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        formatting = ": "+cfix()+"tagged best"
                        if "record_shortest" in tag_stats:
                            record = tag_stats["record_shortest"]
                            yield from client.send_message(message.channel, "<TAG> " + record.user + " currently holds the record for shortest time tagged, with " + record.clever_format())
                        else:
                            yield from client.send_message(message.channel, "<TAG> no record set yet!")
                        sucess = True
                elif params[0] == "worst":
                    if not check_command(message.author.name, "tagged worst", "tagged"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        formatting = ": "+cfix()+"tagged worst [username]"
                        if len(params) > 1:
                            if "user_record" in tag_stats:
                                name = get_name(params[1])
                                if name in tag_stats["user_record"]:
                                    record = tag_stats["user_record"]
                                    client.send_message(message.channel, "<TAG> " + name + "'s record for longest time tagged is " + record.clever_format())
                                else:
                                    yield from client.send_message(message.channel, "<TAG> " + name + " has no record yet!")
                            else:
                                yield from client.send_message(message.channel, "<TAG> nobody has a record yet!")
                        else:
                            if "record_longest" in tag_stats:
                                record = tag_stats["record_longest"]
                                client.send_message(message.channel,
                                                    "<TAB> " + record.user + " currently holds the record for the longest time tagged, with " + record.clever_format())
                            else:
                                yield from client.send_message(message.channel, "<TAG> no record set yet!")
                        sucess = True
                elif params[0] == "help":
                    if not check_command(message.author.name, "tagged help", "tagged"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        formatting = ": "+cfix()+"tagged help"
                        page = 0
                        if len(params) > 1:
                            page = int(params[1]) - 1
                        lines = print_help(tag_help_str, page)
                        if lines is not None:
                            for line in lines:
                                yield from client.send_message(message.author, line)
                            sucess = True
                        else:
                            yield from client.send_message(message.channel, "<TAG> invalid page!")
                else:
                    raise(Exception())
            except():
                yield from client.send_message(message.channel, "<TAG> Failed, do it properly" + formatting)
        elif is_command(message.content, "history"):
            if not check_command(message.author.name, "history"):
                yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
            else:
                msg = "<YOYO> History: " + msg_history[0]
                for i in range(1, len(msg_history)):
                    if msg_history[i] != "":
                        msg = msg + ", " + msg_history[i]
                yield from client.send_message(message.channel, msg)
                sucess = True
        elif is_command(message.content, "hman"):

            formatting = ": see "+cfix()+"hangman help"
            try:
                global hangman_found, hangman_word, hangman_words, hangman_guess, hangman_guessed_letters, hangman_tries
                params = [""]
                if " " in message.content:
                    params = message.content[message.content.find(" ")+1:].split(" ")
                if params[0] == "":
                    if not check_command(message.author.name, "hman check", "hman"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        if hangman_word != "":
                            yield from client.send_message(message.channel, "<HMAN> Current progress: " + str(
                                hangman_found) + " with " + str(
                                hangman_guess) + " (bad) guesses left. Wrong letters guessed: " + hangman_guessed_letters)
                        else:
                            yield from client.send_message(message.channel, "<HMAN> No game in-progress!")
                elif params[0] == "help":
                    if not check_command(message.author.name, "hman help", "hman"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        yield from client.send_message(message.channel, "<HMAN> ("+cfix()+"hman can be used as well) "+cfix()+"hangman to check progress, "+cfix()+"hangman new [word] create new game, random word if none given, "+cfix()+"hangman [letter|word] guess a word or a letter, "+cfix()+"hangman end to give up")
                elif params[0] == "new":
                    if not check_command(message.author.name, "hman new", "hman"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        hangman_word = hangman_words[random.randint(0, len(hangman_words) - 1)]
                        if len(params) > 1:
                            hangman_word = params[1]
                            for i in range(2, len(params)):
                                hangman_word = hangman_word + " " + params[i]
                        hangman_found = "-" * len(hangman_word)
                        for i in range(len(hangman_word)):
                            if hangman_word[i] == " ":
                                hangman_found = hangman_found[:i] + " " + hangman_found[i + 1:]
                        yield from client.send_message(message.channel, "<HMAN> New game created: " + str(hangman_found))
                        hangman_guess = 9
                        hangman_guessed_letters = ""
                        hangman_tries = 0

                elif params[0] == "end":
                    if not check_command(message.author.name, "hman end", "hman"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        yield from client.send_message(message.channel, "<HMAN> Failed! The word was: " + str(
                            hangman_word) + " you got " + hangman_found + " in " + str(hangman_tries) + " tries!")
                        hangman_word = ""
                        hangman_found = ""
                        hangman_guess = 0
                        hangman_guessed_letters = ""
                        hangman_tries = 0
                elif hangman_word != "":
                    if not check_command(message.author.name, "hman guess", "hman"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        letter = params[0].lower()
                        if len(letter) == 1:
                            if letter not in hangman_guessed_letters:
                                hangman_tries += 1
                                if letter in hangman_word:
                                    old_found = hangman_found
                                    hangman_found = ""
                                    for i in range(len(hangman_word)):
                                        if hangman_word[i] == letter:
                                            hangman_found += letter
                                        elif hangman_word[i] == " ":
                                            hangman_found += " "
                                        elif old_found[i] != "-":
                                            hangman_found += old_found[i]
                                        else:
                                            hangman_found += "-"
                                    hangman_guessed_letters = hangman_guessed_letters + " " + letter
                                    if hangman_found == hangman_word:
                                        yield from client.send_message(message.channel,  "<HMAN> You win! The word was: " + str( hangman_word) + " you got it in " + str(hangman_tries) + " tries!")
                                        hangman_word = ""
                                        hangman_found = ""
                                        hangman_guess = 0
                                        hangman_guessed_letters = ""
                                        hangman_tries = 0
                                    else:
                                        yield from client.send_message(message.channel, "<HMAN> Correct letter! Current progress: " + hangman_found + " with " + str(hangman_guess) + " (bad) guesses left. Wrong letters guessed: " + hangman_guessed_letters)
                                else:
                                    hangman_guess -= 1
                                    hangman_guessed_letters = hangman_guessed_letters + " " + letter
                                    if hangman_guess <= 0:
                                        yield from client.send_message(message.channel, "<HMAN> Failed! The word was: " + str( hangman_word) + " you got " + str( hangman_found) + " in " + str(hangman_tries) + " tries!")
                                        hangman_word = ""
                                        hangman_found = ""
                                        hangman_guess = 0
                                        hangman_guessed_letters = ""
                                        hangman_tries = 0
                                    else:
                                        yield from client.send_message(message.channel, "<HMAN> Wrong letter! Current progress: " + hangman_found + " with " + str(hangman_guess) + " (bad) guesses left. Wrong letters guessed: " + hangman_guessed_letters)
                            else:
                                yield from client.send_message(message.channel, "<HMAN> Whoops! " + str(
                                    letter) + " has already been guessed!")
                        else:
                            guess = params[0]
                            for i in range(1, len(params)):
                                guess = guess + " " + params[i]
                            if guess.lower() == hangman_word:
                                yield from client.send_message(message.channel, "<HMAN> You win! The word was: " + str(
                                    hangman_word) + " you got it in " + str(hangman_tries) + " tries!")
                                hangman_word = ""
                                hangman_found = ""
                                hangman_guess = 0
                                hangman_guessed_letters = ""
                                hangman_tries = 0
                            else:
                                hangman_guess -= 1
                                if hangman_guess <= 0:
                                    yield from client.send_message(message.channel, "<HMAN> Failed! The word was: " + str(
                                        hangman_word) + " you got " + str(hangman_found) + " in " + str(
                                        hangman_tries) + " tries!")
                                    hangman_word = ""
                                    hangman_found = ""
                                    hangman_guess = 0
                                    hangman_guessed_letters = ""
                                    hangman_tries = 0
                                else:
                                    yield from client.send_message(message.channel, "<HMAN> Wrong guess! Current progress: " + hangman_found + " with " + str(hangman_guess) + " (bad) guesses left. Wrong letters guessed: " + hangman_guessed_letters)
                else:
                    yield from client.send_message(message.channel,
                                                   "<HMAN> Failed to use hangman, do it properly" + formatting)
                sucess = True
            except():
                yield from client.send_message(message.channel,
                                               "<HMAN> Failed to use hangman, do it properly" + formatting)
        elif is_command(message.content, "8ball"):
            if not check_command(message.author.name, "8ball"):
                yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
            else:
                msg = ball_8[random.randint(0, len(ball_8) - 1)]
                yield from client.send_message(message.channel, "<8BALL> " + msg)
        elif is_command(message.content, "flip"):
            if not check_command(message.author.name, "flip"):
                yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
            else:
                msg = "<COIN> Head"
                if (random.randint(0, 1) == 0):
                    msg = "<COIN> Tail"
                yield from client.send_message(message.channel, msg)
        elif is_command(message.content, "roll"):
            if not check_command(message.author.name, "roll"):
                yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
            else:
                msg = "<DICE> " + str(random.randint(1, 6))
                yield from client.send_message(message.channel, msg)

        elif is_command(message.content, "msg"):
            formatting = ": see "+cfix()+"msg help for usage"
            try:
                params = [""]
                if " " in message.content:
                    params = message.content[message.content.find(" ")+1:].split(" ")
                if params[0] == "send":
                    if not check_command(message.author.name, "msg send", "msg"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        formatting = ": "+cfix()+"msg send <user> <msg>"
                        if len(params) > 2:
                            name = get_name(params[1].lower()).lower()
                            if not message.channel.is_private:
                                for mem in message.author.server.members:
                                    if name in mem.name.lower():
                                        name = mem.name.lower()
                                        break
                            msg = params[2]
                            for i in range(3, len(params)):
                                msg = msg + " " + params[i]
                            leave_message(name, "[" + message.author.name + "] " + msg)
                            yield from client.send_message(message.author, "<MSG> left a message for " + name)
                            sucess = True
                        else:
                            raise (Exception())
                elif params[0] == "help":
                    if not check_command(message.author.name, "msg help", "msg"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        formatting = ": "+cfix()+"msg help"
                        page = 0
                        if len(params) > 1:
                            page = int(params[1]) - 1
                        lines = print_help(msg_help_str, page)
                        if lines is not None:
                            for line in lines:
                                yield from client.send_message(message.author, line)
                            sucess = True
                        else:
                            yield from client.send_message(message.channel, "<MSG> invalid page!")
                elif params[0] == "check":
                    if not check_command(message.author.name, "msg check", "msg"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        formatting = ": "+cfix()+"msg check"
                        name = message.author.name.lower()
                        msgs = get_messages(name)
                        for i in range(len(msgs)):
                            msg = msgs[i]
                            yield from client.send_message(message.author, "<MSG> (" + str(i) + ") " + msg)
                        sucess = True
                elif params[0] == "delete" or params[0] == "del":
                    if not check_command(message.author.name, "msg delete", "msg"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        formatting = ": "+cfix()+"msg delete|del [number]"
                        if len(params) == 1:
                            name = message.author.name.lower()
                            if name in left_messages:
                                del left_messages[name]
                            yield from client.send_message(message.author, "<MSG> deleted all messages")
                        else:
                            name = message.author.name.lower()
                            if name in left_messages:
                                n = 0
                                for i in range(1, len(params)):
                                    if ">" in params[i]:
                                        inds = params[i].split(">")
                                        for index in range(int(inds[0]), int(inds[1]) + 1):
                                            if index < len(left_messages[name]):
                                                del left_messages[name][index - n]
                                                n += 1
                                            else:
                                                break
                                    else:
                                        index = int(params[i]) - n
                                        if index < len(left_messages[name]):
                                            del left_messages[name][index]
                                            n += 1
                            save_messages()
                            yield from client.send_message(message.author, "<MSG> deleted selected messages")
                        sucess = True
                else:
                    raise(Exception())
            except:
                yield from client.send_message(message.author, "<MSG> Failed to use msg" + formatting)
        elif is_command(message.content, "song"):
            params = [""]
            if " " \
                    in message.content:
                params = message.content[message.content.find(" ")+1:].split(" ")
            formatting = ": see "+cfix()+"song help"
            try:
                global song_queue, voice_chn, song_finished, current_music_player, song_paused, skip_votes, song_list
                if params[0] == "add":
                    if not check_command(message.author.name, "song add", "song"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        formatting = ": "+cfix()+"song add <playlist|songlink> [songlink]"
                        collection = "default"
                        songname = params[1]
                        if len(params) > 2:
                            collection = params[1]
                            songname = params[2]
                        if "youtube" in songname and "/watch" in songname:
                            add_song(collection, songname)
                            yield from client.send_message(message.channel, "<SONG> Added song to " + collection)
                            sucess = True
                        else:
                            yield from client.send_message(message.channel, "<SONG> Can only add youtube links!")
                elif params[0] == "del" or params[0] == "delete":
                    if not check_command(message.author.name, "song delete", "song"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        formatting = ": "+cfix()+"song del|delete <song|playlist> [song]"
                        collection = "default"
                        songname = params[1]
                        if len(params) > 2:
                            collection = params[1]
                            songname = params[2]
                        if remove_song(collection, songname):
                            yield from client.send_message(message.channel, "<SONG> removed song from " + collection)
                        else:
                            yield from client.send_message(message.channel,
                                                           "<SONG> could not find that song in " + collection)
                        sucess = True
                elif params[0] == "q" or params[0] == "queue":
                    if not check_command(message.author.name, "song queue", "song"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        formatting = ": "+cfix()+"song q|queue <songlink>"

                        song_queue.append(params[1])
                        yield from client.send_message(message.channel, "<SONG> Queued song!")
                        sucess = True
                elif params[0] == "playlists":
                    if not check_command(message.author.name, "song playlists", "song"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                            formatting = ": "+cfix()+"song playlists"
                            if len(collections) > 0:
                                msg = collections[0]
                                for i in range(1, len(collections)):
                                    msg = msg + ", " + collections[i]
                                yield from client.send_message(message.channel, "<SONG> Playlists: " + msg)
                            else:
                                yield from client.send_message(message.channel, "<SONG> Playlists: No collections :o")
                            sucess = True
                elif params[0] == "help":
                    if not check_command(message.author.name, "song help", "song"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        formatting = ": "+cfix()+"song help"
                        page = 0
                        if len(params) > 1:
                            page = int(params[1]) - 1
                        lines = print_help(song_help_str, page)
                        if lines is not None:
                            for line in lines: yield from client.send_message(message.author, line)
                            sucess = True
                        else:
                            yield from client.send_message(message.channel, "<SONG> invalid page!")
                elif params[0] == "radio":
                    if not check_command(message.author.name, "song radio", "song"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:

                        if voice_chn is None:
                            yield from client.send_message(message.channel,
                                                           "<SONG> cannot start radio when not voice-connected!")
                        else:
                            if radio_channel is None:
                                for ch in message.author.server.channels:
                                    if ch.name.lower() == rchn():
                                        radio_channel = ch
                                        break
                            colls = ["default"]
                            if len(params) > 1:
                                colls = params[1:]
                                if params[1] == "all":
                                    colls = collections
                            str_colls = colls[0]
                            for i in range(1, len(colls)):
                                str_colls = str_colls + ", " + colls[i]
                            if not song_finished:
                                song_list = get_songlist(colls)
                                sucess = True
                                yield from client.send_message(message.channel, "<SONG> radio playlist changed to: " + str_colls)
                            else:
                                yield from start_radio(colls)
                                yield from client.send_message(message.channel,  "<SONG> radio started with playlist set to: " + str_colls)
                        sucess = True
                elif params[0] == "link":
                    if not check_command(message.author.name, "song link", "song"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        if current_music_player is not None:
                            yield from client.send_message(message.channel, "<SONG> Current song: " + current_music_player.url)
                        else:
                            yield from client.send_message(message.channel, "<SONG> Radio is not currently on!")
                elif params[0] == "size":
                    if not check_command(message.author.name, "song size", "song"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        colls = ["default"]
                        if len(params) > 1:
                            colls = params[1:]
                            if params[1] == "all":
                                colls = collections
                        songlist = get_songlist(colls)
                        str_colls = colls[0]
                        for i in range(1, len(colls)):
                            str_colls = str_colls + ", " + colls[i]
                        yield from client.send_message(message.channel,
                                                       "<SONG> There are " + str(len(songlist)) + " songs in " + str_colls)
                        sucess = True
                elif params[0] == "pause":
                    if not check_command(message.author.name, "song pause", "song"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:

                        if current_music_player is not None:
                            if not song_paused:
                                current_music_player.pause()
                                song_paused = True
                                game = discord.Game()
                                game.name = current_music_player.title
                                yield from client.change_status(game, True)
                                yield from client.send_message(message.channel, "<SONG> Radio paused!")
                            else:
                                yield from client.send_message(message.channel,
                                                               "<SONG> Radio already paused! do !song resume to resume it")
                        else:
                            yield from client.send_message(message.channel, "<SONG> The radio isn't on!")
                elif params[0] == "resume":
                    if not check_command(message.author.name, "song resume", "song"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:

                        if current_music_player is not None:
                            if song_paused:
                                current_music_player.resume()
                                song_paused = False
                                game = discord.Game()
                                game.name = current_music_player.title
                                yield from client.change_status(game, False)
                                yield from client.send_message(message.channel, "<SONG> Radio resumed!")
                            else:
                                yield from client.send_message(message.channel,
                                                               "<SONG> Radio isn't paused! !song pause to pause it")
                        else:
                            yield from client.send_message(message.channel, "<SONG> The radio isn't on!")
                elif params[0] == "skip":
                    if not check_command(message.author.name, "song skip", "song"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:

                        if voice_chn is not None:
                            members = voice_chn.channel.voice_members
                            result = False
                            for mem in members:
                                if mem.name == message.author.name:
                                    result = True
                                    break
                            if result:
                                req_votes = math.ceil(0.5 * (len(members) - 1))
                                if message.author.name in skip_votes:
                                    yield from client.send_message(message.channel,
                                                                   "<SONG> You've already voted to skip! " + str(
                                                                       len(skip_votes)) + " out of " + str(
                                                                       req_votes) + " votes required to skip")
                                else:
                                    skip_votes.append(message.author.name)

                                    if len(skip_votes) >= req_votes:
                                        current_music_player.stop()
                                        sucess = True
                                        yield from client.send_message(message.channel, "<SONG> Song skipped!")
                                    else:
                                        yield from client.send_message(message.channel,
                                                                       "<SONG> " + str(len(skip_votes)) + " out of " + str(
                                                                           req_votes) + " votes required to skip")
                            else:
                                yield from client.send_message(message.channel,
                                                               "<SONG> Can only vote to skip if you're listening!")
                        else:
                            yield from client.send_message(message.channel, "<SONG> Radio is not currently on!")
                elif params[0] == "connect":
                    if not check_command(message.author.name, "song connect", "song"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:

                        song_finished = True
                        if voice_chn is not None:
                            yield from voice_chn.disconnect()
                            voice_chn = None
                            current_music_player = None
                        name = params[1].lower()
                        joined = False
                        for channel in message.author.server.channels:

                            if name in channel.name.lower() and channel.type is discord.ChannelType.voice:
                                voice_chn = yield from client.join_voice_channel(channel)
                                yield from client.send_message(message.channel, "<SONG> joined channel " + channel.name)
                                joined = True
                                break
                        if not joined:
                            yield from client.send_message(message.channel, "<SONG> failed to join channel " + name)
                        sucess = True
                elif params[0] == "stop":
                    if not check_command(message.author.name, "song stop", "song"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:

                        if current_music_player is not None:
                            if voice_chn is not None:
                                yield from voice_chn.disconnect()
                            song_paused = False
                            song_queue = []
                            current_music_player.stop()
                            voice_chn = None
                            current_music_player = None
                            song_list = []
                            yield from client.send_message(message.channel, "<SONG> radio stopped")
                        else:
                            yield from client.send_message(message.channel, "<SONG> radio not playing!")
                        sucess = True
                elif params[0] == '':
                    if not check_command(message.author.name, "song random", "song"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        formatting = ": "+cfix()+"song"
                        songname = get_song(["default"])
                        if songname is not None:
                            yield from client.send_message(message.channel, songname)
                            sucess = True
                        else:
                            yield from client.send_message(message.channel, "<SONG> Failed to find a song in default?")
                else:
                    if not check_command(message.author.name, "song random", "song"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        formatting = ": "+cfix()+"song [playlists]"
                        colls = params
                        if params[0] == "all":
                            colls = collections
                        songname = get_song(colls)
                        if songname is not None:
                            yield from client.send_message(message.channel, get_song(colls))
                            sucess = True
                        else:
                            yield from client.send_message(message.channel,
                                                           "<SONG> Failed to find song, you sure those playlists exist?")
            except:
                yield from client.send_message(message.channel, "<SONG> Failed, do it properly" + formatting)
        elif is_command(message.content, "rng"):
            params = [""]
            if " " in message.content:
                params = message.content[message.content.find(" ")+1:].split(" ")
            formatting = ": see "+cfix()+"rng help"
            try:
                if len(params) == 1 and params[0] == '':
                    if not check_command(message.author.name, "rng"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        yield from client.send_message(message.channel, "<RNG> " + str(random.random()))
                        sucess = True
                elif params[0] == "help":
                    if not check_command(message.author.name, "rng help", "rng"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        page = 0
                        if len(params) > 1:
                            page = int(params[1]) - 1
                        lines = print_help(rng_help_str, page)
                        if lines is not None:
                            for line in lines: yield from client.send_message(message.author, line)
                            sucess = True
                        else:
                            yield from client.send_message(message.channel, "<RNG> invalid page!")
                elif len(params) == 1:
                    if not check_command(message.author.name, "rng"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                            formatting = ": "+cfix()+"rng <number>"
                            yield from client.send_message(message.channel,
                                                           "<RNG> " + str(int(float(params[0]) * random.random())))
                            sucess = True
                elif len(params) == 2:
                    if not check_command(message.author.name, "rng"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        formatting = ": "+cfix()+"rng <lower> <upper> | "+cfix()+"rng <f|number> <f|number>"
                        if params[0] == 'f' or params[0] == 'real':
                            formatting = ": "+cfix()+"rng f <number>"
                            yield from client.send_message(message.channel,
                                                           "<RNG> " + str(float(params[1]) * random.random()))
                            sucess = True
                        elif params[1] == 'f' or params[1] == 'real':
                            formatting = ": "+cfix()+"rng <number> f"
                            yield from client.send_message(message.channel,
                                                           "<RNG> " + str(float(params[0]) * random.random()))
                            sucess = True
                        else:
                            formatting = ": "+cfix()+"rng <lower> <upper>"
                            rng = int(float(params[0]) + ((float(params[1]) - float(params[0])) * random.random()))
                            yield from client.send_message(message.channel, "<RNG> " + str(rng))
                            sucess = True
                elif len(params) == 3:
                    if not check_command(message.author.name, "rng"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        formatting = ": "+cfix()+"rng <f|lower> <f|lower|upper> <f|upper>"
                        if (params[0] == 'f' or params[0] == 'real'):
                            formatting = ": "+cfix()+"rng f <lower> <upper>"
                            rng = float(params[1]) + ((float(params[2]) - float(params[1])) * random.random())
                            yield from client.send_message(message.channel, "<RNG> " + str(rng))
                            sucess = True
                        elif (params[1] == 'f' or params[1] == 'real'):
                            formatting = ": "+cfix()+"rng <lower> f <upper>"
                            rng = float(params[0]) + ((float(params[2]) - float(params[0])) * random.random())
                            yield from client.send_message(message.channel, "<RNG> " + str(rng))
                            sucess = True
                        elif (params[2] == 'f' or params[2] == 'real'):
                            formatting = ": "+cfix()+"rng <lower> <upper> f"
                            rng = float(params[0]) + ((float(params[1]) - float(params[0])) * random.random())
                            yield from client.send_message(message.channel, "<RNG> " + str(rng))
                            sucess = True
                else:
                    yield from client.send_message(message.channel, "<RNG> Failed, see "+cfix()+"rng help")
            except:
                yield from client.send_message(message.channel, "<RNG> Failed, do it properly" + formatting)
        elif is_command(message.content, "code"):
            if not check_command(message.author.name, "code"):
                yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
            else:
                yield from client.send_message(message.channel, "<CODE> " + yoyo_code_link)
        elif is_command(message.content, "nick"):
            try:
                params = [""]
                if " " in message.content:
                    params = message.content[message.content.find(" ")+1:].split(" ")
                if len(params) == 2:
                    if not check_command(message.author.name, "nick set other", "nick"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        name = get_name(params[0])
                        if name == params[0]:
                            for mem in message.author.server.members:
                                if name in mem.name.lower():
                                    name = mem.name
                                    break
                        add_nick(name, params[1])
                        yield from client.send_message(message.channel,
                                                       "<NICK> set " + name + "'s nickname to " + params[1])
                        sucess = True
                elif len(params) == 1:
                    if not check_command(message.author.name, "nick set", "nick"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        name = message.author.name
                        add_nick(name, params[0])
                        yield from client.send_message(message.channel,
                                                       "<NICK> set " + name + "'s nickname to " + params[0])
                        sucess = True
                else:
                    raise(Exception())
            except:
                yield from client.send_message(message.channel, "<NICK> Failed to assign nickname")
        elif is_command(message.content, "decide"):
            try:
                if not check_command(message.author.name, "decide"):
                    yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                else:
                    decisions = message.content[8:].split(" or ")
                    yield from client.send_message(message.channel, decisions[random.randint(0, len(decisions) - 1)] + ".")
                    sucess = True
            except:
                yield from client.send_message(message.channel,
                                               "<DECIDE> Failed, do "+cfix()+"decide <decision> or <decision> [or ...]")
        elif is_command(message.content, "nickname"):
            params = [""]
            if " " in message.content:
                params = message.content[message.content.find(" ")+1:].split(" ")
            if len(params[0]) == 0:
                if not check_command(message.author.name, "nickname me", "nickname"):
                    yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                else:
                    name = message.author.name.lower()
                    if name in nick_players:
                        yield from client.send_message(message.channel,
                                                       "<NICK> " + name + "'s current nickname: " + nicknames[name])
                    else:
                        yield from client.send_message(message.channel, "<NICK> " + name + " has no current nickname!")
                sucess = True
            else:
                if not check_command(message.author.name, "nickname other", "nickname"):
                    yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                else:
                    name = get_name(params[0])
                    if name == params[0].lower():
                        for mem in message.author.server.members:
                            if name in mem.name.lower():
                                name = mem.name.lower()
                                break
                    print(name)
                    if name in nick_players:
                        yield from client.send_message(message.channel,
                                                       "<NICK> " + name + "'s current nickname: " + nicknames[name])
                    else:
                        yield from client.send_message(message.channel, "<NICK> " + name + " has no current nickname!")
                sucess = True
        elif is_command(message.content, "hb"):
            try:
                if not check_command(message.author.name, "hb"):
                    yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                else:
                    suffix = ""
                    if " " in message.content:
                        index = message.content.find(" ")
                        suffix = message.content[index + 1:].replace(" ", "-")
                    print(suffix)
                    yield from client.send_message(message.channel, get_humblebundle(suffix))
                    sucess = True
            except:
                yield from client.send_message(message.channel, "<HUMBLE> couldn't find the current bundle!")
        elif is_command(message.content, "xkcd"):
            try:
                if not check_command(message.author.name, "xkcd"):
                    yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                else:
                    number = 0
                    params = [""]
                    if " " in message.content:
                        params = message.content[message.content.find(" ")+1:].split(" ")
                    if params[0] == "":
                        number = random.randint(xkcd_range[0], xkcd_range[1])
                    else:
                        number = int(params[0])
                    link = get_xkcd_link(number)
                    if link is not None:
                        yield from client.send_message(message.channel, link)
                        sucess = True
                    else:
                        yield from client.send_message(message.channel, "<XKCD> Couldn't find that comic!")
            except:
                yield from client.send_message(message.channel, "<XKCD> failed! use "+cfix()+"xkcd [comic-number]")
        elif is_command(message.content, "cah"):
            try:
                if not check_command(message.author.name, "cah"):
                    yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                else:
                    number = 0
                    params = [""]
                    if " " in message.content:
                        params = message.content[message.content.find(" ")+1:].split(" ")
                    if params[0] == "":
                        number = random.randint(cah_range[0], cah_range[1])
                    else:
                        number = int(params[0])
                    link = get_cah_link(number)
                    if link is not None:
                        yield from client.send_message(message.channel, link)
                        sucess = True
                    else:
                        yield from client.send_message(message.channel, "<C&H> Couldn't find that comic!")
            except:
                yield from client.send_message(message.channel, "<C&H> failed! use "+cfix()+"cah [comic-number]")
        elif is_command(message.content, "img"):
            try:
                if not check_command(message.author.name, "img"):
                    yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                else:
                    number = -1
                    params = [""]
                    if " " in message.content:
                        params = message.content[message.content.find(" ")+1:].split(" ")
                    if params[0] != "":
                        number = int(params[0])
                    link = get_metapic(number)
                    if link is not None:
                        yield from client.send_message(message.channel, link)
                        sucess = True
                    else:
                        yield from client.send_message(message.channel, "<IMG> Couldn't find that image!")
            except:
                yield from client.send_message(message.channel, "<IMG> couldn't find an image")
        elif is_command(message.content, "poke"):
            try:
                if not check_command(message.author.name, "poke"):
                    yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                else:
                    params = [""]
                    if " " in message.content:
                        params = message.content[message.content.find(" ")+1:].split(" ")
                    if len(params) == 1 and params[0] != '':
                        name = get_name(params[0].lower()).lower()
                        member = None
                        for mem in message.author.server.members:
                            if name in mem.name.lower():
                                member = mem
                                break

                        if member is not None:
                            name = member.name
                            if (name != "yoyobot"):
                                if (name in poke_cooldowns):
                                    if poke_cooldowns[name] < time.clock():
                                        del poke_cooldowns[name]
                                if (name not in poke_cooldowns):
                                    yield from client.send_message(member, "POKE!!!")
                                    sucess = True
                                    poke_cooldowns[name] = 60 + time.clock()
                                else:
                                    yield from client.send_message(message.channel,
                                                                   "<POKE> don't try to poke them too many times...")
                            else:
                                yield from client.send_message(message.channel, "<POKE> I'm not going to poke myself...")

                        else:
                            raise (Exception("poke", "user doesn't exist"))

            except:
                yield from client.send_message(message.channel, "<POKE> Whoops, you sure that user exists?")
        elif is_command(message.content, "help"):
            try:
                if not check_command(message.author.name, "help"):
                    yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                else:
                    params = [""]
                    if " " in message.content:
                        params = message.content[message.content.find(" ")+1:].split(" ")
                    page = 0
                    if params[0] != "":
                        page = int(params[0]) - 1
                    lines = print_help(help_str, page)
                    if lines is not None:
                        for line in lines: yield from client.send_message(message.author, line)
                        sucess = True
                    else:
                        yield from client.send_message(message.channel, "<HELP> invalid page!")
            except():
                yield from client.send_message(message.channel, "<HELP> you managed to break the help page.. how..")
        elif is_command(message.content, "status"):
            try:
                if not check_command(message.author.name, "status"):
                    yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                else:
                    params = [""]
                    if " " in message.content:
                        params = message.content[message.content.find(" ")+1:].split(" ")
                    idle = False
                    if len(params) > 1:
                        if params[1].lower() == "true" or params[1].lower() == "on":
                            idle = True
                    game = discord.Game()
                    game.name = params[0]
                    yield from client.change_status(game, idle)
                    sucess = True
            except:
                print("status update not working properly...")
        elif is_command(message.content, "invite"):
            if not check_command(message.author.name, "invite"):
                yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
            else:
                inv = yield from client.create_invite(message.author.server, max_age=600)
                yield from client.send_message(message.channel, inv.url)
        elif is_command(message.content, "uptime"):
            if not check_command(message.author.name, "uptime"):
                yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
            else:
                global uptime_cooldown, uptime_start
                secs = int(time.clock())
                if secs > uptime_cooldown:
                    uptime_cooldown = secs + 30
                    cdat = create_current_dat()
                    elap = cdat.minus(uptime_start)
                    yield from client.send_message(message.channel, "I've been alive for " + elap.clever_format())
        elif is_command(message.content, "money"):
            formatting = ": see "+cfix()+"money help"
            try:
                params = [""]
                if " " in message.content:
                    params = message.content[message.content.find(" ")+1:].split(" ")
                if params[0] == "set":
                    formatting = ": "+cfix()+"money set <username> <amount>"
                    if not check_command(message.author.name, "money set", "money"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        name = get_name(params[1].lower()).lower()
                        found = False
                        for mem in message.author.server.members:
                            if name in mem.name.lower():
                                name = mem.name
                                found = True
                                break
                        for user in user_money.keys():
                            if name in user.lower():
                                name = user
                                found = True
                                break
                        if found or name in user_money:
                            amount = int(params[2])
                            set_money(name, amount)
                            yield from client.send_message(message.channel, "<$$$> Set " + name + "'s balance to $" + str(amount))
                        else:
                            yield from client.send_message(message.channel, "<$$$> Couldn't find user " + name)
                        sucess = True
                elif params[0] == "give":
                    formatting = ": "+cfix()+"money give <username> <amount>"
                    if not check_command(message.author.name, "money give", "money"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        name = get_name(params[1].lower()).lower()
                        found = False
                        for mem in message.author.server.members:
                            if name in mem.name.lower():
                                name = mem.name
                                found = True
                                break
                        for user in user_money.keys():
                            if name in user.lower():
                                name = user
                                found = True
                                break
                        if found or name in user_money:
                            amount = int(params[2])
                            balance = give_money(name, amount)
                            yield from client.send_message(message.channel, "<$$$> Gave $" + str(amount) + " to " + name + " (balance: $" + str(balance)+")")
                        else:
                            yield from client.send_message(message.channel, "<$$$> Couldn't find user " + name)
                        sucess = True
                elif params[0] == "trade":
                    formatting = ": "+cfix()+"money trade <username> <amount>"
                    if not check_command(message.author.name, "money trade", "money"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        name = get_name(params[1].lower()).lower()
                        found = False
                        for mem in message.author.server.members:
                            if name in mem.name.lower():
                                name = mem.name
                                found = True
                                break
                        for user in user_money.keys():
                            if name in user.lower():
                                name = user
                                found = True
                                break
                        if found or name in user_money:
                            amount = int(params[2])
                            if trade_money(message.author.name, name, amount):
                                yield from client.send_message(message.channel, "<$$$> " + message.author.name + " traded $" + str(amount) + " to " + name + "(your balance: $" + str(get_money(message.author.name))+")")
                            else:
                                yield from client.send_message(message.channel, "<$$$> You don't have enough money! Your balance: $" + str(get_money(message.author.name)))
                        else:
                            yield from client.send_message(message.channel, "<$$$> Couldn't find user " + name)
                        sucess = True
                elif params[0] == "help":
                    if not check_command(message.author.name, "money help", "money"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        page = 0
                        if len(params) > 1:
                            page = int(params[1]) - 1
                        lines = print_help(money_help_str, page)
                        if lines is not None:
                            for line in lines: yield from client.send_message(message.author, line)
                            sucess = True
                        else:
                            yield from client.send_message(message.channel, "<$$$> invalid page!")
                elif params[0] == "":
                    formatting = ": "+cfix()+"money [username]"
                    if not check_command(message.author.name, "money check", "money"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        yield from client.send_message(message.channel, "<$$$> Your balance is: $" + str(get_money(message.author.name)))
                    sucess = True
                else:
                    formatting = ": "+cfix()+"money [username]"
                    if not check_command(message.author.name, "money check", "money"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        name = params[0].lower()
                        found = False
                        for mem in message.author.server.members:
                            if name in mem.name.lower():
                                name = mem.name
                                found = True
                                break
                        for user in user_money.keys():
                            if name in user.lower():
                                name = user
                                found = True
                                break
                        if found or name in user_money:
                            yield from client.send_message(message.channel, "<$$$> "+ name + "'s balance is: $" + str(get_money(name)))
                        else:
                            yield from client.send_message(message.channel, "<$$$> Couldn't find user " + name)
                    sucess = True
            except:
                yield from client.send_message(message.channel, "<$$$> Failed" + formatting)
        elif is_command(message.content, "reward"):
            formatting = ": see "+cfix()+"reward help"
            try:
                params = [""]
                if " " in message.content:
                    params = message.content[message.content.find(" ")+1:].split(" ")
                if params[0] == "set":
                    formatting = ": "+cfix()+"reward set <reward> <commands>"
                    if not check_command(message.author.name, "reward set", "reward"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        cmds = " ".join(params[2:]).split("||")
                        print(cmds)
                        set_reward(params[1], cmds)
                        yield from client.send_message(message.channel, "<RWD> Set " + params[1] + "'s reward commands.")
                        sucess = True
                elif params[0] == "edit":
                    formatting = ": "+cfix()+"reward edit <reward> <commands>"
                    if not check_command(message.author.name, "reward edit", "reward"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        cmds = []
                        remove = False
                        if params[2].lower() == "remove":
                            remove = True
                            cmds = params[3:]
                        else:
                            cmds = params[2:]
                        if edit_reward(params[1], cmds, remove):
                            yield from client.send_message(message.channel, "<RWD> Edited reward: " + params[1])
                        else:
                            yield from client.send_message(message.channel, "<RWD> Couldn't find a reward named: " + params[1])
                elif params[0] == "delete" or params[0] == "del":
                    formatting = ": "+cfix()+"reward del|delete <reward>"
                    if not check_command(message.author.name, "reward delete", "reward"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        if remove_reward(params[1]):
                            yield from client.send_message(message.channel, "<RWD> Deleted reward: " + params[1])
                        else:
                            yield from client.send_message(message.channel, "<RWD> Couldn't find a reward named: " + params[1])
                elif params[0] == "get":
                    formatting = ": "+cfix()+"reward get <reward>"
                    if not check_command(message.author.name, "reward get", "reward"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        result = get_reward(params[1])
                        if result is not None:
                            yield from client.send_message(message.channel, "<RWD> " + params[1] + "'s commands: \n" + "    \n".join(result))
                        else:
                            yield from client.send_message(message.channel, "<RWD> Couldn't find a reward named: " + params[1])
                elif params[0] == "give":
                    formatting = ": "+cfix()+"reward give <username> <reward>"
                    if not check_command(message.author.name, "reward give", "reward"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        name = get_name(params[1].lower()).lower()
                        member = None
                        for mem in message.author.server.members:
                            if name in mem.name.lower():
                                member = mem
                                break
                        if member is not None:
                            result = get_reward(params[2])
                            if result is not None:
                                yield from use_reward(member, message.channel, result)
                            else:
                                yield from client.send_message(message.channel, "<RWD> Couldn't find a reward named: " + params[1])
                        else:
                            yield from client.send_message(message.channel, "<RWD> Couldn't find a member named " + name + ", are you sure they're online?")
                elif params[0] == "help":
                    formatting = ": "+cfix()+"reward help [page]"
                    if not check_command(message.author.name, "reward help", "reward"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        page = 0
                        if len(params) > 1:
                            page = int(params[1]) - 1
                        lines = print_help(reward_help_str, page)
                        if lines is not None:
                            for line in lines: yield from client.send_message(message.author, line)
                            sucess = True
                        else:
                            yield from client.send_message(message.channel, "<RWD> invalid page!")
                elif is_command(settings["command_prefix"] + params[0], "shop"):
                    if params[1] == "add":
                        formatting = ": "+cfix()+"reward shop add <reward> <price> <category> <name> <short description> "
                        if not check_command(message.author.name, "reward shop add", "reward shop"):
                            yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                        else:
                            item = ShopItem(params[2], int(params[3]), params[5], params[6], [params[6]])
                            add_item(params[4], item)
                            print("saving..")
                            save_shop()
                            print("saved")
                            yield from client.send_message(message.channel, "<ROLE> added item " + params[5] + " to " + params[4])
                    elif params[1] == "remove":
                        formatting = ": "+cfix()+"reward shop remove <category> [name]"
                        if not check_command(message.author.name, "reward shop remove", "reward shop"):
                            yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                        else:
                            catname = params[2]
                            if catname in money_shop:
                                if len(params) == 3:
                                    del money_shop[catname]
                                    save_shop()
                                    yield from client.send_message(message.channel, "<SHOP> Removed " + catname + " from the shop")
                                else:
                                    if money_shop[catname].remove_item(params[3]):
                                        save_shop()
                                        yield from client.send_message(message.channel, "<SHOP> Removed " + params[3] + " from the " + catname)
                                    else:
                                        yield from client.send_message(message.channel, "<SHOP> Couldn't find an " + params[3] + " in " + catname)
                            else:
                                 yield from client.send_message(message.channel, "<SHOP> Couldn't find a category named " + catname)
                        sucess = True
                    elif params[1] == "price":
                        formatting = ": "+cfix()+"reward shop price <category> <name> <price>"
                        if not check_command(message.author.name, "reward shop price", "reward shop"):
                            yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                        else:
                            catname = params[2]
                            if catname in money_shop:
                                itemname = params[3]
                                if money_shop[catname].set_price(itemname, int(params[4])):
                                    save_shop()
                                    yield from client.send_message(message.channel, "<SHOP> Set " + itemname + "'s price to $" + params[4])
                                else:
                                    yield from client.send_message(message.channel, "<SHOP> Couldn't find an " + itemname + " in " + catname)
                            else:
                                yield from client.send_message(message.channel, "<SHOP> Couldn't find a category named " + catname)
                            sucess = True
                    elif params[1] == "move":
                        formatting = ": "+cfix()+"reward shop move <name> <old_category> <new_category>"
                        if not check_command(message.author.name, "reward shop move", "reward shop"):
                            yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                        else:
                            catname1 = params[3]
                            if catname1 in money_shop:
                                catname2 = params[4]
                                if catname2 in money_shop:
                                    itemname = params[2]
                                    if money_shop[catname1].move_item(itemname, money_shop[catname2]):
                                        save_shop()
                                        yield from client.send_message(message.channel, "<SHOP> Moved " + itemname + " from " + catname1 + " to " + catname2)
                                    else:
                                        yield from client.send_message(message.channel, "<SHOP> Couldn't find an " + itemname + " in " + catname1)
                                else:
                                    yield from client.send_message(message.channel, "<SHOP> Couldn't find a category named " + catname2)
                            else:
                                yield from client.send_message(message.channel, "<SHOP> Couldn't find a category named " + catname1)
                            sucess = True
                    elif params[1] == "hide":
                        formatting = ": "+cfix()+"reward shop hide <true|false> <category> [name]"
                        if not check_command(message.author.name, "reward shop hide", "reward shop"):
                            yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                        else:
                            hidden = False
                            if params[2].lower() == "true":
                                hidden = True
                            elif params[2].lower() != "false":
                                raise(Exception())
                            catname = params[3]
                            if catname in money_shop:
                                if len(params) == 4:
                                    money_shop[catname].set_hidden(hidden)
                                    save_shop()
                                    yield from client.send_message(message.channel, "<SHOP> Set " + catname + "'s hidden status to " + hidden)
                                else:
                                    itemname = params[4]
                                    if money_shop[catname].set_hidden(hidden, itemname):
                                        save_shop()
                                        yield from client.send_message(message.channel, "<SHOP> Set " + itemname + "'s hidden status to " + str(hidden))
                                    else:
                                        yield from client.send_message(message.channel, "<SHOP> Couldn't find an " + itemname + " in " + catname)
                            else:
                                yield from client.send_message(message.channel, "<SHOP> Couldn't find a category named " + catname)
                        sucess = True
                    elif params[1] == "short":
                        formatting = ": "+cfix()+"reward shop short <category> <name> <short description>"
                        if not check_command(message.author.name, "reward shop short", "reward shop"):
                            yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                        else:
                            catname = params[2]
                            if catname in money_shop:
                                itemname = params[3]
                                if money_shop[catname].set_short(itemname, params[4]):
                                    save_shop()
                                    yield from client.send_message(message.channel, "<SHOP> Set " + itemname + "'s short description!")
                                else:
                                    yield from client.send_message(message.channel, "<SHOP> Couldn't find an " + itemname + " in " + catname)
                            else:
                                yield from client.send_message(message.channel, "<SHOP> Couldn't find a category named " + catname)
                            sucess = True
                    elif params[1] == "long":
                        formatting = ": "+cfix()+"reward shop long <category> <name> <long description>"
                        if not check_command(message.author.name, "reward shop long", "reward shop"):
                            yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                        else:
                            if params[2] == "add":
                                formatting = ": "+cfix()+"reward shop long add <category> <name> <long description>"
                                catname = params[3]
                                if catname in money_shop:
                                    itemname = params[4]
                                    if money_shop[catname].add_long(itemname, params[5]):
                                        save_shop()
                                        yield from client.send_message(message.channel, "<SHOP> Added to " + itemname + "'s long description!")
                                    else:
                                        yield from client.send_message(message.channel, "<SHOP> Couldn't find an " + itemname + " in " + catname)
                                else:
                                    yield from client.send_message(message.channel, "<SHOP> Couldn't find a category named " + catname)
                                sucess = True
                            elif params[2] == "del":
                                formatting = ": "+cfix()+"reward shop long delete|del <category> <name> [line number]"
                                catname = params[3]
                                if catname in money_shop:
                                    itemname = params[4]
                                    line_number = -1
                                    if len(params) > 5:
                                        line_number = int(params[5])
                                    if money_shop[catname].remove_long(itemname, line_number):
                                        save_shop()
                                        linestr = "last line"
                                        if line_number != -1:
                                            linestr = "line " + str(line_number)
                                        yield from client.send_message(message.channel, "<SHOP> Removed " + linestr + " from " + itemname + "'s long description!")
                                    else:
                                        yield from client.send_message(message.channel, "<SHOP> Couldn't find an " + itemname + " in " + catname)
                                else:
                                    yield from client.send_message(message.channel, "<SHOP> Couldn't find a category named " + catname)
                                sucess = True
                            else:
                                formatting = ": "+cfix()+"reward shop long <category> <name> <long description>"
                                catname = params[2]
                                if catname in money_shop:
                                    itemname = params[3]
                                    if money_shop[catname].set_long(itemname, params[4]):
                                        save_shop()
                                        yield from client.send_message(message.channel, "<SHOP> Reset " + itemname + "'s long description!")
                                    else:
                                        yield from client.send_message(message.channel, "<SHOP> Couldn't find an " + itemname + " in " + catname)
                                else:
                                    yield from client.send_message(message.channel, "<SHOP> Couldn't find a category named " + catname)
                                sucess = True
                    elif params[1] == "info":
                        formatting = ": "+cfix()+"reward shop info [category] [item]"
                        if len(params) == 2:
                            formatting = ": "+cfix()+"reward shop info"
                            yield from client.send_message(message.channel, "<SHOP> " + get_cats(True))
                        elif len(params) == 3:
                            formatting = ": "+cfix()+"reward shop info [category]"
                            line = get_items(params[2], True)
                            if line is not None:
                                yield from client.send_message(message.channel, "<SHOP> " + line)
                            else:
                                yield from client.send_message(message.channel, "<SHOP> Couldn't find a category named " + params[2])
                        else:
                            formatting = ": "+cfix()+"reward shop info [category] [item]"
                            catname = params[2]
                            if catname in money_shop:
                                yield from client.send_message(message.channel, get_item_desc(money_shop[catname], params[3], True))
                            else:
                                yield from client.send_message(message.channel, "<SHOP> Couldn't find a category named " + catname)
                        sucess = True
                    else:
                        raise(Exception())
                else:
                    raise(Exception())
            except:
                yield from client.send_message(message.channel, "<RWD> Failed" + formatting)
        elif is_command(message.content, "plugin"):
            formatting = ": "+cfix()+"plugin help"
            try:
                params = [""]
                if " " in message.content:
                    params = message.content[message.content.find(" ")+1:].split(" ")
                if params[0] == "install":
                    formatting + ": "+cfix()+"plugin install <plugin> <link> - are you sure that link is correct?"
                    if not check_command(message.author.name, "plugin install", "plugin"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        link = " ".join(params[2:])
                        if "pastebin" in link:
                            if "/raw/" in link:
                                if os.path.exists("plugins/"+params[1]+".py"):
                                    os.remove("plugins/"+params[1]+".py")
                                plugin_manager.uninstall(params[1])
                                download_plugin(" ".join(params[2:]), params[1])
                                test = __import__("plugins."+params[1], fromlist=["plugins"])
                                test.setup(plugin_manager, params[1])
                                yield from client.send_message(message.channel, "<PLUG> Installed plugin " + params[1])
                                sucess = True
                            else:
                                yield from client.send_message(message.channel, "<PLUG> Must be a raw link!")
                        else:
                            yield from client.send_message(message.channel, "<PLUG> Must be a pastebin link!")
                elif params[0] == "uninstall":
                    formatting + ": "+cfix()+"plugin uninstall <plugin>"
                    if not check_command(message.author.name, "plugin uninstall", "plugin"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        if "__init__" not in params[1]:
                            if os.path.exists("plugins/"+params[1]+".py"):
                                os.remove("plugins/"+params[1]+".py")
                            plugin_manager.uninstall(params[1])
                            yield from client.send_message(message.channel, "<PLUG> uninstalled " + params[1] + " (if it was installed)")
                        else:
                            yield from client.send_message(message.channel, "<PLUG> You can't uninstall the __init__...")
                elif params[0] == "disable":
                    formatting + ": "+cfix()+"plugin disable <plugin>"
                    if not check_command(message.author.name, "plugin disable", "plugin"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        if "__init__" not in params[1]:
                            if not plugin_disabled(params[1]):
                                plugin_manager.uninstall(params[1])
                                plugin_disables[params[1]] = True
                                save_plugin_disables()
                                yield from client.send_message(message.channel, "<PLUG> Disabled " + params[1])
                            else:
                                yield from client.send_message(message.channel, "<PLUG> " + params[1] + " already disabled!")
                        else:
                            yield from client.send_message(message.channel, "<PLUG> You can't disable the __init__...")
                elif params[0] == "enable":
                    formatting + ": "+cfix()+"plugin disable <plugin>"
                    if not check_command(message.author.name, "plugin disable", "plugin"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        if "__init__" not in params[1]:
                            if plugin_disabled(params[1]):
                                plugin_disables[params[1]] = False
                                save_plugin_disables()
                                test = __import__("plugins."+params[1], fromlist=["plugins"])
                                test.setup(plugin_manager, params[1])
                                yield from client.send_message(message.channel, "<PLUG> Enabled " + params[1])
                            else:
                                yield from client.send_message(message.channel, "<PLUG> " + params[1] + " already enabled!")
                        else:
                            yield from client.send_message(message.channel, "<PLUG> You can't enable the __init__...")
                elif params[0] == "check":
                    formatting + ": "+cfix()+"plugin check <plugin>"
                    if not check_command(message.author.name, "plugin check", "plugin"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        if "__init__" not in params[1]:
                            line = "enabled"
                            if plugin_disabled(params[1]):
                                line = "disabled"
                            yield from client.send_message(message.channel, "<ROLE> " + params[1] + " is currently " + line)
                        else:
                            yield from client.send_message(message.channel, "<PLUG> You can't enable the __init__...")
                elif params[0] == "update":
                    formatting + ": "+cfix()+"plugin update <plugin>"
                    if not check_command(message.author.name, "plugin update", "plugin"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        if "__init__" not in params[1]:
                            if update_plugin(params[1]):
                                plugin_manager.uninstall(params[1])
                                if not plugin_disabled(params[1]):
                                    test = __import__("plugins."+params[1], fromlist=["plugins"])
                                    test.setup(plugin_manager, params[1])
                                yield from client.send_message(message.channel, "<PLUG> Updated " + params[1])
                            else:
                                yield from client.send_message(message.channel, "<PLUG> Couldn't find a plugin named "+params[1]+"!")
                        else:
                            yield from client.send_message(message.channel, "<PLUG> You can't update the __init__...")
                elif params[0] == "list":
                    formatting + ": "+cfix()+"plugin list?"
                    if not check_command(message.author.name, "plugin list", "plugin"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        yield from client.send_message(message.channel, "<PLUG> Loaded plugins: " + ", ".join(plugin_manager.plugin_name_list()))
                    sucess = True
                elif params[0] == "reload":
                    formatting + ": "+cfix()+"plugin reload"
                    if not check_command(message.author.name, "plugin reload", "plugin"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        load_plugins()
                        yield from client.send_message(message.channel, "<PLUG> Reloaded plugins.")
                    sucess = True
                elif params[0] == "help":
                    formatting = ": "+cfix()+"plugin help [page]"
                    if not check_command(message.author.name, "plugin help", "plugin"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        page = 0
                        if len(params) > 1:
                            page = int(params[1]) - 1
                        lines = print_help(plugin_help_str, page)
                        if lines is not None:
                            for line in lines: yield from client.send_message(message.author, line)
                            sucess = True
                        else:
                            yield from client.send_message(message.channel, "<PLUG> invalid page!")
                else:
                    raise(Exception())
            except:
                yield from client.send_message(message.channel, "<PLUG> Failed" + formatting)
        elif is_command(message.content, "bind"):
            formatting = ": "+cfix()+"+bind set|get|add|del <command> [bind]"
            try:
                params = [""]
                if " " in message.content:
                    params = message.content[message.content.find(" ")+1:].split(" ")
                if params[0] == "set":
                    formatting = ": "+cfix()+"+bind set <command> <bind>"
                    if not check_command(message.author.name, "bind set", "bind"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        set_bind(params[1], params[2])
                        yield from client.send_message(message.channel, "<BIND> Set " + params[1] +"'s binding to " + params[2])
                elif params[0] == "get":
                    formatting = ": "+cfix()+"+bind get <command>"
                    if not check_command(message.author.name, "bind get", "bind"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        b = get_binds(params[1])
                        if b is not None:
                            yield from client.send_message(message.channel, "<BIND> " + params[1] + "'s bindings: " + b)
                        else:
                            yield from client.send_message(message.channel, "<BIND> " + params[1] + " has not bindings!")
                elif params[0] == "add":
                    formatting = ": "+cfix()+"+bind add <command> <bind>"
                    if not check_command(message.author.name, "bind add", "bind"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        add_bind(params[1], params[2])
                        yield from client.send_message(message.channel, "<BIND> Added " + params[2] +" to " + params[1] + "'s binds")
                elif params[0] == "del" or params[0] == "delete":
                    formatting = ": "+cfix()+"+bind del|delete <command> <bind>"
                    if not check_command(message.author.name, "bind add", "bind"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        if remove_bind(params[1], params[2]):
                            yield from client.send_message(message.channel, "<BIND> Removed " + params[2] + " from " + params[1] + "'s bindings")
                        else:
                            yield from client.send_message(message.channel, "<BIND> Couldn't find a binding for " + params[1])
                else:
                    raise(Exception())
            except:
                yield from client.send_message(message.channel, "<BIND> Failed" + formatting)
        elif is_command(message.content, "settings"):
            formatting = ": "+cfix()+"settings set|get <setting> [value]"
            try:
                params = [""]
                if " " in message.content:
                    params = message.content[message.content.find(" ")+1:].split(" ")
                if params[0] == "set":
                    formatting = ": "+cfix()+"settings set <setting> <value>"
                    if not check_command(message.author.name, "settings set", "settings"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        settings[params[1]] = " ".join(params[2:])
                        save_settings()
                        if params[1] == "command_prefix":
                            load_help_strs()
                        elif params[1] == "radio_channel":
                            for ch in message.author.server.channels:
                                if ch.name.lower() == rchn():
                                    radio_channel = ch
                                    break
                        yield from client.send_message(message.channel, "<STG> Set " + params[1] + " to " + settings[params[1]])
                    sucess = True
                elif params[0] == "get":
                    formatting = ": "+cfix()+"settings get [setting]"
                    if not check_command(message.author.name, "settings get", "settings"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        if len(params) == 1:
                            yield from client.send_message(message.channel, "<STG> current settings: " + ", ".join(settings.keys()))
                        else:
                            if params[1] in settings:
                                yield from client.send_message(message.channel, "<STG> " + params[1] + " is set to " + settings[params[1]])
                            else:
                                yield from client.send_message(message.channel, "<STG> Setting " + params[1] + " could not be found!")
                            sucess = True
                else:
                    raise(Exception())
            except:
                yield from client.send_message(message.channel, "<STG> Failed, usage: " + formatting)
        elif is_command(message.content, "shop"):
            formatting = ": see"+cfix()+"shop help"
            try:
                params = [""]
                if " " in message.content:
                    params = message.content[message.content.find(" ")+1:].split(" ")
                if params[0] == "get":
                    formatting = ": "+cfix()+"shop get [category] [item]"
                    if not check_command(message.author.name, "shop get", "shop"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        if len(params) == 1:
                            formatting = ": "+cfix()+"shop get"
                            yield from client.send_message(message.channel, "<SHOP> " + get_cats(False))
                        elif len(params) == 2:
                            formatting = ": "+cfix()+"shop get [category]"
                            line = get_shop_items(params[1], False)
                            if line is not None:
                                yield from client.send_message(message.channel, "<SHOP> " + line)
                            else:
                                yield from client.send_message(message.channel, "<SHOP> Couldn't find a category named " + params[2])
                        else:
                            formatting = ": "+cfix()+"shop get [category] [item]"
                            catname = params[1]
                            if catname in money_shop:
                                yield from client.send_message(message.channel, get_item_desc(money_shop[catname], params[2], False))
                            else:
                                yield from client.send_message(message.channel, "<SHOP> Couldn't find a category named " + catname)
                        sucess = True
                elif params[0] == "buy":
                    formatting = ": "+cfix()+"shop but <category> <item>"
                    if not check_command(message.author.name, "shop buy", "shop"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        catname = params[1]
                        if catname in money_shop:
                            itemname = params[2]
                            if itemname in money_shop[catname].items:
                                item = money_shop[catname].items[itemname]
                                reward = get_reward(item.reward)
                                if reward is not None:
                                    money = get_money(message.author.name)
                                    if money > item.price:
                                        give_money(message.author.name, -item.price)
                                        yield from use_reward(message.author, message.channel, reward)
                                        yield from client.send_message(message.channel, "<SHOP> Item bought! Your balance is: " + str(get_money(message.author.name)))
                                    else:
                                        yield from client.send_message(message.channel, "<SHOP> You cannot afford that! Your balance is:" + str(money))
                                else:
                                    yield from client.send_message(message.channel, "<SHOP> " + itemname + " has an invalid reward!")
                            else:
                                yield from client.send_message(message.channel, "<SHOP> Couldn't find an item named " + itemname)
                        else:
                            yield from client.send_message(message.channel, "<SHOP> Couldn't find a category named " + catname)
                elif params[0] == "help":
                    formatting = ": "+cfix()+"shop help"
                    if not check_command(message.author.name, "shop help", "role"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        page = 0
                        if len(params) > 1:
                            page = int(params[1]) - 1
                        lines = print_help(shop_help_str, page)
                        if lines is not None:
                            for line in lines:
                                yield from client.send_message(message.author, line)
                            sucess = True
                        else:
                            yield from client.send_message(message.channel, "<SHOP> invalid page!")
                else:
                    raise(Exception())
            except:
                yield from client.send_message(message.channel, "<SHOP> Failed, usage: " + formatting)
        elif is_command(message.content, "role"):
            formatting = ": see "+cfix()+"role help"
            try:
                params = [""]
                if " " in message.content:
                    params = message.content[message.content.find(" ")+1:].split(" ")
                if params[0] == "set":
                    formatting = ": "+cfix()+"role set <username> <role>"
                    if not check_command(message.author.name, "role set", "role"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        name = get_name(params[1].lower()).lower()
                        for mem in message.author.server.members:
                            if name in mem.name.lower():
                                name = mem.name
                                break
                        rolename = params[2]
                        if set_role(name, rolename):
                            yield from client.send_message(message.channel, "<ROLE> Set " + name + "'s role to " + rolename)
                        else:
                            yield from client.send_message(message.channel, "<ROLE> Couldn't set " + name + "'s name to " + rolename + " are you sure that role/user exist?")
                        sucess = True
                elif params[0] == "help":
                    if not check_command(message.author.name, "role help", "role"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        page = 0
                        if len(params) > 1:
                            page = int(params[1]) - 1
                        lines = print_help(role_help_str, page)
                        if lines is not None:
                            for line in lines:
                                yield from client.send_message(message.author, line)
                            sucess = True
                        else:
                            yield from client.send_message(message.channel, "<ROLE> invalid page!")
                elif params[0] == "edit":
                    formatting = ": "+cfix()+"role edit <rolename> <changes>"
                    if not check_command(message.author.name, "role edit", "role"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        rolename = params[1]
                        changes = params[2:]
                        if change_permissions(rolename, changes):
                            save_permissions()
                            yield from client.send_message(message.channel, "<ROLE> Edited " + rolename)
                        else:
                            yield from client.send_message(message.channel, "<ROLE> Couldn't edit " + rolename + "!")
                elif params[0] == "new":
                    formatting = ": "+cfix()+"role new <rolename>"
                    if not check_command(message.author.name, "role new", "role"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        rolename = params[1]
                        if create_permissions(rolename):
                            yield from client.send_message(message.channel, "<ROLE> Created role " + rolename)
                        else:
                            yield from client.send_message(message.channel, "<ROLE> " + rolename + " already exists!")
                elif params[0] == "get":
                    formatting = ": "+cfix()+"role get <rolename>"
                    if not check_command(message.author.name, "role get", "role"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        rolename = params[1]
                        if rolename in permissions:
                            yield from client.send_message(message.channel, "<ROLE> " + rolename + " permissions: " + permissions[rolename].get_str())
                        else:
                            yield from client.send_message(message.channel, "<ROLE> " + rolename + " doesn't exist!")
                elif params[0] == "roles":
                    formatting = ": "+cfix()+"role roles"
                    if not check_command(message.author.name, "role roles", "role"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        yield from client.send_message(message.channel, "<ROLE> current roles: " + ", ".join(permissions.keys()))
                elif params[0] == "check":
                    formatting = ": "+cfix()+"role check <username>"
                    if not check_command(message.author.name, "role check", "role"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        name = get_name(params[1].lower()).lower()
                        for mem in message.author.server.members:
                            if name in mem.name.lower():
                                name = mem.name
                                break
                        role = get_role(name)
                        if role is not None:
                            yield from client.send_message(message.channel, "<ROLE> " + name + "'s role is " + role.name)
                        else:
                            yield from client.send_message(message.channel, "<ROLE> Couldn't find role, are you sure that user exists?")
                elif params[0] == "":
                    formatting = ": "+cfix()+"role"
                    if not check_command(message.author.name, "role check", "role"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        role = get_role(message.author.name)
                        if role is None:
                            yield from client.send_message(message.channel, "<ROLE> You have an invalid role! setting yours to default.")
                            set_role(message.author.name, "DEFAULT")
                        else:
                            yield from client.send_message(message.channel, "<ROLE> your role is " + role.name)
                else:
                    raise(Exception())
            except:
                yield from client.send_message(message.channel, "<ROLE> Failed, usage: " + formatting)
        elif is_command(message.content, "purge"):
            global current_reward_checker
            try:
                if not check_command(message.author.name, "purge"):
                    yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                else:
                    params = [""]
                    if " " in message.content:
                        params = message.content[message.content.find(" ")+1:].split(" ")
                    current_reward_checker = Purger(" ".join(params[1:]))
                    limit = int(params[0])
                    yield from client.purge_from(message.channel, limit=limit, check=reward_checker)
                    yield from client.send_message(message.channel, "<PURGE> Purge complete.")
            except:
                yield from client.send_message(message.channel, "<PURGE> usage: !purge <limit> <checker>")
        elif is_command(message.content, "custom"):
            formatting = ": "+cfix()+"custom set|get|del <command> [reward]"
            try:
                params = [""]
                if " " in message.content:
                    params = message.content[message.content.find(" ")+1:].split(" ")
                if params[0] == "set":
                    formatting = ": "+cfix()+"custom set <command> <reward>"
                    if not check_command(message.author.name, "custom set", "custom"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        custom_commands[params[1]] = params[2]
                        add_bind("__custom", params[1])
                        save_custom_commands()
                        yield from client.send_message(message.channel, "<CSTM> Set " + params[1] + " to " + params[2])
                elif params[0] == "get":
                    formatting = ": "+cfix()+"custom get <command>"
                    if not check_command(message.author.name, "custom set", "custom"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        if params[1] in custom_commands:
                            yield from client.send_message(message.channel, "<CSTM> " + params[1] + " is set to " + custom_commands[params[1]])
                        else:
                            yield from client.send_message(message.channel, "<CSTM> " + params[1] + " is not a custom command")
                elif params[0] == "del":
                    formatting = ": "+cfix()+"custom del <command>"
                    if not check_command(message.author.name, "custom del", "custom"):
                        yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                    else:
                        if params[1] in custom_commands:
                            del custom_commands[params[1]]
                            remove_bind("__custom", params[1])
                            save_custom_commands()
                            yield from client.send_message(message.channel, "<CSTM> Deleted custom command " + params[1])
                        else:
                             yield from client.send_message(message.channel, "<CSTM> " + params[1] + " is not a custom command")
                else:
                    raise(Exception())
            except:
                yield from client.send_message(message.channel, "<ROLE> Failed, usage: " + formatting)
        elif is_command(message.content, "__custom"):
            cmd = message.content[len(cfix()):]
            if " " in cmd:
                cmd = cmd[:cmd.find(" ")]
            if cmd in custom_commands:
                if not check_command(message.author.name, "_custom " + cmd, "_custom"):
                    yield from client.send_message(message.channel, "<ROLE> You don't have permission to use that command!")
                else:
                    reward = get_reward(custom_commands[cmd])
                    if reward is not None:
                        yield from use_reward(message.author, message.channel, reward)
                    else:
                        yield from client.send_message(message.channel, "<CSTM> Custom command reward " + custom_commands[cmd] + " doesn't exist.")
            else:
                yield from client.send_message(message.channel, "<CSTM> Custom command " + cmd + " has no command?")
        else:
            yield from plugin_manager.on_message(message)
    if sucess and not message.channel.is_private:
        yield from client.delete_message(message)


@asyncio.coroutine
def check_song(loop):
    while True:
        global voice_chn, song_finished
        if voice_chn is not None and song_finished:
            yield from next_song()
        yield from asyncio.sleep(ruprt())


@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    time.clock()
    setup_variables()
    load_songs()
    load_tag()
    load_nicks()
    load_messages()
    load_tag_stats()
    load_hangman_words()
    load_activity()
    load_activity_events()
    load_activity_triggers()
    load_permissions()
    load_roles()
    load_money()
    load_rewards()
    load_shop()
    load_binds()
    load_settings()
    load_help_strs()
    load_custom_commands()
    load_plugin_disables()
    print("Loaded files")
    print('------')
    print("Loading plugins:")
    load_plugins()

    global uptime_start
    uptime_start = create_current_dat()

    loop = asyncio.get_event_loop()
    yield from check_song(loop)

def run():
    print("Type setup to enter setup, otherwise press enter to start bot")
    if input().lower() == "setup":
        setup.run()
        run()
    else:
        print("Starting the bot...")
        if os.path.exists("credentials.txt"):
            username = None
            password = None
            token = None
            f = open("credentials.txt", "r")
            for line in f:
                spl = line.replace("\n", "").split("=")
                if spl[0].lower() == "user" or spl[0].lower() == "username":
                    username = "=".join(spl[1:])
                elif spl[0].lower() == "pass" or spl[0].lower() == "password":
                    password = "=".join(spl[1:])
                elif spl[0].lower() == "token":
                    token = "=".join(spl[1:])
            if username is not None and password is not None:
                print("loaded usernamd and password...")
                client.run(username, password)
            elif token is not None:
                print("loaded bot token...")
                client.run(token)
            else:
                print("Couldn't find credentials!")
        else:
            print("Credential file missing, have you run the setup?")

