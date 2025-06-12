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
    msIdentifier = root.find(".//tei:sourceDesc/tei:msDesc/tei:msIdentifier", namespaces=tei_ns)
    if msIdentifier is None:
        print("Error: Could not find msIdentifier element.")
        return

    country = get_text_or_none(msIdentifier.find("tei:country", namespaces=tei_ns)) #bf:originPlace # Island 
    settlement = get_text_or_none(msIdentifier.find("tei:settlement", namespaces=tei_ns)) #bf:originPlace # Reykjavík
    institution = get_text_or_none(msIdentifier.find("tei:institution", namespaces=tei_ns)) #schema:location # Stofnun Árna Magnússonar í íslenskum fræðum
    repository = get_text_or_none(msIdentifier.find("tei:repository", namespaces=tei_ns)) #bf:place # Handritasvið
    collection = get_text_or_none(msIdentifier.find("tei:collection", namespaces=tei_ns)) #bf:place # Safn Árna Magnússonar
    idno = get_text_or_none(msIdentifier.find("tei:idno", namespaces=tei_ns)) #dcterms:identifier # GKS 1005 fol.
    msname = get_text_or_none(msIdentifier.find("tei:msName", namespaces=tei_ns)) #dcterms:title # Flateyjarbók

    msDesc_elem = root.find(".//tei:sourceDesc/tei:msDesc", namespaces=tei_ns)
    lang = msDesc_elem.get("{%s}lang" % tei_ns['xml']) if msDesc_elem is not None else None #bf:language

    # physDesc/support
    # Corrected XPath to get text directly from the <p> element within support
    support_elem = root.find(".//tei:physDesc/tei:objectDesc/tei:supportDesc/tei:support/tei:p", namespaces=tei_ns)
    support = get_text_or_none(support_elem) # Skinn

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
    doc_uri = URIRef("https://handrit.is/manuscript/view/is/GKS02-1005/11#")
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
        g.serialize(destination="flatjarbok_manuscript.ttl", format="turtle")
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

file = "TOMASI\XML_TEI\GKS02-1005-is.xml"
xml_to_rdf(file)
