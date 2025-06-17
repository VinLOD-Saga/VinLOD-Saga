import os
from lxml import etree

# Directory corrente (o metti il path che vuoi)
base_dir = os.path.abspath(".")

xml_file = os.path.join(base_dir, "xml_files/Wineland_the_Good/Wineland_the_Good.xml")
xslt_file = os.path.join(base_dir, "xml_files/Wineland_the_Good/Wineland_the_Good.xsl")
output_file = os.path.join(base_dir, "xml_files/Wineland_the_Good/wineland.html")

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
