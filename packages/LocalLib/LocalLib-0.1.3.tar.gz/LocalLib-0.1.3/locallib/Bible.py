from locallib import pystrs
from locallib import exc as e
from locallib import dat as d

def GetVerse(version, book, chap, verse):
    if version in d.versions:
        # KJV:
        if version == d.versions[0]:
            fp = open(d.KJV.GetDAT())
            for i, line in enumerate(fp):
                splits = line.split("|")
                if book in d.KJV.books:                 
                    if splits[0] == d.KJV.books[book]:
                        if chap <= int(d.chaps[book]) and chap > int(0):                            
                            if splits[1] == str(chap):
                                if int(verse) <= 176:
                                    if int(verse) > 0:
                                        if splits[2] == str(verse):
                                            return pystrs.RemoveLast(pystrs.RemoveFirst(splits[3], ' '), '~')
                                            fp.close()
                                else:
                                    raise e.VerseOutOfRange(e.iVr)
                        else:
                            raise e.ChapterOutOfRange(e.iC)
                else:
                    raise e.InvalidBook(e.iB)
    else:
        raise e.UnsupportedVersion(e.iV)
