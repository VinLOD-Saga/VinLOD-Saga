from lxml import etree
from rdflib import Graph, Literal, Namespace, URIRef, RDF

def get_text_or_none(element):
    """Safely extracts text from an element, returning None if element or text is missing."""
    return element.text.strip() if element is not None and element.text is not None else None

def xml_to_rdf(file):

    # === 1. Parsing TEI ===
    marc_ns = {'marc': 'http://www.loc.gov/MARC21/slim'} 
    try:
        tree = etree.parse(file)
    except Exception as e:
        print(f"Error in parsing: {e}")
        return

    root = tree.getroot()
    author_datafield = root.find(".//marc:datafield[@tag='100']", namespaces=marc_ns)
    name = get_text_or_none(author_datafield.find("marc:subfield[@code='a']", namespaces=marc_ns)) if author_datafield is not None else None
    name_year = get_text_or_none(author_datafield.find("marc:subfield[@code='d']", namespaces=marc_ns)) if author_datafield is not None else None

    # Title (datafield tag="245")
    title_datafield = root.find(".//marc:datafield[@tag='245']", namespaces=marc_ns)
    main_title = get_text_or_none(title_datafield.find("marc:subfield[@code='a']", namespaces=marc_ns)) if title_datafield is not None else None
    subtitle = get_text_or_none(title_datafield.find("marc:subfield[@code='b']", namespaces=marc_ns)) if title_datafield is not None else None

    # Publication Data (datafield tag="260")
    pub_datafield = root.find(".//marc:datafield[@tag='260']", namespaces=marc_ns)
    place_of_publication = get_text_or_none(pub_datafield.find("marc:subfield[@code='a']", namespaces=marc_ns)) if pub_datafield is not None else None
    publisher = get_text_or_none(pub_datafield.find("marc:subfield[@code='b']", namespaces=marc_ns)) if pub_datafield is not None else None
    pub_date = get_text_or_none(pub_datafield.find("marc:subfield[@code='c']", namespaces=marc_ns)) if pub_datafield is not None else None

    # Description (datafield tag="300")
    phys_desc_datafield = root.find(".//marc:datafield[@tag='300']", namespaces=marc_ns)
    extent = get_text_or_none(phys_desc_datafield.find("marc:subfield[@code='a']", namespaces=marc_ns)) if phys_desc_datafield is not None else None
    phys_details = get_text_or_none(phys_desc_datafield.find("marc:subfield[@code='b']", namespaces=marc_ns)) if phys_desc_datafield is not None else None

    # URI (datafield tag="856")
    all_uris = [] # I needed a list 'cause they have the same datafield, i.e. @tag=856 and didn't want to involve other tags 
    uri_datafields = root.findall(".//marc:datafield[@tag='856']", namespaces=marc_ns)
    for uri_datafield in uri_datafields:
        uri_value = get_text_or_none(uri_datafield.find("marc:subfield[@code='u']", namespaces=marc_ns))
        if uri_value:
            all_uris.append(uri_value)
    
    online_loc = all_uris[0] if all_uris else None
    uri = all_uris[1] if all_uris else None
   
    # === 2. Building RDF and URIs ===
    g = Graph()

    # Namespaces
    vinLOD= Namespace("https://w3id.org/vinLOD-saga/")
    BF = Namespace("http://id.loc.gov/ontologies/bibframe/")
    CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/") 
    FOAF= Namespace("http://xmlns.com/foaf/0.1/")
    VIAF = Namespace("http://viaf.org/viaf/")

    # Bind namespaces for cleaner output
    g.bind("bf", BF)
    g.bind("crm", CRM)
    g.bind("foaf", FOAF)
    g.bind("vinLOD-saga",vinLOD)
    g.bind("viaf", VIAF)

    #Entities
    doc_uri = URIRef("https://w3id.org/vinLOD-saga/item/Finding_of_Wineland")
    author_uri= URIRef("http://viaf.org/viaf/17598880")
    E24 = CRM['E24_Physical_Human_Made_Thing'] 
    E21= CRM['E21_Person']

    #Properties (using defined namespaces directly)
    agent= BF.agent
    main= BF.mainTitle
    sub= BF.subtitle
    place = BF.place
    date = BF.date
    dimensions= BF.dimensions
    elect_loc =BF.electronicLocator
    id= BF.identifiedBy

    # === 3. Populating the Graph ===

    g.add((doc_uri, RDF.type, E24)) # type
    g.add((author_uri, RDF.type, E21))
    g.add((author_uri, FOAF.name,Literal(name)))

    if name:
        g.add((doc_uri, agent, Literal(name)))
    if name_year:
        g.add((doc_uri, agent, Literal(name_year)))
    if main_title:
        g.add((doc_uri, main, Literal(main_title)))
    if subtitle:
        g.add((doc_uri, sub, Literal(subtitle)))
    if place_of_publication:
        g.add((doc_uri, place, Literal(place_of_publication)))
    if publisher:
        g.add((doc_uri, place, Literal(publisher)))
    if pub_date:
        g.add((doc_uri, date, Literal(pub_date)))
    if extent:
        g.add((doc_uri, dimensions, Literal(extent)))
    if phys_details:
        g.add((doc_uri, dimensions, Literal(phys_details)))
    if online_loc:
        g.add((doc_uri, elect_loc, Literal(online_loc)))
    if uri:
        g.add((doc_uri, id, Literal(uri)))

    # === 4. Serializing in Turtle ===
    try:
        g.serialize(destination="turtle_files/Finding_of_Wineland.ttl", format="turtle")
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

file = "object_metadata/Finding_of_Wineland/finding_of_wineland.xml"
xml_to_rdf(file)
