# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

"""This file contains configuration for gcdt tools so we do not need
hardcoded values.
"""

# basic structure:
'''
{
    'kumo': {},
    'tenkai': {},
    'ramuda': {},
    'yugen': {},
    'plugins': {
        '<plugin_name>': {}
    }
}
'''

# note: as a convention this does NOT go into config!
DEFAULT_CONFIG = {
    'ramuda': {
        'settings_file': 'settings.json',
        'runtime': ['python2.7', 'python3.6', 'python3.7', 'nodejs4.3', 'nodejs6.10', 'nodejs8.10'],
        'python_bundle_venv_dir': '.gcdt/venv',
        'keep': False,
        'non_config_commands': ['logs', 'invoke']  # this commands do not require config
    },
    'tenkai': {
        'settings_file': 'settings.json',
        'stack_output_file': 'stack_output.yml',
        'log_group': '/var/log/messages'  # conf from baseami (glomex specific)
    },
    'kumo': {
        'non_config_commands': ['start', 'stop', 'list']  # this commands do not require config
    }
}


# note this config is used in the config_reader to "overlay" the
# gcdt_defaults of gcdt.
CONFIG_READER_CONFIG = {
    # TODO remove baseami
    'lookups': ['secret', 'ssl', 'stack', 'baseami', 'acm'],
    'plugins': {
        'gcdt_slack_integration': {
            'slack_webhook': 'lookup:secret:slack.webhook:CONTINUE_IF_NOT_FOUND'
        },
        'gcdt_lookups': {
            'ami_accountid': '569909643510'
        }
    }
}
