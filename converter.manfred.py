from MyCapytain.resources.collections.cts import XmlCtsWorkMetadata, XmlCtsEditionMetadata
from MyCapytain.common.constants import Mimetypes, get_graph
from MyCapytain.common.reference import URN
from rdflib.namespace import DC, DCTERMS, Namespace
from lxml import etree
import re
from chetc import Epigraph2Markup
from jinja2 import Template
from os import makedirs, path


with open('templates/template.jinja.xml') as f:
    template = Template(f.read())
with open('templates/template.textgroup.xml') as f:
    tgtemplate = Template(f.read())

SAWS = Namespace("http://purl.org/saws/ontology#")

get_graph().bind("dc", DC)
get_graph().bind("dct", DCTERMS)
get_graph().bind("saws", SAWS)

PLACE = re.compile("<b>province:<\/b>(.*)<b>place:<\/b>")
EDCS = re.compile("<b>EDCS-ID:</b> EDCS-(\w+)")
CIL = re.compile("\s*CIL\s*04,\s*(p?\s*[\*a-zA-Z0-9]+)")
CIL_NUMBER = re.compile("^(\d+)\w?$")
TRISMEGISTOS = re.compile("http:\/\/db\.edcs\.eu\/epigr\/partner\.php\?param=.*(T\w+)\"")
TRISMEGISTOS_PLACE = re.compile("http:\/\/www\.trismegistos\.org\/place\/(\w+)")
PUBLICATION = re.compile("publication:<\/b>([a-z,\-\+\/\*A-Z =\(\)0-9]+)<[ab]")
ORT = re.compile("ort='([[a-zA-Z\s\/\-]+)'&amp;latitude='(\d+\.\d+)'&amp;longitude='(\d+\.\d+)'&amp;")

epi_converter = Epigraph2Markup()

with open("sources/Epigraphik Datenbank.html") as source:
    xml = etree.parse(source)
    i = 0
    tgid = "cil04-0000"
    for p in xml.findall("//p"):
        as_string = etree.tostring(p, encoding=str).replace("\n", "")

        text_id, text_image, trismegistos = None, None, None
        placename, longitude, latitude, regio = None, None, None, None
        trismegistos_place = None
        editors = [
            ""
        ]
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
        try:
            trismegistos_place = TRISMEGISTOS_PLACE.findall(as_string)[0]
        except IndexError:
            print("Trismegistos Place not found in {}".format(as_string))

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

        if CIL_NUMBER.match(text_id):
            i = CIL_NUMBER.match(text_id).groups()[0][0:3]
            tgid = "cil004-{}00".format(i)
            i = int(i+"00")
        else:
            i = 0
            tgid = "pages"

        urn = "urn:cts:pompei:{}.{}.manfred-lat1".format(tgid, text_id.strip())

        text = p.xpath(".//br")[-1].tail.replace("&lt;", "<").replace("\n", "").replace("&gt;", ">")
        epi_converter.reset()

        text_converted = epi_converter.convert(text)
        print(text_id, text, text_converted)
        text_xml = template.render(title=text_id, xml=text_converted, urn=urn)

        work = XmlCtsWorkMetadata(urn=(URN(urn)).upTo(URN.WORK))
        work.set_cts_property("title", text_id, lang="eng")

        for ident in additional_ids:
            work.metadata.add(DC.term("identifier"), ident)
        if text_image is not None:
            work.metadata.add(DCTERMS.term("isFormatOf"), text_image)
        if trismegistos is not None:
            work.metadata.add(SAWS.term("identifier"), "www.trismegistos.org/text/"+trismegistos[1:])
        if trismegistos_place is not None:
            work.metadata.add(SAWS.term("isLocatedAt"), "http://www.trismegistos.org/place/"+trismegistos_place)
        if placename is not None:
            work.metadata.add(SAWS.term("isLocatedAt"), placename)
        if longitude is not None and latitude is not None:
            work.metadata.add(SAWS.term("isLocatedAt"), "long:{};lat:{}".format(longitude, latitude))
        if regio is not None:
            work.metadata.add(SAWS.term("isLocatedAt"), regio)
            work.metadata.add(DCTERMS.term("Location"), regio)

        edition = XmlCtsEditionMetadata(urn=urn, parent=work, lang="lat")
        edition.set_cts_property("label", text_id, lang="eng")
        edition.set_cts_property("description", "Automatically converted from Manfred Klaus database")
        edition.metadata.add(DCTERMS.term("provenance"), "http://manfredclauss.de/gb/index.html")
        edition.metadata.add(DCTERMS.term("source"), "http://www.worldcat.org/oclc/459220842")
        edition.metadata.add(DCTERMS.term("contributor"), "Manfred Claus")
        edition.metadata.add(DCTERMS.term("contributor"), "Thibault Clérice")
        edition.metadata.add(DC.term("format"), "text/xml")

        try:
            makedirs("data/{}/{}".format(tgid, text_id.strip()))
        except:
            """Do Nothing"""

        if not path.isfile("data/{}/__cts__.xml".format(tgid)):
            with open("data/{}/__cts__.xml".format(tgid), "w") as tgfile:
                tgfile.write(tgtemplate.render(urn="urn:cts:pompei:"+tgid, start=str(i), end=str(i+100)))

        with open("data/"+tgid+"/"+text_id.strip()+"/{}.{}.manfred-lat1.xml".format(tgid, text_id.strip()), "w") as epidoc:
            epidoc.write(text_xml)

        with open("data/"+tgid+"/"+text_id.strip()+"/__cts__.xml".format(), "w") as metadata:
            metadata.write(work.export(Mimetypes.XML.CapiTainS.CTS).replace("<work", "<work groupUrn=\"{}\"".format(
                "urn:cts:pompei:"+tgid
            )))
        i += 1
