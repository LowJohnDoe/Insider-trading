from pathlib import Path
import base64

import streamlit as st

from stock_tracker_v1 import (
    make_session,
    MANAGERS,
    Holding,
    AggregatedHolding,
    fetch_holdings_for_manager,
    aggregate_holdings,
    filter_cheap_holdings,
    export_to_excel,
)

st.set_page_config(
    page_title="Money Button",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="collapsed",
)

LOCAL_IMAGE_CANDIDATES = [
    Path(__file__).with_name("money.png"),
    Path(__file__).with_name("Unknown.png"),
    Path.home() / "Desktop" / "money.png",
    Path.home() / "Desktop" / "Unknown.png",
]

MONEY_IMAGE_B64 = None
for candidate in LOCAL_IMAGE_CANDIDATES:
    if candidate.exists() and candidate.is_file():
        MONEY_IMAGE_B64 = base64.b64encode(candidate.read_bytes()).decode("utf-8")
        break

CUSTOM_CSS = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

html, body, [data-testid="stAppViewContainer"], .stApp {
    margin: 0 !important;
    padding: 0 !important;
    background: #000 !important;
}

.block-container {
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
}

.main-shell {
    position: fixed;
    inset: 0;
    width: 100%;
    height: 100vh;
    overflow: hidden;
}

.center-stack {
    position: fixed;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    width: min(36vw, 320px);
    max-width: 320px;
    min-width: 180px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 20;
}

.money-image-wrap {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    min-height: min(36vw, 320px);
}

.money-image {
    width: 100%;
    height: auto;
    animation: floatMoney 2.8s ease-in-out infinite, waveMoney 3.4s ease-in-out infinite;
    filter: drop-shadow(0 0 10px rgba(0,255,110,0.35));
    user-select: none;
    -webkit-user-drag: none;
    pointer-events: none;
}

.money-fallback {
    color: #19f58b;
    font-size: min(36vw, 320px);
    line-height: 0.9;
    font-weight: 900;
    animation: floatMoney 2.8s ease-in-out infinite, waveMoney 3.4s ease-in-out infinite;
    filter: drop-shadow(0 0 10px rgba(0,255,110,0.35));
    pointer-events: none;
}

.caption {
    color: rgba(255,255,255,0.76);
    font-size: 0.95rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    text-align: center;
    margin-top: 0.5rem;
}

.status-text {
    color: rgba(255,255,255,0.88);
    text-align: center;
    font-size: 1rem;
    padding: 0 1rem;
    position: fixed;
    left: 50%;
    top: calc(50% + min(36vw, 320px) / 2 + 3rem);
    transform: translateX(-50%);
    width: min(90vw, 700px);
}

div.stButton {
    position: fixed !important;
    left: 50% !important;
    top: 50% !important;
    transform: translate(-50%, -50%) !important;
    width: min(36vw, 320px) !important;
    max-width: 320px !important;
    min-width: 180px !important;
    height: min(72vw, 640px) !important;
    max-height: 640px !important;
    min-height: 360px !important;
    display: block !important;
    z-index: 30 !important;
}

div.stButton > button {
    position: absolute !important;
    inset: 0 !important;
    width: 100% !important;
    height: 100% !important;
    min-width: 100% !important;
    min-height: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    background: transparent !important;
    color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    cursor: pointer !important;
    opacity: 0 !important;
}

div.stButton > button * {
    color: transparent !important;
    opacity: 0 !important;
    font-size: 0 !important;
    line-height: 0 !important;
}

div.stButton > button:hover,
div.stButton > button:focus,
div.stButton > button:focus-visible,
div.stButton > button:active {
    background: transparent !important;
    color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}

div.stDownloadButton {
    position: fixed;
    left: 50%;
    top: calc(50% + min(36vw, 320px) / 2 + 6rem);
    transform: translateX(-50%);
    display: flex;
    justify-content: center;
    width: min(90vw, 320px);
}

div.stDownloadButton > button {
    background: #00d26a !important;
    color: black !important;
    border: none !important;
    border-radius: 999px !important;
    padding: 0.9rem 1.35rem !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    width: 100% !important;
}

