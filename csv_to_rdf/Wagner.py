import pandas as pd
from rdflib.namespace import RDF, DCTERMS
import rdflib as rdf

namespace_dict ={
    "rdf":RDF,
    "vinLOD":rdf.Namespace("https://w3id.org/vinLOD-saga/property/"),
    "schema": rdf.Namespace("https://schema.org/"),
    "bf": rdf.Namespace("http://id.loc.gov/ontologies/bibframe/"),
    "dcterms": DCTERMS,
    "frbroo": rdf.Namespace("http://iflastandards.info/ns/fr/frbr/frbroo/")
}

def resolve_prefixed_uri(prefix_uri):
    prefix, prop = prefix_uri.split(":", 1)
    namespace = namespace_dict.get(prefix)
    if namespace:
        return namespace[prop]
    else:
        raise ValueError(f"Unknown prefix: {prefix}")

anime_df = pd.read_csv("csv_to_rdf/csv_files/Wagner.csv")
graph = rdf.Graph()

# Bind all the namespaces with their prefixes
for prefix, ns in namespace_dict.items():
    graph.bind(prefix, ns)


subj = rdf.URIRef("https://w3id.org/vinLOD-saga/item/Valkyrie_Performance")
for _,row in anime_df.iterrows():
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
graph.serialize(destination="turtle_files/Wagner.ttl", format="turtle")
