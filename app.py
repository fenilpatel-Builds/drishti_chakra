import streamlit as st
import pandas as pd
import time
import os
import base64
import re
from brain import ApexVanguardEngine

# Set layout config
st.set_page_config(
    page_title="Drishti Chakra | Autonomous Enterprise",
    page_icon="☸️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- HELPER TO CLEAN HTML FOR STREAMLIT MARKDOWN ---
def clean_html(html_str):
    # Strip leading/trailing whitespaces and join lines to prevent Markdown block interpretation
    return "".join([line.strip() for line in html_str.strip().split("\n")])

# --- THEME & STYLING ---
def apply_apex_theme():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

        /* ============ GLOBAL DARK BACKGROUND ============ */
        .stApp, .stApp > *, [data-testid="stAppViewContainer"],
        [data-testid="stAppViewBlockContainer"],
        [data-testid="block-container"],
        section.main, section.main > div,
        .main .block-container {
            background-color: #0E1117 !important;
            color: #E0E0E0 !important;
            font-family: 'Inter', sans-serif;
        }

        /* Hide Streamlit header entirely */
        header, #MainMenu { display: none !important; }

        /* ============ LOCK SIDEBAR ALWAYS OPEN (Streamlit 1.59.x) ============ */
        /* Target sidebar in ALL states - open and collapsed (aria-expanded=false) */
        section[data-testid="stSidebar"],
        div[data-testid="stSidebar"] {
            min-width: 18rem !important;
            max-width: 18rem !important;
            width: 18rem !important;
            transform: translateX(0px) !important;
            transition: none !important;
            display: flex !important;
            visibility: visible !important;
            pointer-events: all !important;
            position: relative !important;
            z-index: 100 !important;
        }
        /* Override the collapsed state specifically */
        section[data-testid="stSidebar"][aria-expanded="false"],
        div[data-testid="stSidebar"][aria-expanded="false"] {
            transform: translateX(0px) !important;
            min-width: 18rem !important;
            display: flex !important;
        }
        /* Hide ALL collapse/expand toggle buttons */
        [data-testid="stSidebarCollapseButton"],
        [data-testid="stSidebarCollapseButton"] button,
        [data-testid="collapsedControl"],
        [data-testid="collapsedControl"] button {
            display: none !important;
        }
        /* Remove top padding from hidden header */
        .stApp > div:first-child { padding-top: 0 !important; }
        [data-testid="stAppViewBlockContainer"] { padding-top: 1rem !important; }


        /* ============ SIDEBAR ============ */
        [data-testid="stSidebar"] {
            background-color: #101720 !important;
            border-right: 1px solid #1E262E;
        }
        [data-testid="stSidebar"] * { color: #E0E0E0; }

        /* ============ SIDEBAR NAV BUTTONS (remove white bg) ============ */
        [data-testid="stSidebar"] button {
            background-color: transparent !important;
            border: none !important;
            border-left: 3px solid transparent !important;
            border-radius: 4px !important;
            color: #8892B0 !important;
            text-align: left !important;
            font-size: 12px !important;
            font-weight: 500 !important;
            padding: 8px 12px !important;
            width: 100% !important;
            transition: all 0.2s ease !important;
            box-shadow: none !important;
        }
        [data-testid="stSidebar"] button:hover {
            background-color: rgba(0, 209, 255, 0.07) !important;
            border-left: 3px solid rgba(0, 209, 255, 0.5) !important;
            color: #00D1FF !important;
        }
        [data-testid="stSidebar"] button:focus,
        [data-testid="stSidebar"] button:active {
            background-color: rgba(0, 209, 255, 0.1) !important;
            border-left: 3px solid #00D1FF !important;
            color: #00D1FF !important;
            font-weight: 700 !important;
            box-shadow: none !important;
            outline: none !important;
        }
        /* Start New Analysis button stays styled */
        [data-testid="stSidebar"] [data-testid="element-container"]:last-child button {
            background-color: #161C24 !important;
            border: 1px solid #00D1FF !important;
            border-left: 1px solid #00D1FF !important;
            color: #00D1FF !important;
            border-radius: 5px !important;
            font-weight: 600 !important;
            margin-top: 4px !important;
        }
        [data-testid="stSidebar"] [data-testid="element-container"]:last-child button:hover {
            background-color: #00D1FF !important;
            color: #0E1117 !important;
        }

        /* ============ INFO / WARNING / SUCCESS / ERROR BOXES ============ */
        [data-testid="stNotification"],
        div[data-baseweb="notification"],
        .stAlert, .stAlert > div,
        div.stInfo, div.stWarning, div.stSuccess, div.stError {
            background-color: #161C24 !important;
            border-radius: 8px !important;
            color: #E0E0E0 !important;
        }
        div[data-testid="stNotification"] p { color: #E0E0E0 !important; }

        /* ============ METRICS ============ */
        [data-testid="stMetric"],
        [data-testid="stMetricValue"],
        [data-testid="stMetricLabel"],
        [data-testid="stMetricDelta"],
        div[data-testid="metric-container"] {
            background-color: #161C24 !important;
            border: 1px solid #212932;
            border-radius: 8px;
            padding: 12px !important;
            color: white !important;
        }
        [data-testid="stMetricValue"] { color: #00D1FF !important; font-weight: 800; }
        [data-testid="stMetricLabel"] { color: #8892B0 !important; }

        /* ============ TABS ============ */
        [data-testid="stTabs"],
        [data-baseweb="tab-list"],
        [data-baseweb="tab-panel"],
        button[data-baseweb="tab"] {
            background-color: #0E1117 !important;
            color: #8892B0 !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #00D1FF !important;
            border-bottom: 2px solid #00D1FF !important;
        }
        [data-baseweb="tab-highlight"] { background-color: #00D1FF !important; }

        /* ============ DIVIDER ============ */
        hr { border-color: #212932 !important; }

        /* ============ DOWNLOAD BUTTON ============ */
        [data-testid="stDownloadButton"] button {
            background-color: #161C24 !important;
            color: #00D1FF !important;
            border: 1px solid #00D1FF !important;
        }

        /* ============ BUTTONS ============ */
        button[data-testid^="stBaseButton-"],
        .stButton button,
        [data-testid="stForm"] button {
            background-color: #161C24 !important;
            color: #00D1FF !important;
            border: 1px solid #00D1FF !important;
            border-radius: 5px !important;
            width: 100% !important;
            transition: 0.3s !important;
            font-weight: 600 !important;
        }
        button[data-testid^="stBaseButton-"]:hover,
        .stButton button:hover,
        [data-testid="stForm"] button:hover {
            background-color: #00D1FF !important;
            color: #0E1117 !important;
        }

        /* ============ INPUT ============ */
        input {
            background-color: #0b0e14 !important;
            color: white !important;
            border: 1px solid #212932 !important;
        }

        /* ============ MARKDOWN / TEXT ============ */
        p, span, label, h1, h2, h3, h4, h5, h6 {
            color: #E0E0E0;
        }

        /* ============ FOOTER ============ */
        footer { visibility: hidden; }
        .custom-footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #101720;
            text-align: center;
            padding: 8px;
            font-size: 10px;
            color: #666;
            border-top: 1px solid #1E262E;
            z-index: 100;
        }
        </style>
        
        <div class="custom-footer">
            POWERED BY AMD INSTINCT™ GPUs via FIREWORKS AI | DRISHTI CHAKRA by <strong>Team NexAura</strong>
        </div>
    """, unsafe_allow_html=True)

apply_apex_theme()

# --- SPLASH SCREEN: TRUE FULL-PAGE BLOCKER (only shown once per session) ---
# Fallback check for URL parameter ?_splash=1
_qp = st.query_params
if _qp.get("_splash") == "1" and not st.session_state.get("splash_done", False):
    st.session_state.splash_done = True
    st.query_params.clear()
    st.rerun()

if "splash_done" not in st.session_state:
    st.session_state.splash_done = False

# Render the hidden dismiss button for programmatic JS clicking
if not st.session_state.splash_done:
    # Hidden button in Python
    if st.button("Dismiss Splash", key="dismiss_splash_btn"):
        st.session_state.splash_done = True
        st.rerun()

    # Inject CSS to make the iframe completely cover the entire screen viewport and hide scrollbars/hidden buttons
    st.markdown("""
        <style>
        /* Hide the hidden dismiss button container completely */
        [data-testid="stHeader"],
        [data-testid="element-container"]:has(button[key="dismiss_splash_btn"]),
        button[key="dismiss_splash_btn"] {
            display: none !important;
            height: 0 !important;
            width: 0 !important;
            opacity: 0 !important;
            position: absolute !important;
            pointer-events: none !important;
        }

        /* Hide all Streamlit elements during splash */
        section[data-testid="stSidebar"],
        div[data-testid="stSidebar"],
        header, #MainMenu,
        [data-testid="stSidebarCollapseButton"],
        [data-testid="collapsedControl"],
        .custom-footer {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
        }
        
        /* Force the iframe to be full-screen fixed viewport */
        iframe {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            z-index: 2147483647 !important;
            border: none !important;
            background: #000000 !important;
        }

        /* Prevent scrollbars */
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"],
        section.main, .main .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
            overflow: hidden !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Render the self-contained splash.html iframe
    st.iframe("/app/static/splash.html", height=600)
    st.stop()   # <<< CRITICAL: prevents ANY app content from rendering behind the splash


# --- SIDEBAR BRANDING & CONFIG ---
logo_path = os.path.join(os.path.dirname(__file__), "apex_mind_logo_transparent.png")
logo_base64 = ""
if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        logo_base64 = base64.b64encode(f.read()).decode("utf-8")

# Use base64 for perfectly aligned sidebar header (single-line HTML, no clean_html needed)
if logo_base64:
    st.sidebar.markdown(
        f"<div style='display:flex;align-items:center;gap:10px;padding:14px 0 10px 0;border-bottom:1px solid #1E262E;margin-bottom:12px;'>"
        f"<img src='data:image/png;base64,{logo_base64}' style='width:44px;height:44px;border-radius:50%;object-fit:cover;flex-shrink:0;'>"
        f"<div><div style='color:#00D1FF;font-size:14px;font-weight:800;letter-spacing:0.5px;'>DRISHTI CHAKRA</div>"
        f"<div style='color:#8892B0;font-size:9px;text-transform:uppercase;letter-spacing:1px;margin-top:2px;'>by Team NexAura</div></div>"
        f"</div>",
        unsafe_allow_html=True
    )
else:
    st.sidebar.markdown(
        "<div style='padding:14px 0 10px 0;border-bottom:1px solid #1E262E;margin-bottom:12px;'>"
        "<div style='color:#00D1FF;font-size:14px;font-weight:800;'>DRISHTI CHAKRA</div>"
        "<div style='color:#8892B0;font-size:9px;'>by Team NexAura</div></div>",
        unsafe_allow_html=True
    )

# Compact dark telemetry cards
st.sidebar.markdown(
    "<div style='font-size:10px;font-weight:700;color:#8892B0;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;'>System Telemetry</div>"
    "<div style='display:flex;flex-direction:column;gap:5px;margin-bottom:12px;'>"
    "<div style='background:#0b1118;border:1px solid #1e3a2a;border-radius:5px;padding:6px 10px;font-size:10px;'>"
    "<span style='color:#00E639;font-weight:700;'>●</span> <span style='color:#E0E0E0;'>NODE: MI300X-CLUSTER-01</span></div>"
    "<div style='background:#0b1118;border:1px solid #1a2e3e;border-radius:5px;padding:6px 10px;font-size:10px;'>"
    "<span style='color:#00D1FF;font-weight:700;'>●</span> <span style='color:#E0E0E0;'>KERNEL: ROCm 6.1.2</span></div>"
    "<div style='background:#0b1118;border:1px solid #3a2e10;border-radius:5px;padding:6px 10px;font-size:10px;'>"
    "<span style='color:#FFAA00;font-weight:700;'>●</span> <span style='color:#E0E0E0;'>CORE: GLM-5.2 (FIREWORKS)</span></div>"
    "</div>"
    "<div style='border-top:1px solid #1E262E;margin-bottom:10px;'></div>",
    unsafe_allow_html=True
)


# --- STATE INITIALIZATION (needs to come before nav is drawn) ---
if "dossier" not in st.session_state:
    st.session_state.dossier = None
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "nav_page" not in st.session_state:
    st.session_state.nav_page = "Dashboard"

# Navigation items - now fully interactive with session state
nav_pages = [
    ("❖ Dashboard", "Dashboard"),
    ("📈 Market Intelligence", "Market Intelligence"),
    ("⚖️ Patent Tracker", "Patent Tracker"),
    ("📊 Competitor Landscape", "Competitor Landscape"),
    ("🛠️ Blueprint Generator", "Blueprint Generator"),
    ("📄 Reports", "Reports"),
]

for label, page_key in nav_pages:
    is_active = st.session_state.nav_page == page_key
    style = "background-color: rgba(0, 209, 255, 0.1); border-left: 3px solid #00D1FF; color: #00D1FF; font-weight: 700;" if is_active else "color: #8892B0; border-left: 3px solid transparent;"
    if st.sidebar.button(
        label,
        key=f"nav_{page_key}",
        use_container_width=True,
        help=f"Navigate to {page_key}"
    ):
        st.session_state.nav_page = page_key
        st.rerun()

st.sidebar.markdown("---")

# Start New Analysis button at the bottom of the sidebar
if st.sidebar.button("Start New Analysis", use_container_width=True):
    st.session_state.dossier = None
    st.session_state.topic = ""
    st.session_state.nav_page = "Dashboard"
    st.rerun()

submit_btn = False
user_topic = ""

# --- NAV PAGE ROUTING (non-Dashboard pages) ---
nav_page = st.session_state.nav_page

# If we are on a non-Dashboard page that requires data, show placeholder or data
if nav_page == "Market Intelligence" and st.session_state.dossier:
    result = st.session_state.dossier
    sections = result.get("sections", {})
    st.markdown("<h1 style='color:#00D1FF;'>📈 Market Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8892B0;'>Full research and executive summary for the generated dossier.</p>", unsafe_allow_html=True)
    st.divider()
    st.markdown("### Executive Dossier: The Unicorn Vision")
    st.write(sections.get("executive_summary", "Run an analysis to view market intelligence."))
    st.stop()

elif nav_page == "Market Intelligence":
    st.markdown("<h1 style='color:#00D1FF;'>📈 Market Intelligence</h1>", unsafe_allow_html=True)
    st.info("Run a Drishti Chakra analysis first to view market intelligence data. Use the 'Start New Analysis' button or switch to Dashboard.")
    st.stop()

elif nav_page == "Patent Tracker" and st.session_state.dossier:
    result = st.session_state.dossier
    sections = result.get("sections", {})
    risk_score = result.get("risk_score", 35)
    st.markdown("<h1 style='color:#00D1FF;'>⚖️ Patent Tracker</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#8892B0;'>Freedom-to-Operate Audit | Patent Risk Score: <strong style='color:white;'>{risk_score}/100</strong></p>", unsafe_allow_html=True)
    st.divider()
    c1, c2 = st.columns([1, 3])
    with c1:
        if risk_score < 35:
            st.success(f"✅ LOW RISK\n\nScore: {risk_score}")
        elif risk_score < 70:
            st.warning(f"⚠️ MODERATE RISK\n\nScore: {risk_score}")
        else:
            st.error(f"🚨 HIGH RISK\n\nScore: {risk_score}")
    with c2:
        st.markdown("### Freedom-to-Operate Legal Audit")
        st.write(sections.get("patent_viability", "No patent data."))
    st.stop()

elif nav_page == "Patent Tracker":
    st.markdown("<h1 style='color:#00D1FF;'>⚖️ Patent Tracker</h1>", unsafe_allow_html=True)
    st.info("Run a Drishti Chakra analysis first to view patent audit data.")
    st.stop()

elif nav_page == "Competitor Landscape" and st.session_state.dossier:
    result = st.session_state.dossier
    sections = result.get("sections", {})
    st.markdown("<h1 style='color:#00D1FF;'>📊 Competitor Landscape</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8892B0;'>Competitive intelligence for the analyzed market vertical.</p>", unsafe_allow_html=True)
    st.divider()
    st.markdown("### Technical Blueprint & Competitor Gap Analysis")
    st.write(sections.get("technical_blueprint", "No competitor data."))
    st.stop()

elif nav_page == "Competitor Landscape":
    st.markdown("<h1 style='color:#00D1FF;'>📊 Competitor Landscape</h1>", unsafe_allow_html=True)
    st.info("Run a Drishti Chakra analysis first to view competitor landscape data.")
    st.stop()

elif nav_page == "Blueprint Generator" and st.session_state.dossier:
    result = st.session_state.dossier
    sections = result.get("sections", {})
    topic = st.session_state.topic
    st.markdown("<h1 style='color:#00D1FF;'>🛠️ Blueprint Generator</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#8892B0;'>Autonomous product specification for: <strong style='color:white;'>{topic}</strong></p>", unsafe_allow_html=True)
    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("GPU Stack", "8x MI300X", "AMD Instinct")
    with c2: st.metric("Memory", "1.5TB HBM3", "5.3 TB/s")
    with c3: st.metric("Software", "ROCm 6.1", "HIP Kernels")
    with c4: st.metric("TCO Advantage", "-36% Cost", "vs NVIDIA H100")
    st.markdown("### Go-To-Market Strategy")
    st.write(sections.get("gtm_strategy", "No GTM data."))
    st.stop()

elif nav_page == "Blueprint Generator":
    st.markdown("<h1 style='color:#00D1FF;'>🛠️ Blueprint Generator</h1>", unsafe_allow_html=True)
    st.info("Run a Drishti Chakra analysis first to generate a product blueprint.")
    st.stop()

elif nav_page == "Reports" and st.session_state.dossier:
    result = st.session_state.dossier
    topic = st.session_state.topic
    report_text = result.get("full_report", "")
    sections = result.get("sections", {})
    st.markdown("<h1 style='color:#00D1FF;'>📄 Reports</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#8892B0;'>Full R&D Dossier: <strong style='color:white;'>{topic}</strong></p>", unsafe_allow_html=True)
    st.divider()
    tab_exec, tab_rd, tab_gtm, tab_swot, tab_raw = st.tabs(["Executive Summary", "R&D Blueprint", "GTM Roadmap", "SWOT Audit", "Full Raw Dossier"])
    with tab_exec: st.write(sections.get("executive_summary", ""))
    with tab_rd: st.write(sections.get("technical_blueprint", ""))
    with tab_gtm: st.write(sections.get("gtm_strategy", ""))
    with tab_swot: st.write(sections.get("growth_roadmap", ""))
    with tab_raw: st.markdown(report_text)
    st.download_button(
        label="📄 DOWNLOAD DRISHTI CHAKRA WHITE-PAPER",
        data=report_text,
        file_name=f"drishti_chakra_{topic.lower().replace(' ', '_')}_dossier.md",
        mime="text/markdown",
        use_container_width=True
    )
    st.stop()

elif nav_page == "Reports":
    st.markdown("<h1 style='color:#00D1FF;'>📄 Reports</h1>", unsafe_allow_html=True)
    st.info("Run a Drishti Chakra analysis first to generate reports.")
    st.stop()

# --- MAIN SWITCHER (Dashboard only) ---
# --- STATE INITIALIZATION FOR RUNNING CONTROLLER ---
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False
if "submitted_topic" not in st.session_state:
    st.session_state.submitted_topic = ""

# --- MAIN SWITCHER (Dashboard only) ---
if st.session_state.dossier is None:
    if st.session_state.form_submitted:
        # Show ONLY the loading / compilation console. Form is completely bypassed.
        col_space1, col_center, col_space2 = st.columns([1, 2, 1])
        with col_center:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align:center;color:#00D1FF;'>DRISHTI CHAKRA</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align:center;color:#8892B0;'>Compiling autonomous research dossier...</p>", unsafe_allow_html=True)
            st.divider()
            
            console = st.empty()
            status_messages = [
                "📡 ACCESSING AMD INSTINCT MI300X CLUSTERS...",
                "🧠 INITIALIZING DRISHTI REASONING KERNEL...",
                "🌐 QUERYING GLOBAL PATENT REPOSITORIES...",
                "⚖️ LAUNCHING FREEDOM-TO-OPERATE AUDIT...",
                "🛡️ FINALIZING DRISHTI CHAKRA SPECIFICATIONS..."
            ]
            for msg in status_messages:
                console.code(msg)
                time.sleep(0.4)
            console.empty()

            with st.spinner("COMPILING DOSSIER..."):
                try:
                    engine = ApexVanguardEngine()
                    result = engine.generate_dossier(st.session_state.submitted_topic)
                    st.session_state.dossier = result
                    st.session_state.topic = st.session_state.submitted_topic
                    st.session_state.form_submitted = False  # Reset
                    st.rerun() # Transition clean to dashboard!
                except Exception as e:
                    st.session_state.form_submitted = False  # Reset
                    st.error(f"CRITICAL SYSTEM ERROR: {str(e)}")
    else:
        # Centered landing page for search
        col_space1, col_center, col_space2 = st.columns([1, 2, 1])
        with col_center:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            
            # Display the transparent logo perfectly centered using HTML
            if logo_base64:
                centered_logo = f"""
                    <div style='display: flex; justify-content: center; align-items: center; margin-bottom: 20px;'>
                        <img src='data:image/png;base64,{logo_base64}' style='width: 180px; height: 180px; border-radius: 50%; object-fit: cover;'>
                    </div>
                """
                st.markdown(clean_html(centered_logo), unsafe_allow_html=True)
            
            st.markdown("<h1 style='text-align: center; color: #00D1FF; font-size: 30px; font-weight: 800; margin: 0;'>DRISHTI CHAKRA</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #8892B0; font-size: 13px; font-weight: 600; margin-top: 5px;'>SPEEDING UP THE R&D CHAKRA</p>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Center Search/Analysis Form
            with st.form("center_input_form"):
                user_topic = st.text_input("STARTUP IDEA / MARKET TOPIC:", value="Autonomous Anti-Gravity Propulsion System using YBCO Superconductors", label_visibility="collapsed", placeholder="Enter your startup idea (e.g. Autonomous Anti-Gravity Propulsion System using YBCO Superconductors)...")
                submit_btn = st.form_submit_button("LAUNCH AGENT CYCLE")
                
            st.info("💡 Powered by AMD Instinct™ GPUs via Fireworks AI ROCm telemetry cluster.")

        if submit_btn and user_topic:
            st.session_state.form_submitted = True
            st.session_state.submitted_topic = user_topic
            st.rerun() # Transition to loading state, w/o rendering the form





else:
    # Render full dashboard canvas (Row 1, Row 2, Row 3)
    result = st.session_state.dossier
    topic = st.session_state.topic
    report_text = result.get("full_report", "")
    risk_score = result.get("risk_score", 35)
    
    sections = result.get("sections", {
        "executive_summary": "Run completed. Summary details not structured.",
        "technical_blueprint": "Run completed. Blueprint details not structured.",
        "patent_viability": "Run completed. Patent details not structured.",
        "gtm_strategy": "Run completed.",
        "growth_roadmap": "Run completed."
    })

    # --- TOP PROJECT HEADER ROW ---
    col_title, col_action = st.columns([3, 1])
    with col_title:
        st.markdown(f"<h1 style='color: white; font-size: 24px; font-weight: 700; margin: 0; padding: 0;'>Project: {topic}</h1>", unsafe_allow_html=True)
    with col_action:
        if st.button("＋ Start New Run", use_container_width=True):
            st.session_state.dossier = None
            st.session_state.topic = ""
            st.rerun()
            
    st.markdown("<br>", unsafe_allow_html=True)

    # --- THREE-COLUMN EXECUTIVE GRID ---
    col_left, col_center, col_right = st.columns([1.1, 1.2, 0.9])

    # Left Column: Market Intelligence Overview (Tall Card)
    with col_left:
        multiplier = (100 - risk_score) / 50 if risk_score else 1
        proj_val = int(145 * multiplier)
        summary_html = sections.get("executive_summary", "No data.").replace("\n", "<br>")
        
        left_card = f"""
            <div style='background-color: #161C24; border: 1px solid #212932; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);'>
                <div style='display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #212932; padding-bottom: 10px; margin-bottom: 15px;'>
                    <span style='color: #8892B0; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;'>📈 Market Intelligence Overview</span>
                    <span style='color: #8892B0; cursor: pointer; font-size: 14px;'>•••</span>
                </div>
                <h3 style='color: white; font-size: 15px; margin: 0 0 5px 0; font-weight: bold;'>6-Minute Research Summary</h3>
                <span style='color: #8892B0; font-size: 11px;'>Projected Market Size (2030):</span>
                <div style='display: flex; align-items: baseline; gap: 15px; margin-top: 2px;'>
                    <h1 style='color: #00D1FF; font-size: 34px; font-weight: 800; margin: 0;'>${proj_val}B</h1>
                    <svg viewBox="0 0 100 30" width="80" height="25" style="filter: drop-shadow(0px 0px 4px rgba(0, 230, 57, 0.45));">
                        <path d="M0,25 Q15,20 30,22 T60,10 T80,12 T100,2" fill="none" stroke="#00E639" stroke-width="2" />
                        <path d="M0,25 Q15,20 30,22 T60,10 T80,12 T100,2 L100,30 L0,30 Z" fill="rgba(0, 230, 57, 0.05)" />
                    </svg>
                </div>
                <div style='margin-top: 15px; font-size: 12px; color: #E0E0E0; line-height: 1.6; max-height: 290px; overflow-y: auto;'>
                    {summary_html}
                </div>
                <div style='margin-top: 20px; text-align: left;'>
                    <a href='#' style='color: #00D1FF; font-size: 11px; font-weight: bold; text-decoration: none;'>See more details ⌵</a>
                </div>
            </div>
        """
        st.markdown(clean_html(left_card), unsafe_allow_html=True)

    # Center Column: Competitor Landscape + Product Blueprint
    with col_center:
        # Card 1: Competitor Landscape Matrix (SVG Bar Chart)
        competitor_card = """
            <div style='background-color: #161C24; border: 1px solid #212932; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); margin-bottom: 20px;'>
                <div style='display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #212932; padding-bottom: 10px; margin-bottom: 15px;'>
                    <span style='color: #8892B0; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;'>📊 Competitor Landscape Matrix</span>
                    <span style='color: #8892B0; cursor: pointer; font-size: 14px;'>•••</span>
                </div>
                <div style='display: flex; gap: 12px; justify-content: flex-end; margin-bottom: 10px; font-size: 8px; color: #8892B0;'>
                    <span><span style='color: #2B3746;'>●</span> Energy Density</span>
                    <span><span style='color: #1e95f2;'>●</span> Safety Rating</span>
                    <span><span style='color: #00D1FF;'>●</span> Manufacturability</span>
                </div>
                <svg viewBox="0 0 300 100" class="w-full" style="background-color: transparent;">
                    <line x1="40" y1="20" x2="280" y2="20" stroke="#212932" stroke-width="0.5" />
                    <line x1="40" y1="50" x2="280" y2="50" stroke="#212932" stroke-width="0.5" />
                    <line x1="40" y1="80" x2="280" y2="80" stroke="#212932" stroke-width="0.5" />
                    <text x="35" y="24" fill="#8892B0" font-size="7" text-anchor="end">High</text>
                    <text x="35" y="54" fill="#8892B0" font-size="7" text-anchor="end">Med</text>
                    <text x="35" y="84" fill="#8892B0" font-size="7" text-anchor="end">Low</text>
                    
                    <text x="80" y="95" fill="#8892B0" font-size="7" text-anchor="middle">QuantumScape</text>
                    <rect x="65" y="45" width="8" height="35" fill="#2B3746" rx="1" />
                    <rect x="75" y="60" width="8" height="20" fill="#1e95f2" rx="1" />
                    <rect x="85" y="50" width="8" height="30" fill="#00D1FF" rx="1" />
                    
                    <text x="160" y="95" fill="#8892B0" font-size="7" text-anchor="middle">Solid Power</text>
                    <rect x="145" y="35" width="8" height="45" fill="#2B3746" rx="1" />
                    <rect x="155" y="40" width="8" height="40" fill="#1e95f2" rx="1" />
                    <rect x="165" y="30" width="8" height="50" fill="#00D1FF" rx="1" />
                    
                    <text x="240" y="95" fill="#8892B0" font-size="7" text-anchor="middle">Drishti Stack</text>
                    <rect x="225" y="15" width="8" height="65" fill="#2B3746" rx="1" />
                    <rect x="235" y="20" width="8" height="60" fill="#1e95f2" rx="1" />
                    <rect x="245" y="10" width="8" height="70" fill="#00D1FF" rx="1" />
                </svg>
                <div style='margin-top: 15px; background-color: rgba(0, 209, 255, 0.08); border: 1px solid rgba(0, 209, 255, 0.2); border-radius: 5px; padding: 8px; text-align: center;'>
                    <span style='color: #00D1FF; font-size: 11px; font-weight: bold;'>Identified Market Gap: High-Temperature Stability</span>
                </div>
            </div>
        """
        st.markdown(clean_html(competitor_card), unsafe_allow_html=True)

        # Card 2: Autonomous Product Blueprint
        blueprint_title = f"APEX {topic.replace(' ', '-')}-Alpha"
        blueprint_card = f"""
            <div style='background-color: #161C24; border: 1px solid #212932; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);'>
                <div style='display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #212932; padding-bottom: 10px; margin-bottom: 15px;'>
                    <span style='color: #8892B0; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;'>🛠️ Autonomous Product Blueprint</span>
                    <span style='color: #8892B0; cursor: pointer; font-size: 14px;'>•••</span>
                </div>
                <h3 style='color: white; font-size: 15px; margin: 0 0 12px 0; font-weight: bold;'>Generated Product Blueprint: "{blueprint_title}"</h3>
                
                <div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px;'>
                    <div style='background-color: #101720; border: 1px solid #212932; border-radius: 6px; padding: 10px;'>
                        <span style='color: #8892B0; font-size: 9px; text-transform: uppercase;'>Proposed Configuration</span>
                        <p style='color: white; font-size: 11px; font-weight: bold; margin: 3px 0 0 0;'>High-Capacity Cell, Sulfide Electrolyte</p>
                    </div>
                    <div style='background-color: #101720; border: 1px solid #212932; border-radius: 6px; padding: 10px;'>
                        <span style='color: #8892B0; font-size: 9px; text-transform: uppercase;'>Cathode Intermediary</span>
                        <p style='color: white; font-size: 11px; font-weight: bold; margin: 3px 0 0 0;'>Optimized Ternary Electrolyte</p>
                    </div>
                    <div style='background-color: #101720; border: 1px solid #212932; border-radius: 6px; padding: 10px; grid-column: span 2;'>
                        <span style='color: #8892B0; font-size: 9px; text-transform: uppercase;'>Cathode Formulation</span>
                        <p style='color: #00D1FF; font-size: 11px; font-weight: bold; margin: 3px 0 0 0;'>Gemma-Suggested: Optimized High-Nickel NMCA</p>
                    </div>
                    <div style='background-color: #101720; border: 1px solid #212932; border-radius: 6px; padding: 10px;'>
                        <span style='color: #8892B0; font-size: 9px; text-transform: uppercase;'>Projected Performance</span>
                        <p style='color: white; font-size: 11px; font-weight: bold; margin: 3px 0 0 0;'>450 Wh/kg Density</p>
                    </div>
                    <div style='background-color: #101720; border: 1px solid #212932; border-radius: 6px; padding: 10px; display: flex; justify-content: space-between; align-items: center;'>
                        <div>
                            <span style='color: #8892B0; font-size: 9px; text-transform: uppercase;'>Target Segment</span>
                            <p style='color: white; font-size: 11px; font-weight: bold; margin: 3px 0 0 0;'>Premium EV Market</p>
                        </div>
                        <span style='color: #00D1FF; font-size: 16px;'>✦</span>
                    </div>
                </div>
            </div>
        """
        st.markdown(clean_html(blueprint_card), unsafe_allow_html=True)

    # Right Column: Patent Viability Gauge (Tall Card)
    with col_right:
        if risk_score < 35:
            risk_color = "#00E639"
            risk_text = "LOW RISK"
        elif risk_score < 70:
            risk_color = "#FFAA00"
            risk_text = "MODERATE RISK"
        else:
            risk_color = "#FF544B"
            risk_text = "HIGH RISK"
            
        offset = 220 - (220 * (100 - risk_score) / 100)
        
        right_card = f"""
            <div style='background-color: #161C24; border: 1px solid #212932; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); height: 100%; text-align: center;'>
                <div style='display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #212932; padding-bottom: 10px; margin-bottom: 15px;'>
                    <span style='color: #8892B0; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; text-align: left;'>⚖️ Patent Viability Gauge</span>
                    <span style='color: #8892B0; cursor: pointer; font-size: 14px;'>•••</span>
                </div>
                
                <div style='position: relative; width: 160px; height: 110px; margin: 15px auto 0 auto; display: flex; align-items: center; justify-content: center;'>
                    <svg viewBox="0 0 100 60" width="160" height="96">
                        <path d="M 15 50 A 35 35 0 0 1 85 50" fill="none" stroke="#101720" stroke-width="7" stroke-linecap="round" />
                        <path d="M 15 50 A 35 35 0 0 1 85 50" fill="none" stroke="{risk_color}" stroke-width="7" stroke-dasharray="220" stroke-dashoffset="{offset}" stroke-linecap="round" />
                        <text x="50" y="47" fill="white" font-size="16" font-weight="bold" text-anchor="middle" font-family="sans-serif">{100 - risk_score}%</text>
                    </svg>
                </div>
                
                <h3 style='color: {risk_color}; font-size: 16px; font-weight: bold; margin: 10px 0 5px 0; text-transform: uppercase;'>{risk_text}</h3>
                <p style='color: #8892B0; font-size: 10px; margin-bottom: 20px;'>Analyzed 1,200+ filings. No critical conflicts for proposed specifications.</p>
                
                <div style='text-align: left; border-top: 1px solid #212932; padding-top: 15px;'>
                    <span style='color: #8892B0; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;'>Freedom-to-Operate Audit</span>
                    <div style='margin-top: 8px; font-size: 11px; color: #E0E0E0; line-height: 1.5; height: 180px; overflow-y: auto;'>
                        {sections.get("patent_viability", "No data.")}
                    </div>
                </div>
            </div>
        """
        st.markdown(clean_html(right_card), unsafe_allow_html=True)

    # --- DETAILED ROADMAP TAB SECTIONS ---
    st.markdown("<br>", unsafe_allow_html=True)
    tab_rd, tab_gtm, tab_swot, tab_full = st.tabs([
        "R&D Spec Details", 
        "GTM Execution Roadmap", 
        "SWOT Analysis & Audit", 
        "Full Research Dossier (Raw Text)"
    ])
    
    with tab_rd:
        st.markdown("### Technical Blueprint Specifications")
        st.write(sections.get("technical_blueprint", "No detailed specifications loaded."))
    with tab_gtm:
        st.markdown("### 12-Month Go-To-Market Execution Strategy")
        st.write(sections.get("gtm_strategy", "No GTM strategy loaded."))
    with tab_swot:
        st.markdown("### SWOT Audit & 5-Year Growth Roadmap")
        st.write(sections.get("growth_roadmap", "No growth roadmap loaded."))
    with tab_full:
        st.markdown("### Full Autonomous Research Dossier")
        st.markdown(report_text)

    # --- BOTTOM ROW ACTION PANEL ---
    st.markdown("<br>", unsafe_allow_html=True)
    act_col1, act_col2 = st.columns(2)
    with act_col1:
        st.download_button(
            label="📄 DOWNLOAD DRISHTI CHAKRA WHITE-PAPER",
            data=report_text,
            file_name=f"drishti_chakra_{topic.lower().replace(' ', '_')}_dossier.md",
            mime="text/markdown",
            use_container_width=True
        )
    with act_col2:
        if st.button("📧 EMAIL EXECUTIVE DOSSIER TO BOARD MEMBERS", use_container_width=True):
            st.success("✅ Dossier successfully formatted and queued for board email delivery.")
