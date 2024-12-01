import re
import datetime
from typing import List, Dict, Any


def validate_sv_number(sv_number: str) -> bool:
    """
    Validiert die Sozialversicherungsnummer (Format: XXXXDDMMYY).

    Args:
        sv_number (str): Sozialversicherungsnummer.

    Returns:
        bool: True, wenn gültig, sonst False.
    """
    pattern = r"^\d{4}\d{2}\d{2}\d{2}$"
    if not re.match(pattern, sv_number):
        raise ValueError("Ungültige Sozialversicherungsnummer. Das Format muss XXXXDDMMYY sein.")
    return True


def validate_date_format(date: str, format: str = "%Y-%m-%d") -> bool:
    """
    Überprüft, ob ein Datum dem erwarteten Format entspricht.

    Args:
        date (str): Eingabedatum als String.
        format (str): Erwartetes Datumsformat.

    Returns:
        bool: True, wenn das Datum gültig ist, sonst False.
    """
    try:
        datetime.datetime.strptime(date, format)
        return True
    except ValueError:
        raise ValueError(f"Ungültiges Datum. Erwartetes Format: {format}.")


def validate_test_scores(test_scores: List[Dict[str, Any]]) -> bool:
    """
    Validiert die Testdaten und überprüft, ob die Summe der maximal möglichen Punkte 100 beträgt.

    Args:
        test_scores (List[Dict[str, Any]]): Liste der Testkategorien mit erreichten und maximalen Punkten.

    Returns:
        bool: True, wenn die Testdaten gültig sind, sonst False.
    """
    total_max_points = sum(score.get("max_points", 0) for score in test_scores)
    if total_max_points != 100:
        raise ValueError(f"Die maximal möglichen Punkte aller Kategorien müssen 100 betragen, gefunden: {total_max_points}.")
    return True


def validate_participant_data(participant_data: Dict[str, Any]) -> bool:
    """
    Validiert die Eingabedaten eines Teilnehmers.

    Args:
        participant_data (Dict[str, Any]): Teilnehmerdaten (Name, SV-Nummer, Eintritts- und Austrittsdatum).

    Returns:
        bool: True, wenn die Teilnehmerdaten gültig sind, sonst False.
    """
    if "name" not in participant_data or not participant_data["name"].strip():
        raise ValueError("Der Name des Teilnehmers darf nicht leer sein.")
    if "sv_number" not in participant_data or not validate_sv_number(participant_data["sv_number"]):
        raise ValueError("Ungültige Sozialversicherungsnummer.")
    if "entry_date" not in participant_data or not validate_date_format(participant_data["entry_date"]):
        raise ValueError("Ungültiges Eintrittsdatum.")
    if "exit_date" not in participant_data or not validate_date_format(participant_data["exit_date"]):
        raise ValueError("Ungültiges Austrittsdatum.")

    entry_date = datetime.datetime.strptime(participant_data["entry_date"], "%Y-%m-%d").date()
    exit_date = datetime.datetime.strptime(participant_data["exit_date"], "%Y-%m-%d").date()
    if entry_date >= exit_date:
        raise ValueError("Das Eintrittsdatum muss vor dem Austrittsdatum liegen.")
    
    return True


def validate_test_input(test_input: Dict[str, Any]) -> bool:
    """
    Validiert die Eingabedaten eines Tests.

    Args:
        test_input (Dict[str, Any]): Testdaten (Testdatum, erreichte und maximale Punkte).

    Returns:
        bool: True, wenn die Testdaten gültig sind, sonst False.
    """
    if "test_date" not in test_input or not validate_date_format(test_input["test_date"]):
        raise ValueError("Ungültiges Testdatum.")
    if "scores" not in test_input or not validate_test_scores(test_input["scores"]):
        raise ValueError("Ungültige Testpunkte.")
    return True
  
