# -*- coding: utf-8 -*-

from .utils import *
import json
import aenum


class Plec(aenum.Enum):
    """Płeć"""

    KOBIETA = 0
    MEZCZYZNA = 1


class RodzajSprawdzianu(aenum.Enum):
    """
    Rodzaj sprawdzianu

    Todo:
        Dodać enum testu
    """

    SPRAWDZIAN = 1
    KARTKOWKA = 2
    PRACA_KLASOWA = 3


class Okres(object):
    """
    Okres kwalifikacyjny

    Attributes:
        id (:class:`int`): ID okresu kwalifikacyjnego
        poziom (:class:`int`): Poziom (klasa) okresu kwalifikacyjnego
        numer (:class:`int`): Liczba kolejna okresu kwalifikacyjnego
        od (:class:`datetime.date`): Data rozpoczęcia okresu kwalifikacyjnego
        do (:class:`datetime.date`): Data zakończenia okresu kwalifikacyjnego
    """

    def __init__(self, id=None, poziom=None, numer=None, od=None, do=None):
        self.id = id
        self.poziom = poziom
        self.numer = numer
        self.od = od
        self.do = do

    def __repr__(self):
        return "<Okres: od={!r} do={!r}>".format(str(self.od), str(self.do))

    @classmethod
    def from_json(cls, j):
        id = j.get("IdOkresKlasyfikacyjny")
        poziom = j.get("OkresPoziom")
        numer = j.get("OkresNumer")
        od = timestamp_to_date(j["OkresDataOd"]) if j.get("OkresDataOd") else None
        do = timestamp_to_date(j["OkresDataDo"]) if j.get("OkresDataDo") else None
        return cls(id=id, poziom=poziom, numer=numer, od=od, do=do)


class Klasa(object):
    """
    Oddział (klasa)

    Attributes:
        id (:class:`int`): ID klasy
        kod (:class:`str`): Kod klasy (np. `"8A"`)
        poziom (:class:`int`): Poziom klasy (np. `8`)
        symbol (:class:`str`): Symbol klasy (np. `"A"`)
    """

    def __init__(self, id=None, kod=None, poziom=None, symbol=None):
        self.id = id
        self.kod = kod
        self.poziom = poziom
        self.symbol = symbol

    def __repr__(self):
        return "<Klasa {!s}>".format(self.kod)

    @classmethod
    def from_json(cls, j):
        id = j.get("IdOddzial")
        kod = j.get("OddzialKod")
        poziom = j.get("OkresPoziom")
        symbol = j.get("OddzialSymbol")
        return cls(id=id, kod=kod, poziom=poziom, symbol=symbol)


class Szkola(object):
    """
    Szkoła

    Attributes:
        id (:class:`int`) ID szkoły
        skrot (:class:`str`) Skrót nazwy szkoły
        nazwa (:class:`str`) Pełna nazwa szkoły
        symbol (:class:`str`) Symbol szkoły
    """

    def __init__(self, id=None, skrot=None, nazwa=None, symbol=None):
        self.id = id
        self.skrot = skrot
        self.nazwa = nazwa
        self.symbol = symbol

    def __repr__(self):
        return "<Szkola {!r}>".format(self.skrot)

    @classmethod
    def from_json(cls, j):
        id = j.get("IdJednostkaSprawozdawcza")
        skrot = j.get("JednostkaSprawozdawczaSkrot")
        nazwa = j.get("JednostkaSprawozdawczaNazwa")
        symbol = j.get("JednostkaSprawozdawczaSymbol")
        return cls(id=id, skrot=skrot, nazwa=nazwa, symbol=symbol)


