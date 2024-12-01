import streamlit as st
from components.forms import participant_form, test_form, update_exit_date_form
from components.charts import plot_progress_chart, plot_category_averages, plot_prediction_chart
from components.reports import download_reports
from utils.data_loader import (
    load_participants,
    load_tests,
    save_data,
    get_active_participants,
    get_inactive_participants,
)
from utils.processors import (
    calculate_test_percentages,
    aggregate_progress,
    calculate_statistics,
    prepare_prediction_data,
    calculate_category_averages,
)

# Streamlit-Konfiguration
st.set_page_config(page_title="Mathematik-Kurs Verwaltung", layout="wide")

# Globale Dateipfade (Simulation einer Datenbank)
PARTICIPANTS_FILE = "data/participants.csv"
TESTS_FILE = "data/tests.csv"

# Daten laden
participants = load_participants(PARTICIPANTS_FILE)
tests = load_tests(TESTS_FILE)

# Hauptmenü
st.title("Mathematik-Kurs Verwaltung")
menu = st.sidebar.radio("Navigation", ["Teilnehmer", "Tests", "Berichte", "Prognosen"])

if menu == "Teilnehmer":
    st.header("Teilnehmerverwaltung")

    # Anzeige der Teilnehmer
    show_all = st.checkbox("Alle Teilnehmer anzeigen (inkl. Inaktive)")
    if show_all:
        st.dataframe(participants)
    else:
        active_participants = get_active_participants(participants)
        st.dataframe(active_participants)

    # Teilnehmer hinzufügen
    st.subheader("Teilnehmer hinzufügen")
    new_participant = participant_form()
    if new_participant:
        participants = participants.append(new_participant, ignore_index=True)
        save_data(participants, PARTICIPANTS_FILE)

    # Austrittsdatum ändern
    st.subheader("Austrittsdatum aktualisieren")
    updated_exit = update_exit_date_form(participants.to_dict(orient="records"))
    if updated_exit:
        participants.loc[
            participants["ID"] == updated_exit["participant_id"], "Austrittsdatum"
        ] = updated_exit["new_exit_date"]
        save_data(participants, PARTICIPANTS_FILE)

elif menu == "Tests":
    st.header("Testmanagement")

    # Test hinzufügen
    st.subheader("Test hinzufügen")
    new_test = test_form()
    if new_test:
        new_test_df = pd.DataFrame(new_test["scores"])
        new_test_df["Teilnehmer_ID"] = new_test["participant_id"]
        new_test_df["Testdatum"] = new_test["test_date"]
        tests = tests.append(new_test_df, ignore_index=True)
        save_data(tests, TESTS_FILE)

    # Testergebnisse visualisieren
    st.subheader("Testergebnisse visualisieren")
    participant_id = st.selectbox("Wähle einen Teilnehmer", participants["ID"].tolist())
    participant_tests = tests[tests["Teilnehmer_ID"] == participant_id]
    if not participant_tests.empty:
        participant_tests = calculate_test_percentages(participant_tests)
        progress_data = aggregate_progress(participant_tests, participant_id)
        plot_progress_chart(progress_data)

elif menu == "Berichte":
    st.header("Berichtserstellung")

    participant_id = st.selectbox("Wähle einen Teilnehmer für den Bericht", participants["ID"].tolist())
    participant_tests = tests[tests["Teilnehmer_ID"] == participant_id]

    if not participant_tests.empty:
        # Berichtsdaten
        stats = calculate_statistics(participant_tests, participant_id)
        averages = calculate_category_averages(participant_tests)
        progress_data = aggregate_progress(participant_tests, participant_id)

        # Visualisierung
        st.subheader("Fortschrittsübersicht")
        plot_progress_chart(progress_data)

        st.subheader("Kategoriedurchschnittswerte")
        plot_category_averages(averages)

        # Bericht generieren
        if st.button("Bericht generieren"):
            participant_data = participants.loc[participants["ID"] == participant_id].to_dict(orient="records")[0]
            download_reports(participant_data, progress_data, stats, averages)
            st.success(f"Bericht für {participant_data['name']} wurde erstellt!")

elif menu == "Prognosen":
    st.header("Prognose")

    participant_id = st.selectbox("Wähle einen Teilnehmer für die Prognose", participants["ID"].tolist())
    participant_tests = tests[tests["Teilnehmer_ID"] == participant_id]

    if not participant_tests.empty:
        # Prognosedaten vorbereiten
        prediction_data = prepare_prediction_data(participant_tests, participant_id)

        # Beispiel: Einbindung eines AutoML-Modells
        prediction_data["Gesamtprozentsatz"] = prediction_data["Gesamtprozentsatz"] * 1.05  # Platzhalter
        plot_prediction_chart(prediction_data)
