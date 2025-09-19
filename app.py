import streamlit as st

from apps.sidebars import *  # noqa
from apps.tabs import *  # noqa
from streamtabs.core import STSidebar, STTab

st.set_page_config(page_title="Student Performance Evaluation", layout="wide")

st.title("StreamTabs Example App")

STSidebar.run_sidebars()
STTab.run_tabs(debug=True)
