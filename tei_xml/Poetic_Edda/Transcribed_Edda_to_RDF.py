from lxml import etree
from rdflib import Graph, Literal, Namespace, URIRef, RDF
from rdflib.namespace import RDF, DCTERMS

def get_text_or_none(element):
    """Safely extracts all text (including from child elements), returning None if element is missing."""
    return ''.join(element.itertext()).strip() if element is not None else None # it was the title's fault

def xml_to_rdf(file):

    # === 1. Parsing TEI ===
    tei_ns = {'tei': 'http://www.tei-c.org/ns/1.0'} 
    try:
        tree = etree.parse(file)
    except Exception as e:
        print(f"Error in parsing: {e}")
        return

    root = tree.getroot()

    # title statement 
    title_stmt = root.find(".//tei:teiHeader/tei:fileDesc/tei:titleStmt", namespaces=tei_ns)

    main_title = get_text_or_none(title_stmt.find("tei:title[@type='main']", namespaces=tei_ns)) if title_stmt is not None else None # dcterms: title 
    sub_title = get_text_or_none(title_stmt.find("tei:title[@type='sub']", namespaces=tei_ns)) if title_stmt is not None else None # schema: alternativeHeadline

    resp_stmt = title_stmt.find("tei:respStmt", namespaces=tei_ns) if title_stmt is not None else None
    pers = resp_stmt.find("tei:persName", namespaces=tei_ns) if resp_stmt is not None else None 
    name = f"{get_text_or_none(pers.find('tei:forename', namespaces=tei_ns))} {get_text_or_none(pers.find('tei:surname', namespaces=tei_ns))}" if pers is not None else None # dcterms:contributor (Ilaria De Dominicis)

    # edition statement
    edition_stmt = root.find(".//tei:teiHeader/tei:fileDesc/tei:editionStmt", namespaces=tei_ns)

    edition = get_text_or_none(edition_stmt.find("tei:edition", namespaces=tei_ns)) if edition_stmt is not None else None # bf:editionStatement
    date = get_text_or_none(edition_stmt.find("tei:edition/tei:date", namespaces=tei_ns)) if edition_stmt is not None else None  # date of annotation #dcterms:created

    # extent
    extent = root.find(".//tei:extent", namespaces=tei_ns)
    measure = extent.find("tei:measure", namespaces=tei_ns) if extent is not None else None
    measure_text = get_text_or_none(measure) # bf:dimentions

    # publicationStmt
    pub_stmt = root.find(".//tei:teiHeader/tei:fileDesc/tei:publicationStmt", namespaces=tei_ns) 
    publisher = pub_stmt.find("tei:publisher", namespaces=tei_ns) if pub_stmt is not None else None 
    publisher_text = ''.join(publisher.itertext()).strip() if publisher is not None else None  # bf:agent

    pub_place = pub_stmt.find("tei:pubPlace", namespaces=tei_ns) if pub_stmt is not None else None 
    place_name = pub_place.find("tei:placeName", namespaces=tei_ns) if pub_place is not None else None
    place_uri = place_name.get("sameAs") if place_name is not None else None  # bf:place

    pub_date = pub_place.find("tei:date", namespaces=tei_ns) if pub_place is not None else None
    pub_date_text = get_text_or_none(pub_date) # bf:date

    availability = pub_stmt.find("tei:availability", namespaces=tei_ns) if pub_stmt is not None else None
    licence = availability.find("tei:licence", namespaces=tei_ns) if availability is not None else None
    availability_text = licence.get("target") if license is not None else None # dcterms:rights 

   # Valkyries
    list_org = root.find(".//tei:teiHeader/tei:profileDesc/tei:particDesc/tei:listOrg", namespaces=tei_ns)

    # valkyries = get_text_or_none(list_org.find("tei:org/tei:orgName", namespaces=tei_ns)) if list_org is not None else None # Valkyries
    valkyries = list_org.find("tei:org/tei:orgName", namespaces=tei_ns).get("sameAs") if list_org is not None and list_org.find("tei:org/tei:orgName", namespaces=tei_ns) is not None else None # Valkyries URI

    # Valhalla
    list_place = root.find(".//tei:teiHeader/tei:profileDesc/tei:settingDesc/tei:listPlace", namespaces=tei_ns)
    valhall = list_place.find("tei:place/tei:placeName", namespaces=tei_ns).get("sameAs") if list_place is not None and list_place.find("tei:place/tei:placeName", namespaces=tei_ns) is not None else None # Valhalla URI

# ? Adding has online location ? Even on the te?

    # === 2. Building RDF and URIs === 
    g = Graph()

    # Namespaces
    vinLOD= Namespace("https://w3id.org/vinLOD-saga/")
    BF = Namespace("http://id.loc.gov/ontologies/bibframe/")
    SCHEMA = Namespace("https://schema.org/")
    CRM= Namespace("http://www.cidoc-crm.org/cidoc-crm/")

    # Bind namespaces for cleaner output
    g.bind("bf", BF)
    g.bind("schema", SCHEMA)
    g.bind("crm", CRM)

    #Entities       
    doc_uri= URIRef("https://w3id.org/vinLOD-saga/item/Transcribed_Edda")
    valkyries_URI= URIRef(valkyries)
    valhall_URI= URIRef(valhall)
    # ? my URI
    Digital_doc= SCHEMA.DigitalDocument
    Poetic_Edda = vinLOD["item/Translated_Poetic_Edda"]

    #Properties (using defined namespaces directly)
    title= DCTERMS.title
    sub= SCHEMA.alternativeHeadline
    contributor= DCTERMS.contributor
    edition_statement = BF.editionStatement
    date_created = DCTERMS.created
    measurements= BF.dimensions
    agent= BF.agent
    place= BF.place
    bf_date= BF.date
    rights = DCTERMS.rights
    shows_features_of= CRM.P130_shows_features_of
    is_about= CRM.P129_is_about

    # === 3. Populating the Graph ===

    g.add((doc_uri, RDF.type, Digital_doc)) # type
    g.add((doc_uri, shows_features_of, Poetic_Edda))
    g.add((doc_uri, is_about, valkyries_URI))
    g.add((doc_uri, is_about, valhall_URI))
    
    if main_title:
        g.add((doc_uri, title, Literal(main_title))) 
    if sub_title:
        g.add((doc_uri, sub, Literal(sub_title))) 
    if name:
        g.add((doc_uri, contributor, Literal(name)))
    if edition:
        g.add((doc_uri, edition_statement, Literal(edition)))
    if date:
        g.add((doc_uri, date_created, Literal(date)))
    if measure_text:
        g.add((doc_uri, measurements, Literal(measure_text)))
    if publisher_text:
        g.add((doc_uri, agent, Literal(publisher_text)))
    if place_uri:
        g.add((doc_uri, place, Literal(place_uri)))
    if pub_date_text:
        g.add((doc_uri, bf_date, Literal(pub_date_text)))
    if availability_text:
        g.add((doc_uri, rights, Literal(availability_text)))

    # === 4. Serializing in Turtle ===
    try:
        g.serialize(destination="turtle_files/Transcribed_Edda.ttl", format="turtle")
        print("RDF graph successfully serialized to finding_of_Wineland.ttl")
    except Exception as e:
        print(f"Error during serialization: {e}")

    # Printing for verification
    print("\n--- Triples in Graph ---")
    count= 1
    for s, p, o in g:
        print(f"{count}) {s} {p} {o}")
        count+=1
    print("------------------------")

file = "tei_xml/Poetic_Edda/Transcribed_Edda.xml"
xml_to_rdf(file)