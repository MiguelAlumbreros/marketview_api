import urllib
import urllib.parse
from .ParsingFunctions import _parse_num, _parse_int, _parse_float, _parse_datetime
import datetime

TimeseriesParamMapping = {
    "pricesymbol": str,
    "tradedatetimeutc": _parse_datetime,
    "open": _parse_float,
    "high": _parse_float,
    "low": _parse_float,
    "close": _parse_float,
    "volume": _parse_int,
    "midpoint": _parse_float,
    "openinterest": _parse_int
}

QuoteParamMapping = {
    "pricesymbol": str,
    "tradedatetimeutc": _parse_datetime,
    "open": _parse_float,
    "high": _parse_float,
    "low": _parse_float,
    "close": _parse_float,
    "volume": _parse_int,
    "midpoint": _parse_float,
    "openinterest": _parse_int,
    "tradevolume": _parse_int,
    "historicvolume": _parse_int,
    "tickcount": _parse_int,
    "last": _parse_float,
    "netchange": _parse_float,
    "percentchange": _parse_float,
    "closedate": _parse_datetime,
    "mostrecentvalue": _parse_float,
    "mostrecentvaluedate": _parse_datetime,
    "lasttradedirection": _parse_float,
    "prevlast": _parse_float,
    "lastopen": _parse_float,
    "lasthigh": _parse_float,
    "lastlow": _parse_float,
    "lastclose": _parse_float,
    "lastvolume": _parse_int,
    "bid": _parse_float,
    "ask": _parse_float,
    "bidsize": _parse_int,
    "asksize": _parse_int,
    "biddatetimeutc": _parse_datetime,
    "askdatetimeutc": _parse_datetime,
    "settledate": _parse_datetime,
    "displaycontractexpdate": _parse_datetime,
    "expirationdate": _parse_datetime,
    "strike": _parse_float,
    "tradestarttimeutc": _parse_datetime,
    "tradestoptimeutc": _parse_datetime,
    "sessionstarttimeutc": _parse_datetime,
    "sessionstoptimeutc": _parse_datetime,
    "blocktradedatetimeutc": _parse_datetime,
    "settleupdatetime": _parse_datetime,
    "prevsettleupdatetime": _parse_datetime,
    "symboldescription": str,
    "currency": str,
    "putcallunderlier": str,
    "optionroot": str,
    "market": str,
    "lotunit": str,
    "exchangecode": str,
}

class TsEnum:
    days = 1
    weeks = 2
    months = 3
    contract_months = 4
    quarters = 5
    years = 6
    intraday = 7

    ALL = [days, weeks, months, contract_months, quarters, years, intraday]

class QuoteFields:
    symbol = 'pricesymbol'
    description = 'symboldescription'

    trade_date = 'tradedatetimeutc'
    open = 'open'
    high = 'high'
    low = 'low'
    close = 'close'  # settle
    last = 'last'
    mid_point = 'midpoint'
    volume = 'volume'
    trade_volume = 'tradevolume'
    historic_volume = 'historicvolume'
    tick_count = 'tickcount'

    net_change = 'netchange'
    percent_change = 'percentchange'
    open_interest = 'openinterest'

    close_date = 'closedate'
    currency = 'currency'
    most_recent_value = 'mostrecentvalue'
    most_recent_value_date = 'mostrecentvaluedate'
    last_trade_direction = 'lasttradedirection'

    previous_last = 'prevlast'
    previous_open = 'lastopen'
    previous_high = 'lasthigh'
    previous_low = 'lastlow'
    previous_close = 'lastclose'
    previous_volume = 'lastvolume'

    put_call_underlier = 'putcallunderlier'

    bid = 'bid'
    ask = 'ask'
    bid_size = 'bidsize'
    ask_size = 'asksize'
    bid_time = 'biddatetimeutc'
    ask_time = 'askdatetimeutc'

    option_root = 'optionroot'
    settle_date = 'settledate'
    contract_expiration_date = 'displaycontractexpdate'
    market = 'market'
    expiration_date = 'expirationdate'
    lot_unit = 'lotunit'
    strike = 'strike'

    trade_start_time = 'tradestarttimeutc'
    trade_stop_time = 'tradestoptimeutc'
    session_start_time = 'sessionstarttimeutc'
    session_stop_time = 'sessionstoptimeutc'
    block_trade_time = 'blocktradedatetimeutc'

    settle_update = 'settleupdatetime'
    prev_settle_update = 'prevsettleupdatetime'

    exchange_code = 'exchangecode'

    ALL = [symbol, description, trade_date, open, high, low, close, last, mid_point, volume, trade_volume,
           historic_volume, tick_count, net_change, percent_change, open_interest, close_date, currency,
           most_recent_value, most_recent_value_date, last_trade_direction, previous_last, previous_open, previous_high,
           previous_low, previous_close, previous_volume, put_call_underlier, bid, ask, bid_size, ask_size, bid_time,
           ask_time, option_root, settle_date, contract_expiration_date, market, expiration_date, lot_unit, strike,
           trade_start_time, trade_stop_time, session_start_time, session_stop_time, block_trade_time, settle_update, prev_settle_update,exchange_code]

    STANDARD = [symbol, trade_date, open, high, low, last, volume, open_interest]

    STANDARDWITHSETTLEDATE = [symbol, trade_date, open, high, low, last, volume, open_interest, settle_date]


