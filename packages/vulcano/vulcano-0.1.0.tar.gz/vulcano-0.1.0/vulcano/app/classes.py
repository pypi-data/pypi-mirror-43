# -* coding: utf-8 *-
"""
:py:mod:`vulcano.app.classes`
-----------------------------
Vulcano APP Classes
"""
# System imports
import sys

# Third-party imports
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

# Local imports
from vulcano.command import builtin
from vulcano.core.classes import Singleton
from vulcano.command.classes import CommandManager
from vulcano.command.parser import inline_parser


class VulcanoApp(Singleton):
    """ VulcanoApp is the class choosen for managing the application.

    It has the all the things needed to command/execute/manage commands."""

    def __init__(self):
        #: List of commands registered under this Vulcano APP
        self._manager = getattr(
            self, "_manager", CommandManager()
        )  # type: CommandManager
        self.context = getattr(self, "context", {})  # Type: dict

    @property
    def request_is_for_args(self):
        """ Returns if the request is for running with args or in REPL mode

        :return: Request is to be run with args or not
        :rtype: bool
        """
        return len(sys.argv) >= 2

    def command(self, *args, **kwargs):
        """ Register a command under current Vulcano instance

        For more options take a look at `vulcano.command.classes.CommandManager.command`
        """
        return self._manager.command(*args, **kwargs)

    def run(self):
        """ Start the application

        It will run the application in Args or REPL mode, depending on the
        parameters sent"""
        self._prepare_builtins()
        if self.request_is_for_args:
            self._exec_from_args()
        else:
            self._exec_from_repl()

    def _prepare_builtins(self):
        self._manager._register_command(builtin.exit, "exit")
        self._manager._register_command(builtin.help(self), "help")

    def _exec_from_args(self):
        command = sys.argv[1]
        arguments = sys.argv[2:]
        self._manager.run(command, *arguments)

    def _exec_from_repl(self):
        self.do_repl = True
        sql_completer = WordCompleter(self._manager.command_names, ignore_case=True)
        session = PromptSession(completer=sql_completer)
        while self.do_repl:
            try:
                user_input = session.prompt(u">> ")
            except KeyboardInterrupt:
                continue  # Control-C pressed. Try again.
            except EOFError:
                break  # Control-D Pressed. Finish

            try:
                command = user_input.split()[0]
                arguments = " ".join(user_input.split()[1:])
                args, kwargs = inline_parser(arguments)
                self._manager.run(command, *args, **kwargs)
            except Exception as error:
                print("Error executing: {}. Error: {}".format(command, error))
