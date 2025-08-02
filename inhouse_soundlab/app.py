"""
Main entry point for the INHOUSE SoundLab Streamlit app.

This application bundles four simple tools into a single web app:

* **Hook Generator** – Produces a random, catchy lyrical hook from a predefined list.
* **Melody Generator** – Generates a short sequence of random notes as a starting point for melodic ideas.
* **Drum Pattern Generator** – Builds a simple eight‑beat drum pattern using kick, snare and hi‑hat sounds.
* **Promo Funnel** – Allows visitors to sign up for the "Welcome Home" INHOUSE Pack by entering an email address.

Each section includes a call to action so you can collect email addresses from visitors who want more information or
access to the promo pack. Email addresses and timestamps are appended to `shared_assets/email_signups.csv` in
comma‑separated format.

To run the app locally you will need to install the Streamlit dependency. Once installed, launch the app from
the command line with:

    pip install streamlit
    streamlit run app.py

When deploying to a hosting provider (e.g. Streamlit Community Cloud) make sure the `requirements.txt` file
includes `streamlit>=1.32`. The app expects a `shared_assets` folder with an `inhouse_logo.png` and a writable
`email_signups.csv`.
"""

import datetime
import random
from pathlib import Path

import streamlit as st

# Determine the location of the shared assets folder relative to this file.
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "shared_assets"
LOGO_PATH = ASSETS_DIR / "inhouse_logo.png"
SIGNUPS_FILE = ASSETS_DIR / "email_signups.csv"


def save_email(email: str) -> None:
    """Append an email and the current timestamp to the signups CSV."""
    if not email:
        return
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    with SIGNUPS_FILE.open("a", encoding="utf-8") as f:
        now = datetime.datetime.now().isoformat()
        f.write(f"{email},{now}\n")


def hook_generator() -> None:
    """Display the Hook Generator interface and handle user interaction."""
    st.header("Hook Generator")
    st.markdown(
        "Generate a catchy lyric hook for your next track. Click the button to receive a random hook suggestion."
    )
    hooks = [
        "Feel the rhythm, let it take control",
        "We light up the night like stars in the sky",
        "Keep on moving to the beat of your heart",
        "Never let go, this love is on fire",
        "Ride the wave, don’t ever slow down",
        "Dance all night, we’re young and free",
    ]
    if st.button("Generate Hook", key="hook_button"):
        st.success(random.choice(hooks))
    with st.expander("Get the 'Welcome Home' INHOUSE Pack"):
        email = st.text_input("Enter your email", key="hook_email")
        if st.button("Submit", key="hook_submit"):
            save_email(email)
            st.success("Thanks! Check your inbox for the pack soon.")


def melody_generator() -> None:
    """Display the Melody Generator interface and handle user interaction."""
    st.header("Melody Generator")
    st.markdown(
        "Create a short random melody as inspiration. The generator picks notes from the C major scale and assigns them octave numbers."
    )
    if st.button("Generate Melody", key="melody_button"):
        notes = ["C", "D", "E", "F", "G", "A", "B"]
        accidentals = ["", "♯", "♭"]
        melody = [
            random.choice(notes) + random.choice(accidentals) + str(random.randint(3, 5))
            for _ in range(8)
        ]
        st.success(" – ".join(melody))
    with st.expander("Get the 'Welcome Home' INHOUSE Pack"):
        email = st.text_input("Enter your email", key="melody_email")
        if st.button("Submit", key="melody_submit"):
            save_email(email)
            st.success("Thanks! Check your inbox for the pack soon.")


def drum_pattern_generator() -> None:
    """Display the Drum Pattern Generator interface and handle user interaction."""
    st.header("Drum Pattern Generator")
    st.markdown("Build a simple eight‑beat drum pattern using kicks, snares and hi‑hats.")
    if st.button("Generate Drum Pattern", key="drum_button"):
        elements = ["Kick", "Snare", "Hi‑hat"]
        pattern = [random.choice(elements) for _ in range(8)]
        st.success(" | ".join(pattern))
    with st.expander("Get the 'Welcome Home' INHOUSE Pack"):
        email = st.text_input("Enter your email", key="drum_email")
        if st.button("Submit", key="drum_submit"):
            save_email(email)
            st.success("Thanks! Check your inbox for the pack soon.")


def promo_funnel() -> None:
    """Display the Promo Funnel interface where users can sign up directly."""
    st.header("Promo Funnel")
    st.markdown(
        "Sign up to receive the free 'Welcome Home' INHOUSE Pack. Enter your email address below and we’ll deliver the goodies straight to your inbox."
    )
    email = st.text_input("Enter your email", key="promo_email")
    if st.button("Submit", key="promo_submit"):
        save_email(email)
        st.success("Thanks! Check your inbox for the pack soon.")


def main() -> None:
    """Main entry point of the Streamlit application."""
    st.set_page_config(page_title="INHOUSE SoundLab", page_icon="🎶", layout="centered")
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=200)
    st.title("INHOUSE SoundLab")
    st.markdown(
        "Welcome to the INHOUSE SoundLab. Select a tool from the sidebar to start creating music or claim your promo pack."
    )

    page = st.sidebar.radio(
        "Choose a tool",
        ("Hook Generator", "Melody Generator", "Drum Pattern Generator", "Promo Funnel"),
    )
    if page == "Hook Generator":
        hook_generator()
    elif page == "Melody Generator":
        melody_generator()
    elif page == "Drum Pattern Generator":
        drum_pattern_generator()
    else:
        promo_funnel()


if __name__ == "__main__":
    main()
Add unified INHOUSE SoundLab app
