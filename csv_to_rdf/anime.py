import pandas as pd
from rdflib.namespace import RDF, DCTERMS, RDFS
import rdflib as rdf

namespace_dict ={
    "rdf":RDF,
    "rdfs":RDFS,
    "vinLOD":rdf.Namespace("https://w3id.org/vinLOD-saga/property/"),
    "jvmg": rdf.Namespace("http://mediagraph.link/jvmg/ont#"),
    "frbroo": rdf.Namespace("http://iflastandards.info/ns/fr/frbr/frbroo/"),
    "aclick":rdf.Namespace("http://mediagraph.link/aclick/ont/")
}

def resolve_prefixed_uri(prefix_uri):
    prefix, prop = prefix_uri.split(":", 1)
    namespace = namespace_dict.get(prefix)
    if namespace:
        return namespace[prop]
    else:
        raise ValueError(f"Unknown prefix: {prefix}")

painting_df = pd.read_csv("csv_to_rdf/csv_files/Anime.csv")
graph = rdf.Graph()

# Bind all the namespaces with their prefixes
for prefix, ns in namespace_dict.items():
    graph.bind(prefix, ns)


subj = rdf.URIRef("https://w3id.org/vinLOD-saga/item/Vinland_Anime")
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
graph.serialize(destination="turtle_files/anime.ttl", format="turtle")
