import streamlit as st

import services.logging_service as logging_service
import services.medication_service as medication_service
from utils.date_utils import today


def render_home() -> None:
    st.title("Crohn Clinical Log")
    st.write(f"**Date:** {today().strftime('%A, %d %B %Y')}")

    # --- Medication block ---
    medications = medication_service.get_medications_for_today()
    if medications:
        st.subheader("Medications")
        for med in medications:
            taken = medication_service.is_medication_taken_today(med.id)
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{med.name}** ({med.type})")
            with col2:
                if st.button("Mark as taken", key=f"med_{med.id}", disabled=taken):
                    medication_service.mark_medication_taken(med.id)
                    st.rerun()

    # --- Bowel logging block ---
    st.subheader("Bowel Log")
    if "bowel_type" not in st.session_state:
        st.session_state["bowel_type"] = None

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🟢 Normal", use_container_width=True):
            st.session_state["bowel_type"] = "normal"
    with col2:
        if st.button("🔴 Diarrhea", use_container_width=True):
            st.session_state["bowel_type"] = "diarrhea"
    with col3:
        if st.button("⚠️ Urgency", use_container_width=True):
            st.session_state["bowel_type"] = "urgency"

    if st.session_state["bowel_type"]:
        st.write(f"Type selected: **{st.session_state['bowel_type']}**")
        st.write("Pain?")
        col_yes, col_no = st.columns(2)
        with col_yes:
            if st.button("Yes", key="pain_yes", use_container_width=True):
                logging_service.log_bowel(st.session_state["bowel_type"], True)
                st.session_state["bowel_type"] = None
                st.success("Saved.")
                st.rerun()
        with col_no:
            if st.button("No", key="pain_no", use_container_width=True):
                logging_service.log_bowel(st.session_state["bowel_type"], False)
                st.session_state["bowel_type"] = None
                st.success("Saved.")
                st.rerun()

    # --- Fatigue block ---
    st.subheader("Fatigue")
    current_fatigue = logging_service.get_today_fatigue()
    if current_fatigue is not None:
        st.write(f"Fatigue today: **{current_fatigue}/5**")
    else:
        cols = st.columns(5)
        for i, col in enumerate(cols, start=1):
            with col:
                if st.button(str(i), key=f"fatigue_{i}", use_container_width=True):
                    logging_service.log_fatigue(i)
                    st.rerun()

    # --- Navigation ---
    st.divider()
    if st.button("View consultation summary", use_container_width=True):
        st.session_state["page"] = "consultation"
        st.rerun()
