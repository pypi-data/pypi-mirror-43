# coding: utf-8

import json
import os
import os.path
import sys
import time


from .model import create_all, create_session_factory, QueuedExecution
from .monitor import enqueue, Executor


class Cli(object):
    def __init__(self, registry, config):
        self.registry = registry
        self.config = config

    def _get_session(self):
        return create_session_factory(self.config['DBURI'])()

    def command_cron(self):
        print("running cron...")
        session = self._get_session()
        self.registry.dispatch_missing(session)
        session.commit()

    def command_migrate(self, *args):
        """ execute migrations on the database
        """
        from alembic.config import CommandLine, Config
        alembic_cli = CommandLine(prog=None)
        options = alembic_cli.parser.parse_args(args)
        if not hasattr(options, "cmd"):
            alembic_cli.parser.error("too few arguments")
        else:
            ini_path = os.path.join(os.path.dirname(__file__),
                                            'migrations', 'alembic.ini')

            cfg = Config(file_=ini_path,
                            ini_section=options.name,
                            cmd_opts=options)

            cfg.set_main_option("script_location", "probe:migrations")
            cfg.set_main_option("sqlalchemy.url", self.config['DBURI'])

            alembic_cli.run_cmd(cfg, options)

    def command_work(self):
        """ starts the worker
        """
        print("working...")
        session = self._get_session()
        executor = Executor(self.registry, self.config)

        while True:
            executor.dispatch_missing(session)
            session.commit()

            for ex in QueuedExecution.get_all(session):
                print("dispatching Event {} to {}".format(
                                                    ex.event.id, ex.monitor))
                executor.dispatch_execution(session, ex)
            session.commit()
            time.sleep(0.5)

    def command_trigger(self, type, data):
        """ triggers an event
        """
        session = self._get_session()

        enqueue(session, self.registry, type, json.loads(data))
        session.commit()

    def command_help(self):
        """ displays the help message
        """
        print("usage: cli <command> [<args>...]")
        print()
        print("commands:")
        width = max(len(name) for name in self.commands.keys())
        for name, func in self.commands.items():
            print("  {} - {}".format(name.ljust(width),
                                        (func.__doc__ or '').strip()))

    @property
    def commands(self):
        return dict((name[len('command_'):], getattr(self, name))
                        for name in dir(self)
                        if name.startswith('command_'))

    def main(self, args=None):
        if args is None:
            args = sys.argv[1:]
        if not args or args[0] not in self.commands:
            self.command_help()
        else:
            self.commands[args[0]](*args[1:])
