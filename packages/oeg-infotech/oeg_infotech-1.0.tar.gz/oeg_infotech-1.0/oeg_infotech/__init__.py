# coding: utf-8
"""
Infotech staff
"""
import csv
try:
    from StringIO import StringIO
    from StringIO import StringIO as BytesIO
except ImportError:
    from io import StringIO, BytesIO

from .ordered_attrib import ET


def to_coord(val, delit, decim):
    """
    int to coord string
    """
    mask = "%0." + str(decim) + "f"
    return mask % round(val / delit, decim)


def orient_to_str(val):
    """
    horizontal weld orientation (minutes, int) to string (hours, float)
    """
    if val >= 0:
        hours = int(val / 60)
        hours_float = int(round((val - hours * 60) / 6.0, 0))
        return "{}.{}".format(hours, hours_float)

    return ''


def int_to_string(val):
    """
    convert integer to string
    """
    if val:
        return str(val)

    return ''


def datetime_to_string(val):
    """
    convert datetime to string
    """
    return val.strftime("%d.%m.%Y %H:%M:%S")


def to_int(text):
    """
    text to int
    """
    try:
        return int(text)
    except ValueError:
        return ''


def reverse_orient(orient):
    """
    reverse orientation
    """
    if not orient:
        return orient

    hours = 12.0 - float(orient.replace(',', '.'))
    if hours == 12.0:
        hours = 0.0

    return "{0:0.1f}".format(hours).replace('.', ',')


def numerate(items, from_index):
    """
    enumerate items from given from_index
    """
    for item in items:
        item.number = "{}".format(from_index)
        from_index += 1


def indent(elem, level=0, ident_item="    "):
    """
    http://effbot.org/zone/element-lib.htm#prettyprint
    in-place prettyprint formatter
    """
    i = "\n" + level*ident_item
    if len(elem):  # pylint: disable=len-as-condition
        if not elem.text or not elem.text.strip():
            elem.text = i + ident_item
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:  # pylint: disable=redefined-argument-from-local
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


class AbstractItem(object):  # pylint: disable=too-few-public-methods
    """
    abstract class for xml item
    """
    def is_valid(self):
        """
        check for valid field values
        """
        return bool(self)


class DistItem(AbstractItem):
    """
    abstract class for item on dist
    """
    field_typeobj = 'IDTYPEOBJ'
    field_odometer = 'ODOMETER'
    field_comment = 'REM'
    # not required fields
    field_coord_longitude = 'L'
    field_coord_latitude = 'B'
    field_coord_height = 'H'
    field_coord_system = 'SRID'

    dist_attribs = [
      field_typeobj,
      field_odometer,
    ]

    coords_attribs = [
      field_coord_longitude,
      field_coord_latitude,
      field_coord_height,
      field_coord_system,
    ]

    def __init__(self):
        self.objtype = None
        self.dist = None
        self.comment = ''

        self.coord_longitude = None
        self.coord_latitude = None
        self.coord_height = None
        self.coord_system = None

    def fill_from_xml(self, xml_item):
        """
        fill item data from existing xml element
        """
        self.objtype = xml_item.attrib[DistItem.field_typeobj]
        self.dist = to_int(xml_item.attrib[DistItem.field_odometer])
        self.comment = xml_item.attrib[DistItem.field_comment]

        self.coord_longitude = xml_item.attrib.get(DistItem.field_coord_longitude, None)
        self.coord_latitude = xml_item.attrib.get(DistItem.field_coord_latitude, None)
        self.coord_height = xml_item.attrib.get(DistItem.field_coord_height, None)
        self.coord_system = xml_item.attrib.get(DistItem.field_coord_system, None)

    def as_csv_row(self, infotech, with_navigation=False):
        """
        return list of item fields for csv output
        """
        suffix = []
        if with_navigation:
            suffix = [
              self.coord_longitude,
              self.coord_latitude,
              self.coord_height,
              self.coord_system,
            ]

        return [
          infotech.obj_dict[self.objtype],
          "{}".format(self.dist),
          self.comment,
        ] + suffix

    def reverse(self, total_length, _object_index):
        """
        reverse object distance
        """
        self.dist = total_length - self.dist

    def base_xml(self, node):
        """
        set base attributes to xml node of object
        """
        node.set(DistItem.field_typeobj, self.objtype)
        node.set(DistItem.field_odometer, "{}".format(self.dist))
        node.set(DistItem.field_comment, self.comment)

        if self.coord_system is not None:
            node.set(DistItem.field_coord_longitude, self.coord_longitude)
            node.set(DistItem.field_coord_latitude, self.coord_latitude)
            node.set(DistItem.field_coord_height, self.coord_height)
            node.set(DistItem.field_coord_system, self.coord_system)


