from collections import namedtuple
import string
from dataclasses import dataclass
from itertools import chain
import logging


# ---------------------utils---------------------


def function_doc_header(function):
    """Returns first line of the function's docstring"""

    try:
        return function.__doc__.split('\n')[0]
    except (AttributeError):
        return None


def is_public_name(attribute_name):
    """Recognize names of public attributes

    "some_attribute" : True : public
    "_internal" : False: user internal
    "__dict__" : False: system internal
    """

    return not (attribute_name.startswith('_'))


def order_attributes(attributes):
    simple_attributes = [attr for attr in attributes if not (attr.is_callable)]
    private_attributes = [attr for attr in simple_attributes if not (attr.is_public)]
    public_attributes = [attr for attr in simple_attributes if attr.is_public]

    methods = [attr for attr in attributes if attr.is_callable]
    private_methods = [attr for attr in methods if not (attr.is_public)]
    public_methods = [attr for attr in methods if attr.is_public]

    return private_attributes + public_attributes + private_methods + public_methods


# ---------------------main classes--------------------------


@dataclass
class ObjectMeta:
    def __init__(self, o):
        self.type = str(type(o))
        self.attributes = [AttributeMeta(o, name) for name in dir(o)]

    def format_head_line(self):
        return self.type

    def format(self):
        lines = []
        lines.append(self.format_head_line())
        lines.append('')
        for attribute in order_attributes(self.attributes):
            lines.append(attribute.format())
        return '\n'.join(lines)


from dev_tools import *


@dataclass
class AttributeMeta:
    """Attribute metadata"""

    name: str
    is_public: bool
    is_callable: bool = None

    def __init__(self, object_, attribute_name):
        logging.debug('parsing %s', attribute_name)
        self.name = attribute_name
        self.is_public = is_public_name(attribute_name)
        try:
            value = getattr(object_, attribute_name)
            self.error = False
        except Exception:
            logging.debug('failed to access value of %s', attribute_name)
            self.error = True
            return

        self.is_callable = callable(value)
        if self.is_callable:
            self.value_str = function_doc_header(value)
        else:
            self.value_str = str(value)

    def format_name(self):
        """Printable attribute name

        methods are postfixed with "()"
        attributes are left as is
        """

        return f'{self.name}{"()" if self.is_callable else ""}'

    def format_value(self):
        return self.value_str

    def format(self):
        """Format the whole attribute in one line
        """

        return f'{self.format_name()}: {self.format_value()}'


# ---------------------Main Methods--------------------------


def format(object_):
    return ObjectMeta(object_).format()


def lookat(object_):
    print(format(object_))
