import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# Function to generate normal distribution data
def generate_norm_pdf(mean, std, snr_range):
    x = np.linspace(snr_range[0], snr_range[1], 100)
    pdf = stats.norm.pdf(x, mean, std)
    return x, pdf

# Streamlit Application
st.title("Hearing Assessment Suite")

menu = ["Screener", "Diagnosis", "Fitting", "Monitoring"]
choice = st.sidebar.selectbox("Select Assessment", menu)

if choice == "Screener":
    st.header("Screener")
    age = st.number_input("Age", min_value=0, max_value=120, value=30)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    social_status = st.text_input("Social Status")
    hearing_frequency = st.selectbox("Frequency of Hearing Problems", ["Never", "Rarely", "Occasionally", "Frequently"])

    if st.button("Run Screener"):
        # Simulate SNR data
        mean = -8
        std = 1.6
        snr_range = (-15, 5)
        x, pdf = generate_norm_pdf(mean, std, snr_range)
        individual_snr = np.random.normal(mean, std)  # Simulate individual SNR
        p_value = stats.norm.cdf(individual_snr, mean, std) #generate p value
        
        # Plotting
        fig, ax = plt.subplots()
        ax.plot(x, pdf, label="Normative Data")
        ax.axvline(individual_snr, color='red', linestyle='--', label=f"Individual SNR: {individual_snr:.2f}")
        ax.set_xlabel("SNR (dB)")
        ax.set_ylabel("Probability Density")
        ax.legend()
        st.pyplot(fig)
        st.write(f"P-value: {p_value:.4f}")

elif choice == "Diagnosis":
    st.header("Diagnosis")
    age = st.number_input("Age", min_value=0, max_value=120, value=30)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    social_status = st.text_input("Social Status")
    hearing_frequency = st.selectbox("Frequency of Hearing Problems", ["Never", "Rarely", "Occasionally", "Frequently"])

    if st.button("Run Diagnosis"):
        #simulated SNR graph
        mean = -8
        std = 1.6
        snr_range = (-15, 5)
        x, pdf = generate_norm_pdf(mean, std, snr_range)
        individual_snr = np.random.normal(mean, std)
        fig, ax = plt.subplots(1, 2, figsize = (10,4))
        ax[0].plot(x, pdf, label="Normative Data")
        ax[0].axvline(individual_snr, color='red', linestyle='--', label=f"Individual SNR: {individual_snr:.2f}")
        ax[0].set_xlabel("SNR (dB)")
        ax[0].set_ylabel("Probability Density")
        ax[0].legend()
        #simulated error proportion bar chart
        vowels = ["a", "o", "i"]
        consonants = ["Low", "Mid", "High"]
        error_proportion = np.random.randint(0, 101, size=6)
        labels = vowels + consonants
        ax[1].bar(labels, error_proportion)
        ax[1].set_ylabel("Error Proportion (%)")
        st.pyplot(fig)

elif choice == "Fitting":
    st.header("Fitting")
    diagnosis_snr = st.number_input("Diagnosis SNR", value=-8.0)
    if st.button("Run Fitting"):
        vowels = ["a", "o", "i"]
        consonants = ["Low", "Mid", "High"]
        pre_fitting = np.random.randint(0, 101, size=6)
        post_fitting = np.random.randint(0, 101, size=6)
        labels = vowels + consonants
        x = np.arange(len(labels))
        width = 0.35
        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/2, pre_fitting, width, label="Pre-Fitting")
        rects2 = ax.bar(x + width/2, post_fitting, width, label="Post-Fitting")
        ax.set_ylabel("Percentage Correct (%)")
        ax.set_xticks(x, labels)
        ax.legend()
        st.pyplot(fig)

elif choice == "Monitoring":
    st.header("Monitoring")
    monitoring_snr = st.number_input("Screener/Diagnosis SNR", value=-8.0)
    if st.button("Run Monitoring"):
        # Simulate SNR trend data
        time_points = np.arange(1, 11)  # 10 time points
        snr_trends = monitoring_snr + np.random.normal(0, 1, size=10).cumsum()  # Simulate trend with noise

        # Plotting
        fig, ax = plt.subplots()
        ax.plot(time_points, snr_trends, marker='o')
        ax.set_xlabel("Time Point")
        ax.set_ylabel("SNR (dB)")
        ax.set_title("SNR Trend Over Time")
        st.pyplot(fig)
