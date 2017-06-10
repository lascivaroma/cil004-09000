import MyCapytain
#from lxml import etree
from lxml.html import etree
from bs4 import BeautifulSoup
import re
import sys

PLACE = re.compile("<b>province:<\/b>(.*)<b>place:<\/b>")
NOSCRIPT = re.compile("<noscript>.*<\/noscript>")

with open("sources/Epigraphik Datenbank.html") as source:
    content = etree.parse(source)
    content = source.read()
    content = NOSCRIPT.sub("", content)
    xml = BeautifulSoup(content, "lxml")
    print(content[:5000])
    sys.exit()
    for p in xml.find_all("p")[:50]:
        if "publication" in str(p):
            as_string = str(p)
            print(as_string.split("<b>"))
            print(as_string)
            print(PLACE.match(as_string).groups())