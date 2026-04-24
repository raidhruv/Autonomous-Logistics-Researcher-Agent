import streamlit as st
from agents.orchestrator import Orchestrator
from state_manager import state_manager
import threading

# SESSION STATE INIT
if "status" not in st.session_state:
    st.session_state.status = "Idle"
def update_status(msg):
    st.session_state.status = msg

if "logs" not in st.session_state:
    st.session_state.logs = []

if "report" not in st.session_state:
    st.session_state.report = None

if "evaluation" not in st.session_state:
    st.session_state.evaluation = None

if "citations" not in st.session_state:
    st.session_state.citations = []

def sync_state():
    backend_state = state_manager.get()
    st.session_state.status = backend_state

# STATE HELPERS

def update_status(status, message=""):
    st.session_state.status = status
    st.session_state.status_message = message

def log_event(stage, message):
    entry = f"[{stage}] {message}"
    st.session_state.logs.append(entry)

# PAGE CONFIG
st.set_page_config(
    page_title="Autonomous Logistics Research Agent",
    page_icon="🤖",
    layout="wide"
)

# STYLES 
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}

.card {
    background: #1c1f26;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.metric-card {
    background: #1c1f26;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# TITLE
st.title("Autonomous Logistics Research Agent")
st.caption("AI-powered research system")

import os

# ---------------------------
# SIMPLE FILE UPLOAD
# ---------------------------
st.markdown("## 📄 Upload PDF")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    os.makedirs("uploads", exist_ok=True)

    file_path = os.path.join("uploads", uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"File uploaded successfully: {uploaded_file.name}")

# INPUT 
query = st.text_input("🔍 Enter your research query")

run_button = st.button("Run Research")

# SIDEBAR: SYSTEM STATUS
with st.sidebar:
    st.markdown("## System Status")

    status = st.session_state.get("status", "Idle")
    message = st.session_state.get("status_message", "")

    status_map = {
    "searching": "Searching...",
    "filtering": "Filtering...",
    "scraping": "Scraping...",
    "scraping_url": "Scraping webpage...",
    "processing_content": "Processing content...",
    "cleaning": "Cleaning...",
    "chunking": "Chunking...",
    "storing": "Saving...",
    "done": "Completed",
    "idle": "Idle"
    }

    st.info(status_map.get(status, status))

    if message:
        st.caption(message)

    st.markdown("---")

    st.markdown("## Execution Trace")

    logs = st.session_state.get("logs", [])

    if logs:
        for log in logs[-8:]:
            st.text(log)
    else:
        st.caption("No activity yet")

# RUN LOGIC
if run_button:
    # RESET STATE FOR NEW RUN
    st.session_state.logs = []
    st.session_state.status = "searching"
    st.session_state.status_message = ""
    if not query:
        st.warning("Please enter a query")
    else:
        orchestrator = Orchestrator()

        update_status("Planning", "Expanding query...")
        log_event("Planning", "Expanding queries")

        orchestrator = Orchestrator()

        with st.spinner("Running research pipeline..."):
            sync_state()
            update_status("Planning", "Expanding query...")
            log_event("Planning", "Expanding query")

            update_status("Researching", "Searching & scraping...")
            log_event("Researching", "Fetching sources")

            sync_state()
            result = orchestrator.run(query)
            sync_state()

            st.session_state.report = result.get("report")
            st.session_state.evaluation = result.get("evaluation")
            st.session_state.citations = result.get("citations", [])

            log_event("Generating", "Writing report")

            update_status("Completed", "Done")
            sync_state()
            log_event("Completed", "Pipeline finished")

            report = st.session_state.report

            st.success("Research completed")

        
        # FORMAT REPORT
    
        report = st.session_state.get("report", "")

        formatted_report = report.replace("\n", "<br>")

        formatted_report = formatted_report.replace(
            "[", "<span style='color:#4CAF50'>["
        ).replace(
            "]", "]</span>"
        )

        # LAYOUT
        col1, col2 = st.columns([3, 1])

        # REPORT
        with col1:
            st.markdown("## Research Report")

            st.markdown(f"""
            <div class="card">
            {formatted_report}
            </div>
            """, unsafe_allow_html=True)

        
        # SIDE PANEL
        with col2:

            # METRICS
            st.markdown("## 📊 Evaluation")

            evaluation = st.session_state.get("evaluation")

            if evaluation:
                col1, col2 = st.columns(2)
                col3, col4 = st.columns(2)

                col1.metric("Quality", f"{evaluation.get('quality_score', 0):.2f}")
                col2.metric("Relevance", f"{evaluation.get('retrieval_relevance', 0):.2f}")
                col3.metric("Coverage", f"{evaluation.get('evidence_coverage', 0):.2f}")
                col4.metric("Citation Density", f"{evaluation.get('citation_density', 0):.2f}")

                st.metric("Hallucination Risk", f"{evaluation.get('hallucination_risk', 0):.2f}")

                issues = evaluation.get("issues", [])
                if issues:
                    st.warning("\n".join(issues))
            else:
                st.info("No evaluation available")


           