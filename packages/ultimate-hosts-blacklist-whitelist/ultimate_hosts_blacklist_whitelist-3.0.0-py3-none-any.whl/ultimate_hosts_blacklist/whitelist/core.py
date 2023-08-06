"""
The whitelist script of the Ultimate-Hosts-Blacklist project.

Provide the main logic.

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
# pylint: disable=bad-continuation, logging-format-interpolation
import logging
from itertools import filterfalse

from domain2idna import get as domain2idna

from ultimate_hosts_blacklist.helpers import Download, File, Regex
from ultimate_hosts_blacklist.whitelist.configuration import Configuration
from ultimate_hosts_blacklist.whitelist.match import Match
from ultimate_hosts_blacklist.whitelist.parser import Parser


class Core:  # pylint: disable=too-few-public-methods,too-many-arguments, too-many-instance-attributes
    """
    Brain of our system.
    """

    def __init__(
        self,
        output_file=None,
        secondary_whitelist=None,
        secondary_whitelist_file=None,
        use_official=True,
    ):
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s -- %(message)s", level=logging.INFO
        )

        self.secondary_whitelist_file = secondary_whitelist_file
        self.secondary_whitelist_list = secondary_whitelist
        self.output = output_file
        self.use_core = use_official

        self.parser = Parser()
        self.whitelist_process = self.parser.parse(self.__get_whitelist_list_to_parse())

    def __get_whitelist_list_to_parse(self):
        """
        Return the not parsed/formatted whitelist list.
        """

        if self.use_core:
            result = (
                Download(Configuration.links["core"], destination=None)
                .link()
                .split("\n")
            )
        else:
            result = []

        if self.secondary_whitelist_file and isinstance(
            self.secondary_whitelist_file, list
        ):  # pragma: no cover
            for file in self.secondary_whitelist_file:
                result.extend(file.read().splitlines())

        if self.secondary_whitelist_list and isinstance(
            self.secondary_whitelist_list, list
        ):
            result.extend(self.secondary_whitelist_list)

        return result

    @classmethod
    def format_upstream_line(cls, line):  # pylint: disable=too-many-branches
        """
        Format the given line in order to habe the domain in IDNA format.

        :param line: The line to format.
        :type line: str
        """

        if line.startswith("#"):
            return line

        regex_delete = r"localhost$|localdomain$|local$|broadcasthost$|0\.0\.0\.0$|allhosts$|allnodes$|allrouters$|localnet$|loopback$|mcastprefix$"  # pylint: disable=line-too-long
        comment = ""
        element = ""
        tabs = "\t"
        space = " "

        if Regex(line, regex_delete, return_data=True).match():  # pragma: no cover
            return line

        tabs_position, space_position = (line.find(tabs), line.find(space))

        if not tabs_position == -1:
            separator = tabs
        elif not space_position == -1:
            separator = space
        else:
            separator = None

        if separator:
            splited_line = line.split(separator)

            index = 0
            while index < len(splited_line):
                if (
                    splited_line[index]
                    and not Regex(
                        splited_line[index], regex_delete, return_data=False
                    ).match()
                ):
                    break
                index += 1

            if "#" in splited_line[index]:
                index_comment = splited_line[index].find("#")

                if index_comment > -1:
                    comment = splited_line[index][index_comment:]

                    element = splited_line[index].split(comment)[0]
                    splited_line[index] = domain2idna(element) + comment
            else:
                splited_line[index] = domain2idna(splited_line[index])

            return separator.join(splited_line)
        return domain2idna(line)

    def __write_output(self, line):  # pragma: no cover
        """
        Write the output file.

        :param line: One or multiple lines.
        :type line: str or list

        :return: The lines
        """

        if self.output:
            if isinstance(line, list):
                line = "\n".join(line)

            File(self.output).write("{0}\n".format(line), overwrite=True)

        return line

    def __get_content(
        self, file=None, string=None, items=None, already_formatted=False
    ):  # pragma: no cover
        """
        Return the content we have to check.
        """

        result = []

        if file:
            if not already_formatted:
                with open(file, "r", encoding="utf-8") as file_stream:
                    for line in file_stream:
                        result.append(self.format_upstream_line(line))
            else:
                result = File(file).to_list()
        elif string:
            if not already_formatted:
                for line in string.split("\n"):
                    result.append(self.format_upstream_line(line))
            else:
                result = string.split("\n")
        elif items:
            if not already_formatted:
                for line in items:
                    result.append(self.format_upstream_line(line))
            else:
                result = items

        return result

    def is_whitelisted(self, line):
        """
        Check if the given line is whitelisted.
        """

        logging.debug("Checking line: {0}".format(repr(line)))

        if self.whitelist_process:
            for describer, element in self.whitelist_process:
                if describer == "ends":
                    if Match.ends(line, element):
                        logging.debug(
                            "Line {0} whitelisted by {1} rule: {2}.".format(
                                repr(line), repr(describer), repr(element)
                            )
                        )
                        return True

                    continue  # pragma: no cover

                if describer == "strict":
                    if Match.strict(line, element):
                        logging.debug(
                            "Line {0} whitelisted by {1} rule: {2}.".format(
                                repr(line), repr(describer), repr(element)
                            )
                        )
                        return True

                    continue  # pragma: no cover

                if describer == "regex":
                    if Match.regex(line, element):
                        logging.debug(
                            "Line {0} whitelisted by {1} rule: {2}.".format(
                                repr(line), repr(describer), repr(element)
                            )
                        )
                        return True

                    continue  # pragma: no cover

                if describer == "present":
                    if Match.present(line, element):
                        logging.debug(
                            "Line {0} whitelisted by {1} rule.".format(
                                repr(line), repr(describer)
                            )
                        )
                        return True

                    continue  # pragma: no cover

        logging.debug("Line {0} not whitelisted, no rule matched.".format(repr(line)))
        return False

    def filter(self, file=None, string=None, items=None, already_formatted=False):
        """
        Process the whitelisting.
        """

        if self.whitelist_process:

            return self.__write_output(
                list(
                    filterfalse(
                        self.is_whitelisted,
                        self.__get_content(
                            file=file,
                            string=string,
                            items=items,
                            already_formatted=already_formatted,
                        ),
                    )
                )
            )

        return self.__write_output(
            self.__get_content(
                file=file,
                string=string,
                items=items,
                already_formatted=already_formatted,
            )
        )
