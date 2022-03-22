import xml.dom.minidom
import yaml


attrib = {
    'xmlns:xs': "http://www.w3.org/2001/XMLSchema",
    'xmlns:oor': "http://openoffice.org/2001/registry",
    'oor:name': "Addons",
    'oor:package': "org.openoffice.Office",
}

LIB = "com.rdt.comp.Utils"
MODULE = 'rdt_tools'
IMAGE_LOCATION = "%origin%/assets/"


def get_command_line(command):
    lib = f"vnd.sun.star.script:{MODULE}.oxt|python|{MODULE}.py$"
    return f"{lib}{command}?language=Python&location=user:uno_packages"

AT_REPLACE = ('oor:op', 'replace')
at_name = lambda x: ('oor:name', x)


def get_node(doc, *args):
    node = doc.createElement('node')
    for a in args:
        node.setAttribute(a[0], a[1])
    return node


class AddonUi:

    def __init__(self, conf_path: str = 'make/addon_ui.yml'):
        self.read_addon_yaml(conf_path)
        self.doc = xml.dom.minidom.Document()
        root = self.doc.createElementNS(
            "http://openoffice.org/2001/registry", 'oor:component-data')
        [root.setAttribute(k, v) for k, v in attrib.items()]
        self.doc.appendChild(root)
        n_addonUI = self.doc.createElement('node')
        n_addonUI.setAttribute('oor:name', 'AddonUI')
        root.appendChild(n_addonUI)

        # add Office Menu Bar
        n_addonUI.appendChild(self.build_menu_bar())

        # different strategy as we build tb & images in the same time
        self.build_toolbar(n_addonUI)

    def build_menu_bar(self):
        mb = get_node(self.doc, at_name('OfficeMenuBar'))

        node = get_node(self.doc, at_name(LIB), AT_REPLACE)
        mb.appendChild(node)

        node.appendChild(get_prop(self.doc, 'Title', 'RDT'))
        node.appendChild(get_prop(self.doc, 'Target', '_self'))
        node.appendChild(get_prop(self.doc, 'ImageIdentifier'))

        menu_bar_conf = self.conf.get('OfficeMenuBar')
        submenu = node.appendChild(self.get_new_submenu_node())
        for i, (k, v) in enumerate(menu_bar_conf.items(), 1):
            if not 'submenu' in v.keys():
                m = MenuEntry(self.doc, k, v['title'], i)
                submenu.appendChild(m.root)
            else:
                node.appendChild(self.create_subentries(v, i))
        return mb

    def build_toolbar(self, root):
        tb = get_node(self.doc, at_name('OfficeToolBar'),)
        tb_node = get_node(self.doc, at_name(LIB), AT_REPLACE)
        tb.appendChild(tb_node)
        root.appendChild(tb)

        # images
        tb_images = get_node(self.doc, at_name('Images'))
        root.appendChild(tb_images)

        toolbar_conf = self.conf.get('OfficeToolBar')
        for i, (k,v) in enumerate(toolbar_conf.items(), 1):
            tb_node.appendChild(MenuEntry(self.doc, k, v['title'], i, v['context']).root)
            tb_images.appendChild(ImageEntry(self.doc, k, v['icon'], i).root)

    def create_subentries(self, entries: dict, i: int):
        submenu = get_node(self.doc, at_name('Submenu'))
        node = get_node(self.doc, at_name(f"N{i:03}"), AT_REPLACE)
        submenu.appendChild(node)

        node.appendChild(get_prop(self.doc, 'Title', entries['title']))
        for i, (k, v) in enumerate(entries.get('submenu').items(), 1):
            if not 'submenu' in v.keys():
                m = InnerMenuEntry(self.doc, k, v['title'], i)
                node.appendChild(m.root)
        return submenu

    def get_new_submenu_node(self):
        nn = self.doc.createElement('node')
        nn.setAttribute('oor:name', 'Submenu')
        return nn

    def read_addon_yaml(self, conf_path):
        with open(conf_path, 'r') as f:
            self.conf = yaml.safe_load(f)


def get_prop(doc, name, value=''):
    prop = doc.createElement('prop')
    prop.setAttribute('oor:type', 'xs:string')
    prop.setAttribute('oor:name', name)

    v = doc.createElement('value')
    text = doc.createTextNode(value)
    v.appendChild(text)
    if name == 'Title':
        v.setAttribute('xml:lang', 'fr')
    prop.appendChild(v)
    return prop


class MenuEntry:
    def __init__(self, doc, command, title, index, context=''):
        self.index_el = get_node(doc, AT_REPLACE, at_name(f"N{index:03}"))
        self.index_el.appendChild(get_prop(doc, 'Context', context))
        self.index_el.appendChild(get_prop(doc, 'Title', title))
        self.index_el.appendChild(get_prop(doc, 'URL', get_command_line(command)))
        self.index_el.appendChild(get_prop(doc, 'Target', '_self'))
        self.root = self.index_el


class InnerMenuEntry(MenuEntry):
    def __init__(self, doc, command, title, index):
        super().__init__(doc, command, title, index)
        new_root = doc.createElement('node')
        new_root.setAttribute('oor:name', 'Submenu')
        new_root.appendChild(self.index_el)
        self.root = new_root


class ImageEntry:
    def __init__(self, doc, command, icon, index):
        root_node = get_node(doc, at_name(LIB + f".N{index:03}"), AT_REPLACE)
        root_node.appendChild(get_prop(doc, 'URL', get_command_line(command)))
        node = get_node(doc, at_name('UserDefinedImages'))
        root_node.appendChild(node)
        node.appendChild(get_prop(doc, 'ImageSmallURL', IMAGE_LOCATION + icon))
        self.root = root_node
