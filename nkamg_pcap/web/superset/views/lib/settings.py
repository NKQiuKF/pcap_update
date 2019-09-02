import os
import re
import subprocess
import string
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class AttribDict(dict):
    def __getattr__(self, name):
        return self[name] if name in self else None

    def __setattr__(self, name, value):
        self[name] = value


config = AttribDict()
CONFIG_FILE = os.path.join(ROOT_DIR, "web.conf")


def read_config(config_file):

    global config

    if not os.path.isfile(config_file):
        exit("[!] missing web configuration file '%s'" % config_file)
    else:
        print "[i] using web configuration file '%s'" % config_file

    config.clear()

    try:
        array = None
        content = open(config_file, "rb").read()

        for line in content.split("\n"):
            line = line.strip('\r')
            line = re.sub(r"\s*#.*", "", line)
            if not line.strip():
                continue

            if line.count(' ') == 0:
                if re.search(r"[^\w]", line):

                    exit("[!] invalid configuration (line: '%s')" % line)
                array = line.upper()
                config[array] = []
                continue

            if array and line.startswith(' '):
                config[array].append(line.strip())
                continue
            else:
                array = None
                try:
                    name, value = line.strip().split(' ', 1)
                except ValueError:
                    name = line
                    value = ""
                finally:
                    name = name.strip().upper()
                    value = value.strip("'\"").strip()

            if any(name.startswith(_) for _ in ("USE_")):
                value = value.lower() in ("1", "true")
            elif value.isdigit():
                value = int(value)
            else:
                for match in re.finditer(r"\$([A-Z0-9_]+)", value):
                    if match.group(1) in globals():
                        value = value.replace(
                            match.group(0), str(
                                globals()[
                                    match.group(1)]))
                    else:
                        value = value.replace(
                            match.group(0), os.environ.get(
                                match.group(1), match.group(0)))
                if subprocess.mswindows and "://" not in value:
                    value = value.replace("/", "\\")

            config[name] = value

    except (IOError, OSError):
        pass
    for option in ("HOST_IP", "HTTP_PORT"):
        if option not in config:
            exit(
                "[!] missing mandatory option '%s' in configuration file '%s'" %
                (option, config_file))
