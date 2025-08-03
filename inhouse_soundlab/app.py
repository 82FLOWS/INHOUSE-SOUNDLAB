"""
Main entry point for the INHOUSE SoundLab Streamlit app.

This application bundles four tools:

* Hook Generator – Produces a random, catchy lyrical hook.
* Melody Generator – Generates a random melody and a downloadable audio clip.
* Drum Pattern Generator – Builds a drum pattern and a downloadable audio clip.
* Promo Funnel – Allows visitors to sign up for the INHOUSE Pack.

Email addresses and timestamps are appended to `shared_assets/email_signups.csv`.
"""

import datetime
import os
import random
from pathlib import Path

import io
import numpy as np
import streamlit as st

# Determine the location of the shared assets folder relative to this file.
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "shared_assets"
LOGO_PATH = ASSETS_DIR / "inhouse_logo.png"
SIGNUPS_FILE = ASSETS_DIR / "email_signups.csv"

def save_email(email: str) -> None:
    """Append an email and timestamp to the signups CSV."""
    if not email:
        return
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    with SIGNUPS_FILE.open("a", encoding="utf-8") as f:
        now = datetime.datetime.now().isoformat()
        f.write(f"{email},{now}\n")

# Helper functions for note frequencies and audio synthesis
def _note_to_frequency(note: str) -> float:
    note_map = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
    letter = note[0]
    accidental = ""
    octave_part = ""
    for ch in note[1:]:
        if ch in ("♯", "♭"):
            accidental = ch
        else:
            octave_part += ch
    octave = int(octave_part) if octave_part else 4
    semitone = note_map[letter]
    if accidental == "♯":
        semitone += 1
    elif accidental == "♭":
        semitone -= 1
    semitone_offset_from_A4 = semitone + (octave - 4) * 12 - 9
    return 440.0 * (2 ** (semitone_offset_from_A4 / 12))


def _generate_sine_wave(frequency: float, duration: float, sample_rate: int = 44100) -> np.ndarray:
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return np.sin(2 * np.pi * frequency * t)

def _write_wav(samples: np.ndarray, sample_rate: int = 44100) -> bytes:
    samples_int16 = np.int16(samples / np.max(np.abs(samples)) * 32767)
    buf = io.BytesIO()
    import wave
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(samples_int16.tobytes())
    return buf.getvalue()

def generate_melody_audio(melody: list[str], duration_per_note: float = 0.5) -> bytes:
    sample_rate = 44100
    audio_segments = []
    for note in melody:
        freq = _note_to_frequency(note)
        audio_segments.append(_generate_sine_wave(freq, duration_per_note, sample_rate))
    full_audio = np.concatenate(audio_segments)
    return _write_wav(full_audio, sample_rate)

def generate_drum_audio(pattern: list[str], duration_per_beat: float = 0.25) -> bytes:
    sample_rate = 44100
    segments = []
    freq_map = {"Kick": 60.0, "Snare": 180.0, "Hi‑hat": 300.0}
    for element in pattern:
        freq = freq_map.get(element, 180.0)
        t = np.linspace(0, duration_per_beat, int(sample_rate * duration_per_beat), endpoint=False)
        envelope = np.exp(-5 * t)
        if element == "Hi‑hat":
            tone = np.random.uniform(-1, 1, size=t.shape)
        else:
            tone = np.sin(2 * np.pi * freq * t)
        segments.append(tone * envelope)
    full_audio = np.concatenate(segments)
    return _write_wav(full_audio, sample_rate)


def hook_generator() -> None:
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
        "In this moment, we own the night",
        "Lost in the groove, under city lights",
        "Heartbeat racing, bodies swayin’ to the beat",
        "Turn it up, let the world feel our heat",
        "Every step’s a story, every breath’s a song",
        "We’re unstoppable, nothing can go wrong",
    ]
    if "used_hooks" not in st.session_state:
        st.session_state.used_hooks = set()
    if st.button("Generate Hook", key="hook_button"):
        if len(st.session_state.used_hooks) >= len(hooks):
            st.session_state.used_hooks.clear()
        remaining_hooks = [h for h in hooks if h not in st.session_state.used_hooks]
        hook = random.choice(remaining_hooks)
        st.session_state.used_hooks.add(hook)
        st.success(hook)
    with st.expander("Get the 'Welcome Home' INHOUSE Pack"):
        email = st.text_input("Enter your email", key="hook_email")
        if st.button("Submit", key="hook_submit"):
            save_email(email)
            st.success("Thanks! Check your inbox for the pack soon.")

def melody_generator() -> None:
    st.header("Melody Generator")
    st.markdown(
        "Create a short random melody as inspiration. The generator picks notes from the C major scale"
        " and assigns them octave numbers."
    )
    if st.button("Generate Melody", key="melody_button"):
        notes = ["C", "D", "E", "F", "G", "A", "B"]
        accidentals = ["", "♯", "♭"]
        melody = [
            random.choice(notes) + random.choice(accidentals) + str(random.randint(3, 5))
            for _ in range(8)
        ]
        st.success(" – ".join(melody))
        audio_bytes = generate_melody_audio(melody, duration_per_note=0.5)
        st.audio(audio_bytes, format="audio/wav")
        st.download_button(
            label="Download Melody",
            data=audio_bytes,
            file_name="melody.wav",
            mime="audio/wav",
        )
    with st.expander("Get the 'Welcome Home' INHOUSE Pack"):
        email = st.text_input("Enter your email", key="melody_email")
        if st.button("Submit", key="melody_submit"):
            save_email(email)
            st.success("Thanks! Check your inbox for the pack soon.")


def drum_pattern_generator() -> None:
    st.header("Drum Pattern Generator")
    st.markdown("Build a simple eight‑beat drum pattern using kicks, snares and hi‑hats.")
    if st.button("Generate Drum Pattern", key="drum_button"):
        elements = ["Kick", "Snare", "Hi‑hat"]
        pattern = [random.choice(elements) for _ in range(8)]
        st.success(" | ".join(pattern))
        audio_bytes = generate_drum_audio(pattern, duration_per_beat=0.25)
        st.audio(audio_bytes, format="audio/wav")
        st.download_button(
            label="Download Drum Pattern",
            data=audio_bytes,
            file_name="drum_pattern.wav",
            mime="audio/wav",
        )
    with st.expander("Get the 'Welcome Home' INHOUSE Pack"):
        email = st.text_input("Enter your email", key="drum_email")
        if st.button("Submit", key="drum_submit"):
            save_email(email)
            st.success("Thanks! Check your inbox for the pack soon.")

def promo_funnel() -> None:
    st.header("Promo Funnel")
    st.markdown(
        "Sign up to receive the free 'Welcome Home' INHOUSE Pack. Enter your email address below and"
        " we’ll deliver the goodies straight to your inbox."
    )
    email = st.text_input("Enter your email", key="promo_email")
    if st.button("Submit", key="promo_submit"):
        save_email(email)
        st.success("Thanks! Check your inbox for the pack soon.")

def main() -> None:
    st.set_page_config(page_title="INHOUSE SoundLab", page_icon="🎶", layout="centered")
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=200)
    st.title("INHOUSE SoundLab")
    st.markdown(
        "Welcome to the INHOUSE SoundLab. Select a tool from the sidebar to start creating music or"
        " claim your promo pack."
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
