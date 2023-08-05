def Contains(string, substring):
    if substring in string:
        return True
    else:
        return False

def TrimLastChar(string):
    return string[:-1]    

def TrimFirstChar(string):
    return string[1:]

def RemoveAt(string, index):
    return string[:index] + string[index+1:]

def Remove(string, char):
    return string.replace(char, "")

def RemoveFirst(string, char):
    if char in string:        
        return string.replace(char, "", 1)
    else:
        return string

def RemoveLast(string, char):
    if char in string:
        return string[:string.rfind(char)] + "" + string[string.rfind(char)+1:]
    else:
        return string

def RemoveRange(string, startindex, stopindex):
    if len(string) > stopindex:
        string = string[0: startindex:] + string[stopindex + 1::]
        return string
