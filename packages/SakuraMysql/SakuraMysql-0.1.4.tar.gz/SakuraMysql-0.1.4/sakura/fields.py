class Field(object):
    def __init__(self, column_type, convert, *, primary_key=False):
        self.column_type = column_type
        self.convert = convert
        self.primary_key = primary_key

    @classmethod
    def default_value(cls):
        raise NotImplementedError


class BaseStringField(Field):
    @classmethod
    def default_value(cls):
        return ''


class VarcharField(BaseStringField):
    def __init__(self, length, *args, **kwargs):
        super().__init__(f'varchar({length})', str, *args, **kwargs)


class BaseIntField(Field):
    @classmethod
    def default_value(cls):
        return 0


class IntField(BaseIntField):
    def __init__(self, length, *args, **kwargs):
        super().__init__(f'int({length})', int, *args, **kwargs)


class BigIntField(BaseIntField):
    def __init__(self, length, *args, **kwargs):
        super().__init__(f'bigint({length})', int, *args, **kwargs)


class TinyIntField(BaseIntField):
    def __init__(self, length, *args, **kwargs):
        super().__init__(f'tinyint({length})', int, *args, **kwargs)


class BaseFloatField(Field):
    @classmethod
    def default_value(cls):
        return .0


class FloatField(BaseFloatField):
    def __init__(self, length, *args, **kwargs):
        super().__init__(f'float({length})', float, *args, **kwargs)


class DoubleField(BaseFloatField):
    def __init__(self, length, *args, **kwargs):
        super().__init__(f'double({length})', float, *args, **kwargs)
