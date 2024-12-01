import pandas as pd
from utils.cache import cache_data
import datetime


def load_participants(file_path: str) -> pd.DataFrame:
    """
    Lädt die Teilnehmerdaten aus einer CSV-Datei und cached sie.

    Args:
        file_path (str): Pfad zur CSV-Datei.

    Returns:
        pd.DataFrame: Teilnehmerdaten als DataFrame.
    """
    def loader():
        data = pd.read_csv(file_path)
        data["Eintrittsdatum"] = pd.to_datetime(data["Eintrittsdatum"])
        data["Austrittsdatum"] = pd.to_datetime(data["Austrittsdatum"])
        data["Aktiv"] = data["Austrittsdatum"] > datetime.date.today()
        return data

    return cache_data(loader)


def load_tests(file_path: str) -> pd.DataFrame:
    """
    Lädt die Testdaten aus einer CSV-Datei und cached sie.

    Args:
        file_path (str): Pfad zur CSV-Datei.

    Returns:
        pd.DataFrame: Testdaten als DataFrame.
    """
    def loader():
        data = pd.read_csv(file_path)
        data["Testdatum"] = pd.to_datetime(data["Testdatum"])
        return data

    return cache_data(loader)


def save_data(data: pd.DataFrame, file_path: str) -> None:
    """
    Speichert einen DataFrame in eine CSV-Datei.

    Args:
        data (pd.DataFrame): Zu speichernde Daten.
        file_path (str): Pfad zur CSV-Datei.

    Returns:
        None
    """
    data.to_csv(file_path, index=False)


def add_participant(participants: pd.DataFrame, participant_data: dict) -> pd.DataFrame:
    """
    Fügt einen neuen Teilnehmer zu den Daten hinzu.

    Args:
        participants (pd.DataFrame): Aktuelle Teilnehmerdaten.
        participant_data (dict): Daten des neuen Teilnehmers.

    Returns:
        pd.DataFrame: Aktualisierte Teilnehmerdaten.
    """
    new_entry = pd.DataFrame([participant_data])
    updated_data = pd.concat([participants, new_entry], ignore_index=True)
    return updated_data


def update_exit_date(participants: pd.DataFrame, participant_id: int, new_exit_date: str) -> pd.DataFrame:
    """
    Aktualisiert das Austrittsdatum eines Teilnehmers.

    Args:
        participants (pd.DataFrame): Aktuelle Teilnehmerdaten.
        participant_id (int): ID des Teilnehmers.
        new_exit_date (str): Neues Austrittsdatum (YYYY-MM-DD).

    Returns:
        pd.DataFrame: Aktualisierte Teilnehmerdaten.
    """
    participants.loc[participants["ID"] == participant_id, "Austrittsdatum"] = pd.to_datetime(new_exit_date)
    participants["Aktiv"] = participants["Austrittsdatum"] > datetime.date.today()
    return participants


def get_active_participants(participants: pd.DataFrame) -> pd.DataFrame:
    """
    Filtert die aktiven Teilnehmer.

    Args:
        participants (pd.DataFrame): Teilnehmerdaten.

    Returns:
        pd.DataFrame: Aktive Teilnehmer.
    """
    return participants[participants["Aktiv"]]


def get_inactive_participants(participants: pd.DataFrame) -> pd.DataFrame:
    """
    Filtert die inaktiven Teilnehmer.

    Args:
        participants (pd.DataFrame): Teilnehmerdaten.

    Returns:
        pd.DataFrame: Inaktive Teilnehmer.
    """
    return participants[~participants["Aktiv"]]
