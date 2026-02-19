import streamlit as st

import services.summary_service as summary_service


def render_consultation() -> None:
    st.title("Consultation Summary")

    period = st.selectbox("Period", options=[30, 90], format_func=lambda x: f"{x} days")

    bowel = summary_service.get_bowel_summary(period)
    fatigue = summary_service.get_fatigue_summary(period)
    medication = summary_service.get_medication_adherence(period)

    st.subheader("Bowel")
    st.metric("Movements per day (avg)", bowel["movements_per_day"])
    st.metric("Days with diarrhea", bowel["days_with_diarrhea"])

    st.subheader("Medication")
    adherence = medication["adherence_percentage"]
    st.metric(
        "Adherence",
        f"{adherence}%" if adherence is not None else "No data",
    )

    st.subheader("Fatigue")
    avg_fatigue = fatigue["average_fatigue"]
    st.metric(
        "Average fatigue",
        f"{avg_fatigue}/5" if avg_fatigue is not None else "No data",
    )

    st.divider()
    csv_data = summary_service.export_csv(period)
    st.download_button(
        label="Export CSV",
        data=csv_data,
        file_name=f"crohn_summary_{period}days.csv",
        mime="text/csv",
        use_container_width=True,
    )

    if st.button("← Back", use_container_width=True):
        st.session_state["page"] = "home"
        st.rerun()
