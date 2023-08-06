from pkgutil import get_data
from getpass import getuser
import json
import sys
import os
import subprocess
# from pathlib import Path

name = "qbs"


class qbscolors:
    reset = "\033[0m"
    bold = "\033[1m"
    brightred = "\033[91m"
    brightyellow = "\033[93m"
    green = "\033[32m"
    warn = bold + brightyellow + "Warning:" + reset
    err = bold + brightred + "Error:" + reset


class UnsupportedLanguageError(Exception):
    def __init__(self, lang):
        self.lang = lang

    def __str__(self):
        return "qbs does not know how to build " + self.lang


class UnsupportedCommandError(Exception):
    def __init__(self, command, lang="this language"):
        self.command = command
        self.lang = lang

    def __str__(self):
        return "qbs does not know how to do " + self.command + " for "\
               + self.lang


class AmbiguousCommandError(Exception):
    def __init__(self, command, possibilities, lang="this language"):
        self.command = command
        self.possibilities = possibilities
        self.lang = lang

    def __str__(self):
        return self.command + " could mean " + str(self.possibilities)\
               + " for " + self.lang


class UnsupportedArgumentError(Exception):
    def __init__(self, argument):
        self.argument = argument

    def __str__(self):
        return "argument " + self.argument + " not allowed"


class NoClobberError(Exception):
    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return "refusing to clobber " + self.filename


def parseCommand(command, allowedCommands, lang="no language configured",
                 config={}):
    result = [x for x in allowedCommands if x.startswith(command)]
    if len(result) == 0:
        raise UnsupportedCommandError(command, lang)
    elif len(result) > 1:
        raise AmbiguousCommandError(command, result, lang)
    else:
        result = result[0]
        return result


def getLanguageAlias(lang, config):
    while lang in config and isinstance(config[lang], str):
        lang = config[lang]
    if lang not in config:
        raise UnsupportedLanguageError(lang)
    return lang


def main():
    config = json.loads(get_data("qbs", "conf/default_config.json"))
    config_prefix = []

    if sys.platform.startswith("linux") or \
       sys.platform.startswith("cygwin") or \
       sys.platform.startswith("darwin"):
        config_prefix = ["/etc/",
                         "/home/{user}/.".format(user=getuser()),
                         "/home/{user}/.config/".format(user=getuser()),
                         "./.",
                         "./"]
    elif sys.platform.startswith("win"):
        config_prefix = ["C:\\ProgramData\\qbs\\",
                         "C:\\Users\\{user}\\AppData\\Roaming\\qbs\\"
                         .format(user=getuser()),
                         ".\\"]
    updated = False
    for pref in config_prefix:
        try:
            with open(pref + "qbs.json", "r") as conffile:
                config.update(json.load(conffile))
                updated = True
        except OSError:
            pass  # it's fine if the file doesn't exist
        except json.JSONDecodeError as e:
            print(qbscolors.warn + " parsing of " + conffile.name
                  + " failed:\n" + str(e), file=sys.stderr)
    if not updated:
        print(qbscolors.warn + " could not load any external configuration"
              " files. Using qbs defaults.", file=sys.stderr)
    cache = None
    try:
        with open("./.qbs.cache", "r") as cachefile:
            loadedcache = json.load(cachefile)
            cache = dict()
            cache["lang"] = getLanguageAlias(loadedcache["lang"], config)
            # that shouldn't be necessary but it can't hurt to be safe
            cache["filename"] = loadedcache["filename"]
        if cache["lang"] not in config:
            raise UnsupportedLanguageError(cache["lang"])
    except OSError:
        pass  # this is fine
    except (json.JSONDecodeError, KeyError):
        print(qbscolors.err + " .qbs.cache has been tampered with. Please fix "
              "it or delete it and re-initialize qbs.", file=sys.stderr)
        sys.exit(1)
    except UnsupportedLanguageError as e:
        print(qbscolors.err + " " + str(e) + " (from cache)", file=sys.stderr)
        sys.exit(2)

    arglist = sys.argv[1:]

    allowedCommands = []
    if cache is None:
        allowedCommands = ["init"]
        cache = {"lang": "no language configured"}
    else:
        allowedCommands = list(config[cache["lang"]].keys())
        allowedCommands.append("init")
        # allowedCommands.append("test")

    try:
        i = 0
        while i < len(arglist):
            command = parseCommand(arglist[i], allowedCommands,
                                   cache["lang"], config)
            if command == "init":
                # special case: init supports options
                i += 1
                template = None
                language = None
                while arglist[i].startswith("-"):
                    if arglist[i] == "-t":
                        i += 1
                        template = arglist[i]
                    elif arglist[i] == "-l":
                        i += 1
                        language = arglist[i]
                    else:
                        raise UnsupportedArgumentError(arglist[i])
                    i += 1
                filename = arglist[i]
                filepath, fileext = os.path.splitext(filename)

                if language is None:
                    language = fileext[1:]  # remove the dot
                if template is not None:
                    if os.path.exists(filename):
                        raise NoClobberError(filename)
                    with open(template, "r") as infile,\
                         open(filename, "w") as outfile:
                        for line in infile:
                            line = line.replace("{progname}",
                                                os.path.basename(filepath))
                            line = line.replace("{progext}", fileext)
                            outfile.write(line)
                if language not in config:
                    raise UnsupportedLanguageError(language)
                cache["lang"] = getLanguageAlias(language, config)
                cache["filename"] = filename
                # write out cache
                with open("./.qbs.cache", "w") as cachefile:
                    json.dump(cache, cachefile)
                # regenerate allowed commands
                allowedCommands = list(config[cache["lang"]].keys())
                allowedCommands.append("init")
                # allowedCommands.append("test")
            else:
                filepath, fileext = os.path.splitext(cache["filename"])
                cmdline = [x.format(progname=filepath, progext=fileext)
                           for x in config[cache["lang"]][command]]
                if len(cmdline) > 0:
                    print(qbscolors.green + "+ " + " ".join(cmdline)
                          + qbscolors.reset, file=sys.stderr)
                    cproc = subprocess.run(cmdline)
                    if cproc.returncode != 0:
                        print(qbscolors.err + " nonzero return code "
                              + str(cproc.returncode), file=sys.stderr)
                        sys.exit(cproc.returncode)
                else:
                    print(qbscolors.warn + " doing nothing for " + command,
                          file=sys.stderr)
            i += 1
    except UnsupportedLanguageError as e:
        print(qbscolors.err + " " + str(e), file=sys.stderr)
        sys.exit(2)
    except (AmbiguousCommandError,
            UnsupportedCommandError,
            UnsupportedArgumentError) as e:
        print(qbscolors.err + " " + str(e), file=sys.stderr)
        sys.exit(3)
    except NoClobberError as e:
        print(qbscolors.err + " " + str(e), file=sys.stderr)
        sys.exit(4)
    except OSError as e:
        print(qbscolors.err + " " + str(e), file=sys.stderr)
        sys.exit(1)