class TimeSeriesFields:
    symbol = "pricesymbol"
    trade_date = "tradedatetimeutc"
    open = "open"
    high = "high"
    low = "low"
    close = "close"
    volume = "volume"
    mid_point = "midpoint"
    open_interest = "openinterest"

    ALL = [symbol, trade_date, open, high, low, close, volume, mid_point, open_interest]
    INTRADAY = [symbol, trade_date, open, high, low, close, volume]

class FillMethod:
    FillForward = 0
    FillBackward = 1
    Average = 2
    Interpolate = 3
    NoFill = 4


class FillFrequency:
    Business = 0
    SixDays = 1
    SevenDays = 2


class AggregateType:
    Daily = 0
    Peak = 1
    OffPeak = 2


class ForwardCurveValueType:
    Price = 0
    Spread = 1
    SpreadPercent = 2
    Relative = 3
    RelativePercent = 4
    SpreadWave = 5
    SpreadPercentWave = 6
    Spread100PecentWave = 7
    SpreadAvg = 8

class ForwardCurveFields:
    symbol = "symbol"
    description = "description"
    curveroot = "curveroot"
    curvedate = "curvedate"
    displaydate = "displaydate"
    ALL = [symbol, description, curveroot, curvedate, displaydate]

DailyCurveParamMapping = {
    "symbol": str,
    "description": str,
    "curveroot": str,
    "curvedate": _parse_datetime,
    "displaydate": _parse_datetime
}

class LeadLagType:
    CalendarDays = 0,
    QuotedDays = 1,
    Weeks = 2

class Units:
    BBL = "BBL"  # Barrels
    LTR = "LTR"  # Liters
    KLTR = "KLTR"  # Kiloliters
    CM = "CM"  # Cubic Meters
    GAL = "GAL"  # Gallons
    MSCF = "MSCF"  # Thou/Std Cubic Ft.
    MT = "MT"  # Metric Tons
    ST = "ST"  # Short Tons
    MMB = "MMB"  # MMBTUs
    THM = "THM"  # Therms
    GJ = "GJ"  # Gigajoules
    GWH = "GWH"  # Gigawatt Hours
    KWH = "KWH"  # Kilowatt Hours
    MWH = "MWH"  # Megawatt Hours

class UnitConversion:
    def __init__(self, unit, factor=None):
        """
        Unit conversion for the symbol
        :param unit: See Units class for available units
        :param factor: Conversion factor (optional)
        """
        self.unit = unit
        self.factor = factor


class Currencies:
    USD = "USD"  # U.S. Dollar
    USC = "USC"  # U.S. Cents
    GBP = "GBP"  # British Pound
    GBC = "GBC"  # British Pence
    EUR = "EUR"  # Euro
    EUC = "EUC"  # Euro Cents
    JPY = "JPY"  # Janapese Yen
    CNV = "CNV"  # Chinese Yuan
    CHF = "CHF"  # Swiss Franc
    SGD = "SGD"  # Singapore Dollar
    CAD = "CAD"  # Canadian Dollar
    CAC = "CAC"  # Canadian Cents
    AUD = "AUD"  # Australian Dollar
    NZD = "NZD"  # New Zealand Dollar
    MYR = "MYR"  # Malaysian Ringgit
    HKD = "HKD"  # Hong Kong Dollar
    KRW = "KRW"  # South Korean Won
    THB = "THB"  # Thai Baht
    DKK = "DKK"  # Danish Krone
    NOK = "NOK"  # Norwegian Kroner
    SEK = "SEK"  # Swedish Krona
    TWD = "TWD"  # Taiwan Dollar
    ZAR = "ZAR"  # South African Rand
    BRL = "BRL"  # Brazilian Real
    MXN = "MXN"  # Mexican Peso
    BHD = "BHD"  # Bahrain Dinar
    SAR = "SAR"  # Saudi Arabian Riyal
    RUB = "RUB"  # Russian Ruble
    ARS = "ARS"  # Argentine Peso


