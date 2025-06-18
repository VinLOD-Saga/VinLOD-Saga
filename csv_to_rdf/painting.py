import pandas as pd
from rdflib.namespace import RDF, DCTERMS, RDFS
import rdflib as rdf

namespace_dict ={
    "rdf":RDF,
    "rdfs":RDFS,
    "vinLOD":rdf.Namespace("https://w3id.org/vinLOD-saga/property/"),
    "schema": rdf.Namespace("https://schema.org/"),
    "dcterms": DCTERMS,
    "crm":rdf.Namespace("http://www.cidoc-crm.org/cidoc-crm/")
}

def resolve_prefixed_uri(prefix_uri):
    prefix, prop = prefix_uri.split(":", 1)
    namespace = namespace_dict.get(prefix)
    if namespace:
        return namespace[prop]
    else:
        raise ValueError(f"Unknown prefix: {prefix}")

painting_df = pd.read_csv("csv_to_rdf/csv_files/Painting.csv")
graph = rdf.Graph()

# Bind all the namespaces with their prefixes
for prefix, ns in namespace_dict.items():
    graph.bind(prefix, ns)


subj = rdf.URIRef("https://w3id.org/vinLOD-saga/item/Eiriksson_Painting")
for _,row in painting_df.iterrows():
    predicate = resolve_prefixed_uri(row["Predicate"])
    print(predicate)
    if ":" in row["Object"] and not row["Object"].startswith("http"):
        try:
            obj = resolve_prefixed_uri(row["Object"])
        except ValueError:
            obj = rdf.Literal(row["Object"])
    elif row["Object"].startswith("http"):
        obj = rdf.URIRef(row["Object"])
    else:
        obj = rdf.Literal(row["Object"])
    print(obj)
    graph.add((subj, predicate, obj))

print("Graph populated")
graph.serialize(destination="turtle_files/painting.ttl", format="turtle")
