from lxml import etree
from rdflib import Graph, Literal, Namespace, URIRef, RDF
from rdflib.namespace import DCTERMS, RDFS # Added RDFS for potential future use or better schema definition

def get_text_or_none(element):
    """Safely extracts text from an element, returning None if element or text is missing."""
    return element.text if element is not None else None

def xml_to_rdf(file):
    # === 1. Parsing LIDO/XML ===

    lido_ns = {"lido": "http://www.lido-schema.org", "xml": "http://www.w3.org/XML/1998/namespace"}
    try:
        tree = etree.parse(file)
    except Exception as e:
        print(f"Error in parsing: {e}")
        return

    root = tree.getroot()

    #Go through each section of the file

    ####lido/descriptiveMetadata/objectClassificationWrap###
    objectClass = root.find(".//lido:lido/lido:descriptiveMetadata/lido:objectClassificationWrap", namespaces=lido_ns)
    workType = get_text_or_none(objectClass.find(".//lido:objectWorkType/lido:conceptID[@lido:type='URI']", namespaces=lido_ns)) #nmo:hasObjectType #URI
    nominalClass = get_text_or_none(objectClass.find("lido:classificationWrap/lido:classification/lido:conceptID[@lido:type='URI']", namespaces=lido_ns)) #nmo:hasDenomination #URI
    #using xpath() here to handle to complex path query (more than one attribute)
    creationPeriod = get_text_or_none(objectClass.xpath("lido:classificationWrap/lido:classification/lido:term[@lido:label='division' and @xml:lang='en']", namespaces=lido_ns)[0]) #nmo:hasDate #Literal

    print(workType)
    print(nominalClass)
    print(creationPeriod)

    ####lido/descriptiveMetadata/lido:objectIdentificationWrap###
    objectId = root.find(".//lido:lido/lido:descriptiveMetadata/lido:objectIdentificationWrap", namespaces=lido_ns)
    inscripFront = get_text_or_none(objectId.find(".//lido:inscriptions[@lido:type='front']/lido:inscriptionTranscription", namespaces=lido_ns)) # nmo:hasObverse #literal
    inscripBack = get_text_or_none(objectId.find(".//lido:inscriptions[@lido:type='back']/lido:inscriptionTranscription", namespaces=lido_ns)) # nmo:hasReverse #literal
    legalBody = get_text_or_none(objectId.find(".//lido:repositoryName/lido:legalBodyID", namespaces=lido_ns)) #nmo:hasCollection #URI
    workID = get_text_or_none(objectId.find(".//lido:repositorySet/lido:workID", namespaces=lido_ns)) #DCTERMS.identifier #URI
    measurement = get_text_or_none(objectId.find(".//lido:displayObjectMeasurements", namespaces=lido_ns)) #nmo:hasMeasurement #Literal
    print(inscripFront)
    print(inscripBack)
    print(legalBody)
    print(workID)
    print(measurement)

    ####lido/descriptiveMetadata/lido:eventWrap###
    event = root.findall(".//lido:lido/lido:descriptiveMetadata/lido:eventWrap/lido:eventSet", namespaces=lido_ns)
    creationDate = get_text_or_none(event[1].find(".//lido:eventDate/lido:displayDate", namespaces=lido_ns)) #nmo:hasProductionDate #Literal
    creationPlace = get_text_or_none(event[1].find(".//lido:eventPlace/lido:place[@lido:politicalEntity='minting_place']/lido:placeID", namespaces=lido_ns)) #SCHEMA.locationCreated #URI
    mintMark = get_text_or_none(event[1].find(".//lido:eventPlace/lido:place[@lido:politicalEntity='minting_place']/lido:namePlaceSet/lido:appellationValue", namespaces=lido_ns)) # nmo:hasMintmark  #Literal
    material = get_text_or_none(event[1].find(".//lido:eventMaterialsTech/lido:materialsTech/lido:termMaterialsTech[@lido:type='http://terminology.lido-schema.org/termMaterialsTech_type/material']/lido:conceptID", namespaces=lido_ns)) #nmo:hasMaterial #URI
    technique = get_text_or_none(event[1].find(".//lido:eventMaterialsTech/lido:materialsTech/lido:termMaterialsTech[@lido:type='http://terminology.lido-schema.org/termMaterialsTech_type/technique']/lido:term[@lido:lang='en']", namespaces=lido_ns)) #nmo:hasManufacture #Literal
    findSpot = get_text_or_none(event[2].find(".//lido:eventPlace/lido:place/lido:placeID", namespaces=lido_ns)) # nmo:hasFindspot #URI
    print(creationDate)
    print(creationPlace)
    print(mintMark)
    print(material)
    print(technique)
    print(findSpot)

    # === 2. Building RDF and URIs ===
    
    g = Graph()

    # Namespaces + DCTERMS, BF, CIDOC-CRM
    CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/") # CIDOC CRM namespace
    NMO = Namespace("http://nomisma.org/ontology#") 
    SCHEMA = Namespace("http://schema.org/") #for creation location property

    # Bind namespaces for cleaner output
    g.bind("dcterms", DCTERMS)
    g.bind("schema", SCHEMA)
    g.bind("crm", CRM)
    g.bind("nmo", NMO)

    #Entities
    coin_uri = URIRef("https://w3id.org/vinLOD-saga/item/Cnut_Coin")
    E24 = CRM['E24_Physical_Human-Made_Thing'] # Using CRM namespace for E24
    cnut = URIRef("https://w3id.org/vinLOD-saga/person/Cnut_the_Great")

    # === 3. Populating the Graph ===

    g.add((coin_uri , RDF.type, E24)) # type
    g.add((coin_uri, NMO.hasAuthority, cnut))
    g.add((coin_uri, NMO.hasPortrait, cnut))

    if workType:
        g.add((coin_uri, NMO.hasObjectType, URIRef(workType)))
    if nominalClass:
        g.add((coin_uri, NMO.hasDenomination, URIRef(nominalClass)))
    if creationPeriod:
        g.add((coin_uri, NMO.hasDate, Literal(creationPeriod)))

    if inscripFront:
        g.add((coin_uri, NMO.hasObverse, Literal(inscripFront)))
    if inscripBack:
        g.add((coin_uri, NMO.hasReverse, Literal(inscripBack)))
    if legalBody:
        g.add((coin_uri, NMO.hasCollection, URIRef(legalBody)))
    if workID:
        g.add((coin_uri, DCTERMS.identifier, URIRef(workID)))
    if measurement:
        g.add((coin_uri, NMO.hasMeasurement, Literal(creationPeriod)))

    if creationDate:
        g.add((coin_uri, NMO.hasProductionDate, Literal(creationDate)))
    if creationPlace:
        g.add((coin_uri, SCHEMA.locationCreated, URIRef(creationPlace)))
    if mintMark:
        g.add((coin_uri, NMO.hasMintmark, Literal(mintMark)))
    if material:
        g.add((coin_uri, NMO.hasMaterial, URIRef(material)))
    if technique:
        g.add((coin_uri, NMO.hasManufacture, Literal(technique)))
    if findSpot:
        g.add((coin_uri, NMO.hasFindspot, URIRef(findSpot)))
# there should be 17 triples 

    # === 4. Serializing in Turtle ===
    
    try:
        g.serialize(destination="turtle_files/cnut_coin.ttl", format="turtle")
        print("RDF graph successfully serialized to cnut_coin.ttl")
    except Exception as e:
        print(f"Error during serialization: {e}")

    # Printing for verification
    print("\n--- Triples in Graph ---")
    count= 1
    for s, p, o in g:
        print(f"{count}) {s} {p} {o}")
        count+=1
    print("------------------------")

xml_to_rdf("object_metadata/Cnut_Coin/lido-IKMK-Berlin-18202952.xml")