class CurrencySources:
    BCB = "BCB"  # Bank of Brasil
    BNM = "BNM"  # Bank of Malaysia
    BNZ = "BNZ"  # Bank of New Zealand
    BOC = "BOC"  # Bank of Canada
    BOE = "BOE"  # Bank of England
    BOI = "BOI"  # Bank of Indonesia
    BOJ = "BOJ"  # Bank of Tokyo
    BOM = "BOM"  # Bank of Mexico
    BOT = "BOT"  # Bank of Thailand
    DNB = "DNB"  # Danish National Bank
    ECB = "ECB"  # European Central Bank
    FXZ = "FXZ"  # Bank of China
    IMF = "IMF"  # Int. Monetary Fund
    RBA = "RBA"  # Reserve Bank of Australia
    USF = "USF"  # US Fed. Reserve


class ConvertedSymbol:
    """
    Represents symbol if currency/unit conversion is needed.
    """

    def __init__(self, symbol, currency=None, currency_source=None, unit=None, unit_factor=None):
        """
        Represent symbol which prices should be converted
        :param symbol: Symbol name (string)
        :param currency: Currency name (string) - see Currencies class for a list of available currencies 
        :param currency_source: Exchange name (string) - see CurrencySources class for a list of sources 
        :param unit: unit name (string) - see Units class
        :param unit_factor: unit conversion factor (float, optional) 
        """
        if symbol is None:
            raise ValueError("Symbol can't be undefined")

        symbol = urllib.parse.quote_plus(symbol)

        if len(currency or "") == 0: 
            currency = None
            
        if len(currency_source or "") == 0: 
            currency_source = None
            
        if len(unit or "") == 0: 
            unit = None
            
        if unit_factor is not None and unit_factor == 0:
            unit_factor = None

        def format_part(first, second):
            if first is not None:
                ret_val = "@{}".format(first)
                if second is not None:
                    ret_val = ret_val + ":" + str(second)

                return ret_val
            else:
                return None

        def format_formula(first, second):
            if first is None and second is None:
                return None

            if first is None:
                return second

            if second is None:
                return first

            return first + ',' + second

        currency_part = format_part(currency, currency_source)
        unit_part = format_part(unit, unit_factor)
        formula_part = format_formula(currency_part, unit_part)

        if formula_part is None:
            self.formula = symbol
            self.is_formula = False
        else:
            self.formula = '=""{}"";[{}]'.format(symbol, formula_part)
            self.is_formula = True

    def __str__(self):
        return self.formula
    
class ValueTenor:
    def __init__(self, tenor = None, relative = None, value = None):
        self.tenor = tenor
        self.relative = relative
        self.value = value

class RequestBody:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def to_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, list):
                if all(isinstance(item, RequestBody) for item in value):
                    result[key] = [item.to_dict() for item in value]
                else:
                    result[key] = value
            elif isinstance(value, RequestBody):
                result[key] = value.to_dict()
            elif isinstance(value, datetime.date):
                result[key] = value.strftime('%Y-%m-%d')
            else:
                result[key] = value
        return result
        
    def to_csv_data(self):
        if not hasattr(self, 'fields'):
            raise ValueError("RequestBody for CSV data must contain 'fields' attribute to define column order")
        
        fields = self.fields
        row_count = None
        field_arrays = {}
        
        for field in fields:
            if not hasattr(self, field):
                raise ValueError(f"Missing array for field: {field}")
            
            field_value = getattr(self, field)
            if not isinstance(field_value, list):
                raise ValueError(f"Field {field} must be an array")
                
            field_arrays[field] = field_value
            
            if row_count is None:
                row_count = len(field_value)
            elif len(field_value) != row_count:
                raise ValueError(f"All field arrays must have the same length. Expected {row_count}, but {field} has {len(field_value)}")
        
        rows = []
        for i in range(row_count):
            row = [field_arrays[field][i] for field in fields]
            rows.append(row)
        
        return fields, rows