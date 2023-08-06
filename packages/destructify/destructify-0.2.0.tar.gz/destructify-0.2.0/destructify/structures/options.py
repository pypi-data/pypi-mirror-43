from bisect import bisect


class StructureOptions:
    def __init__(self, meta=None):
        self.meta = meta

        self.structure = None
        self.fields = []
        self.structure_name = None

        self.byte_order = None
        self.encoding = 'utf-8'
        self.alignment = None
        self.checks = ()
        self.capture_raw = False

    def contribute_to_class(self, cls, name):
        setattr(cls, '_meta', self)

        self.structure = cls
        self.structure_name = cls.__name__

        if self.meta:
            meta_attrs = self.meta.__dict__.copy()
            for name in self.meta.__dict__:
                # Ignore any private attributes we don't care about.
                if name.startswith('_'):
                    del meta_attrs[name]
            for attr_name in ('structure_name', 'byte_order', 'encoding',
                              'alignment', 'checks', 'capture_raw'):
                if attr_name in meta_attrs:
                    setattr(self, attr_name, meta_attrs.pop(attr_name))
                elif hasattr(self.meta, attr_name):
                    setattr(self, attr_name, getattr(self.meta, attr_name))

            # Any leftover attributes must be invalid.
            if meta_attrs != {}:
                raise TypeError("'class Meta' got invalid attribute(s): %s" % ','.join(meta_attrs))
        del self.meta

    def add_field(self, field):
        self.fields.insert(bisect(self.fields, field), field)

    def get_previous_field(self, field):
        """Returns the field before the field provided by *field*. Returns :const:`None` if the field is the first
        field. Raises :exc:`ValueError` if the field is not found.
        """
        i = self.fields.index(field)
        if i <= 0:
            return None
        return self.fields[i - 1]

    def get_next_field(self, field):
        """Returns the field following the field provided by *field*. Returns :const:`None` if the field is the last
        field. Raises :exc:`ValueError` if the field is not found.
        """
        try:
            return self.fields[self.fields.index(field) + 1]
        except IndexError:
            return None

    def get_field_by_name(self, name):
        for field in self.fields:
            if field.name == name:
                return field
        raise KeyError("Field not found")

    def initialize_fields(self):
        for field in self.fields:
            field.initialize()
