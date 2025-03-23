# ULIPlus.py
# Author : Jorge Mejia
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import json
from datetime import datetime
from adaptivetest import adaptive_test

# Set browser tab title and icon
st.set_page_config(
    page_title="Hearing Assessment Suite",
    page_icon="👂",
    layout="centered"
)

# --- Ensure Session State is Initialized ---
if "choice" not in st.session_state:
    st.session_state.choice = "Profile"  # Default selection is now 'Profile'

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
        font-size: 160px;
        font-weight: 172px;
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

# --- Navigation Buttons ---
col0, col1, col2, col3, col4, col5 = st.columns(6)

if col0.button("Profile"):
    st.session_state.choice = "Profile"
if col1.button("Screener"):
    st.session_state.choice = "Screener"
if col2.button("Diagnosis"):
    st.session_state.choice = "Diagnosis"
if col3.button("Fitting"):
    st.session_state.choice = "Fitting"
if col4.button("Monitoring"):
    st.session_state.choice = "Monitoring"
if col5.button("Summary"):
    st.session_state.choice = "Summary"


choice = st.session_state.choice  # Persist menu selection across reruns

# --- Main Section Based on Choice ---
if choice == "Profile":
    # Fancy stacked icon header
    st.markdown("""
        <div style='text-align: center; margin-top: 1em; margin-bottom: 1em;'>
            <div style='font-size: 60px;'>👤</div>
            <h2 style='margin: 0;'>Profile</h2>
        </div>
    """, unsafe_allow_html=True)

    # --- Basic Patient Information ---
    with st.expander("🗞 Basic Information", expanded=True):
        name = st.text_input("Full Name", key="profile_name")
        age = st.number_input("Age", min_value=0, max_value=120, value=30, key="profile_age")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="profile_gender")
        primary_language = st.text_input("Primary Language Spoken", key="profile_language")

    # --- Medical & Hearing History ---
    with st.expander("🚒 Medical & Hearing History"):
        past_hearing_test = st.selectbox("Have you had a hearing test before?", ["Yes", "No"], key="profile_past_test")
        freqs = ["250 Hz", "500 Hz", "1000 Hz", "2000 Hz", "4000 Hz", "8000 Hz"]
        air_condition = {}
        bone_condition = {}

        if past_hearing_test == "Yes":
            air_condition = {"Left": {}, "Right": {}}
            bone_condition = {"Left": {}, "Right": {}}

            st.markdown("**Enter Previous Hearing Test Results (dB HL) for Each Ear:**")

            st.markdown("*Air Conduction*")
            st.markdown("**Left Ear**")
            ac_left_cols = st.columns(len(freqs))
            for i, freq in enumerate(freqs):
                with ac_left_cols[i]:
                    air_condition["Left"][freq] = st.number_input(f"L AC {freq}", value=0, key=f"ac_L_{freq}")

            st.markdown("**Right Ear**")
            ac_right_cols = st.columns(len(freqs))
            for i, freq in enumerate(freqs):
                with ac_right_cols[i]:
                    air_condition["Right"][freq] = st.number_input(f"R AC {freq}", value=0, key=f"ac_R_{freq}")

            st.markdown("*Bone Conduction*")
            st.markdown("**Left Ear**")
            bc_left_cols = st.columns(len(freqs))
            for i, freq in enumerate(freqs):
                with bc_left_cols[i]:
                    bone_condition["Left"][freq] = st.number_input(f"L BC {freq}", value=0, key=f"bc_L_{freq}")

            st.markdown("**Right Ear**")
            bc_right_cols = st.columns(len(freqs))
            for i, freq in enumerate(freqs):
                with bc_right_cols[i]:
                    bone_condition["Right"][freq] = st.number_input(f"R BC {freq}", value=0, key=f"bc_R_{freq}")

    with st.expander("📉 Hearing Difficulties & Impact"):
        hearing_changes = st.selectbox("Have you experienced sudden or rapid hearing changes?", ["Yes", "No"], key="profile_changes")
        ear_conditions = st.text_area("Any history of ear infections, surgeries, or trauma?", key="profile_ear_conditions")
        family_history = st.selectbox("Do you have a family history of hearing loss?", ["Yes", "No", "Not sure"], key="profile_family_history")
        tinnitus = st.selectbox("Do you experience ringing in your ears (tinnitus)?", ["Yes", "No", "Sometimes"], key="profile_tinnitus")
        balance_issues = st.selectbox("Do you have dizziness or balance issues?", ["Yes", "No", "Sometimes"], key="profile_balance")
        medications = st.text_area("List any current medications (esp. ototoxic ones):", key="profile_medications")

    with st.expander("🎤 Hearing Symptoms and Communication Challenges"):
        worse_ear = st.selectbox("Which ear do you feel is worse?", ["Left", "Right", "Both", "Not sure"], key="profile_worse_ear")
        background_noise = st.selectbox("Do you struggle to hear in noisy settings?", ["Never", "Sometimes", "Often", "Always"], key="profile_noise_struggle")
        phone_difficulty = st.selectbox("Do you have trouble hearing on the phone?", ["Yes", "No"], key="profile_phone")
        volume_increase = st.selectbox("Do you turn up the volume on devices more than others?", ["Yes", "No"], key="profile_volume")
        mumbling_complaints = st.selectbox("Do others seem to mumble?", ["Yes", "No"], key="profile_mumble")
        hearing_duration = st.text_input("How long have you noticed hearing difficulties?", key="profile_duration")

    with st.expander("📣 Hearing Aid Use and Daily Impact"):
        hearing_aid_use = st.selectbox("Do you currently use hearing aids or assistive devices?", ["Yes", "No"], key="profile_ha_use")
        hearing_aid_experience = st.text_area("If yes, how are they working for you? If no, have you tried them before?", key="profile_ha_experience")
        daily_impact = st.text_area("How is your hearing affecting your daily life (work, social, family)?", key="profile_impact")
        patient_goals = st.text_area("What would you like to achieve with better hearing?", key="profile_goals")

    with st.expander("🔋 Wellbeing & Energy Check-In"):
        sleep_quality = st.selectbox("How would you rate your sleep quality this week?", ["Very Poor", "Poor", "Fair", "Good", "Excellent"], key="profile_sleep_quality")
        sleep_hours = st.radio("Avg. hours of sleep per night?", ["<4", "4–6", "6–8", "8+"], key="profile_sleep_hours")
        wakes_rested = st.selectbox("Do you wake up feeling rested?", ["Yes", "No", "Sometimes"], key="profile_wake_rested")
        fatigue_level = st.slider("How fatigued do you feel at the end of a typical day?", 0, 10, 5, key="profile_fatigue_level")
        energy_dip = st.selectbox("When do you feel the lowest energy?", ["Morning", "Afternoon", "Evening", "It varies"], key="profile_energy_dip")
        fatigue_impact = st.selectbox("Does fatigue affect your daily tasks?", ["Never", "Rarely", "Sometimes", "Often", "Always"], key="profile_fatigue_impact")
        stress_triggers = st.multiselect("⚠️ Which situations are most challenging for you?", ["Social interactions", "Workload pressure", "Noise", "Unpredictability", "Deadlines", "Group settings", "Other"], key="profile_stress_triggers")
        social_fatigue = st.selectbox("Do social interactions leave you emotionally drained?", ["Never", "Rarely", "Sometimes", "Often", "Always"], key="profile_social_fatigue")
        situation_avoidance = st.selectbox("Do you avoid situations due to discomfort/exhaustion?", ["Yes", "No", "Sometimes"], key="profile_situation_avoidance")

    # --- Save Button ---
    if st.button("💾 Save Profile to logevent.json"):
        profile_data = {
            "timestamp": datetime.now().isoformat(),
            "name": name,
            "age": age,
            "gender": gender,
            "primary_language": primary_language,
            "past_hearing_test": past_hearing_test,
            "air_condition": air_condition,
            "bone_condition": bone_condition,
            "hearing_changes": hearing_changes,
            "ear_conditions": ear_conditions,
            "family_history": family_history,
            "tinnitus": tinnitus,
            "balance_issues": balance_issues,
            "medications": medications,
            "worse_ear": worse_ear,
            "background_noise": background_noise,
            "phone_difficulty": phone_difficulty,
            "volume_increase": volume_increase,
            "mumbling_complaints": mumbling_complaints,
            "hearing_duration": hearing_duration,
            "hearing_aid_use": hearing_aid_use,
            "hearing_aid_experience": hearing_aid_experience,
            "daily_impact": daily_impact,
            "patient_goals": patient_goals,
            "sleep_quality": sleep_quality,
            "sleep_hours": sleep_hours,
            "wakes_rested": wakes_rested,
            "fatigue_level": fatigue_level,
            "energy_dip": energy_dip,
            "fatigue_impact": fatigue_impact,
            "stress_triggers": stress_triggers,
            "social_fatigue": social_fatigue,
            "situation_avoidance": situation_avoidance
        }

        with open("logevent.json", "w") as f:
            json.dump(profile_data, f, indent=2)

        st.success("Profile data saved successfully!")

