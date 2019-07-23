from lxml import etree

parser = etree.XMLParser(load_dtd=True)
tree = etree.parse('vocabulary.xml')
xmltree = etree.XML(etree.tostring(tree), parser=parser)

for foo in xmltree.findall('action'):
    if foo.find('name').text == 'yes':
        print(etree.tostring(foo, pretty_print=True))