div.stDownloadButton > button:hover {
    background: #1df58b !important;
    color: black !important;
}

@keyframes floatMoney {
    0% { transform: translateY(0px) scale(1); }
    50% { transform: translateY(-16px) scale(1.03); }
    100% { transform: translateY(0px) scale(1); }
}

@keyframes waveMoney {
    0% { rotate: -5deg; }
    50% { rotate: 5deg; }
    100% { rotate: -5deg; }
}

@media (max-width: 768px) {
    .center-stack {
        top: 50%;
        width: min(52vw, 260px);
        max-width: 260px;
        min-width: 150px;
    }

    div.stButton {
        top: 50% !important;
        width: min(52vw, 260px) !important;
        max-width: 260px !important;
        min-width: 150px !important;
        height: min(104vw, 520px) !important;
        max-height: 520px !important;
        min-height: 300px !important;
    }

    .money-image-wrap {
        min-height: min(52vw, 260px);
    }

    .money-fallback {
        font-size: min(52vw, 260px);
    }

    .status-text {
        top: calc(50% + min(52vw, 260px) / 2 + 2.5rem);
        width: min(92vw, 520px);
    }

    div.stDownloadButton {
        top: calc(50% + min(52vw, 260px) / 2 + 5.25rem);
        width: min(88vw, 280px);
    }
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def build_excel_bytes() -> tuple[bytes, int, int, int]:
    session = make_session()
    all_holdings: list[Holding] = []

    for manager in MANAGERS:
        manager_holdings = fetch_holdings_for_manager(
            session=session,
            manager_name=manager["name"],
            cik=manager["cik"],
            max_filings=2,
        )
        all_holdings.extend(manager_holdings)

    aggregated_holdings: list[AggregatedHolding] = aggregate_holdings(all_holdings)
    cheap_holdings: list[AggregatedHolding] = filter_cheap_holdings(
        aggregated_holdings,
        max_price=25.0,
        min_total_shares=1.0,
    )

    temp_path = Path("stock_tracker_output.xlsx")
    export_to_excel(
        raw_holdings=all_holdings,
        aggregated_holdings=aggregated_holdings,
        output_path=str(temp_path),
    )

    file_bytes = temp_path.read_bytes()
    temp_path.unlink(missing_ok=True)

    return file_bytes, len(all_holdings), len(aggregated_holdings), len(cheap_holdings)


if "excel_bytes" not in st.session_state:
    st.session_state.excel_bytes = None
    st.session_state.raw_count = None
    st.session_state.agg_count = None
    st.session_state.cheap_count = None
    st.session_state.ready = False

st.markdown('<div class="main-shell">', unsafe_allow_html=True)

st.markdown('<div class="center-stack">', unsafe_allow_html=True)
if MONEY_IMAGE_B64:
    st.markdown(
        f'<div class="money-image-wrap"><img class="money-image" src="data:image/png;base64,{MONEY_IMAGE_B64}" alt="money"></div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown('<div class="money-image-wrap"><div class="money-fallback">$</div></div>', unsafe_allow_html=True)

clicked = st.button(" ", key="money_button", use_container_width=True)
st.markdown('<div class="caption"></div>', unsafe_allow_html=True)
st.markdown('</div></div>', unsafe_allow_html=True)

if clicked:
    with st.spinner("Scanning filings and building workbook..."):
        file_bytes, raw_count, agg_count, cheap_count = build_excel_bytes()
        st.session_state.excel_bytes = file_bytes
        st.session_state.raw_count = raw_count
        st.session_state.agg_count = agg_count
        st.session_state.cheap_count = cheap_count
        st.session_state.ready = True

if st.session_state.ready and st.session_state.excel_bytes is not None:
    st.markdown(
        f'<div class="status-text">Ready.<br>Raw holdings: {st.session_state.raw_count} | Aggregated: {st.session_state.agg_count} | Cheap matches: {st.session_state.cheap_count}</div>',
        unsafe_allow_html=True,
    )
    st.download_button(
        label="Download Excel",
        data=st.session_state.excel_bytes,
        file_name="stock_tracker_output.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=False,
    )
else:
    st.markdown('<div class="status-text"></div>', unsafe_allow_html=True)