import sys
import os

# Ensure crohn_app is on the path so all imports resolve correctly
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st

from database.db import init_db
from ui.home import render_home
from ui.consultation import render_consultation

init_db()

if "page" not in st.session_state:
    st.session_state["page"] = "home"

if st.session_state["page"] == "home":
    render_home()
else:
    render_consultation()
