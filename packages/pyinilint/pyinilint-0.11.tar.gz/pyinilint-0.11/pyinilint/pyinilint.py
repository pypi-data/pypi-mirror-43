"""Lint Python INI-style configuration files."""

import argparse
import configparser
import logging
import os
import sys

__author__ = "Daniel J. R. May"
__copyright__ = "Copyright 2019, Daniel J. R. May"
__credits__ = ["Daniel J. R. May"]
__license__ = "GPLv3"
__version__ = "0.11"
__maintainer__ = "Daniel J. R. May"
__email__ = "daniel.may@danieljrmay.com"
__status__ = "Beta"

EXIT_OK = 0
EXIT_NON_EXISTANT_FILE = 1
EXIT_SYNTAX_ERROR = 2
EXIT_UNREADABLE_FILE = 3
EXIT_DUPLICATE_SECTION = 4
EXIT_DUPLICATE_OPTION = 5
EXIT_INTERPOLATION_MISSING_OPTION = 6
EXIT_INTERPOLATION_DEPTH = 7
EXIT_MISSING_SECTION_HEADER = 8
EXIT_PARSING_ERROR = 9
EXIT_UNKNOWN_ERROR = 10


# pylint: disable=R0912
# pylint: disable=R0915
# Disable too-many-branches and too-many-statements
# It is a reasonable warning as this function is too long, so it
# should be refactored soon.
def main():
    """Entry point"""
    argparser = get_command_line_argument_parser()
    args = argparser.parse_args()

    logging.basicConfig(
        format="[%(levelname)s] %(message)s",
        level=get_log_level(args))
    logging.debug('pyinilint started')
    logging.debug("args=%s", args)

    try:
        validate_args(args)
        rpaths = readable_paths(args.paths)
        config_parser = get_config_parser(args)

        if args.merge:
            lint(config_parser, rpaths, args)
        else:
            for path in rpaths:
                lint(config_parser, path, args)

    except ValueError as val_err:
        logging.error(str(val_err))
        sys.exit(EXIT_SYNTAX_ERROR)
    except FileNotFoundError as fnf_err:
        logging.error(str(fnf_err))
        sys.exit(EXIT_NON_EXISTANT_FILE)
    except PermissionError as perm_err:
        logging.error(str(perm_err))
        sys.exit(EXIT_UNREADABLE_FILE)
    except configparser.DuplicateSectionError as err:
        message = "Section '{}' already exists.".format(err.section)
        error_message = format_error_message(
            "ERROR", "Duplicate section", err.lineno,
            err.source, message)
        print(error_message)
        sys.exit(EXIT_DUPLICATE_SECTION)
    except configparser.DuplicateOptionError as err:
        message = "Option '{}' already exists in section '{}'.".format(
            err.option, err.section)
        error_message = format_error_message(
            "ERROR", "Duplicate option", err.lineno,
            err.source, message)
        print(error_message)
        sys.exit(EXIT_DUPLICATE_OPTION)
    except configparser.InterpolationMissingOptionError as err:
        message = (
            "Option '{}' in section '{}' contains interpolation "
            "key '{}' which does not exist in this fileset.").format(
                err.option, err.section, err.reference)
        error_message = format_error_message(
            "WARNING", "Interpolation missing option", 0,
            rpaths[0], message)
        print(error_message)
        sys.exit(EXIT_INTERPOLATION_MISSING_OPTION)
    except configparser.InterpolationDepthError as err:
        message = ("Recursion limit exceeded in interpolation key '{}' "
                   "in substitution of option '{}' in section '{}'."
                   .format(err.args[2], err.option, err.section))
        error_message = format_error_message(
            "ERROR", "Interpolation depth error", 0,
            rpaths[0], message)
        print(error_message)
        sys.exit(EXIT_INTERPOLATION_MISSING_OPTION)
    except configparser.MissingSectionHeaderError as err:
        message = ("No section header before the line '{}'."
                   .format(err.line.strip()))
        error_message = format_error_message(
            "ERROR", "Missing section header", err.lineno,
            err.source, message)
        print(error_message)
        sys.exit(EXIT_MISSING_SECTION_HEADER)
    except configparser.ParsingError as err:
        error_message = ""
        for line_err in err.errors:
            line_number = line_err[0]
            line = line_err[1]
            message = "Parsing error on line {}.".format(line.strip())
            error_message += "\n" + format_error_message(
                "ERROR", "Parsing error", line_number,
                err.source, message)
        print(error_message)
        sys.exit(EXIT_PARSING_ERROR)
    except configparser.Error as err:
        message = err.message
        error_message = format_error_message(
            "ERROR", "Unknown error", 0,
            rpaths[0], message)
        print(error_message)
        sys.exit(EXIT_UNKNOWN_ERROR)
    finally:
        logging.debug('pyinilint finished')