class Section(object):
    """
    abstract class for xml section
    """
    item_attributes = None

    def __init__(self, infotech, cls, section):
        self.infotech = infotech
        self.cls = cls
        self.section = section
        self._items = None

    @property
    def items(self):
        """
        lazy restore list of section's items
        """
        if self._items is None:
            self._items = []
            for obj in self.infotech.xml.getroot().find(self.section):
                item = self.cls.from_xml(obj)
                if item.is_valid():
                    self._items.append(item)

        return self._items

    def as_csv_body(self, title, column_titles, with_navigation=False):
        """
        dump section as csv string
        """
        output = StringIO()
        writer = csv.writer(output, delimiter=';', lineterminator='\n')

        writer.writerow([title] + ['' for _tmp in column_titles][1:])
        writer.writerow(column_titles)
        for item in self.items:
            writer.writerow([
              field.encode(self.infotech.codepage)
              for field in item.as_csv_row(self.infotech, with_navigation=with_navigation)
            ])

        content = output.getvalue()
        output.close()

        return content

    def rebuild_xml(self):
        """
        generate new xml data based on current section data
        """
        section = self.infotech.xml.getroot().find(self.section)
        section.clear()

        for item in self.items:
            node = item.add_xml_child(section)
            if self.item_attributes:
                node.ordered_attributes = self.item_attributes

    def reverse(self, total_length):
        """
        reverse vector of objects and modify self.infotech.xml
        """
        self._items = reversed(self.items)
        section = self.infotech.xml.getroot().find(self.section)
        section.clear()
        object_index = 1

        for item in self.items:
            item.reverse(total_length, object_index)
            item.add_xml_child(section)
            object_index += 1

        indent(section, level=1)

    def add_from_xml(self, xml_section, at_dist, dist_shift):
        """
        add objects from another infotech section from given dist
        """
        items = self.items
        for item in xml_section.items:
            item.dist = item.dist - dist_shift + at_dist
            items.append(item)


def dump_xml(xmltree):
    """
    Debug dump
    """
    root = xmltree.getroot()
    print("#", root.tag)
    print("#", root.attrib)

    for child in root:
        print(child.tag, child.attrib)
        for item in child:
            print("#", item.tag, item.attrib)