elif choice == "Screener":
    # Fancy stacked icon header
    st.markdown("""
        <div style='text-align: center; margin-top: 1em; margin-bottom: 1em;'>
            <div style='font-size: 60px;'>👂</div>
            <h2 style='margin: 0;'>Screener</h2>
        </div>
    """, unsafe_allow_html=True)

    if "run_screener_triggered" not in st.session_state:
        st.session_state.run_screener_triggered = False

    with st.expander("📝 Test Instructions", expanded=not st.session_state.run_screener_triggered):
        st.markdown("""
        You will hear **VCV** words (like _\"ala\"_, _\"omo\"_, _\"iki\"_).
        Choose the word you hear by pressing the correct option below.
        Try your best even if uncertain!
        """)

    if not st.session_state.run_screener_triggered:
        st.subheader("🧪 Setup Parameters")
        client_name = st.session_state.get("profile_name", "").strip()
        if not client_name:
            client_name = st.text_input("Enter Client Name or ID", key="client_name_manual")

        threshold_val = st.number_input("Initial Threshold Value", value=-8.0, step=0.1)
        convergence_criteria = st.number_input("Convergence Criteria", value=1.0, step=0.1)

        if st.button("Run Screener"):
            st.session_state.run_screener_triggered = True
            st.rerun()
    else:
        # 🎯 Call the test UI
        client_name = st.session_state.get("profile_name") or st.session_state.get("client_name_manual", "")
        threshold_val = -8.0
        convergence_criteria = 1.0
        result_word = adaptive_test(threshold_val, convergence_criteria, client_name)

        if result_word:
            st.success(f"You selected: {result_word}")

