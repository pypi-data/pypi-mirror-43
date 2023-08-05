from os.path import expanduser, join
import json
import yaml
from netmiko.ssh_dispatcher import CLASS_MAPPER_BASE
from netcli.errors import NetcliError
from netcli.formatters import color_string, load_json


class Config:
    EXIT_WORDS = ["end", 'exit', 'save']
    COMMANDS_PATH = join(expanduser("~"), ".netcli_commands.json")

    CLI_HELP = """
CLI shortcuts:
  - Use 'e- ' to add/edit custom commands
  - Use 'r- ' to run raw commands
  - Use ' | ' to match specific words
  - Use '?' to get command info
"""

    def __init__(self):
        self.custom_commands = load_json(self.COMMANDS_PATH)

    def add(self, command):
        """
        Example: "custom_command arg1:default arg2:555"
        """
        custom_command, args = self._get_custom_command_and_args(command)

        if custom_command in self.custom_commands:
            print(color_string(f"Sorry, custom command {custom_command} already there.", 'red'))
            return

        description = self._ask_description()

        vendor_commands = None
        resp = input("Do you want to add a concrete vendor implementation (y/N)?")
        if resp.lower() in ['y', 'yes']:
            vendor_commands = self._ask_vendor_commands()
        if not vendor_commands:
            print(color_string("Keep in mind that no actual implementation added", 'yellow'))

        self._update(custom_command, description, args, vendor_commands)

        print(color_string(f"Added command {command}", 'green'))

    def edit(self, custom_command):
        if custom_command not in self.custom_commands:
            resp = input(f"Custom command {custom_command} not present yet. Do you want to add it (y/N)?")
            if resp.lower() not in ['y', 'yes']:
                return

        description, args, vendor_commands = None, None, None

        resp = input(f"Do you want to edit description (y/N)?")
        if resp.lower() in ['y', 'yes']:
            description = self._ask_description()

        resp = input(f"Do you want to edit arguments (y/N)?")
        if resp.lower() in ['y', 'yes']:
            args = self._ask_for_args()

        resp = input(f"Do you want to edit vendor commands (y/N)?")
        if resp.lower() in ['y', 'yes']:
            vendor_commands = self._ask_vendor_commands()

        self._update(custom_command, description, args, vendor_commands)
        self._save_to_file()
        print(color_string(f"Edited command {custom_command}", 'green'))

    def delete(self, command):
        res = self.custom_commands.pop(command, None)
        if not res:
            print(color_string("Command doesn't exit", 'red'))
            return

        self._save_to_file()
        print(color_string(f"Deleted command {command}", 'green'))

    def show(self, command):
        if command:
            try:
                print(yaml.dump(self.custom_commands[command], default_flow_style=False))
            except KeyError:
                print(f"Command {command} does not exist.")
        else:
            print(yaml.dump(self.custom_commands, default_flow_style=False))

    def show_brief(self, cli=False):
        if cli:
            print(color_string(self.CLI_HELP, 'yellow'))
        if self.custom_commands:
            print(color_string("  - List of your custom commands:", 'yellow'))
            for command in sorted(self.custom_commands):
                print(color_string(f'    * {command}: {self.custom_commands[command]["description"]}', 'yellow'))

    def show_details(self, command):
        for custom_command in sorted(self.custom_commands):
            if command in custom_command:
                print(color_string(f' * {custom_command}: {self.custom_commands[custom_command]["description"]}',
                                   'yellow'))
                if 'args' in self.custom_commands[custom_command]:
                    print(color_string(f'   {" " * len(custom_command)}  '
                                       '{self.custom_commands[custom_command]["args"]}',
                                       'yellow'))

    def _save_to_file(self):
        try:
            with open(self.COMMANDS_PATH, 'w') as destination_file:
                json.dump(self.custom_commands, destination_file)
        except Exception as error:
            raise NetcliError(error)

    def _ask_vendor_commands(self):
        vendor_commands = {}
        print("Time to add vendor commands, hint: <type> - <command vrf [vrf]>. Remember to end/save")
        user_input = ""
        while user_input.lower() not in self.EXIT_WORDS:
            user_input = input(color_string("=> ", 'cyan'))
            if user_input in ['']:
                continue
            if user_input.lower() not in self.EXIT_WORDS:
                try:
                    vendor_type = user_input.split(" - ")[0]
                    if vendor_type not in CLASS_MAPPER_BASE:
                        print(color_string(f"Vendor type {vendor_type} not supported by Netmiko", 'red'))
                        continue

                    vendor_command = user_input.split(" - ")[1]
                    vendor_commands.update({vendor_type: vendor_command})
                except IndexError:
                    print(color_string("Your command is not following the proper pattern", 'red'))
        return vendor_commands

    @staticmethod
    def _get_custom_command_and_args(command):
        fields = command.split()
        custom_command = []
        arguments = []
        for field in fields:
            if ":" in field:
                arg = field.split(":")
                arguments.append((arg[0], arg[1]))
                continue
            custom_command.append(field)

        return " ".join(custom_command), arguments

    def _update(self, custom_command, description=None, arguments=None, vendor_commands=None):
        """
        "ip table":
            "description": "what it is supposed to do",
            "args": {
                "v": "4",
                "vrf": "default"
            },
            "type": {
                "junos": "show ip route vrf [vrf] ipv[v]",
                "cisco_xr": "show route ipv[v] vrf [vrf]"
            }
        """
        try:
            self.custom_commands[custom_command]
        except KeyError:
            self.custom_commands[custom_command] = {}

        if description:
            self.custom_commands[custom_command]['description'] = description
        if arguments:
            for arg in arguments:
                arg_dict = {arg[0]: arg[1]}
                if 'args' in self.custom_commands[custom_command]:
                    self.custom_commands[custom_command]['args'].update(arg_dict)
                else:
                    self.custom_commands[custom_command]['args'] = arg_dict
        if vendor_commands:
            for vendor_command in vendor_commands:
                vendor_command_dict = {vendor_command: vendor_commands[vendor_command]}
                if 'types' in self.custom_commands[custom_command]:
                    self.custom_commands[custom_command]['types'].update(vendor_command_dict)
                else:
                    self.custom_commands[custom_command]['types'] = vendor_command_dict

        self._save_to_file()

    @staticmethod
    def _ask_description():
        return input("\nPlease provide a useful description that"
                     " will remind you what this command is supposed to do: \n")

    def _ask_for_args(self):
        arguments = []
        print("Time to add arguments, hint: <arg_name> - <default_value>. Remember to end/save")
        user_input = ""
        while user_input.lower() not in self.EXIT_WORDS:
            user_input = input(color_string("=> ", 'cyan'))
            if user_input in ['']:
                continue
            if user_input.lower() not in self.EXIT_WORDS:
                try:
                    fields = user_input.split(":")
                    arguments.append((fields[0], fields[1]))
                except IndexError:
                    print(color_string("Your argument is not following the proper pattern:"
                                       " <arg_name> - <default_value>", 'red'))
        return arguments
