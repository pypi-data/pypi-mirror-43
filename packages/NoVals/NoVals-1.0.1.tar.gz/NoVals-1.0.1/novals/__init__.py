name = "novals"

import sys, os, re

class FoundString(Exception):
    def __init__(self, lineNumber):
        super().__init__("Found string on line: %i" % lineNumber)

class FoundNumber(Exception):
    def __init__(self, lineNumber):
        super().__init__("Found number on line: %i" % lineNumber)

class FoundNone(Exception):
    def __init__(self, lineNumber):
        super().__init__("Found NoneType on line: %i" % lineNumber)

class FoundBool(Exception):
    def __init__(self, lineNumber):
        super().__init__("Found boolean on line: %i" % lineNumber)

with open(os.path.abspath(sys.argv[0])) as f:
    lines = [line.strip() for line in f]

for lineNumber, line in enumerate(lines):
    if "'" in line or "\"" in line or "`" in line:
        raise FoundString(lineNumber+1)
    if re.search("^(.*[^a-zA-z])?[0-9]", line) is not None:
        raise FoundNumber(lineNumber+1)
    for m in re.finditer("^(.*[^a-zA-z])?None", line):
        raise FoundNone(lineNumber+1)
    for m in re.finditer("^(.*[^a-zA-z])?(True|False)", line):
        raise FoundBool(lineNumber+1)
