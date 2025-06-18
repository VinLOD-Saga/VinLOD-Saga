from lxml import etree
from rdflib import Graph, Literal, Namespace, URIRef, RDF, DCTERMS

def get_text_or_none(element):
    """Safely extracts text from an element, returning None if element or text is missing."""
    return element.text.strip() if element is not None and element.text is not None else None

def xml_to_rdf(file):

    # === 1. Parsing MARC ===
    marc_ns = {'marc': 'http://www.loc.gov/MARC21/slim'} 
    try:
        tree = etree.parse(file)
    except Exception as e:
        print(f"Error in parsing: {e}")
        return

    root = tree.getroot()
    
    ### Numbers and Code Fields (datafield 01X-09X) ###
    # 010 - Library of Congress Control Number
    locNumber = get_text_or_none(root.find(".//marc:datafield[@tag='010']/marc:subfield", namespaces=marc_ns)) if root is not None else None
    #041 - Language Code
    langCode = root.find(".//marc:datafield[@tag='041']", namespaces=marc_ns)
    text_lang_en = get_text_or_none(langCode.find("marc:subfield[@code='a']", namespaces=marc_ns)) if root is not None else None
    og_lang_ice = get_text_or_none(langCode.find("marc:subfield[@code='h']", namespaces=marc_ns)) if root is not None else None

    # print(locNumber)
    # print(text_lang_en)
    # print(og_lang_ice)

    ### Main Entry Fields (datafield 1XX) ###
    # 130 - Main Entry-Uniform Title
    uniformTitle = get_text_or_none(root.find(".//marc:datafield[@tag='130']/marc:subfield", namespaces=marc_ns))

    print(uniformTitle)
    
    ### Title and Title-Related Fields (datafield 20X-24X) ###
    # 245 - Title Statement
    titleStmt = root.find(".//marc:datafield[@tag='245']", namespaces=marc_ns)
    title = get_text_or_none(titleStmt.find("marc:subfield[@code='a']", namespaces=marc_ns)) if root is not None else None
    respStmt = get_text_or_none(titleStmt.find("marc:subfield[@code='c']", namespaces=marc_ns)) if root is not None else None

    # print(title)
    # print(respStmt)

    # ### Edition, Imprint, Etc. Fields (datafield 25X-28X) ###
    # # 260 - Publication, Distribution, etc.
    pubStmt = root.find(".//marc:datafield[@tag='260']", namespaces=marc_ns)
    pubPlace = get_text_or_none(pubStmt.find("marc:subfield[@code='a']", namespaces=marc_ns)) if root is not None else None
    pubName = get_text_or_none(pubStmt.find("marc:subfield[@code='b']", namespaces=marc_ns)) if root is not None else None
    pubDate = get_text_or_none(pubStmt.find("marc:subfield[@code='c']", namespaces=marc_ns)) if root is not None else None

    # print(pubPlace)
    # print(pubName)
    # print(pubDate)
    
    # ### Physical Description, Etc. Fields (datafield 3XX) ###
    # # 300 - Physical Description
    physDesc = root.find(".//marc:datafield[@tag='300']", namespaces=marc_ns)
    extent = get_text_or_none(physDesc.find("marc:subfield[@code='a']", namespaces=marc_ns)) if root is not None else None
    physDt = get_text_or_none(physDesc.find("marc:subfield[@code='b']", namespaces=marc_ns)) if root is not None else None
    dimensions = get_text_or_none(physDesc.find("marc:subfield[@code='c']", namespaces=marc_ns)) if root is not None else None

    # print(extent)
    # print(physDt)
    # print(dimensions)

    # ### Series Statement Fields (datafield 4XX) ###
    # # 440 - Series Statement/Added Entry-Title
    seriesStmt = root.find(".//marc:datafield[@tag='440']", namespaces=marc_ns)
    seriesTitle = get_text_or_none(seriesStmt.find("marc:subfield[@code='a']", namespaces=marc_ns)) if root is not None else None
    volNumber = get_text_or_none(seriesStmt.find("marc:subfield[@code='v']", namespaces=marc_ns)) if root is not None else None

    # print(seriesTitle)
    # print(volNumber)

    # ### Note Fields (datafield 5XX) ###
    # # 505 - Formatted Contents Note
    contentNote = root.find(".//marc:datafield[@tag='505']", namespaces=marc_ns)
    note = get_text_or_none(contentNote.find("marc:subfield[@code='a']", namespaces=marc_ns)) if root is not None else None

    # print(note)

    # ### Added Entry Fields (datafield 70X-75X) ###
    # # 700 - Added Entry-Personal Name
    authorDesc = root.find(".//marc:datafield[@tag='700']", namespaces=marc_ns)
    authorName = get_text_or_none(authorDesc.find("marc:subfield[@code='a']", namespaces=marc_ns)) if root is not None else None
    authorDate = get_text_or_none(authorDesc.find("marc:subfield[@code='d']", namespaces=marc_ns)) if root is not None else None

    # print(authorName)
    # print(authorDate)

    # === 2. Building RDF and URIs ===
    g = Graph()

    # # Namespaces
    vinLOD= Namespace("https://w3id.org/vinLOD-saga/")
    BF = Namespace("http://id.loc.gov/ontologies/bibframe/")
    CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/") 

    # # Bind namespaces for cleaner output
    g.bind("bf", BF)
    g.bind("crm", CRM)
    g.bind("vinLOD-saga",vinLOD)
    g.bind("dcterms", DCTERMS)

    # #Entities
    doc_uri = URIRef("https://w3id.org/vinLOD-saga/item/Translated_Poetic_Edda")
    author_uri= URIRef("https://lccn.loc.gov/n88144893")
    E24 = CRM['E24_Physical_Human_Made_Thing'] 
    locURI = URIRef("https://lccn.loc.gov/23016414")

    # === 3. Populating the Graph ===

    g.add((doc_uri, RDF.type, E24)) 
    g.add((doc_uri, BF.agent, author_uri))
    g.add((doc_uri, DCTERMS.identifier, locURI))

    if locNumber:
        g.add((doc_uri, BF.identifiedBy, Literal(locNumber)))
    if text_lang_en:
        g.add((doc_uri, BF.language, Literal(text_lang_en)))
    if og_lang_ice:
        g.add((doc_uri, BF.translationOf, Literal(og_lang_ice)))

    if uniformTitle:
        g.add((doc_uri, BF.variantType, Literal(uniformTitle)))
    if title:
        g.add((doc_uri, BF.mainTitle, Literal(title)))
    if respStmt:
        g.add((doc_uri, BF.subtitle, Literal(respStmt)))

    if pubPlace:
        g.add((doc_uri, BF.place, Literal(pubPlace)))
    if pubName:
        g.add((doc_uri, BF.agent, Literal(pubName)))
    if pubDate:
        g.add((doc_uri, BF.date, Literal(pubDate)))
    
    if extent and physDt:
        g.add((doc_uri, BF.material, Literal(f'{extent} {physDt}')))
    if dimensions:
        g.add((doc_uri, BF.dimensions, Literal(dimensions)))

    if seriesTitle:
        g.add((doc_uri, BF.hasSeries, Literal(seriesTitle)))
    if volNumber:
        g.add((doc_uri, BF.itemPortion, Literal(volNumber)))
    if note:
        part1 = note.split("--")[0]
        part2 = note.split("--")[1]
        g.add((doc_uri, BF.hasPart, Literal(part1)))
        g.add((doc_uri, BF.hasPart, Literal(part2)))

    

    # === 4. Serializing in Turtle ===
    try:
        g.serialize(destination="turtle_files/poetic_edda.ttl", format="turtle")
        print("RDF graph successfully serialized to poetic_edda.ttl")
    except Exception as e:
        print(f"Error during serialization: {e}")

    # Printing for verification
    print("\n--- Triples in Graph ---")
    count= 1
    for s, p, o in g:
        print(f"{count}) {s} {p} {o}")
        count+=1
    print("------------------------")

file = "object_metadata/Poetic_Edda/poetic_edda_marcxml.xml"
xml_to_rdf(file)
