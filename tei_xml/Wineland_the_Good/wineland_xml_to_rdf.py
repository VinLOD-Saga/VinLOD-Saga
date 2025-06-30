from lxml import etree
from rdflib import Graph, Literal, Namespace, URIRef, RDF, OWL
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
    title = get_text_or_none(titleStmt.find("tei:title[@type='main']", namespaces=tei_ns)) #bf:mainTitle
    subtitle = get_text_or_none(titleStmt.find("tei:title[@type='sub']", namespaces=tei_ns)) #bf:subtitle

    #fileDesc/editionStmt
    editionStmt = root.find(".//tei:editionStmt", namespaces=tei_ns)
    edition = get_text_or_none(editionStmt.find("tei:edition", namespaces=tei_ns)) #bf:editionStatement
    date = get_text_or_none(editionStmt.find("tei:edition/tei:date", namespaces=tei_ns)) #bf:date
    resp = get_text_or_none(editionStmt.find("tei:respStmt/tei:resp", namespaces=tei_ns)) #bf:responsibilityStatement
    annotator = get_text_or_none(editionStmt.find("tei:respStmt/tei:persName", namespaces=tei_ns)) #bf:responsibilityStatement

    #fileDesc/extent
    extent = get_text_or_none(root.find(".//tei:fileDesc/tei:extent/tei:measure[@unit='kb']", namespaces=tei_ns)) #bf:dimensions

    #fileDesc/publicationStmt
    publicationStmt = root.find(".//tei:fileDesc/tei:publicationStmt", namespaces=tei_ns)
    publisher = get_text_or_none(publicationStmt.find("tei:publisher", namespaces=tei_ns)) #bf:agent
    pubPlace = (publicationStmt.find("tei:pubPlace/tei:placeName", namespaces=tei_ns)).get('sameAs') #bf:place
    licenceURI = (publicationStmt.find("tei:availability/tei:licence", namespaces=tei_ns)).get('target') #dcterms:license
    licenceName = get_text_or_none(publicationStmt.find("tei:availability/tei:licence", namespaces=tei_ns)) #dcterms:license
    licenceComment = get_text_or_none(publicationStmt.find("tei:availability/tei:p", namespaces=tei_ns)) #dcterms:license

    #projectDesc
    projectDesc = get_text_or_none(root.find(".//tei:projectDesc/tei:p", namespaces=tei_ns)) #schema:description

    #relevant people and places
    profileDesc = root.find(".//tei:profileDesc", namespaces=tei_ns)
    leifURI = (profileDesc.find(".//tei:person[@xml:id='LE']", namespaces=tei_ns)).get('sameAs')
    erikDBpedia = (profileDesc.find(".//tei:person[@xml:id='ER']", namespaces=tei_ns)).get('source')
    vinlandURI = (profileDesc.find(".//tei:place[@xml:id='VL']", namespaces=tei_ns)).get('sameAs')

    # === 2. Building RDF and URIs ===
    g = Graph()

    # Namespaces + DCTERMS, BF, CIDOC-CRM
    SCHEMA = Namespace("http://schema.org/") # Using schema.org for 'location'
    BF = Namespace("http://id.loc.gov/ontologies/bibframe/")
    CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/") # CIDOC CRM namespace
    vinLOD= Namespace("https://w3id.org/vinLOD-saga/") #

    # Bind namespaces for cleaner output
    g.bind("dcterms", DCTERMS)
    g.bind("bf", BF)
    g.bind("schema", SCHEMA)
    g.bind("crm", CRM)
    g.bind("vinLOD", vinLOD)
    g.bind("owl", OWL)


    #Entities
    doc_uri = URIRef("https://w3id.org/vinLOD-saga/item/Transcribed_Wineland")
    E24 = CRM['E24_Physical_Human-Made_Thing'] # Using CRM namespace for E24
    digital_doc= SCHEMA.DigitalDocument
    wineland_original = URIRef("https://w3id.org/vinLOD-saga/item/Finding_of_Wineland")
    norse_exploration = URIRef("https://w3id.org/vinLOD-saga/event/Norse_Exploration")
    erik = URIRef("https://w3id.org/vinLOD-saga/person/Erik_the_Red")
    erikSaga = URIRef("https://w3id.org/vinLOD-saga/narrative/Erik_Saga")


    # === 3. Populating the Graph ===
    g.add((doc_uri, RDF.type, E24)) # type
    g.add((doc_uri, RDF.type, digital_doc))
    g.add((doc_uri, CRM.P130_shows_features_of, wineland_original))
    g.add((doc_uri, CRM.P129_is_about, URIRef(leifURI)))
    g.add((doc_uri, CRM.P129_is_about, norse_exploration))
    g.add((erik, OWL.sameAs, URIRef(erikDBpedia)))
    g.add((URIRef(leifURI), CRM.P152_has_parent, erik))
    g.add((doc_uri, CRM.P130_shows_features_of, erikSaga))
    g.add((erikSaga, CRM.P129_is_about, erik))

    if title:
        g.add((doc_uri, BF.mainTitle, Literal(title)))
    if subtitle:
        g.add((doc_uri, BF.subtitle, Literal(subtitle)))

    if edition:
        g.add((doc_uri, BF.editionStatement, Literal(edition)))
    if date:
        g.add((doc_uri, BF.date, Literal(date)))
    if resp and annotator:
        g.add((doc_uri, BF.responsibilityStatement, Literal(f'{resp} {annotator}')))

    if extent:
        g.add((doc_uri, BF.dimensions, Literal(extent)))

    if publisher:
        g.add((doc_uri, BF.agent, Literal(publisher)))
    if pubPlace:
        g.add((doc_uri, BF.place, URIRef(pubPlace)))
    if licenceURI:
        g.add((doc_uri, DCTERMS.license, URIRef(licenceURI)))

    if projectDesc:
        g.add((doc_uri, SCHEMA.description, Literal(projectDesc)))

    if erik:
        g.add((doc_uri, CRM.P129_is_about, URIRef(erik)))
    if vinlandURI:
        g.add((doc_uri, CRM.P129_is_about, URIRef(vinlandURI)))

# there should be 10 triples 

    # === 4. Serializing in Turtle ===
    try:
        g.serialize(destination="turtle_files/Transcribed_Wineland.ttl", format="turtle")
        print("RDF graph successfully serialized to Transcribed_Wineland.ttl")
    except Exception as e:
        print(f"Error during serialization: {e}")

    # Printing for verification
    print("\n--- Triples in Graph ---")
    count= 1
    for s, p, o in g:
        print(f"{count}) {s} {p} {o}")
        count+=1
    print("------------------------")

file = "tei_xml/Wineland_the_Good/Wineland_the_Good.xml"
xml_to_rdf(file)
