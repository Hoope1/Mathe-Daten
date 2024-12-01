import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd


def plot_progress_chart(progress_data: pd.DataFrame, title: str = "Fortschritt über Zeit") -> None:
    """
    Visualisiert den Fortschritt eines Teilnehmers über einen Zeitraum von Tests.

    Args:
        progress_data (pd.DataFrame): Fortschrittsdaten mit Datum und Prozentwerten.
        title (str): Titel des Diagramms.

    Returns:
        None
    """
    plt.figure(figsize=(10, 6))
    plt.plot(progress_data["Tage"], progress_data["Gesamtprozentsatz"], label="Gesamtfortschritt", linewidth=2, color="black")

    categories = ["Textaufgaben", "Raumvorstellung", "Gleichungen", "Brüche", "Grundrechenarten", "Zahlenraum"]
    for category in categories:
        plt.plot(progress_data["Tage"], progress_data[f"{category}_Prozent"], linestyle="--", label=category)

    plt.axvline(x=0, color="gray", linestyle="--", linewidth=1, label="Heute")
    plt.ylim(0, 100)
    plt.xlim(-30, 30)
    plt.title(title)
    plt.xlabel("Tage (von -30 bis +30)")
    plt.ylabel("Prozent (%)")
    plt.legend()
    plt.grid(alpha=0.5)
    st.pyplot(plt)


def plot_category_averages(category_averages: dict) -> None:
    """
    Visualisiert die Durchschnittswerte der Kategorien als Balkendiagramm.

    Args:
        category_averages (dict): Durchschnittswerte pro Kategorie.

    Returns:
        None
    """
    plt.figure(figsize=(8, 5))
    categories = list(category_averages.keys())
    averages = list(category_averages.values())

    plt.bar(categories, averages, color="skyblue")
    plt.title("Durchschnittswerte der Kategorien")
    plt.xlabel("Kategorien")
    plt.ylabel("Durchschnitt (%)")
    plt.ylim(0, 100)
    for i, avg in enumerate(averages):
        plt.text(i, avg + 1, f"{avg:.2f}%", ha="center", fontsize=9)

    st.pyplot(plt)


def plot_prediction_chart(predicted_data: pd.DataFrame, title: str = "Prognose über Zeit") -> None:
    """
    Visualisiert die Prognosen eines Teilnehmers über einen Zeitraum.

    Args:
        predicted_data (pd.DataFrame): Prognosedaten mit Tagen und vorhergesagten Prozentwerten.
        title (str): Titel des Diagramms.

    Returns:
        None
    """
    plt.figure(figsize=(10, 6))
    plt.plot(predicted_data["Tage"], predicted_data["Gesamtprozentsatz"], label="Prognose (Gesamt)", linewidth=2, color="blue")

    categories = ["Textaufgaben", "Raumvorstellung", "Gleichungen", "Brüche", "Grundrechenarten", "Zahlenraum"]
    for category in categories:
        plt.plot(predicted_data["Tage"], predicted_data[f"{category}_Prozent"], linestyle="--", label=f"Prognose ({category})")

    plt.axvline(x=0, color="gray", linestyle="--", linewidth=1, label="Heute")
    plt.ylim(0, 100)
    plt.xlim(-30, 30)
    plt.title(title)
    plt.xlabel("Tage (von -30 bis +30)")
    plt.ylabel("Prozent (%)")
    plt.legend()
    plt.grid(alpha=0.5)
    st.pyplot(plt)
  
