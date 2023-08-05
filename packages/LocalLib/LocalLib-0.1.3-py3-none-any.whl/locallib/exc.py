iV = "The specified version is currently unsupported."
iB = "The specified book is invalid."
iC = "The specified chapter is out of range of valid values."
iVr = "The specified verse is out of range of valid values."

class UnsupportedVersion(Exception):
    pass

class VerseOutOfRange(Exception):
    pass

class InvalidBook(Exception):
    pass

class ChapterOutOfRange(Exception):
    pass
