from .Structures import ConvertedSymbol
import urllib
import urllib.parse

def filter_list_into_parameter(self, input_list):
    return ",".join(input_list)

def parse_symbols(self, symbols):
    if isinstance(symbols, str) or isinstance(symbols, ConvertedSymbol):
        symbols_list = [symbols]
    else:
        symbols_list = symbols

    escaped_symbols = []
    for symbol in symbols_list:
        if isinstance(symbol, str):
            escaped = urllib.parse.quote_plus(symbol)
            escaped_symbols.append(escaped)
        else:
            escaped_symbols.append(symbol)

    escaped_symbols = ['"{}"'.format(str(x)) for x in escaped_symbols]
    symbols = ",".join(escaped_symbols)
    return symbols

def parse_fields(self, fields_list):
    fields = []
    field_mapping = {}

    for item in fields_list:
        if isinstance(item, str):
            fields.append(item.strip('"'))
        elif isinstance(item, list) and len(item) == 2:
            field, field_type = item
            field = field.strip('"')
            fields.append(field)
            if callable(field_type):
                field_mapping[field] = field_type
            else:
                raise ValueError("The second item in the list must be a callable for parsing")
        else:
            raise ValueError("Invalid input format in fields_list")

    arg_fields = ",".join(fields)

    return arg_fields, fields, field_mapping if field_mapping else None