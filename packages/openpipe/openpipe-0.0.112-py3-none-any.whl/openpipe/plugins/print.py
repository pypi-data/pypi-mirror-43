"""
Print an item
"""
from openpipe.pipeline.engine import PluginRuntime


class Plugin(PluginRuntime):

    optional_config = """
    $_$     # The item to be printed, the default is the input item
    """

    def on_input(self, item):
        print(self.config)
        self.put(item)