def get_command_line_argument_parser():
    """Return an ArgumentParser object."""
    description = ('pyinilint (version {}) is a linter and '
                   'inspector for INI format files.'.format(__version__))
    epilog = ('See https://github.com/danieljrmay/pyinilint '
              'for more information.')

    parser = argparse.ArgumentParser(
        prog='pyinilint',
        description=description,
        epilog=epilog
    )
    parser.add_argument(
        '-b', '--basic',
        action='store_true',
        help='use basic interpolation, the default is extended'
    )
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='show debugging messages'
    )
    parser.add_argument(
        '-e', '--encoding',
        help='set the encoding to be used, omit to use the default'
    )
    parser.add_argument(
        '-i', '--interpolate',
        action='store_true',
        help='interpolate the parsed configuration without output'
    )
    parser.add_argument(
        '-m', '--merge',
        action='store_true',
        help='merge files into a single configuration'
    )
    parser.add_argument(
        '-o', '--output',
        action='store_true',
        help='output the parsed configuration to stdout'
    )
    parser.add_argument(
        '-r', '--raw',
        action='store_true',
        help='output raw, do not interpolate'
    )
    parser.add_argument(
        '-s', '--serialize',
        action='store_true',
        help='output the interpolated and serialized configuration to stdout'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='show verbose messages'
    )
    parser.add_argument(
        'paths',
        nargs='+',
        help='paths of the file(s) to check'
    )
    return parser


def get_log_level(args):
    """Return the log level requsted by the command line arguments."""
    if args.debug:
        return logging.DEBUG

    if args.verbose:
        return logging.INFO

    return logging.WARNING


def validate_args(args):
    """Validate the parsed command line arguments."""
    if args.basic and args.raw:
        raise ValueError(
            "The -b (--basic) and -r (--raw) options "
            "can not be used together.")

    if args.debug and args.verbose:
        raise ValueError(
            "The -d (--debug) and -v (--verbose) options "
            "can not be used together.")


def readable_paths(paths):
    """Get a list of readable paths."""
    rpaths = []

    for path in paths:
        if not os.path.isfile(path):
            raise FileNotFoundError("File not found at path {}".format(path))
        elif not os.access(path, os.R_OK):
            raise PermissionError("Unreadable file at path {}".format(path))
        else:
            logging.debug("Readable file at path %s", path)
            rpaths.append(path)

    return rpaths


def get_config_parser(args):
    """Return the config parser."""
    if args.raw:
        return configparser.ConfigParser(interpolation=None)

    if args.basic:
        return configparser.ConfigParser(
            interpolation=configparser.BasicInterpolation())

    return configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation())


def lint(config, paths, args):
    """Lint the INI-style files at the specified paths."""
    logging.debug("About to read paths %s", paths)
    linted_paths = config.read(
        paths,
        args.encoding)

    if args.verbose:
        print("\n".join(linted_paths))

    if args.interpolate:
        logging.debug("Interpolating config:")
        interpolate(config)

    if args.output:
        logging.debug("Printing uninterpolated config:")
        config.write(sys.stdout)

    if args.serialize:
        logging.debug("Serializing interpolated config:")
        print(serialize(config))

    return config


def interpolate(config):
    """Interpolate the parsed config, but do not output anything."""
    for section in config.sections():
        options = config.options(section)
        for option in options:
            config.get(section, option)


def serialize(config):
    """Return the interpolated and serialized config."""
    output = ""

    for section in config.sections():
        output += "[" + section + "]\n"

        options = config.options(section)
        for option in options:
            output += option + " = " + config.get(section, option) + "\n"

        output += "\n"

    return output


def format_error_message(level, identity, line_number, filename, message):
    """Return an error message suitable for flycheck-ini-pyinilint."""
    return "[{}] {} at line {} of {}: {}".format(
        level, identity, line_number, filename, message)


if __name__ == "__main__":
    main()
