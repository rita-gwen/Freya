import re

rusFileName = "Freya_rus.txt"
engFileName = "Freya_eng.txt"

with open(rusFileName, encoding = 'UTF8') as f:
    rusLines = f.readlines()

with open(engFileName, encoding = 'UTF8') as f:
    engLines = f.readlines()

bilingFile = open("Freya_bi.html", 'w', encoding = 'UTF8')

bilingFile.write("<html><body><table>")

bilingFile.write("<tr>")
rusParagraph = []
engParagraph = []
paraMark = re.compile(r"\{([0-9]+)\}")
engPos = 0

def appendLine(lst, str):
    if re.match("^##", str):
        str = "<b>" + str + "</b>"
    lst.append(str.replace("\n", "<br>"))

#read lines from the Russian file
for rusLine in rusLines:
    if paraMark.search(rusLine) == None:
        appendLine(rusParagraph, rusLine)
    else:   #until we find the paragraph number
        appendLine(rusParagraph, rusLine)
        paraNum = int( paraMark.search(rusLine).group(1) )
        while paraMark.search( engLines[engPos] ) ==  None:
            appendLine(engParagraph, engLines[engPos])
            engPos += 1
        appendLine(engParagraph, engLines[engPos])
        engPos += 1
        if paraNum != int( paraMark.search(engLines[engPos-1]).group(1) ):
            raise Exception("Paragraph numbering is out of order: rus {rus}, eng: {eng}".format(rus = paraNum, eng = paraMark.search(engLines[engPos-1]).group(1)))
        else:
            bilingFile.write("<td>{para}</td><td>{rus}</td><td>{eng}</td></tr>".format(para = paraNum, rus = "".join(rusParagraph), eng = "".join(engParagraph)))
            rusParagraph.clear()
            engParagraph.clear()



bilingFile.write("</table></body></html>")
bilingFile.close()