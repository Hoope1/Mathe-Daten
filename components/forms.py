import streamlit as st
from utils.validators import validate_participant_data, validate_test_input


def participant_form() -> dict:
    """
    Erstellt ein Formular für das Hinzufügen oder Bearbeiten eines Teilnehmers.

    Returns:
        dict: Validierte Teilnehmerdaten.
    """
    st.header("Teilnehmer hinzufügen oder ändern")

    name = st.text_input("Name", placeholder="Vor- und Nachname eingeben")
    sv_number = st.text_input("Sozialversicherungsnummer", placeholder="XXXXDDMMYY")
    entry_date = st.date_input("Eintrittsdatum")
    exit_date = st.date_input("Austrittsdatum")
    submit_button = st.button("Teilnehmer speichern")

    if submit_button:
        participant_data = {
            "name": name.strip(),
            "sv_number": sv_number.strip(),
            "entry_date": entry_date.strftime("%Y-%m-%d"),
            "exit_date": exit_date.strftime("%Y-%m-%d"),
        }
        try:
            validate_participant_data(participant_data)
            st.success("Teilnehmerdaten erfolgreich gespeichert!")
            return participant_data
        except ValueError as e:
            st.error(f"Fehler: {e}")
    return {}


def test_form() -> dict:
    """
    Erstellt ein Formular für die Eingabe von Testergebnissen.

    Returns:
        dict: Validierte Testdaten.
    """
    st.header("Test hinzufügen")

    test_date = st.date_input("Testdatum")
    st.subheader("Punkte pro Kategorie (erreicht / maximal)")

    categories = ["Textaufgaben", "Raumvorstellung", "Gleichungen", "Brüche", "Grundrechenarten", "Zahlenraum"]
    scores = []

    for category in categories:
        col1, col2 = st.columns(2)
        with col1:
            reached_points = st.number_input(f"{category} - Erreicht", min_value=0, step=1)
        with col2:
            max_points = st.number_input(f"{category} - Maximal", min_value=1, step=1)
        scores.append({"category": category, "reached_points": reached_points, "max_points": max_points})

    submit_button = st.button("Test speichern")

    if submit_button:
        test_data = {
            "test_date": test_date.strftime("%Y-%m-%d"),
            "scores": scores,
        }
        try:
            validate_test_input(test_data)
            st.success("Testdaten erfolgreich gespeichert!")
            return test_data
        except ValueError as e:
            st.error(f"Fehler: {e}")
    return {}


def update_exit_date_form(participants: list) -> dict:
    """
    Erstellt ein Formular für das Aktualisieren des Austrittsdatums eines Teilnehmers.

    Args:
        participants (list): Liste aller Teilnehmer.

    Returns:
        dict: Aktualisierte Daten mit Teilnehmer-ID und neuem Austrittsdatum.
    """
    st.header("Austrittsdatum aktualisieren")

    participant_id = st.selectbox("Wähle einen Teilnehmer", options=[p["ID"] for p in participants])
    new_exit_date = st.date_input("Neues Austrittsdatum")
    submit_button = st.button("Austrittsdatum speichern")

    if submit_button:
        try:
            updated_data = {
                "participant_id": participant_id,
                "new_exit_date": new_exit_date.strftime("%Y-%m-%d"),
            }
            st.success("Austrittsdatum erfolgreich aktualisiert!")
            return updated_data
        except ValueError as e:
            st.error(f"Fehler: {e}")
    return {}
      
