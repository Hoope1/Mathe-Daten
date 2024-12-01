import pandas as pd
from typing import Dict


def calculate_test_percentages(test_data: pd.DataFrame) -> pd.DataFrame:
    """
    Berechnet die Prozentwerte für jede Testkategorie und den Gesamtprozentsatz.

    Args:
        test_data (pd.DataFrame): Testdaten mit erreichten und maximal möglichen Punkten.

    Returns:
        pd.DataFrame: Testdaten mit zusätzlichen Spalten für Prozentwerte.
    """
    categories = ["Textaufgaben", "Raumvorstellung", "Gleichungen", "Brüche", "Grundrechenarten", "Zahlenraum"]
    for category in categories:
        test_data[f"{category}_Prozent"] = (test_data[f"{category}_Erreicht"] / test_data[f"{category}_Max"]) * 100
    test_data["Gesamtprozentsatz"] = test_data[[f"{cat}_Erreicht" for cat in categories]].sum(axis=1)
    return test_data


def aggregate_progress(test_data: pd.DataFrame, participant_id: int) -> pd.DataFrame:
    """
    Aggregiert den Fortschritt eines Teilnehmers über alle Tests.

    Args:
        test_data (pd.DataFrame): Testdaten.
        participant_id (int): ID des Teilnehmers.

    Returns:
        pd.DataFrame: Aggregierte Fortschrittsdaten, sortiert nach Datum.
    """
    participant_tests = test_data[test_data["Teilnehmer_ID"] == participant_id]
    progress = participant_tests[["Testdatum", "Gesamtprozentsatz"] + [f"{cat}_Prozent" for cat in [
        "Textaufgaben", "Raumvorstellung", "Gleichungen", "Brüche", "Grundrechenarten", "Zahlenraum"
    ]]]
    progress = progress.sort_values(by="Testdatum").reset_index(drop=True)
    return progress


def calculate_statistics(test_data: pd.DataFrame, participant_id: int) -> Dict[str, float]:
    """
    Berechnet Statistiken wie den Durchschnitt der letzten zwei Tests.

    Args:
        test_data (pd.DataFrame): Testdaten.
        participant_id (int): ID des Teilnehmers.

    Returns:
        Dict[str, float]: Statistiken des Teilnehmers.
    """
    participant_tests = test_data[test_data["Teilnehmer_ID"] == participant_id].sort_values(by="Testdatum", ascending=False)
    if len(participant_tests) < 2:
        raise ValueError("Nicht genügend Tests für statistische Berechnungen.")
    
    latest_two = participant_tests.iloc[:2]
    avg_last_two = latest_two["Gesamtprozentsatz"].mean()
    return {"Durchschnitt_letzte_zwei": round(avg_last_two, 2)}


def prepare_prediction_data(test_data: pd.DataFrame, participant_id: int) -> pd.DataFrame:
    """
    Bereitet die Daten für Prognosemodelle vor.

    Args:
        test_data (pd.DataFrame): Testdaten.
        participant_id (int): ID des Teilnehmers.

    Returns:
        pd.DataFrame: Daten im Format für Prognosemodelle.
    """
    participant_tests = test_data[test_data["Teilnehmer_ID"] == participant_id]
    participant_tests = participant_tests[["Testdatum", "Gesamtprozentsatz"]]
    participant_tests["Tage_seit_Ersttest"] = (participant_tests["Testdatum"] - participant_tests["Testdatum"].min()).dt.days
    return participant_tests


def calculate_category_averages(test_data: pd.DataFrame) -> Dict[str, float]:
    """
    Berechnet die Durchschnittswerte für jede Kategorie über alle Tests.

    Args:
        test_data (pd.DataFrame): Testdaten.

    Returns:
        Dict[str, float]: Durchschnittswerte pro Kategorie.
    """
    categories = ["Textaufgaben", "Raumvorstellung", "Gleichungen", "Brüche", "Grundrechenarten", "Zahlenraum"]
    averages = {}
    for category in categories:
        averages[f"{category}_Durchschnitt"] = test_data[f"{category}_Prozent"].mean()
    return {k: round(v, 2) for k, v in averages.items()}
  
