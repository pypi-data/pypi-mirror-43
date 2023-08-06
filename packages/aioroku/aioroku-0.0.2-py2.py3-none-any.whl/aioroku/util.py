from contextlib import closing
from io import BytesIO

import xml.etree.ElementTree as ET


def serialize_apps(apps):

    root = ET.Element('apps')

    for app in apps:
        attrs = {'id': app.id, 'version': app.version}
        elem = ET.SubElement(root, 'app', attrs)
        elem.text = app.name

    with closing(BytesIO()) as bffr:
        tree = ET.ElementTree(root)
        tree.write(bffr, xml_declaration=True, encoding="utf-8")
        content = bffr.getvalue()

    return content
