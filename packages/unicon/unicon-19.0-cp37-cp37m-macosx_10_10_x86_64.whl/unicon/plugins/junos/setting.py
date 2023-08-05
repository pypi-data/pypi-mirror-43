"""
Module:
    unicon.plugins.junos

Authors:
    PyATS TEAM (pyats-support@cisco.com)

Description:
  This module defines the Junos settings to setup
  the unicon environment required for generic based
  unicon connection
"""
from unicon.settings import Settings

class JunosSettings(Settings):
    """" Junos platform settings """

    def __init__(self):
        super().__init__()
        self.HA_INIT_EXEC_COMMANDS = [
            'set cli screen-length 0',
            'set cli screen-width 0'
        ]
        self.CONSOLE_TIMEOUT = 60
        self.ATTACH_CONSOLE_DISABLE_SLEEP = 100

        # Default error pattern
        self.ERROR_PATTERN=[]

        # Maximum number of retries for password handler
        self.PASSWORD_ATTEMPTS = 3

        # User defined login and password prompt pattern.
        self.LOGIN_PROMPT = None
        self.PASSWORD_PROMPT = None

        # Ignore log messages before executing command
        self.IGNORE_CHATTY_TERM_OUTPUT = False

        # When connecting to a device via telnet, how long (in seconds)
        # to pause before checking the spawn buffer
        self.ESCAPE_CHAR_CHATTY_TERM_WAIT_RETRIES = 12
        # number of cycles to wait for if the terminal is still chatty
        self.ESCAPE_CHAR_CHATTY_TERM_WAIT = 0.25

        # prompt wait retries
        # (wait time: 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75 == total wait: 7.0s)
        self.ESCAPE_CHAR_PROMPT_WAIT_RETRIES = 7
        # prompt wait delay
        self.ESCAPE_CHAR_PROMPT_WAIT = 0.25
