import struct

from destructify.exceptions import DefinitionError
from . import FixedLengthField


BYTE_ORDER_MAPPING = {
    # native
    '@': '@',
    'native': '@',

    # standard
    '=': '=',
    'std': '=',
    'standard': '=',

    # little-endian
    '<': '<',
    'le': '<',
    'little': '<',
    'little-endian': '<',

    # big-endian
    '>': '>',
    'be': '>',
    'big': '>',
    'big-endian': '>',

    # network-order
    '!': '>',
    'network': '>',
}


class StructField(FixedLengthField):
    format = None
    byte_order = ""

    def __init__(self, format=None, byte_order=None, *args, multibyte=True, **kwargs):
        if format is not None:
            self.format = format
        if byte_order is not None:
            self.byte_order = BYTE_ORDER_MAPPING[byte_order]

        self.multibyte = multibyte

        if self.format[0] in "@=<>!":
            if not self.byte_order:
                self.byte_order = BYTE_ORDER_MAPPING[self.format[0]]
            self.format = self.format[1:]

        self._struct = struct.Struct(self.byte_order + self.format)
        super().__init__(length=self._struct.size, *args, **kwargs)

    def initialize(self):
        super().initialize()

        # If byte_order is specified in the meta of the structure, we change our own default byte order (if not set)
        if self.bound_structure._meta.byte_order and not self.byte_order:
            try:
                self.byte_order = BYTE_ORDER_MAPPING[self.bound_structure._meta.byte_order]
            except KeyError:
                raise DefinitionError("byte_order %s is invalid" % self.bound_structure._meta.byte_order)
            else:
                self._struct = struct.Struct(self.byte_order + self.format)
                self.length = self._struct.size

    def from_stream(self, stream, context):
        result, length = super().from_stream(stream, context)
        if self.multibyte:
            return self._struct.unpack(result), length
        return self._struct.unpack(result)[0], length

    def to_stream(self, stream, value, context):
        if value is None:
            value = 0
        if self.multibyte:
            return super().to_stream(stream, self._struct.pack(*value), context)
        return super().to_stream(stream, self._struct.pack(value), context)


class SingleByteStructField(StructField):
    def __init__(self, *args, **kwargs):
        kwargs.update({"multibyte": False})
        super().__init__(*args, **kwargs)


def _factory(name, bases=(SingleByteStructField, ), **kwargs):
    return type(name, bases, kwargs)


CharField = _factory("CharField", format="c", _ctype="char")
ByteField = _factory("ByteField", format="b", _ctype="signed char")
UnsignedByteField = _factory("UnignedByteField", format="B", _ctype="unsigned char")
BoolField = _factory("BoolField", format="?", _ctype="_Bool")
ShortField = _factory("ShortField", format="h", _ctype="short")
UnsignedShortField = _factory("UnsignedShortField", format="H", _ctype="unsigned short")
IntField = _factory("IntField", format="i", _ctype="int")
UnsignedIntField = _factory("UnsignedIntField", format="I", _ctype="unsigned int")
LongField = _factory("LongField", format="l", _ctype="long")
UnsignedLongField = _factory("UnsignedLongField", format="L", _ctype="unsigned long")
LongLongField = _factory("LongField", format="q", _ctype="long long")
UnsignedLongLongField = _factory("UnsignedLongField", format="Q", _ctype="unsigned long long")
SizeField = _factory("SizeField", format="n", _ctype="ssize_t")
UnsignedSizeField = _factory("UnsignedSizeField", format="N", _ctype="size_t")
HalfPrecisionFloatField = _factory("HalfPrecisionFloatField", format="e", _ctype="binary16")
FloatField = _factory("FloatField", format="f", _ctype="float")
DoubleField = _factory("DoubleField", format="d", _ctype="double")
