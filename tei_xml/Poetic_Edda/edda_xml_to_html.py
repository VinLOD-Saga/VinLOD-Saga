import os
from lxml import etree

# Current directory or path
base_dir = os.path.abspath(".")

xml_file = os.path.join(base_dir, "xml_files/Poetic_Edda/Transcribed_Edda.xml")
xslt_file = os.path.join(base_dir, "xml_files/Poetic_Edda/Transcribed_Edda.xsl")
output_file = os.path.join(base_dir, "Transcribed_Edda.html")

# Parsing XML
xml = etree.parse(xml_file)

# Parsing XSLT
xslt = etree.parse(xslt_file)
transform = etree.XSLT(xslt)

# Apply the transformation
result = transform(xml)

# Write in HTML
try:
    with open(output_file, "wb") as f:
        f.write(etree.tostring(result, pretty_print=True, method="html", encoding="UTF-8"))
    print("HTML created successfully:", output_file)
except Exception as e:
    print(f"Error: {e}")
