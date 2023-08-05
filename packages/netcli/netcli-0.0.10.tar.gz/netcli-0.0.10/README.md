[![Build Status](https://travis-ci.org/chadell/netcli.svg?branch=master)](https://travis-ci.org/chadell/netcli)

# NETCLI

netcli is the CLI for the people who doesn't want to remember every command from every vendor gear.

Networking nowadays is moving away from traditional CLI operation, but there is still some debugging use-cases when a CLI interaction gives some benefits. However, when you spend more time coding than CLIing, you end up forgetting about specific CLI syntax, still necessary when you are managing a multi-vendor fleet.

To ovecome this issue, **netcli** lets you create your own CLI language, for interact with any device using your own custom commands.

netcli solves this problem using a simple approach:
* You have a **config** mode to handle your custom commands and the translation for all the specific vendors you are interested in.
* You have a **connect** mode to run an interactive CLI against your devices and enjoy your commands

## Installation

```
pip install netcli
```

## How to run it

## Config

> Your customs commands will be stored in `~/.my_netcli_commands.json`

### Add

```
$ netcli config add "bgp received routes neighbor:192.0.2.1"
```

Note:
* Use quotes to add your command
* Arguments should come at the end, using the pattern `<arg_name>:<default_value>`

This will enter an interactive mode to provide:
* Description: Useful to remember what this command is doing
* Vendor specific implementations, using this format: `<vendor_type> - <vendor_command>`
    * **important** within `<vendorcommand>` you can place the arguments provided using `[arg_name]`
    * Example: `show bgp summary [instance (vrf)]`
        * Every argument is between square brackets `[]`
        * Within the brackets, the parenthesis `()` is the keyword that will be replaced
        * If an argument keyword has the string value "None", the argument (and related text) will be omitted
    * `<vendor_type>` comes from [Netmiko library](https://github.com/ktbyers/netmiko/blob/develop/netmiko/ssh_dispatcher.py#L76)

### Delete

```
$ netcli config delete "bgp received routes"
```

### Show

```
$ netcli config show
```

It listes the custom commands with the description and ports.
If you need the vendor implementation, use `--verbose`


## Interactive CLI

```
$ netcli connect <target> -v <vendor_type>
```

Enjoy it!

Notes:
* To overwrite a default value use `[<arg_name>:<new_value>]`
* Execution of **raw commands** is possible starting the command with `r- ` 
* **Matching output** of custom commands can be achieved by adding ` | ` and the string to match
* Use `help`/`h` to get extra help

### Default options

You can overwrite default behaviours by using file `~/.netcli.cfg` to define some custom values to easy your operation:

```
{
        "dns_suffix": ".opendns.com",
        "global_delay_factor": 6,
        "max_lines": 20
}
```

Supported values:

* **dns_suffix** is concatenated at the end of your target name
* **max_lines** limit the maximum number of lines to be returned to the CLI (this doesn't affect the logs)
* **log_path** full path to store the logging of the session. By default is the current directory with the timestamp (i.e. netcli_20190303-194937)
* **timeout** Netmiko timeout
* **global_delay_factor** Netmiko global_delay_factor