class Uczen(object):
    """
    Uczeń

    Attributes:
        id (:class:`int`): ID ucznia
        nazwa (:class:`str`): Nazwisko, imię oraz drugie imię ucznia
        imie (:class:`str`): Pierwsze imię ucznia
        drugie_imie (:class:`str` or :class:`None`): Drugie imię ucznia
        nazwisko (:class:`str`): Nazwisko ucznia
        pseudonim (:class:`str` or :class:`None`): Pseudonim ucznia
        plec (:class:`vulcan.models.Plec`): Płeć ucznia
        okres (:class:`vulcan.models.Okres`): Aktualny okres klasyfikacyjny ucznia
        klasa (:class:`vulcan.models.Klasa`): Klasa ucznia
        szkola (:class:`vulcan.models.Szkola`): Szkoła ucznia
    """

    def __init__(
        self,
        id=None,
        login_id=None,
        nazwa=None,
        imie=None,
        drugie_imie=None,
        nazwisko=None,
        pseudonim=None,
        plec=None,
        okres=None,
        klasa=None,
        szkola=None,
    ):
        self.id = id
        self.login_id = login_id
        self.nazwa = nazwa
        self.imie = imie
        self.drugie_imie = drugie_imie
        self.nazwisko = nazwisko
        self.pseudonim = pseudonim
        self.plec = plec
        self.okres = okres
        self.klasa = klasa
        self.szkola = szkola

    def __repr__(self):
        return "<Uczen {!r}>".format(self.nazwa)

    @classmethod
    def from_json(cls, j):
        id = j.get("Id")
        login_id = j.get("UzytkownikLoginId")
        nazwa = j.get("UzytkownikNazwa")
        imie = j.get("Imie")
        drugie_imie = j.get("Imie2") or None
        nazwisko = j.get("Nazwisko")
        pseudonim = j.get("Pseudonim")
        plec = Plec(j.get("UczenPlec"))
        okres = Okres.from_json(j)
        klasa = Klasa.from_json(j)
        szkola = Szkola.from_json(j)
        return cls(
            id=id,
            login_id=login_id,
            nazwa=nazwa,
            imie=imie,
            drugie_imie=drugie_imie,
            nazwisko=nazwisko,
            pseudonim=pseudonim,
            plec=plec,
            okres=okres,
            klasa=klasa,
            szkola=szkola,
        )


class Przedmiot(object):
    """
    Przedmiot

    Attributes:
        id (:class:`int`): ID przedmiotu
        nazwa (:class:`str`): Pełna nazwa przedmiotu
        kod (:class:`str`): Kod nazwy przedmiotu
    """

    def __init__(self, id=None, nazwa=None, kod=None):
        self.id = id
        self.nazwa = nazwa
        self.kod = kod

    def __repr__(self):
        return "<Przedmiot {!r}>".format(self.nazwa)

    @classmethod
    def from_json(cls, j):
        id = j.get("Id")
        nazwa = j.get("Nazwa")
        kod = j.get("Kod")
        return cls(id=id, nazwa=nazwa, kod=kod)


class Pracownik(object):
    """
    Pracownik szkoły

    Attributes:
        id (:class:`int`): ID pracownika
        nazwa (:class:`nazwa`): Nazwisko oraz imię pracownika
        imie (:class:`str`): Imię pracownika
        nazwisko (:class:`str`): Nazwisko pracownika
        kod (:class:`str`): Kod pracownika
        login_id (:class:`int`): ID konta pracownika
    """

    def __init__(self, id=None, imie=None, nazwisko=None, kod=None, login_id=None):
        self.id = id
        self.nazwa = "{!s} {!s}".format(nazwisko, imie)
        self.imie = imie
        self.nazwisko = nazwisko
        self.kod = kod
        self.login_id = login_id

    def __repr__(self):
        return "<Pracownik {!r}>".format(self.nazwa)

    @classmethod
    def from_json(cls, j):
        id = j.get("Id")
        imie = j.get("Imie")
        nazwisko = j.get("Nazwisko")
        kod = j.get("Kod")
        login_id = j.get("LoginId")
        return cls(id=id, imie=imie, nazwisko=nazwisko, kod=kod, login_id=login_id)


class PoraLekcji(object):
    """
    Pora lekcji

    Attributes:
        id (:class:`int`): ID pory lekcji
        numer (:class:`int`): Numer kolejny pory lekcji
        od (:class:`datetime.datetime`): Godzina i minuta rozpoczęcia lekcji
        do (:class:`datetime.datetime`): Godzina i minuta zakończenia lekcji
    """

    def __init__(self, id=None, numer=None, od=None, do=None):
        self.id = id
        self.numer = numer
        self.od = od
        self.do = do

    def __repr__(self):
        return "<PoraLekcji {!s}: od='{!s}:{:02d}' do='{!s}:{:02d}'>".format(
            self.numer, self.od.hour, self.od.minute, self.do.hour, self.do.minute
        )

    @classmethod
    def from_json(cls, j):
        id = j.get("Id")
        numer = j.get("Numer")
        od = timestamp_to_datetime(j.get("Poczatek"))
        do = timestamp_to_datetime(j.get("Koniec"))
        return cls(id=id, numer=numer, od=od, do=do)


