#!/usr/bin/env python
import os
import time
# pylint: disable=useless-import-alias,unused-argument,no-value-for-parameter,too-many-arguments
try:
    import queue as queue
except ImportError:
    import Queue as queue
import click

from netcli.config import Config
from netcli.connect import ConnectThread
from netcli.formatters import Spinner, color_string
from netcli.errors import NetcliError

TIMEOUT = 0.1


@click.group()
@click.pass_context
def cli(ctx):
    """
    If you can't remember any fu....ing CLI command, this is your CLI!
    -> Here you can create your own aliases and apply to every specific CLI language.
    """
    ctx.obj = {
        "config": Config()
    }


@click.group()
@click.pass_context
def config(ctx):
    """
    Manage your custom commands
    """


cli.add_command(config)


@config.command()
@click.argument('command')
@click.pass_context
def add(ctx, command):
    """
    Add a custom command (Example: "custom_command arg1:default)"
    """
    ctx.obj['config'].add(command)


@config.command()
@click.argument('command')
@click.pass_context
def delete(ctx, command):
    """
    Delete a custom command. Example: "custom_command"
    """
    ctx.obj['config'].delete(command)


@config.command()
@click.argument(
    'command',
    required=False,
    )
@click.option(
    '--verbose/--no-verbose',
    default=False,
    help='Provide full detail of custom command.',
)
@click.pass_context
def show(ctx, command, verbose):
    """
    Show custom command details (if no command, brief show of all commands).
    """
    if verbose or command:
        ctx.obj['config'].show(command)
    else:
        ctx.obj['config'].show_brief()
        print()
        print("Please, if you need more info add --verbose option")


@config.command()
@click.argument('command')
@click.pass_context
def edit(ctx, command):
    """
    Edit a custom command
    """
    ctx.obj['config'].edit(command)


@cli.command()
@click.argument('target')
@click.option(
    '--user', '-u',
    default=os.getlogin(),
    help="Specify username to connect, by default the logged user.",
)
@click.option(
    '--password', '-p',
    default=None,
    help="Specify password for user, if not provider SSH keys used.",
)
@click.option(
    '--vendor', '-v',
    required=True,
    help="Define vendor type to pick the right vendor commands.",
)
@click.option(
    '--logging', '--log',
    is_flag=True,
    help="Enable CLI session logging.",
)
@click.pass_context
def connect(ctx, target, user, password, vendor, logging):
    """
    Connect to a device and run and interactive CLI session
    """
    print(color_string(f"\nWelcome {user} to the laziest CLI ever!!!\n", 'green'))

    cli_queue = queue.Queue()
    with Spinner(f"Connecting to {target} using vendor {vendor}"):
        try:
            connection_config = {
                "target": target,
                "user": user,
                "password": password,
                "device_type": vendor,
                "log_enabled": logging,
            }
            connection_thread = ConnectThread(connection_config,
                                              cli_queue)
            connection_thread.start()
            thread_response = cli_queue.get()
            if not thread_response[0]:
                Spinner.result('KO', 'red')
                print(color_string(thread_response[1], 'red'))
                return
        except NetcliError as error:
            Spinner.result('KO', 'red')
            print(color_string(error, 'red'))
            return

    Spinner.result('OK', 'green')
    print()
    print(color_string("Interactive NETCLI", 'green'))
    print()

    end_loop = False
    while not end_loop:
        try:
            user_input = input(color_string('=> ', 'cyan'))
        except (EOFError, KeyboardInterrupt):
            cli_queue.put((True, "end"))
            end_loop = True
            break
        if user_input in ['']:
            continue
        elif user_input in ['help', 'h']:
            ctx.obj['config'].show_brief(cli=True)
            continue
        elif user_input[-1] == '?':
            ctx.obj['config'].show_details(user_input[:-2])
            continue
        elif user_input[0:3] == 'e- ':
            # Edit mode to update commands
            ctx.obj['config'].edit(user_input[3:])
            user_input = 'edit_command'
        print()
        cli_queue.put((True, user_input))
        time.sleep(TIMEOUT)

        if user_input not in ['end', 'exit', 'quit']:
            res = cli_queue.get()
            print(color_string(res[1], "green" if res[0] else "red"))
        else:
            end_loop = True

    time.sleep(TIMEOUT*3)
    print(color_string("Bye, bye!", 'yellow'))


if __name__ == "__main__":
    cli()
