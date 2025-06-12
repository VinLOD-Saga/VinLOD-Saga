import os
from lxml import etree

# Directory corrente (o metti il path che vuoi)
base_dir = os.path.abspath(".")

xml_file = os.path.join(base_dir, "C:\\Users\\ilari\\Desktop\\PYTHON\\TOMASI\\XML_TEI\\The_Poetic_Edda.xml")
xslt_file = os.path.join(base_dir, "C:\\Users\\ilari\\Desktop\\PYTHON\\TOMASI\\XML_TEI\\The_Poetic_Edda.xsl")
output_file = os.path.join(base_dir, "output.html")

# Carica l'XML
xml = etree.parse(xml_file)

# Carica l'XSLT
xslt = etree.parse(xslt_file)
transform = etree.XSLT(xslt)

# Applica la trasformazione
result = transform(xml)

# Scrivi il risultato in HTML
try:
    with open(output_file, "wb") as f:
        f.write(etree.tostring(result, pretty_print=True, method="html", encoding="UTF-8"))
    print("HTML created successfully:", output_file)
except Exception as e:
    print(f"Error: {e}")
