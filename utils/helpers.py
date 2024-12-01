import datetime
import re
from typing import Dict, Union


def calculate_percentage(part: float, total: float) -> float:
    """
    Berechnet den Prozentsatz eines Teils im Verhältnis zum Gesamtwert.

    Args:
        part (float): Erreichter Wert.
        total (float): Maximal möglicher Wert.

    Returns:
        float: Prozentsatz (0-100).
    """
    if total == 0:
        return 0.0
    return round((part / total) * 100, 2)


def parse_sv_number(sv_number: str) -> Dict[str, Union[str, int]]:
    """
    Extrahiert das Geburtsdatum und Alter aus der Sozialversicherungsnummer.

    Args:
        sv_number (str): Sozialversicherungsnummer im Format XXXXDDMMYY.

    Returns:
        Dict[str, Union[str, int]]: Geburtsdatum und Alter.
    """
    match = re.match(r"^\d{4}(\d{2})(\d{2})(\d{2})$", sv_number)
    if not match:
        raise ValueError("Ungültige Sozialversicherungsnummer.")
    
    day, month, year = map(int, match.groups())
    birth_date = datetime.date(2000 + year if year < 50 else 1900 + year, month, day)
    age = datetime.date.today().year - birth_date.year
    if (datetime.date.today().month, datetime.date.today().day) < (birth_date.month, birth_date.day):
        age -= 1
    
    return {"birth_date": birth_date, "age": age}


def format_date(date: Union[str, datetime.date]) -> str:
    """
    Formatiert ein Datum im Format DD.MM.YYYY.

    Args:
        date (Union[str, datetime.date]): Eingabedatum.

    Returns:
        str: Formatiertes Datum.
    """
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    return date.strftime("%d.%m.%Y")
  
