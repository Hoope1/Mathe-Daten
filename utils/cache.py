import streamlit as st
from typing import Callable, Any


@st.cache_data(ttl=3600, max_entries=100)
def cache_data(loader_function: Callable, *args, **kwargs) -> Any:
    """
    Lädt und cached Daten mit einer Time-to-Live (TTL) von 1 Stunde.

    Args:
        loader_function (Callable): Funktion, die die Daten lädt.
        *args: Argumente für die Funktion.
        **kwargs: Keyword-Argumente für die Funktion.

    Returns:
        Any: Die geladenen und gecachten Daten.
    """
    return loader_function(*args, **kwargs)


@st.cache_resource
def cache_resource(func: Callable, *args, **kwargs) -> Any:
    """
    Cached ressourcenintensive Operationen persistierend.

    Args:
        func (Callable): Funktion, die gecached wird.
        *args: Argumente für die Funktion.
        **kwargs: Keyword-Argumente für die Funktion.

    Returns:
        Any: Das Ergebnis der Funktion.
    """
    return func(*args, **kwargs)


def clear_cache() -> None:
    """
    Löscht den Streamlit-Cache.

    Returns:
        None
    """
    st.cache_data.clear()
    st.cache_resource.clear()
    st.success("Cache wurde erfolgreich gelöscht.")


def simulate_loading(message: str = "Lade Daten...", duration: int = 2) -> None:
    """
    Simuliert einen Ladeprozess mit einem Spinner.

    Args:
        message (str): Nachricht, die angezeigt wird.
        duration (int): Dauer des Ladeprozesses in Sekunden.

    Returns:
        None
    """
    with st.spinner(message):
        import time
        time.sleep(duration)
      
