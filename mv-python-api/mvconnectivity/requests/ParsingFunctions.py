import datetime
import dateutil.parser

def _parse_num(val, fn):
    try:
        ret = fn(val)
        return ret
    except:
        return None

def _parse_int(val):
    val = _parse_num(val, float)
    return _parse_num(val, int)

def _parse_float(val):
    return _parse_num(val, float)

def _parse_datetime(dt_str):
    try:
        ret = datetime.datetime.strptime(dt_str, "%m/%d/%Y %I:%M:%S %p")
        return ret
    except:
        try:
            ret = datetime.datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S")
            return ret
        except:
            try:
                ret = dateutil.parser.parse(dt_str)
                return ret
            except:
                return None

class FieldTypes:
    INT = _parse_int
    FLOAT = _parse_float
    STRING = str
    DATETIME = _parse_datetime

