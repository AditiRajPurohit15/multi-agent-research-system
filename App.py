"""
Streamlit UI for the multi-agent research pipeline defined in pipeline.py

Run with:
    streamlit run app.py

Place this file in the SAME folder as pipeline.py, agents.py, and tools.py.
"""

import streamlit as st
from pipeline import run_research_pipeline

# ----------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔎",
    layout="wide",
)

# ----------------------------------------------------------------------
# Session state init
# ----------------------------------------------------------------------
if "state" not in st.session_state:
    st.session_state.state = None
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "error" not in st.session_state:
    st.session_state.error = None

# ----------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------
with st.sidebar:
    st.title("🔎 Research Pipeline")
    st.markdown(
        "This app runs a 4-stage multi-agent pipeline:\n"
        "1. **Search Agent** — finds recent, relevant sources\n"
        "2. **Reader Agent** — scrapes the best source in depth\n"
        "3. **Writer Chain** — drafts a full report\n"
        "4. **Critic Chain** — reviews the report and gives feedback"
    )
    st.divider()

    topic = st.text_input(
        "Research topic",
        value=st.session_state.topic,
        placeholder="e.g. Latest advances in solid-state batteries",
    )

    run_clicked = st.button("🚀 Run pipeline", type="primary", use_container_width=True)

    st.divider()
    if st.session_state.state is not None:
        if st.button("🗑️ Clear results", use_container_width=True):
            st.session_state.state = None
            st.session_state.topic = ""
            st.session_state.error = None
            st.rerun()

# ----------------------------------------------------------------------
# Run pipeline
# ----------------------------------------------------------------------
if run_clicked:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.topic = topic
        st.session_state.error = None
        st.session_state.state = None

        steps = [
            "Searching the web for relevant sources...",
            "Reading and scraping the top source...",
            "Drafting the report...",
            "Running the critic review...",
        ]

        progress_placeholder = st.empty()
        status_placeholder = st.empty()

        try:
            with st.spinner("Running multi-agent research pipeline..."):
                status_placeholder.info(steps[0])
                result = run_research_pipeline(topic)
            st.session_state.state = result
            progress_placeholder.empty()
            status_placeholder.empty()
            st.success("Pipeline finished successfully.")
        except Exception as e:
            progress_placeholder.empty()
            status_placeholder.empty()
            st.session_state.error = str(e)

# ----------------------------------------------------------------------
# Error display
# ----------------------------------------------------------------------
if st.session_state.error:
    st.error(f"Something went wrong while running the pipeline:\n\n{st.session_state.error}")

# ----------------------------------------------------------------------
# Results display
# ----------------------------------------------------------------------
state = st.session_state.state

if state is None and not run_clicked:
    st.title("Multi-Agent Research System")
    st.markdown(
        "Enter a topic in the sidebar and click **Run pipeline** to get started. "
        "Results from each agent will appear here as tabs once the run completes."
    )

if state is not None:
    st.title(f"Research Report: {st.session_state.topic}")

    tab_report, tab_critic, tab_search, tab_scraped = st.tabs(
        ["📄 Final Report", "🧐 Critic Feedback", "🔍 Search Results", "📚 Scraped Content"]
    )

    with tab_report:
        st.markdown(state.get("report", "_No report generated._"))
        st.download_button(
            "⬇️ Download report (.md)",
            data=str(state.get("report", "")),
            file_name=f"{st.session_state.topic.replace(' ', '_')}_report.md",
            mime="text/markdown",
        )

    with tab_critic:
        st.markdown(state.get("feedback", "_No feedback generated._"))

    with tab_search:
        st.text_area(
            "Raw search results",
            value=state.get("search_results", ""),
            height=400,
        )

    with tab_scraped:
        st.text_area(
            "Raw scraped content",
            value=state.get("scraped_content", ""),
            height=400,
        )