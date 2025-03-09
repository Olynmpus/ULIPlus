# ULIPlus.py
# Author : Jorge Mejia

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import time

# Function to generate normal distribution data
def generate_norm_pdf(mean, std, snr_range):
    x = np.linspace(snr_range[0], snr_range[1], 100)
    pdf = stats.norm.pdf(x, mean, std)
    return x, pdf

# Function for the test keypad screen
def run_test_keypad():
    st.header("Test Keypad")

    keypad = [
        ["aka", "obo", "ili"],
        ["low", "mid", "high"],
        ["apa", "oto", "uku"]
    ]

    cols = st.columns(3)
    for i in range(3):
        for j in range(3):
            if cols[j].button(keypad[i][j]):
                st.write(f"Pressed: {keypad[i][j]}")  # Example action

    if 'test_running' not in st.session_state:
        st.session_state.test_running = False
    if 'test_complete' not in st.session_state:
        st.session_state.test_complete = False
    if 'progress_percent' not in st.session_state:
        st.session_state.progress_percent = 0

    progress_bar = st.progress(st.session_state.progress_percent)

    col_start, col_stop, col_exit = st.columns(3)

    if col_start.button("Start Test"):
        st.session_state.test_running = True
        st.session_state.progress_percent = 0
        st.session_state.test_complete = False
        progress_bar.progress(0)
        st.write("Test started...")

    if col_stop.button("Stop Test"):
        st.session_state.test_running = False
        st.session_state.test_complete = True
        st.write("Test stopped.")
        return False

    if col_exit.button("Exit Test"):
        st.session_state.test_running = False
        st.session_state.test_complete = False
        return False

    if st.session_state.test_running:
        while st.session_state.progress_percent < 100:
            st.session_state.progress_percent += 1
            progress_bar.progress(st.session_state.progress_percent)
            time.sleep(0.1)  # Simulate test progress
        st.session_state.test_running = False
        st.session_state.test_complete = True
        st.write("Test complete.")
        return False

    return True

# Streamlit Application
st.set_page_config(page_title="ULI", page_icon="👂")

st.markdown(
    """
    <style>
    .uli-title {
        font-size: 48px !important;
        font-weight: 900;
        color: #007bff;
        text-align: center;
        margin-bottom: 5px;
    }
    .uli-subtitle {
        font-size: 24px;
        text-align: center;
        color: #6c757d;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<p class="uli-title">AI-based Universal Language Independent Test</p>', unsafe_allow_html=True)

st.markdown("---")

# --- Icon-Based Navigation ---
col1, col2, col3, col4 = st.columns(4)

if col1.button("👂 Screener"):
    choice = "Screener"
elif col2.button("🩺 Diagnosis"):
    choice = "Diagnosis"
elif col3.button("⚙️ Fitting"):
    choice = "Fitting"
elif col4.button("📈 Monitoring"):
    choice = "Monitoring"
else:
    choice = "Screener"  # default selection

if 'test_complete' not in st.session_state:
    st.session_state.test_complete = False

# --- Content Based on Selection ---
if choice == "Screener":
    st.header("Screener")
    age = st.number_input("Age", min_value=0, max_value=120, value=30)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    social_status = st.text_input("Social Status")
    hearing_frequency = st.selectbox("Frequency of Hearing Problems", ["Never", "Rarely", "Occasionally", "Frequently"])

    if st.button("Run Screener"):
        if run_test_keypad():
            if st.session_state.test_complete:
                # Simulate SNR data
                mean = -8
                std = 1.6
                snr_range = (-15, 5)
                x, pdf = generate_norm_pdf(mean, std, snr_range)
                individual_snr = np.random.normal(mean, std)
                p_value = stats.norm.cdf(individual_snr, mean, std)

                # Plotting
                fig, ax = plt.subplots()
                ax.plot(x, pdf, label="Normative Data")
                ax.axvline(individual_snr, color='red', linestyle='--', label=f"Individual SNR: {individual_snr:.2f}")
                ax.set_xlabel("SNR (dB)")
                ax.set_ylabel("Probability Density")
                ax.legend()
                st.pyplot(fig)
                st.write(f"P-value: {p_value:.4f}")

            st.session_state.test_complete = False  # reset

elif choice == "Diagnosis":
    st.header("Diagnosis")
    age = st.number_input("Age", min_value=0, max_value=120, value=30)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    social_status = st.text_input("Social Status")
    hearing_frequency = st.selectbox("Frequency of Hearing Problems", ["Never", "Rarely", "Occasionally", "Frequently"])

    if st.button("Run Diagnosis"):
        if run_test_keypad():
            if st.session_state.test_complete:
                # Simulated SNR graph
                mean = -8
                std = 1.6
                snr_range = (-15, 5)
                x, pdf = generate_norm_pdf(mean, std, snr_range)
                individual_snr = np.random.normal(mean, std)

                fig, ax = plt.subplots(figsize=(6, 4))
                ax.plot(x, pdf, label="Normative Data")
                ax.axvline(individual_snr, color='red', linestyle='--', label=f"Individual SNR: {individual_snr:.2f}")
                ax.set_xlabel("SNR (dB)")
                ax.set_ylabel("Probability Density")
                ax.legend()
                st.pyplot(fig)

            st.session_state.test_complete = False  # reset

elif choice == "Fitting":
    st.header("Fitting")
    diagnosis_snr = st.number_input("Diagnosis SNR", value=-8.0)
    if st.button("Run Fitting"):
        if run_test_keypad():
            if st.session_state.test_complete:
                vowels = ["a", "o", "i"]
                consonants = ["Low", "Mid", "High"]
                pre_fitting = np.random.randint(0, 101, size=6)
                post_fitting = np.random.randint(0, 101, size=6)

                fig, ax = plt.subplots()
                ax.bar(vowels + consonants, pre_fitting, alpha=0.6, label="Pre-Fitting")
                ax.bar(vowels + consonants, post_fitting, alpha=0.6, label="Post-Fitting", bottom=pre_fitting)
                ax.set_ylabel("Percentage Correct (%)")
                ax.legend()
                st.pyplot(fig)
