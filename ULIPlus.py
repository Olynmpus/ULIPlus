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

    progress_bar = st.progress(0)
    progress_percent = 0
    test_running = False

    col_start, col_stop, col_exit = st.columns(3)

    if col_start.button("Start Test") and not test_running:
        test_running = True
        progress_percent = 0
        progress_bar.progress(0)
        st.write("Test started...")

    if col_stop.button("Stop Test") and test_running:
        test_running = False
        st.session_state.test_complete = True  # test stopped, allow graphs to appear
        st.write("Test stopped.")
        return False

    if col_exit.button("Exit Test"):
        st.session_state.test_complete = False  # test exited, don't allow graphs to appear
        return False

    if test_running:
        if progress_percent < 100:
            progress_percent += 1
            progress_bar.progress(progress_percent)
            time.sleep(0.1)  # Simulate test progress
        else:
            test_running = False
            st.session_state.test_complete = True  # test complete, allow graphs to appear
            st.write("Test complete.")
            return False

    return True

# Streamlit Application
st.set_page_config(page_title="ULI", page_icon="👂")  # Set page title and icon

st.markdown(
    """
    <style>
    .uli-title {
        font-size: 48px !important;
        font-weight: 900; /* Extra bold */
        color: #007bff; /* A nice blue color */
        text-align: center;
        margin-bottom: 5px; /* Add a little space below the title */
    }
    .uli-subtitle {
        font-size: 24px;
        text-align: center;
        color: #6c757d; /* A subtle gray */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<p class="uli-title">AI-based Universal Language Independent Test</p>', unsafe_allow_html=True)

st.markdown("---")  # Add a horizontal line for visual separation

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
                individual_snr = np.random.normal(mean, std)  # Simulate individual SNR
                p_value = stats.norm.cdf(individual_snr, mean, std)  # generate p value

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
                # simulated SNR graph
                mean = -8
                std = 1.6
                snr_range = (-15, 5)
                x, pdf = generate_norm_pdf(mean, std, snr_range)
                individual_snr = np.random.normal(mean, std)
                fig, ax = plt.subplots(1, 2, figsize=(10, 4))
                ax[0].plot(x, pdf, label="Normative Data")
                ax[0].axvline(individual_snr, color='red', linestyle='--', label=f"Individual SNR: {individual_snr:.2f}")
                ax[0].set_xlabel("SNR (dB)")
                ax[0].set_ylabel("Probability Density")
                ax[0].legend()
                # simulated error proportion bar chart
                vowels = ["a", "o", "i"]
                consonants = ["Low", "Mid", "High"]
                error_proportion = np.random.randint(0, 101, size=6)
                labels = vowels + consonants
                ax[1].bar(labels, error_proportion)
                ax[1].set_ylabel("Error Proportion (%)")
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
                labels = vowels + consonants
                x = np.arange(len(labels))
                width = 0.35
                fig, ax = plt.subplots()
                rects1 = ax.bar(x - width / 2, pre_fitting, width, label="Pre-Fitting")
                rects2 = ax.bar(x + width / 2, post_fitting, width, label="Post-Fitting")
                ax.set_ylabel("Percentage Correct (%)")
                ax.set_xticks(x, labels)
                ax.legend()
                st.
