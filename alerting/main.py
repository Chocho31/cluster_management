import importlib

PLUGIN_NAME = "plugins.one"

plugin_module = importlib.import_module(PLUGIN_NAME, ".")

print(plugin_module)

plugin = plugin_module.Plugin("hello world", key=123)

result = plugin.execute(2, 3)

print(result)
