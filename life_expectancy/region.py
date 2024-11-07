"""enum of countries"""

from enum import Enum


class Region(Enum):
    """List of countries and regions in EU dataset and applicable codes.
    Note that these codes do not strictly conform to ISO2 standards,
    with notable examples Greece and United Kingdom."""

    AUSTRIA = "AT"
    BELGIUM = "BE"
    BULGARIA = "BG"
    SWITZERLAND = "CH"
    CYPRUS = "CY"
    CZECHIA = "CZ"
    DENMARK = "DK"
    ESTONIA = "EE"
    GREECE = "EL"
    SPAIN = "ES"
    EU27_2020 = "EU27_2020"
    FINLAND = "FI"
    FRANCE = "FR"
    CROATIA = "HR"
    HUNGARY = "HU"
    ICELAND = "IS"
    ITALY = "IT"
    LIECHTENSTEIN = "LI"
    LITHUANIA = "LT"
    LUXEMBOURG = "LU"
    LATVIA = "LV"
    MALTA = "MT"
    NETHERLANDS = "NL"
    NORWAY = "NO"
    POLAND = "PL"
    PORTUGAL = "PT"
    ROMANIA = "RO"
    SWEDEN = "SE"
    SLOVENIA = "SI"
    SLOVAKIA = "SK"
    GERMANY = "DE"
    DE_TOT = "DE_TOT"
    ALBANIA = "AL"
    EA18 = "EA18"
    EA19 = "EA19"
    EFTA = "EFTA"
    IRELAND = "IE"
    MONTENEGRO = "ME"
    NORTH_MACEDONIA = "MK"
    SERBIA = "RS"
    ARMENIA = "AM"
    AZERBAIJAN = "AZ"
    GEORGIA = "GE"
    TURKEY = "TR"
    UKRAINE = "UA"
    BELARUS = "BY"
    EEA30_2007 = "EEA30_2007"
    EEA31 = "EEA31"
    EU27_2007 = "EU27_2007"
    EU28 = "EU28"
    UNITED_KINGDOM = "UK"
    KOSOVO = "XK"
    METROPOLITAN_FRANCE = "FX"
    MOLDOVA = "MD"
    SAN_MARINO = "SM"
    RUSSIAN_FEDERATION = "RU"

    @classmethod
    def region_list(cls):
        """generate a list of actual countries for the EU dataset"""
        return [
            r.name
            for r in cls
            if r.value
            not in [
                "EU27_2020",
                "DE_TOT",
                "EA18",
                "EA19",
                "EFTA",
                "EEA30_2007",
                "EEA31",
                "EU27_2007",
                "EU28",
            ]
        ]

    def __str__(self):
        return self.value
