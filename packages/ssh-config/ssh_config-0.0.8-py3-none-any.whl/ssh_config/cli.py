import os
import sys
import csv
import abc
import argparse
import logging
import pprint
import inspect
import fnmatch
from functools import partial

from docopt import docopt
from docopt import DocoptExit
from jinja2 import Template

import ssh_config
from .client import SSHConfig, Host

if sys.version_info[0] < 3:
    input = raw_input


def input_is_yes(msg, default="n"):
    if default not in ["y", "n"]:
        raise Exception("Only accept 'y' or 'n'")
    if default is "n":
        msg += " [yN]? "
    else:
        msg += " [Yn]? "
    answer = input(msg)
    if len(answer) == 1 and answer[0].upper() == "Y":
        return True
    return False


class NoExistCommand(Exception):
    def __init__(self, command, supercommand):
        super().__init__("No Exist Command: %s" % command)

        self.command = command
        self.supercommand = supercommand


class DocOptDispather:
    """ssh_config.

    Usage:
        ssh_config [options] [COMMAND] [ARGS...]
        
    Options:
        -h --help           Show this screen.
        -v --version        Show version.
        -f --config FILE    Specify an ssh client file [default: ~/.ssh/config]
        
    Commands:
        ls          Show list of Hosts in client file
        add         Add new Host configuration
        update      UPdate Host configuration
        rm          Remove exist Host configuration
        import      Import Hosts from csv file to SSH Client config
        host        Get Host information
        version     Show version information
    """

    def __init__(self, *argv, **kwargs):
        try:
            options = docopt(self.__doc__, *argv, **kwargs)
        except DocoptExit:
            raise SystemExit(self.__doc__)
        command = options["COMMAND"]

        if command is None:
            raise SystemExit(self.__doc__)

        if not hasattr(self, command):
            if hasattr(self, "_%s" % command):
                command = "_%s" % command
            else:
                raise NoExistCommand(command, self)

        command_handler = getattr(self, command)
        command_docstring = inspect.getdoc(command_handler)
        template = Template(command_docstring, trim_blocks=True, lstrip_blocks=True)
        command_docstring = template.render(attrs=Host.attrs)
        command_options = docopt(command_docstring, options["ARGS"], options_first=True)

        # options, command_handler, command_options
        command_handler(options, command_options)

    def get_sshconfig(self, configpath, create=True):
        sshconfig = None
        config = os.path.expanduser(configpath)
        if os.path.exists(config):
            try:
                sshconfig = SSHConfig.load(config)
            except ssh_config.EmptySSHConfig as e:
                sshconfig = SSHConfig(config)
        elif create:
            answer = input_is_yes(
                "%s does not exists, Do you want to create new one" % config,
                default="n",
            )
            if answer:
                open(config, "w").close()
                print("Created!")
            sshconfig = SSHConfig(config)
        return sshconfig

    def ls(self, options, command_options):
        """
        List hosts.

        usage: ls [options] [PATTERN]

        Options:
            -q --quiet      Only display Names
            -v --verbose    Verbose output
            -h --help       Show this screen
        """
        sshconfig = self.get_sshconfig(options.get("--config"), create=False)
        if sshconfig is None:
            print("No config exist: %s" % options.get("--config"))
            return

        pattern = command_options.get("PATTERN", None)
        for host in sshconfig:
            if pattern is None or fnmatch.fnmatch(host.name, pattern):
                if command_options.get("--quiet"):
                    print(host.name)
                elif command_options.get("--verbose"):
                    print(host)
                else:
                    print("%s: %s" % (host.name, host.HostName))

    def add(self, options, command_options):
        """
        Add host.
        Usage: add [options] (HOSTNAME) <attribute=value>...

        Options:
            --update            If host exists, update it.
            -p --use-pattern    Use pattern to find hosts
            -y --yes            Force answer yes
            -v --verbose        Verbose Output
            -h --help           Shwo this screen

        Attributes:
            {% for attr, attr_type in attrs %}
            {{ attr }}
            {% endfor %}
        """
        sshconfig = self.get_sshconfig(options.get("--config"))
        verbose = command_options.get("--verbose")
        hostname = command_options.get("HOSTNAME")
        attrs = command_options.get("<attribute=value>", [])
        use_pattern = command_options.get("--use-pattern")
        if use_pattern:
            """ use-pattern is only accept update, not add """
            hosts = [host for host in sshconfig if fnmatch.fnmatch(host.name, hostname)]
            if hosts:
                for host in hosts:
                    sshconfig.update(
                        host.name,
                        {attr.split("=")[0]: attr.split("=")[1] for attr in attrs},
                    )
            else:
                print("No hosts found")
                return
        else:
            host = sshconfig.get(hostname, raise_exception=False)
            if command_options.get("--update"):
                if not host:
                    print("No host to be updated, %s" % hostname)
                if verbose:
                    print("Update attributes: %s" % attrs)
                sshconfig.update(
                    hostname, {attr.split("=")[0]: attr.split("=")[1] for attr in attrs}
                )
            else:
                if host:
                    print("%s host already exist" % hostname)
                    return
                host = Host(
                    hostname, {attr.split("=")[0]: attr.split("=")[1] for attr in attrs}
                )
                sshconfig.append(host)

        if command_options.get("--verbose"):
            print("%s" % host)
        if command_options.get("--yes") or input_is_yes("Do you want to save it", default="n"):
            sshconfig.write()

    def rm(self, options, command_options):
        """
        Remove Host.
        Usage: rm [options] (HOSTNAME)

        Options:
            -v --verbose    Verbose output
            -y --yes        Force answer yes
            -h --help       Show this screen
        """
        sshconfig = self.get_sshconfig(options.get("--config"), create=False)
        verbose = command_options.get("--verbose")
        hostname = command_options.get("HOSTNAME")
        host = sshconfig.get(hostname, raise_exception=False)
        if host is None: 
            print("No hostname")
            return
        if verbose:
            print("%s" % host)
        sshconfig.remove(hostname)
        if command_options.get("--yes") or input_is_yes("Do you want to remove %s" % hostname, default="n"):
            sshconfig.write()

    def _import(self, options, command_options):
        """
        Import hosts.
        Usage: import [options] (FILE)

        Options:
            -v --verbose    Verbose output
            -q --quiet      Quiet output
            -y --yes        Force answer yes
            -h --help       Show this screen
        """
        sshconfig = self.get_sshconfig(options.get("--config"), create=True)
        queit = command_options.get("--quiet")
        csv_file = command_options.get("FILE")
        if not csv_file or not os.path.exists(csv_file):
            print("No FILE")
            return
        with open(csv_file) as csvfile:
            reader = csv.DictReader(csvfile)
            if "Name" not in reader.fieldnames:
                print("No Name field")
                return
            for field in reader.fieldnames[1:]:
                if field not in [attr[0] for attr in Host.attrs]:
                    print("Unallowed attribute exist: %s" % field)
                    return
            for row in reader:
                hostname = row.pop("Name")
                host = Host(hostname, row)
                sshconfig.append(host)
                if not queit:
                    print("Import: %s, %s" % (host.name, host.HostName))

        if command_options.get("--yes") or input_is_yes("Do you want to save it", default="n"):
            sshconfig.write()


def main(argv=sys.argv):
    dispatcher = DocOptDispather(
        argv[1:], options_first=True, version="ssh_config %s" % ssh_config.__version__
    )


if __name__ == "__main__":
    main()
