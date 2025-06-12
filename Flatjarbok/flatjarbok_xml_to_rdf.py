from lxml import etree
from rdflib import Graph, Literal, Namespace, URIRef, RDF
from rdflib.namespace import DCTERMS 

# ! They did not have the text, but the description of the images since it is a facsimile

# === 1. Parsing TEI ===
tei_ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
tree = etree.parse("C:\Users\ilari\Desktop\PYTHON\TOMASI\GKS02-1005-is.xml")
root = tree.getroot() 

# sourceDesc/msDesc/msIdentifier root
msIdentifier= root.find(".//tei:sourceDesc/tei:msDesc/tei:msIdentifier", namespaces=tei_ns) 

country = msIdentifier.find("tei:country", namespaces=tei_ns).text #bf:originPlace
settlement = msIdentifier.find("tei:settlement", namespaces=tei_ns).text #bf:originPlace
institution = msIdentifier.find("tei:institution", namespaces=tei_ns).text #schema:location
repository = msIdentifier.find("tei:repository", namespaces=tei_ns).text #bf:place
collection = msIdentifier.find("tei:collection", namespaces=tei_ns).text #bf:place
idno = msIdentifier.find("tei:idno", namespaces=tei_ns).text #dcterms:identifier
msname = msIdentifier.find("tei:msName", namespaces=tei_ns).text #dcterms:title
lang= root.find(".//tei:sourceDesc/tei:msDesc", namespaces=tei_ns).get("xml:lang") #bf:language

# /msContents root
msContents=root.find(".//tei:sourceDesc/tei:msDesc/tei:msContents/", namespaces=tei_ns)

# /msItems root
Jomsviking = msContents.find("tei:msItem[@n='10.1']/tei:title", namespaces=tei_ns).text #dcterms:title
Erikrecl = msContents.find("tei:msItem[@n='10.34']/tei:title", namespaces=tei_ns).text #dcterms:title
Greenlender = msContents.find("tei:msItem[@n='10.45']/tei:title", namespaces=tei_ns).text #dcterms:title


# physDesc/support
support= root.find(".//tei:physDesc/tei:objectDesc/tei:support/tei:p/", namespaces=tei_ns).text #dcterms:medium


# === 2. Building RDF and URIs ===
g = Graph()

# Namespaces + DCTERMS
SCHEMA=Namespace("http://example.org/resource/")
BF=Namespace("http://id.loc.gov/ontologies/bibframe/")

#Entities
doc_uri = URIRef["https://handrit.is/manuscript/view/is/GKS02-1005/11#"]
E24= URIRef["http://www.cidoc-crm.org/cidoc-crm/E24_Physical_Human-Made_Thing"]

#Properties
originPlace=URIRef(BF+"originPlace")
place=URIRef(BF+"place")
language=URIRef(BF+"language")
location=URIRef(SCHEMA+"location")

# === 3. Populating the Graph ===

g.add((doc_uri,RDF.type,E24)) # type

g.add((doc_uri, DCTERMS.title, Literal(msname)))
g.add((doc_uri, DCTERMS.title, Literal(Jomsviking)))
g.add((doc_uri, DCTERMS.title, Literal(Erikrecl)))
g.add((doc_uri, DCTERMS.title, Literal(Greenlender)))

g.add((doc_uri, DCTERMS.medium, Literal(support)))
g.add((doc_uri, DCTERMS.identifier, Literal(idno)))

g.add((doc_uri, originPlace, Literal(country)))
g.add((doc_uri, originPlace, Literal(settlement)))
g.add((doc_uri, location, Literal(institution)))
g.add((doc_uri, place, Literal(repository)))
g.add((doc_uri, place, Literal(collection)))

g.add((doc_uri, language, Literal(lang)))

# === 4. Serializing in Turtle ===
g.serialize(destination="flatjarbok_manuscript.ttl", format="turtle")
