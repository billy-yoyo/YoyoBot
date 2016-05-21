
class PluginManager:
    def __init__(self, client):
        self.client = client
        self.plugins = {}

    def get_plugin(self, plugin_name):
        for event in self.plugins:
            for plugin in self.plugins[event]:
                if plugin.name == plugin_name or plugin.file_name == plugin_name:
                    return plugin
        return None

    def update_help(self):
        list = self.plugin_list()
        for plugin in list:
            plugin.update_help()

    def uninstall(self, plugin_name):
        plugin = self.get_plugin(plugin_name)
        if plugin is not None:
            for event in self.plugins:
                if plugin in self.plugins[event]:
                    self.plugins[event].remove(plugin)
        else:
            print("  [PLUGIN] couldn't find " + plugin_name)

    def plugin_list(self):
        plugins = []
        for event in self.plugins:
            for plugin in self.plugins[event]:
                if plugin not in plugins:
                    plugins.append(plugin)
        return plugins

    def plugin_name_list(self):
        plugins = []
        for event in self.plugins:
            for plugin in self.plugins[event]:
                if plugin.name not in plugins:
                    plugins.append(plugin.name)
        return plugins

    def register(self, plugin, events):
        for event in events:
            self.register_event(plugin, event)

    def register_event(self, plugin, event):
        if event not in self.plugins:
            self.plugins[event] = []
        self.plugins[event].append(plugin)

    def on_message(self, message):
        if "on_message" in self.plugins:
            for plugin in self.plugins["on_message"]:
                try:
                    result = yield from plugin.on_message(message)
                    if result:
                        break
                except(TypeError):
                    pass

    def on_message_delete(self, message):
        if "on_message_delete" in self.plugins:
            for plugin in self.plugins["on_message_delete"]:
                try:
                    result = yield from plugin.on_message_delete(message)
                    if result:
                        break
                except(TypeError):
                    pass

    def on_member_join(self, member):
        if "on_member_join" in self.plugins:
            for plugin in self.plugins["on_member_join"]:
                try:
                    result = yield from plugin.on_member_join(member)
                    if result:
                        break
                except(TypeError):
                    pass

    def on_member_remove(self, member):
        if "on_member_remove" in self.plugins:
            for plugin in self.plugins["on_member_remove"]:
                try:
                    result = yield from plugin.on_member_remove(member)
                    if result:
                        break
                except(TypeError):
                    pass

    def on_member_update(self, before, after):
        if "on_member_update" in self.plugins:
            for plugin in self.plugins["on_member_update"]:
                try:
                    result = yield from plugin.on_member_update(before, after)
                    if result:
                        break
                except(TypeError):
                    pass

    def on_voice_state_update(self, before, after):
        if "on_voice_state_update" in self.plugins:
            for plugin in self.plugins["on_voice_state_update"]:
                try:
                    result = yield from plugin.on_voice_state_update(before, after)
                    if result:
                        break
                except(TypeError):
                    pass

    def on_member_ban(self, member):
        if "on_member_ban" in self.plugins:
            for plugin in self.plugins["on_member_ban"]:
                try:
                    result = yield from plugin.on_member_ban(member)
                    if result:
                        break
                except(TypeError):
                    pass

    def on_member_unban(self, member):
        if "on_member_unban" in self.plugins:
            for plugin in self.plugins["on_member_unban"]:
                try:
                    result = yield from plugin.on_member_unban(member)
                    if result:
                        break
                except(TypeError):
                    pass

    def on_typing(self, channel, user, when):
        if "on_typing" in self.plugins:
            for plugin in self.plugins["on_typing"]:
                try:
                    result = yield from plugin.on_typing(channel, user, when)
                    if result:
                        break
                except(TypeError):
                    pass

class Plugin:
    def __init__(self, plugin_manager, file_name):
        self.name = "NONE"
        self.file_name = file_name
        self.plugin_manager = plugin_manager

    def update_help(self):
        return

    def setup(self):
        return

    def on_message(self, message):
        return False

    def on_message_delete(self, message):
        return False

    def on_member_join(self, member):
        return False

    def on_member_remove(self, member):
        return False

    def on_member_update(self, before, after):
        return False

    def on_voice_state_update(self, before, after):
        return False

    def on_member_ban(self, member):
        return False

    def on_member_unban(self, member):
        return False

    def on_typing(self, channel, user, when):
        return False