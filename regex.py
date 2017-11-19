import re

def flatten(array):
    class ListFlattener(list):
        def push(self,*values):
            for value in values:
                if type(value) in [list, tuple, set]:
                    self.push(*value)
                else:
                    self.append(value)
    flat = ListFlattener()
    flat.push(*array)
    return list(filter(None, list(flat)))

def contains(pattern, string, case):
    return bool(re.search(pattern, string, case))

def findall(pattern, string, case):
    return re.findall(pattern, string, case)

def findor(pattern, string, case):
    if '|' not in pattern:
        return re.findall(pattern, string, case)
    regex_match = list(map(list, re.findall(pattern, string, case)))
    return regex_match

def group(pattern, string, case):
    matches = re.findall(pattern, string, case)
    rev = list(sub(pattern, string, '\0', case))
    m = 0
    for i in range(len(rev)):
        if rev[i] == '\0':
            rev[i] = matches[m]
            m += 1
    return rev

def match(pattern, string, case):
    return bool(re.fullmatch(pattern, string, case))

def repeated_sub(pattern, string, replace, case):
    while re.search(pattern, string, case):
        string = re.sub(pattern, replace, string, case)
    return string

def split(pattern, string, case):
    return re.split(pattern, string, case)

def start(pattern, string, case):
    return bool(re.match(pattern, string, case))

def sub(pattern, string, replace, case):
    return re.sub(pattern, replace, string, case)

def unsub(pattern, string, replace, case):
    matches = re.findall(pattern, string, case)
    rev = list(re.sub(pattern, replace, string, case))
    m = 0
    for i in range(len(rev)):
        if rev[i] == replace:
            rev[i] = matches[m]
            m += 1
        else:
            rev[i] = replace
    return ''.join(rev)
