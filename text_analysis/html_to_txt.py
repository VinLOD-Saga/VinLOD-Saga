import xml.etree.ElementTree as ET

# I need ONLY the original text, without the commentary, to perform the text analysis

def extract_text_xml(file_html, target_file):
    try:
        tree = ET.parse(file_html)
        root = tree.getroot()

        # Finding the titles in the "title-stmt" div
        title_elements = root.findall('.//div[@type="title-stmt"]/title')
        titles = [t.text.strip() for t in title_elements if t.text]

        # Finding the elements in the main text, included the intro and the ballad 
        text_element = root.find('.//div[@type="main-text"]') # ! this is the Poetic Edda's path
        texts = []
        if text_element is not None:
            for elem in text_element.iter(): # iter iterates over ALL the descendants
                if elem.text and elem.text.strip(): # verify elem.text and the potential text in .strip
                    texts.append(elem.text.strip())

        extracted_text = titles + texts
        final_text = "\n".join(extracted_text)

        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(final_text)

        print(f"Text successfully extracted and saved in '{target_file}'.")

    except Exception as e:
        print(f"Oh no! Error: {e}")
