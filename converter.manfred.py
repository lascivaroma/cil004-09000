import MyCapytain
from lxml import etree
import re
from chetc import chetc

with open("replacements.txt") as f:
    replacements = f.read()

PLACE = re.compile("<b>province:<\/b>(.*)<b>place:<\/b>")
EDCS = re.compile("<b>EDCS-ID:</b> EDCS-(\w+)")
CIL = re.compile("\s*CIL\s*04,\s*(p?\s*[\*a-zA-Z0-9]+)")
TRISMEGISTOS = re.compile("http:\/\/db\.edcs\.eu\/epigr\/partner\.php\?param=.*(T\w+)\"")
TRISMEGISTOS_PLACE = re.compile("http:\/\/www\.trismegistos\.org\/place\/(\w+)")
PUBLICATION = re.compile("publication:<\/b>([a-z,\-\+\/\*A-Z =\(\)0-9]+)<[ab]")
ORT = re.compile("ort='([[a-zA-Z\s\/\-]+)'&amp;latitude='(\d+\.\d+)'&amp;longitude='(\d+\.\d+)'&amp;")

with open("sources/Epigraphik Datenbank.html") as source:
    xml = etree.parse(source)
    i = 0
    for p in xml.findall("//p"):#[:50]:
        as_string = etree.tostring(p, encoding=str).replace("\n", "")

        text_id, text_image, trismegistos = None, None, None
        placename, longitude, latitude, regio = None, None, None, None
        additional_ids = []

        try:
            placename, latitude, longitude = tuple(ORT.findall(as_string)[0])
        except IndexError:
            print("ORT definitions not found in {}".format(as_string))

        edcs = EDCS.findall(as_string)
        if len(edcs):
            additional_ids += ["EDCS-"+ed for ed in edcs]

        try:
            trismegistos = TRISMEGISTOS.findall(as_string)[0]
        except IndexError:
            print("Trismegistos not found in {}".format(as_string))

        # Find the Place
        try:
            place = PLACE.findall(as_string)[0].strip()
        except IndexError:
            print("Place not found in {}".format(as_string))

        # Find the Publication ID and image
        try:
            publication = PUBLICATION.findall(as_string)[0].strip()
            text_image = None
            if "CIL" not in publication:
                publication = p.xpath("a")[0]
                text_image = str(publication.get("href")).strip().replace("\n", "")
                publication = publication.text.strip().replace("\n", "")
            publications = publication.split("=")
            text_id = [pub for pub in publications if "CIL 04," in pub][0]
            additional_ids += [pub for pub in publications if "CIL 04," not in pub]
            text_id = CIL.match(text_id).groups()[0].replace("*", "").replace(" ", "")
        except AttributeError:
            print("CIL not found in {}".format(text_id))
        except IndexError:
            print("Publication not found in {}".format(as_string))

        trismegistos_place = TRISMEGISTOS_PLACE.findall(as_string)[0]

        urn = "urn:cts:pompei:cil04.{}.manfred-lat1".format(text_id.strip())
        i += 1

        text = p.xpath(".//br")[-1].tail.replace("&lt;", "<").replace("\n", "").replace("&gt;", ">")
        converter = chetc.Epigraph2Markup(replacements)
        converter.init()
        print(converter.convert(text))
        print(converter.id)