elif choice == "Diagnosis":
    # Fancy stacked icon header
    st.markdown("""
        <div style='text-align: center; margin-top: 1em; margin-bottom: 1em;'>
            <div style='font-size: 60px;'>🩺</div>
            <h2 style='margin: 0;'>Diagnosis</h2>
        </div>
    """, unsafe_allow_html=True)
    
    if "diagnosis_count" not in st.session_state:
        st.session_state.diagnosis_count = 0
    if "diagnosis_results" not in st.session_state:
        st.session_state.diagnosis_results = []

    # --- Instructions ---
    st.markdown("### 📝 Test Instructions")
    st.markdown("""
    In this unaided test, you'll hear **VCV (vowel-consonant-vowel)** words in background noise.  
    Listen carefully and select the option that sounds most like what you heard.
    This helps us understand your natural hearing ability in noisy environments.
    """)

    # --- Run Test ---
    if st.button("▶️ Run Diagnosis Test"):
        mean, std, snr_range = -8, 1.6, (-15, 5)
        x, pdf = generate_norm_pdf(mean, std, snr_range)
        individual_snr = np.random.normal(mean, std)
        error_proportion = np.random.randint(0, 101, 6)

        # Save to session state
        st.session_state.diagnosis_count += 1
        st.session_state.diagnosis_results.append({
            "snr": round(individual_snr, 2),
            "error_proportion": error_proportion.tolist(),
            "timestamp": datetime.now().isoformat()
        })

        # Plot Results
        st.markdown(f"#### Your SNR: **{individual_snr:.2f} dB**")
        fig, axs = plt.subplots(1, 2, figsize=(12, 4))

        axs[0].plot(x, pdf, label="Normative Data")
        axs[0].axvline(individual_snr, color='red', linestyle='--', label=f"Your SNR")
        axs[0].set_xlabel("SNR (dB)")
        axs[0].set_ylabel("Probability Density")
        axs[0].legend()

        vowels, consonants = ["a", "o", "i"], ["Low", "Mid", "High"]
        axs[1].bar(vowels + consonants, error_proportion)
        axs[1].set_ylabel("Error Proportion (%)")

        st.pyplot(fig)

    st.markdown(f"🧾 Total diagnosis sessions: **{st.session_state.diagnosis_count}**")

    # --- Subjective Feedback ---
    with st.expander("🧠 Subjective Experience"):
        perceived_difficulty = st.slider("How difficult was the listening task?", 0, 10, 5)
        noise_level = st.selectbox("Was background noise distracting?", ["Not at all", "A little", "Moderately", "Very much"])
        emotional_state = st.selectbox("How did you feel during the task?", ["Calm", "Focused", "Frustrated", "Anxious", "Confident"])
        time_of_day = st.selectbox("What time of day was the test done?", ["Morning", "Afternoon", "Evening"])
        notes = st.text_area("Any additional notes or context (e.g., noisy room, tired, etc.)")

    # --- Save Diagnosis Data ---
    if st.button("💾 Save Diagnosis Data"):
        last_result = st.session_state.diagnosis_results[-1] if st.session_state.diagnosis_results else {}
        diagnosis_log = {
            "timestamp": datetime.now().isoformat(),
            "snr": last_result.get("snr"),
            "error_proportion": last_result.get("error_proportion"),
            "subjective": {
                "perceived_difficulty": perceived_difficulty,
                "noise_level": noise_level,
                "emotional_state": emotional_state,
                "time_of_day": time_of_day,
                "notes": notes
            }
        }

        with open("diagnosis_log.json", "a") as f:
            f.write(json.dumps(diagnosis_log) + "\n")
        st.success("Diagnosis session saved.")

