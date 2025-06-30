import os
from rdflib import Graph

# Directory where your TTL files are stored
ttl_directory = "turtle_files"  # ← Change this to your folder path
output_file = "vinLOD_fullDataset.ttl"

# Create an empty graph
merged_graph = Graph()

# Add DNB Ride of the Valkyrie ttl file first
merged_graph.parse("object_metadata/Ride_of_Valkyrie/ride_of_valkyrie(DNB).ttl", format="turtle")

# Loop through all TTL files and parse them
for filename in os.listdir(ttl_directory):
    if filename.endswith(".ttl"):
        file_path = os.path.join(ttl_directory, filename)
        print(f"Parsing: {filename}")
        merged_graph.parse(file_path, format="turtle")

# Serialize the merged graph to a single TTL file
merged_graph.serialize(destination=output_file, format="turtle")
print(f"\n✅ Merged graph saved to: {output_file}")