class Lekcja(object):
    """
    Lekcja

    Attributes:
        numer (:class:`int`): Numer lekcji
        pora (:class:`vulcan.models.PoraLekcji`): Informacje o porze lekcji
        przedmiot (:class:`vulcan.models.Przedmiot`): Przedmiot na lekcji
        dzien (:class:`datetime.date`): Data lekcji
        od (:class:`datetime.datetime`): Data i godzina rozpoczęcia lekcji
        do (:class:`datetime.datetime`): Data i godzina zakończenia lekcji
    """

    def __init__(
        self,
        numer=None,
        pora=None,
        przedmiot=None,
        pracownik=None,
        dzien=None,
        od=None,
        do=None,
    ):
        self.numer = numer
        self.pora = pora
        self.przedmiot = przedmiot
        self.pracownik = pracownik
        self.dzien = dzien
        self.od = od
        self.do = do

    def __repr__(self):
        return "<Lekcja {!s}: przedmiot={!r} pracownik={!r}>".format(
            self.numer, self.przedmiot.nazwa, self.pracownik.nazwa
        )

    @classmethod
    def from_json(cls, j):
        numer = j.get("NumerLekcji")
        pora = PoraLekcji.from_json(j.get("PoraLekcji"))
        przedmiot = Przedmiot.from_json(j.get("Przedmiot"))
        pracownik = Pracownik.from_json(j.get("Pracownik"))
        dzien_datetime = timestamp_to_datetime(j.get("Dzien"))
        dzien = dzien_datetime.date()
        od = concat_hours_and_minutes(dzien_datetime, j["PoraLekcji"]["Poczatek"])
        do = concat_hours_and_minutes(dzien_datetime, j["PoraLekcji"]["Koniec"])
        return cls(
            numer=numer,
            pora=pora,
            przedmiot=przedmiot,
            pracownik=pracownik,
            dzien=dzien,
            od=od,
            do=do,
        )


class Sprawdzian(object):
    """
    Sprawdzian, test, praca klasowa lub kartkówka

    Attributes:
        id (:class:`int`): ID sprawdzianu
        rodzaj (:class:`vulcan.models.RodzajSprawdzianu`): Rodzaj sprawdzianu
        przedmiot (:class:`vulcan.models.Przedmiot`): Przedmiot, z którego jest sprawdzian
        pracownik (:class:`vulcan.models.Pracownik`): Pracownik szkoły, który wpisał sprawdzian
        opis (:class:`str`): Opis sprawdzianu
        dzien (:class:`datetime.date`): Dzień sprawdzianu
    """

    def __init__(
        self,
        id=None,
        rodzaj=None,
        przedmiot=None,
        pracownik=None,
        klasa=None,
        opis=None,
        dzien=None,
    ):
        self.id = id
        self.rodzaj = rodzaj
        self.przedmiot = przedmiot
        self.pracownik = pracownik
        self.opis = opis
        self.dzien = dzien

    def __repr__(self):
        return "<Sprawdzian: przedmiot={!r}>".format(self.przedmiot.nazwa)

    @classmethod
    def from_json(cls, j):
        id = j.get("Id")
        rodzaj = RodzajSprawdzianu(j.get("RodzajNumer"))
        przedmiot = Przedmiot.from_json(j.get("Przedmiot"))
        pracownik = Pracownik.from_json(j.get("Pracownik"))
        opis = j.get("Opis")
        dzien = timestamp_to_date(j.get("Data"))
        return cls(
            id=id,
            rodzaj=rodzaj,
            przedmiot=przedmiot,
            pracownik=pracownik,
            opis=opis,
            dzien=dzien,
        )


class ZadanieDomowe(object):
    """
    Zadanie domowe

    Attributes:
        id (:class:`int`): ID zadania domowego
        przedmiot (:class:`vulcan.models.Przedmiot`): Przedmiot, z którego jest zadane zadanie
        pracownik (:class:`vulcan.models.Pracownik`): Pracownik szkoły, który wpisał to zadanie
        opis (:class:`str`): Opis zadania domowego
        dzien (:class:`datetime.date`): Dzień zadania domowego
    """

    def __init__(self, id=None, pracownik=None, przedmiot=None, opis=None, dzien=None):
        self.id = id
        self.pracownik = pracownik
        self.przedmiot = przedmiot
        self.opis = opis
        self.dzien = dzien

    def __repr__(self):
        return "<ZadanieDomowe przedmiot={!r}>".format(self.przedmiot.nazwa)

    @classmethod
    def from_json(cls, j):
        id = j.get("Id")
        pracownik = Pracownik.from_json(j.get("Pracownik"))
        przedmiot = Przedmiot.from_json(j.get("Przedmiot"))
        opis = j.get("Opis")
        dzien = timestamp_to_date(j.get("Data"))
        return cls(
            id=id, pracownik=pracownik, przedmiot=przedmiot, opis=opis, dzien=dzien
        )
