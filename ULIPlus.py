# ULIPlus.py
# Author : Jorge Mejia
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# Set page title and icon
st.set_page_config(page_title="Hearing Assessment Suite", page_icon="👂")

# --- Ensure Session State is Initialized ---
if "choice" not in st.session_state:
    st.session_state.choice = "Screener"  # Default selection

# --- Helper Functions ---
def generate_norm_pdf(mean, std, snr_range):
    """Generates a normal distribution PDF for SNR comparison."""
    x = np.linspace(snr_range[0], snr_range[1], 100)
    pdf = stats.norm.pdf(x, mean, std)
    return x, pdf

# --- UI Layout ---
st.markdown(
    """
    <style>
    .uli-title {
        font-size: 60px;
        font-weight: 900;
        color: #007bff;
        text-align: center;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<p class="uli-title"><b>Hearing Assessment Suite</b></p>', unsafe_allow_html=True)
st.markdown("---")

# --- Persist Menu Selection ---
col1, col2, col3, col4 = st.columns(4)

if col1.button("👂 Screener"):
    st.session_state.choice = "Screener"
if col2.button("🩺 Diagnosis"):
    st.session_state.choice = "Diagnosis"
if col3.button("⚙️ Fitting"):
    st.session_state.choice = "Fitting"
if col4.button("📈 Monitoring"):
    st.session_state.choice = "Monitoring"

choice = st.session_state.choice  # Persist menu selection across reruns

# --- Main Section Based on Choice ---
if choice == "Screener":
    st.header("Screener")

    # Pre-Test Inputs
    age = st.number_input("Age", min_value=0, max_value=120, value=30)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    social_status = st.text_input("Social Status")
    hearing_frequency = st.selectbox("Frequency of Hearing Problems", ["Never", "Rarely", "Occasionally", "Frequently"])

    if st.button("Run Screener"):
        st.write("### Test Results:")
        mean, std, snr_range = -8, 1.6, (-15, 5)
        x, pdf = generate_norm_pdf(mean, std, snr_range)
        individual_snr = np.random.normal(mean, std)
        p_value = stats.norm.cdf(individual_snr, mean, std)

        fig, ax = plt.subplots()
        ax.plot(x, pdf, label="Normative Data")
        ax.axvline(individual_snr, color='red', linestyle='--', label=f"Your SNR: {individual_snr:.2f} dB")
        ax.set_xlabel("SNR (dB)")
        ax.set_ylabel("Probability Density")
        ax.legend()
        st.pyplot(fig)
        st.write(f"P-value: {p_value:.4f}")

elif choice == "Diagnosis":
    st.header("Diagnosis")

    # Pre-Test Inputs
    age = st.number_input("Age", min_value=0, max_value=120, value=30)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    social_status = st.text_input("Social Status")
    hearing_frequency = st.selectbox("Frequency of Hearing Problems", ["Never", "Rarely", "Occasionally", "Frequently"])

    if st.button("Run Diagnosis"):
        st.write("### Diagnosis Results:")
        mean, std, snr_range = -8, 1.6, (-15, 5)
        x, pdf = generate_norm_pdf(mean, std, snr_range)
        individual_snr = np.random.normal(mean, std)

        fig, axs = plt.subplots(1, 2, figsize=(12, 4))

        axs[0].plot(x, pdf, label="Normative Data")
        axs[0].axvline(individual_snr, color='red', linestyle='--', label=f"Your SNR: {individual_snr:.2f}")
        axs[0].set_xlabel("SNR (dB)")
        axs[0].set_ylabel("Probability Density")
        axs[0].legend()

        vowels, consonants = ["a", "o", "i"], ["Low", "Mid", "High"]
        error_proportion = np.random.randint(0, 101, 6)
        axs[1].bar(vowels + consonants, error_proportion)
        axs[1].set_ylabel("Error Proportion (%)")

        st.pyplot(fig)

elif choice == "Fitting":
    st.header("Fitting")

    diagnosis_snr = st.number_input("Diagnosis SNR", value=-8.0)

    if st.button("Run Fitting"):
        st.write("### Fitting Results:")
        vowels, consonants = ["a", "o", "i"], ["Low", "Mid", "High"]
        pre_fitting = np.random.randint(50, 101, 6)
        post_fitting = np.random.randint(50, 101, 6)

        fig, ax = plt.subplots()
        ax.bar(vowels + consonants, pre_fitting, alpha=0.6, label="Pre-Fitting")
        ax.bar(vowels + consonants, post_fitting, alpha=0.6, label="Post-Fitting", bottom=pre_fitting)
        ax.set_ylabel("Percentage Correct (%)")
        ax.legend()
        st.pyplot(fig)

elif choice == "Monitoring":
    st.header("Monitoring")

    if st.button("Generate Monitoring Data"):
        st.write("### Monitoring Results:")
        snr_trend = np.random.normal(-8, 1.6, 10)
        fig, ax = plt.subplots()
        ax.plot(range(1, 11), snr_trend, marker='o', linestyle='-', label="SNR Trend")
        ax.set_xlabel("Time (Sessions)")
        ax.set_ylabel("SNR (dB)")
        ax.legend()
        st.pyplot(fig)
