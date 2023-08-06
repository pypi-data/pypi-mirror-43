"""
The whitelist script of the Ultimate-Hosts-Blacklist project.

License:
::


    MIT License

    Copyright (c) 2018-2019 Ultimate-Hosts-Blacklist
    Copyright (c) 2018-2019 Nissar Chababy
    Copyright (c) 2019 Mitchell Krog

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import argparse

from colorama import Fore, Style
from colorama import init as initiate

from ultimate_hosts_blacklist.whitelist.core import Core

VERSION = "2.2.0"


def clean_string_with_official_whitelist(data):
    """
    Clean the given string.

    .. note:
        We consider 1 element per line.

    :param data: The string to clean.
    :type data: str

    :return: A string without the whitelisted elements.
    :rtype: string
    """

    return "\n".join(Core(use_core=True).filter(string=data))


def clean_list_with_official_whitelist(data):
    """
    Clean the given list.

    :param data: The list to clean.
    :type data: list

    :return: A list without the whitelisted elements.
    :rtype: list
    """

    return Core(use_core=True).filter(items=data)


def _command_line():
    """
    Provide the CLI.
    """

    # We initiate the auto coloration
    initiate(autoreset=True)

    parser = argparse.ArgumentParser(
        description="The tool to clean a list or a hosts file with the Ultimate Hosts Blacklist whitelist list or your own.",  # pylint: disable=line-too-long
        epilog="Crafted with %s by %s"
        % (
            Fore.RED + "♥" + Fore.RESET,
            Style.BRIGHT + Fore.CYAN + "Nissar Chababy (Funilrys) " + Style.RESET_ALL,
        ),
    )

    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="Read the given file and remove all element to whitelist.",
    )

    parser.add_argument(
        "-w",
        "--whitelist",
        type=argparse.FileType("r"),
        nargs="+",
        help="Read the given file and append its data to the our whitelist list.",
    )

    parser.add_argument(
        "-wc",
        "--without-core",
        action="store_false",
        help="Disable the usage of the Ultimate Hosts Blacklist whitelist list.",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Save the result to the given filename or path.",
    )

    parser.add_argument(
        "-v",
        "--version",
        help="Show the version end exist.",
        action="version",
        version="%(prog)s " + VERSION,
    )

    arguments = parser.parse_args()

    if arguments.file:
        if not arguments.output:
            print(
                "\n".join(
                    Core(
                        secondary_whitelist_file=arguments.whitelist,
                        use_core=arguments.without_core,
                    ).filter(file=arguments.file)
                )
            )
        else:
            Core(
                secondary_whitelist_file=arguments.whitelist,
                output_file=arguments.output,
                use_core=arguments.without_core,
            ).filter(file=arguments.file)
