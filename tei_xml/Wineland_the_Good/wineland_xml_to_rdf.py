from lxml import etree
from rdflib import Graph, Literal, Namespace, URIRef, RDF
from rdflib.namespace import DCTERMS, RDFS # Added RDFS for potential future use or better schema definition

def get_text_or_none(element):
    """Safely extracts text from an element, returning None if element or text is missing."""
    return element.text if element is not None else None

def xml_to_rdf(file):
    # === 1. Parsing TEI ===
    tei_ns = {'tei': 'http://www.tei-c.org/ns/1.0', 'xml': 'http://www.w3.org/XML/1998/namespace'}
    try:
        tree = etree.parse(file)
    except Exception as e:
        print(f"Error in parsing: {e}")
        return

    root = tree.getroot()

    # sourceDesc/msDesc/msIdentifier root
    #fileDesc/titleStmt
    titleStmt = root.find(".//tei:fileDesc/tei:titleStmt", namespaces=tei_ns)
    title = get_text_or_none(titleStmt.find("tei:title[@type='main']", namespaces=tei_ns))
    subtitle = get_text_or_none(titleStmt.find("tei:title[@type='main']", namespaces=tei_ns))
    annotator = get_text_or_none(titleStmt.find("tei:respStmt/tei:persName", namespaces=tei_ns))

    #fileDesc/editionStmt
    editionStmt = root.find(".//tei:editionStmt", namespaces=tei_ns)
    edition = get_text_or_none(editionStmt.find("tei:edition", namespaces=tei_ns))
    date = get_text_or_none(editionStmt.find("tei:edition/tei:date", namespaces=tei_ns))

    #fileDesc/extent
    extent = get_text_or_none(editionStmt.find("tei:fileDesc/tei:extent/tei:measure[@unit='kb']", namespaces=tei_ns))

    #fileDesc/publicationStmt
    publicationStmt = root.find(".//tei:fileDesc/publicationStmt", namespaces=tei_ns)
    publisher = get_text_or_none(publicationStmt.find("tei:publisher", namespaces=tei_ns))
    pubPlace = (publicationStmt.find("tei:pubPlace/placeName", namespaces=tei_ns)).get('sameAs')
    licenceURI = (publicationStmt.find("tei:availability/tei:licence", namespaces=tei_ns)).get('target')
    licenceName = get_text_or_none(publicationStmt.find("tei:availability/tei:licence", namespaces=tei_ns))
    licenceComment = get_text_or_none(publicationStmt.find("tei:availability/tei:p", namespaces=tei_ns))

    #projectDesc
    projectDesc = get_text_or_none(root.find(".//tei:projectDesc/tei:p", namespaces=tei_ns))

    # === 2. Building RDF and URIs ===
    g = Graph()

    # Namespaces + DCTERMS, BF, CIDOC-CRM
    SCHEMA = Namespace("http://schema.org/") # Using schema.org for 'location'
    BF = Namespace("http://id.loc.gov/ontologies/bibframe/")
    CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/") # CIDOC CRM namespace

    # Bind namespaces for cleaner output
    g.bind("dcterms", DCTERMS)
    g.bind("bf", BF)
    g.bind("schema", SCHEMA)
    g.bind("crm", CRM)


    #Entities
    doc_uri = URIRef("https://w3id.org/vinLOD-saga/item/Flatjarbok_Manuscript")
    E24 = CRM['E24_Physical_Human-Made_Thing'] # Using CRM namespace for E24

    #Properties (using defined namespaces directly)
    originPlace = BF.originPlace
    place = BF.place
    language_prop = BF.language # Renamed to avoid conflict with 'lang' variable
    location = SCHEMA.location # Using schema.org for location

    # === 3. Populating the Graph ===

    g.add((doc_uri, RDF.type, E24)) # type

    if msname:
        g.add((doc_uri, DCTERMS.title, Literal(msname)))
    if support:
        g.add((doc_uri, DCTERMS.medium, Literal(support)))
    if idno:
        g.add((doc_uri, DCTERMS.identifier, Literal(idno)))

    if country:
        g.add((doc_uri, originPlace, Literal(country)))
    if settlement:
        g.add((doc_uri, originPlace, Literal(settlement)))
    if institution:
        g.add((doc_uri, location, Literal(institution)))
    if repository:
        g.add((doc_uri, place, Literal(repository)))
    if collection:
        g.add((doc_uri, place, Literal(collection)))

    if lang:
        g.add((doc_uri, language_prop, Literal(lang)))
# there should be 10 triples 

    # === 4. Serializing in Turtle ===
    try:
        g.serialize(destination="turtle_files/flatjarbok_manuscript.ttl", format="turtle")
        print("RDF graph successfully serialized to flatjarbok_manuscript.ttl")
    except Exception as e:
        print(f"Error during serialization: {e}")

    # Printing for verification
    print("\n--- Triples in Graph ---")
    count= 1
    for s, p, o in g:
        print(f"{count}) {s} {p} {o}")
        count+=1
    print("------------------------")

file = "object_metadata/Flatjarbok/GKS02-1005-is.xml"
xml_to_rdf(file)
