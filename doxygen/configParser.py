import logging
import os
import re
from doxygen.exceptions import ParseException


class ConfigParser:
    """
    This class should be used to parse and store a doxygen configuration file
    """

    def __init__(self):
        self.__single_line_option_regex = re.compile("^\s*(\w+)\s*=\s*([^\\\\]*)\s*$")
        self.__first_line_of_multine_option_regex = re.compile("^\s*(\w+)\s*=\s*(.*)\\\\$")

    def load_configuration(self, doxyfile: str) -> dict:
        """
        Parse a Doxygen configuration file
        :param doxyfile: Path to the Doxygen configuration file
        :return: A dict with all doxygen configuration
        :raise FileNotFoundError: When doxyfile doesn't exist
        """

        if not os.path.exists(doxyfile):
            logging.error("Impossible to access to {}".format(doxyfile))
            raise FileNotFoundError(doxyfile)

        configuration = dict()

        with open(doxyfile, 'r') as file:

            in_multiline_option = False
            current_multiline_option_name = None

            for line in file.readlines():
                line = line.strip()
                if len(line) == 0:
                    continue

                if self.__is_comment_line(line):
                    continue

                if in_multiline_option:
                    if not line.endswith('\\'):
                        in_multiline_option = False
                    option_value = line.rstrip('\\').strip()
                    configuration[current_multiline_option_name].append(option_value)

                elif self.__is_first_line_of_multiline_option(line):
                    current_multiline_option_name, option_value = self.__extract_multiline_option_name_and_first_value(line)
                    configuration[current_multiline_option_name] = [option_value]
                    in_multiline_option = True

                elif self.__is_single_line_option(line):
                    option_name, option_value = self.__extract_single_line_option_name_and_value(line)
                    configuration[option_name] = option_value

        return configuration

    def store_configuration(self, config: dict, doxyfile: str):
        """
        Store the doxygen configuration to the disk
        :param config: The doxygen configuration you want to write on disk
        :param doxyfile: The output path where configuration will be written. If the file exist, it will be truncated
        """

        logging.debug("Store configuration in {}".format(doxyfile))

        lines = []
        for option_name, option_value in config.items():
            if type(option_value) is list:
                lines.append("{} = {} \\".format(option_name, self.__add_double_quote_if_required(option_value[0])))
                lines.extend(["\t{} \\".format(self.__add_double_quote_if_required(value)) for value in option_value[1:-1]])
                lines.append("\t{}".format(self.__add_double_quote_if_required(option_value[-1])))
            elif type(option_value) is str:
                lines.append("{} = {}".format(option_name, self.__add_double_quote_if_required(option_value)))

        with open(doxyfile, 'w') as file:
            file.write("\n".join(lines))

    def __extract_multiline_option_name_and_first_value(self, line) -> (str, str):
        """
        Extract the option name and the first value of multi line option
        :param line: The line you want to parse
        :return: the option name and the option first value
        :raise ParseException: When process fail to extract data
        """

        matches = self.__first_line_of_multine_option_regex.search(line)
        if matches is None or len(matches.groups()) != 2:
            logging.error("Impossible to extract first value off multi line option from: {}" % line)
            raise ParseException("Impossible to extract first value off multi line option from: {}" % line)

        return matches.group(1), self.__remove_double_quote_if_required(matches.group(2))

    def __extract_single_line_option_name_and_value(self, line) -> (str, str):
        """
       Extract the option name and the value of single line option
       :param line: The line you want to parse
       :return: the option name and the option value
       :raise ParseException: When process fail to extract data
       """

        matches = self.__single_line_option_regex.search(line)

        if matches is None or len(matches.groups()) != 2:
            logging.error("Impossible to extract option name and value from: {}" % line)
            raise ParseException("Impossible to extract option name and value from: {}" % line)

        return matches.group(1), self.__remove_double_quote_if_required(matches.group(2))

    def __is_single_line_option(self, line: str) -> bool:
        return self.__single_line_option_regex.match(line) is not None

    def __is_comment_line(self, line: str) -> bool:
        return line.startswith("#")

    def __is_first_line_of_multiline_option(self, line) -> bool:
        return self.__first_line_of_multine_option_regex.match(line) is not None

    @staticmethod
    def __remove_double_quote_if_required(option_value: str) -> str:
        """
        Remove the double quote around string in option value.
        Will be replaced when rewrite the configuration
        :param option_value: The value you want to work on
        :return: The option value proper
        """
        if option_value.startswith('"') and option_value.endswith('"'):
            option_value_formatted = option_value[1:-1]
            logging.debug("Remove quote from {} to {}".format(option_value, option_value_formatted))
            return option_value_formatted

        return option_value

    @staticmethod
    def __add_double_quote_if_required(option_value: str) -> str:
        """
        Add the double quote around string in option value if its required
        :param option_value: The value you want to work on
        :return: The option value proper
        """
        if " " in option_value:
            option_value_formatted = '"{}"'.format(option_value)
            logging.debug("Add quote from {} to {}".format(option_value, option_value_formatted))
            return option_value_formatted

        return option_value