class Infotech(object):
    """
    Infotech xml export
    """
    typobj_section = 'TYPEOBJS'
    typobj_item = 'TYPEOBJ'
    typobj_id = 'IDTYPEOBJ'
    typobj_title = 'TITLE'

    gps_sys_code = '0'
    gps_sys_name = 'WGS-84'

    template = """<?xml version="1.0" encoding="windows-1251"?>
<IPL_INSPECT>
<TYPEOBJS></TYPEOBJS>
<DEFECTS></DEFECTS>
<LINEOBJS></LINEOBJS>
<WELDS></WELDS>
<PIGPASS></PIGPASS>
</IPL_INSPECT>
"""

    def __init__(self, codepage="windows-1251"):
        self.xml = ET.parse(StringIO(self.template))
        self.obj_dict = {}
        self.codepage = codepage
        self.is_navigate = None

        from . import defect, weld, lineobj, pigpass
        self.welds = weld.Section(self)
        self.defects = defect.Section(self)
        self.lineobjects = lineobj.Section(self)
        self.pigpass = pigpass.Section(self)

    def __unicode__(self):
        # dump_xml(self.xml)
        output = BytesIO()
        self.xml.write(output, encoding=self.codepage)

        return output.getvalue()

    def __str__(self):
        return self.__unicode__()

    @classmethod
    def from_file(cls, file_name):
        """
        load data from xml file
        """
        obj = cls()
        obj.xml = ET.parse(file_name)
        sect = obj.xml.getroot().find(obj.typobj_section)
        obj.obj_dict = {typ.attrib[obj.typobj_id]: typ.find(obj.typobj_title).text for typ in sect}

        return obj

    def rebuild_typeobjs(self):
        """
        generate new content for TYPEOBJS section of xml, based on obj_dict data
        """
        section = self.xml.getroot().find(self.typobj_section)
        section.clear()

        if self.is_navigate:
            node = ET.SubElement(section, self.typobj_item)
            node.set(self.typobj_id, self.gps_sys_code)
            title = ET.SubElement(node, self.typobj_title)
            title.text = self.gps_sys_name

        for key, val in self.obj_dict.items():
            node = ET.SubElement(section, self.typobj_item)
            node.set(self.typobj_id, key)
            title = ET.SubElement(node, self.typobj_title)
            title.text = val

    def total_dist(self):
        """
        return length of inspection
        """
        return self.welds.items[-1].end()

    def start_dist(self):
        """
        return start distance of inspection
        """
        return self.welds.items[0].dist

    def reverse(self):
        """
        reverse vector of objects and return string dump of updated xml
        """
        total_length = self.total_dist()
        self.lineobjects.reverse(total_length)
        self.welds.reverse(total_length)
        self.defects.reverse(total_length)

        return "{}".format(self)

    def fix(self):
        """
        repair umdp-1400 data in PIGPASS section
        """
        umdp = u'УМДП-1400'  # encode(self.codepage)
        umdp_key = None

        for key, val in self.obj_dict.items():
            if val == umdp:
                umdp_key = key
                break

        if not umdp_key:
            return "{}".format(self)

        for pig in self.xml.getroot().find('PIGPASS'):
            if pig.attrib.get('IDTYPEOBJ', None) == umdp_key:
                pig.set('MANUFACT_DATE', '2017')
                pig.set('PIGTYPE', '990004033563')
                pig.set('OBSLTYPE', '2')

        return "{}".format(self)

    def join(self, file_list):
        """
        join several xml files and connect tubes
        """
        from .codes import Tube, NAME
        is_updated = False

        for item in file_list:
            current_length = self.total_dist()
            try:
                self.welds.add_tube(Tube.UNKNOWN, current_length, int(item))
                if Tube.UNKNOWN not in self.obj_dict:
                    self.obj_dict[Tube.UNKNOWN] = NAME[Tube.UNKNOWN]

                is_updated = True

            except ValueError:

                try:
                    info = Infotech.from_file(item)
                except IOError as exc:
                    return str(exc)

                for key in info.obj_dict:
                    if len(key) > 2:
                        if key not in self.obj_dict:
                            self.obj_dict[key] = info.obj_dict[key]

                start = info.start_dist()

                self.welds.add_from_xml(info.welds, current_length, start)
                self.defects.add_from_xml(info.defects, current_length, start)
                self.lineobjects.add_from_xml(info.lineobjects, current_length, start)

                is_updated = True

        if is_updated:
            numerate(self.welds.items, 1)
            numerate(self.defects.items, 1)

            self.rebuild_typeobjs()
            self.welds.rebuild_xml()
            self.defects.rebuild_xml()
            self.lineobjects.rebuild_xml()

        indent(self.xml.getroot(), level=0)

        return "{}".format(self)
