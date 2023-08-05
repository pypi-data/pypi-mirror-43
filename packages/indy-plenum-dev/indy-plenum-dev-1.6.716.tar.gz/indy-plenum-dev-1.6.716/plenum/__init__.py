"""
plenum package

"""
from __future__ import absolute_import, division, print_function

import sys
if sys.version_info < (3, 5, 0):
    raise ImportError("Python 3.5.0 or later required.")

import pip  # noqa
import os   # noqa
import importlib    # noqa
from importlib.util import module_from_spec, spec_from_file_location    # noqa: E402

import plenum   # noqa: E402
import plenum.server.plugin     # noqa: E402

from plenum.common.config_util import getConfigOnce   # noqa: E402

PLUGIN_LEDGER_IDS = set()
PLUGIN_CLIENT_REQUEST_FIELDS = {}


def find_and_load_plugin(plugin_name, plugin_root, installed_packages):
    if plugin_name in installed_packages:
        # TODO: Need a test for installed packages
        plugin_name = plugin_name.replace('-', '_')
        plugin = importlib.import_module(plugin_name)
    else:
        plugin_path = os.path.join(plugin_root.__path__[0],
                                   plugin_name, '__init__.py')
        spec = spec_from_file_location('__init__.py', plugin_path)
        plugin = module_from_spec(spec)
        spec.loader.exec_module(plugin)

    return plugin


def setup_plugins():
    # TODO: Should have a check to make sure no plugin defines any conflicting ledger id or request field
    global PLUGIN_LEDGER_IDS
    global PLUGIN_CLIENT_REQUEST_FIELDS

    config = getConfigOnce()

    plugin_root = config.PLUGIN_ROOT
    try:
        plugin_root = importlib.import_module(plugin_root)
    except ImportError:
        raise ImportError('Incorrect plugin root {}. No such package found'.
                          format(plugin_root))
    sys.path.insert(0, plugin_root.__path__[0])
    enabled_plugins = config.ENABLED_PLUGINS
    installed_packages = {p.project_name: p for p in pip.get_installed_distributions()}
    for plugin_name in enabled_plugins:
        plugin = find_and_load_plugin(plugin_name, plugin_root, installed_packages)
        plugin_globals = plugin.__dict__

        if 'LEDGER_IDS' in plugin_globals:
            PLUGIN_LEDGER_IDS.update(plugin_globals['LEDGER_IDS'])
        if 'CLIENT_REQUEST_FIELDS' in plugin_globals:
            PLUGIN_CLIENT_REQUEST_FIELDS.update(plugin_globals['CLIENT_REQUEST_FIELDS'])

    # Reloading message types since some some schemas would have been changed
    import plenum.common.messages.fields
    import plenum.common.messages.node_messages
    import plenum.common.messages.node_message_factory
    importlib.reload(plenum.common.messages.node_messages)
    importlib.reload(plenum.common.messages.node_message_factory)


setup_plugins()


from .__metadata__ import *  # noqa

from plenum.common.jsonpickle_util import setUpJsonpickle   # noqa: E402
setUpJsonpickle()