elif choice == "Fitting":
        # Fancy stacked icon header
    st.markdown("""
        <div style='text-align: center; margin-top: 1em; margin-bottom: 1em;'>
            <div style='font-size: 60px;'>🦻</div>
            <h2 style='margin: 0;'>Fitting</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if "fitting_log" not in st.session_state:
        st.session_state.fitting_log = {
            "unaided_quiet": [],
            "unaided_noise": [],
            "aided_quiet": [],
            "aided_noise": []
        }

    st.markdown("Run VCV tests under different conditions to compare benefit.")

    # --- Condition Selection ---
    col1, col2 = st.columns(2)
    mode = col1.radio("Hearing Mode", ["Unaided", "Aided"], horizontal=True)
    env = col2.radio("Listening Environment", ["Quiet", "Noise"], horizontal=True)

    condition_key = f"{mode.lower()}_{env.lower()}"

    if st.button(f"▶️ Run Test ({mode} in {env})"):
        snr_val = np.random.normal(-8 if env == "Noise" else -2, 1.2)  # Simulated performance
        st.session_state.fitting_log[condition_key].append({
            "timestamp": datetime.now().isoformat(),
            "snr": round(snr_val, 2)
        })
        st.success(f"{mode} in {env} SNR: {snr_val:.2f} dB")

    # --- Summary Counts ---
    st.markdown("### ✅ Session Counts")
    for k, v in st.session_state.fitting_log.items():
        label = k.replace("_", " ").title()
        st.markdown(f"- {label}: **{len(v)} session(s)**")

    # --- Subjective Experience ---
    with st.expander("🧠 Subjective Experience"):
        perceived_benefit = st.slider("How much benefit did you feel in this condition?", 0, 10, 5)
        clarity = st.selectbox("Was speech clearer in this test?", ["Yes", "No", "Unsure"])
        effort = st.slider("Listening effort required?", 0, 10, 5)
        feedback_notes = st.text_area("Additional comments for this condition:")

    # --- Save Session ---
    if st.button("💾 Save Fitting Entry"):
        last_snr = st.session_state.fitting_log[condition_key][-1]["snr"]
        entry = {
            "timestamp": datetime.now().isoformat(),
            "mode": mode,
            "environment": env,
            "snr": last_snr,
            "subjective": {
                "benefit": perceived_benefit,
                "clarity": clarity,
                "effort": effort,
                "notes": feedback_notes
            }
        }

        with open("fitting_log_extended.json", "a") as f:
            f.write(json.dumps(entry) + "\n")
        st.success("Fitting entry saved.")

    # --- Visual Comparison ---
    if any(len(v) > 0 for v in st.session_state.fitting_log.values()):
        st.markdown("### 📊 Condition Comparison")
        fig, ax = plt.subplots()
        for key, results in st.session_state.fitting_log.items():
            if results:
                label = key.replace("_", " ").title()
                snrs = [r["snr"] for r in results]
                ax.plot(snrs, marker='o', label=label)
        ax.set_ylabel("SNR (dB)")
        ax.set_xlabel("Session")
        ax.legend()
        st.pyplot(fig)

elif choice == "Monitoring":
    st.markdown("""
    <div style='text-align: center; margin-top: 1em; margin-bottom: 1em;'>
        <div style='font-size: 60px;'>📈</div>
        <h2 style='margin: 0;'>Monitoring</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("Choose the check-in that best fits your time of day:")

    col1, col2, col3 = st.columns(3)
    checkin_time = None

    if col1.button("🕗 Morning Check-In"):
        checkin_time = "Morning"
    if col2.button("☀️ Day Activity Check-In"):
        checkin_time = "Day"
    if col3.button("🌙 Evening Check-In"):
        checkin_time = "Evening"

    if checkin_time == "Morning":
        with st.expander("🛌 Sleep & Readiness"):
            sleep_quality = st.selectbox("How would you rate your sleep quality last night?", ["Very Poor", "Poor", "Fair", "Good", "Excellent"])
            hours_slept = st.radio("How many hours did you sleep?", ["<4", "4–6", "6–8", "8+"])
            wake_feeling = st.selectbox("How rested do you feel this morning?", ["Exhausted", "Tired", "Okay", "Refreshed"])
            physical_readiness = st.slider("How physically ready do you feel for today?", 0, 10, 5)
            mental_readiness = st.slider("How mentally ready do you feel for today?", 0, 10, 5)

        with st.expander("🧘 Wellbeing & Goals"):
            mood_morning = st.selectbox("What is your current mood?", ["Stressed", "Anxious", "Neutral", "Optimistic", "Excited"])
            planned_goals = st.text_area("What are your listening-related goals today? (e.g., meeting, social lunch, call)", "")
            anticipated_challenges = st.text_area("Any challenging situations expected today?", "")

    elif checkin_time == "Day":
        with st.expander("🎧 Listening Experience"):
            listening_effort = st.slider("How much effort is it taking to follow conversations today?", 0, 10, 5)
            communication_success = st.slider("How successful are you in understanding others?", 0, 10, 6)
            situations = st.multiselect("What listening situations have you encountered so far?", ["One-on-one", "Group", "Online Meeting", "Phone", "Public Transport", "Restaurant", "Other"])
            interest_level = st.slider("How interested were you in the conversations?", 0, 10, 5)

        with st.expander("🎯 Focus & Energy"):
            distractions = st.slider("How distracted have you felt?", 0, 10, 5)
            energy_current = st.slider("Current energy level:", 0, 10, 5)
            challenges_faced = st.text_area("Describe any challenges you've faced so far today:", "")

    elif checkin_time == "Evening":
        with st.expander("😮‍💨 Fatigue & Wind-Down"):
            hearing_fatigue = st.slider("How tired are your ears from today's listening?", 0, 10, 5)
            general_fatigue = st.slider("Overall fatigue level now:", 0, 10, 6)
            emotional_state = st.selectbox("What's your emotional state right now?", ["Drained", "Okay", "Content", "Happy"])
            energy_dip_time = st.selectbox("When did you feel the biggest energy dip today?", ["Morning", "Afternoon", "Evening", "All day"])

        with st.expander("✅ Reflection & Accomplishment"):
            goals_accomplished = st.text_area("Which goals did you accomplish today?", "")
            hearing_success = st.slider("How successful do you feel in managing hearing challenges today?", 0, 10, 5)
            suggestions_to_self = st.text_area("Any ideas to improve tomorrow's experience?", "")

    # Save Check-in Log
    if checkin_time and st.button("💾 Save Check-In"):
        checkin_log = {
            "timestamp": datetime.now().isoformat(),
            "checkin_type": checkin_time
        }

        if checkin_time == "Morning":
            checkin_log.update({
                "sleep_quality": sleep_quality,
                "hours_slept": hours_slept,
                "wake_feeling": wake_feeling,
                "physical_readiness": physical_readiness,
                "mental_readiness": mental_readiness,
                "mood_morning": mood_morning,
                "planned_goals": planned_goals,
                "anticipated_challenges": anticipated_challenges
            })
        elif checkin_time == "Day":
            checkin_log.update({
                "listening_effort": listening_effort,
                "communication_success": communication_success,
                "situations": situations,
                "interest_level": interest_level,
                "distractions": distractions,
                "energy_current": energy_current,
                "challenges_faced": challenges_faced
            })
        elif checkin_time == "Evening":
            checkin_log.update({
                "hearing_fatigue": hearing_fatigue,
                "general_fatigue": general_fatigue,
                "emotional_state": emotional_state,
                "energy_dip_time": energy_dip_time,
                "goals_accomplished": goals_accomplished,
                "hearing_success": hearing_success,
                "suggestions_to_self": suggestions_to_self
            })

        with open("daily_log.json", "a") as f:
            f.write(json.dumps(checkin_log) + "\n")
        st.success(f"{checkin_time} check-in saved successfully!")

elif choice == "Summary":
    st.markdown("""
        <div style='text-align: center; margin-top: 1em; margin-bottom: 1em;'>
            <div style='font-size: 60px;'>📄 </div>
            <h2 style='margin: 0;'> Summary</h2>
        </div>
    """, unsafe_allow_html=True)

    st.info("This section will eventually include AI-generated clinical notes based on user test results and self-reported data.")

    # Placeholder summary
    name = st.session_state.get("profile_name", "Patient")
    age = st.session_state.get("profile_age", "N/A")
    primary_language = st.session_state.get("profile_language", "N/A")
    tinnitus = st.session_state.get("profile_tinnitus", "N/A")
    ha_use = st.session_state.get("profile_ha_use", "N/A")

    diagnosis_results = st.session_state.get("diagnosis_results", [])
    latest_diagnosis = diagnosis_results[-1] if diagnosis_results else {}

    diagnosis_snr = latest_diagnosis.get("snr", "N/A")
    diagnosis_time = latest_diagnosis.get("timestamp", "N/A")

    st.markdown("### 🧾 Summary Preview:")
    st.markdown(f"""
    - **Patient Name**: {name}
    - **Age**: {age}
    - **Primary Language**: {primary_language}
    - **Hearing Aid Use**: {ha_use}
    - **Tinnitus**: {tinnitus}
    - **Most Recent Diagnosis SNR**: {diagnosis_snr} dB (Date: {diagnosis_time})
    _Clinical interpretation and recommendations will appear here once the AI note generator is enabled._
    """)

    st.text_area("🗒️ Additional Clinician Notes", placeholder="Enter any manual comments or observations here...")

    if st.button("💾 Save Summary"):
        notes_data = {
            "timestamp": datetime.now().isoformat(),
            "name": name,
            "age": age,
            "primary_language": primary_language,
            "tinnitus": tinnitus,
            "hearing_aid_use": ha_use,
            "diagnosis_snr": diagnosis_snr,
            "diagnosis_time": diagnosis_time,
            "manual_notes": ""
        }
        with open("clinical_notes.json", "a") as f:
            f.write(json.dumps(notes_data) + "\n")
        st.success("Summary saved for this session.")
