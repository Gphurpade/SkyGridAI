"""Custom CSS styles for the SkyGridAI frontend."""

from __future__ import annotations

import streamlit as st


def inject_styles(theme: dict[str, str]) -> None:
    """Inject the shared application stylesheet."""
    st.markdown(
        f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

            :root {{
                --bg: {theme["background"]};
                --surface: {theme["surface"]};
                --surface-strong: {theme["surface_strong"]};
                --text: {theme["text"]};
                --muted: {theme["muted"]};
                --border: {theme["border"]};
                --primary: {theme["primary"]};
                --secondary: {theme["secondary"]};
                --accent: {theme["accent"]};
                --warning: {theme["warning"]};
                --danger: {theme["danger"]};
                --hero-a: {theme["hero_a"]};
                --hero-b: {theme["hero_b"]};
            }}

            html, body, [class*="css"] {{
                font-family: 'Manrope', sans-serif;
            }}

            .stApp {{
                background:
                    radial-gradient(circle at top right, rgba(17, 135, 216, 0.12), transparent 24%),
                    radial-gradient(circle at top left, rgba(28, 168, 116, 0.10), transparent 20%),
                    linear-gradient(180deg, var(--bg) 0%, var(--bg) 100%);
                color: var(--text);
            }}

            .block-container {{
                max-width: 1360px;
                padding-top: 1.15rem;
                padding-bottom: 2.5rem;
            }}

            [data-testid="stSidebar"] {{
                background: linear-gradient(180deg, var(--surface-strong), var(--surface));
                border-right: 1px solid var(--border);
            }}

            [data-testid="stSidebar"] .block-container {{
                padding-top: 1.1rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }}

            .app-card,
            .hero-panel {{
                background: var(--surface);
                border: 1px solid var(--border);
                border-radius: 24px;
                box-shadow: 0 18px 50px rgba(15, 23, 42, 0.09);
                backdrop-filter: blur(14px);
            }}

            .hero-panel {{
                padding: 2.1rem 2.2rem;
                background: linear-gradient(135deg, var(--hero-a), var(--hero-b));
                overflow: hidden;
                position: relative;
            }}

            .hero-panel::after {{
                content: "";
                position: absolute;
                width: 320px;
                height: 320px;
                top: -120px;
                right: -90px;
                background: radial-gradient(circle, rgba(17, 185, 218, 0.22), transparent 68%);
                pointer-events: none;
            }}

            .hero-grid {{
                display: grid;
                grid-template-columns: minmax(0, 1.5fr) minmax(280px, 0.85fr);
                gap: 1.2rem;
                align-items: stretch;
            }}

            .hero-brand {{
                display: flex;
                gap: 1rem;
                align-items: flex-start;
            }}

            .hero-logo {{
                width: 68px;
                height: 68px;
                border-radius: 20px;
                overflow: hidden;
                box-shadow: 0 16px 30px rgba(12, 78, 163, 0.22);
                flex-shrink: 0;
            }}

            .hero-wordmark {{
                width: min(440px, 100%);
                display: block;
                filter: drop-shadow(0 12px 26px rgba(12, 78, 163, 0.16));
            }}

            .hero-kicker {{
                color: var(--secondary);
                font-size: 0.82rem;
                font-weight: 700;
                letter-spacing: 0.12em;
                text-transform: uppercase;
            }}

            .hero-title {{
                color: var(--text);
                font-size: clamp(2rem, 4vw, 3.65rem);
                line-height: 1.05;
                font-weight: 800;
                margin: 0.55rem 0;
            }}

            .hero-subtitle {{
                color: var(--muted);
                font-size: 1rem;
                line-height: 1.65;
                max-width: 760px;
            }}

            .hero-stats {{
                display: grid;
                grid-template-columns: 1fr;
                gap: 0.8rem;
            }}

            .hero-stat-card {{
                padding: 1rem 1.05rem;
                border-radius: 20px;
                background: rgba(255, 255, 255, 0.24);
                border: 1px solid rgba(255, 255, 255, 0.28);
                backdrop-filter: blur(12px);
            }}

            .hero-stat-label {{
                color: var(--muted);
                font-size: 0.78rem;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                font-weight: 800;
            }}

            .hero-stat-value {{
                color: var(--text);
                font-size: 1.15rem;
                font-weight: 800;
                margin-top: 0.35rem;
            }}

            .metric-card {{
                padding: 1.3rem 1.35rem;
                min-height: 172px;
                transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
            }}

            .metric-card:hover {{
                transform: translateY(-6px);
                box-shadow: 0 22px 42px rgba(15, 23, 42, 0.14);
                border-color: rgba(17, 135, 216, 0.24);
            }}

            .metric-label {{
                color: var(--muted);
                font-size: 0.86rem;
                font-weight: 700;
                letter-spacing: 0.04em;
                text-transform: uppercase;
            }}

            .metric-value {{
                color: var(--text);
                font-size: 2.25rem;
                font-weight: 800;
                margin: 0.35rem 0 0.2rem 0;
            }}

            .metric-desc {{
                color: var(--muted);
                font-size: 0.9rem;
                line-height: 1.5;
            }}

            .metric-row {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 0.8rem;
            }}

            .metric-icon {{
                width: 46px;
                height: 46px;
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.2rem;
                background: rgba(255, 255, 255, 0.18);
                border: 1px solid rgba(255, 255, 255, 0.22);
            }}

            .metric-gradient-rain {{
                background: linear-gradient(135deg, rgba(12, 78, 163, 0.94), rgba(17, 185, 218, 0.8));
            }}

            .metric-gradient-max {{
                background: linear-gradient(135deg, rgba(245, 158, 11, 0.92), rgba(249, 115, 22, 0.84));
            }}

            .metric-gradient-min {{
                background: linear-gradient(135deg, rgba(24, 122, 191, 0.92), rgba(39, 196, 134, 0.8));
            }}

            .metric-gradient-rain .metric-label,
            .metric-gradient-rain .metric-value,
            .metric-gradient-rain .metric-desc,
            .metric-gradient-max .metric-label,
            .metric-gradient-max .metric-value,
            .metric-gradient-max .metric-desc,
            .metric-gradient-min .metric-label,
            .metric-gradient-min .metric-value,
            .metric-gradient-min .metric-desc {{
                color: white;
            }}

            .metric-mini {{
                color: rgba(255, 255, 255, 0.84);
                font-size: 0.84rem;
                font-weight: 600;
            }}

            .section-title {{
                color: var(--text);
                font-size: 1.22rem;
                font-weight: 800;
                margin-bottom: 0.45rem;
            }}

            .section-copy {{
                color: var(--muted);
                margin-bottom: 0.9rem;
                line-height: 1.65;
            }}

            .section-card,
            .chart-card,
            .map-card,
            .table-card,
            .heatmap-card {{
                padding: 1.15rem 1.2rem 1rem 1.2rem;
            }}

            .status-pill {{
                display: inline-block;
                padding: 0.35rem 0.7rem;
                border-radius: 999px;
                font-size: 0.8rem;
                font-weight: 700;
                margin-right: 0.4rem;
                margin-top: 0.4rem;
            }}

            .pill-ok {{
                background: rgba(34, 197, 94, 0.14);
                color: var(--accent);
            }}

            .pill-warn {{
                background: rgba(249, 115, 22, 0.14);
                color: var(--warning);
            }}

            .pill-danger {{
                background: rgba(220, 38, 38, 0.14);
                color: var(--danger);
            }}

            .small-note {{
                color: var(--muted);
                font-size: 0.82rem;
            }}

            .footer-wrap {{
                padding: 1.4rem 1.6rem;
            }}

            .footer-grid {{
                display: grid;
                grid-template-columns: 1.3fr 1fr;
                gap: 1rem;
                align-items: center;
            }}

            .footer-meta {{
                display: flex;
                flex-wrap: wrap;
                gap: 0.5rem;
                justify-content: flex-end;
            }}

            .stButton > button,
            .stDownloadButton > button {{
                border-radius: 15px;
                border: 1px solid var(--border);
                min-height: 2.95rem;
                font-weight: 700;
                box-shadow: 0 8px 20px rgba(15, 23, 42, 0.05);
                transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
            }}

            .stButton > button:hover,
            .stDownloadButton > button:hover {{
                transform: translateY(-1px);
                box-shadow: 0 12px 24px rgba(15, 23, 42, 0.08);
            }}

            .stButton > button[kind="primary"] {{
                background: linear-gradient(135deg, var(--primary), var(--secondary));
                color: white;
                border: none;
                box-shadow: 0 14px 28px rgba(17, 135, 216, 0.28);
            }}

            .stNumberInput label,
            .stSelectbox label,
            .stSlider label,
            .stTextInput label {{
                color: var(--text) !important;
                font-weight: 700 !important;
            }}

            .stSelectbox > div > div,
            .stNumberInput > div > div,
            .stTextInput > div > div {{
                border-radius: 16px !important;
            }}

            .app-card {{
                padding: 1.2rem 1.25rem;
            }}

            .sidebar-brand {{
                padding: 1rem 1rem 1.15rem 1rem;
                border-radius: 22px;
                background: linear-gradient(145deg, var(--surface-strong), rgba(17, 135, 216, 0.08));
                border: 1px solid var(--border);
                margin-bottom: 1rem;
            }}

            .sidebar-brand-row {{
                display: flex;
                gap: 0.9rem;
                align-items: center;
            }}

            .sidebar-brand img {{
                width: 52px;
                height: 52px;
                border-radius: 16px;
                box-shadow: 0 12px 24px rgba(12, 78, 163, 0.2);
                object-fit: cover;
            }}

            .sidebar-title {{
                color: var(--text);
                font-size: 1.18rem;
                font-weight: 800;
            }}

            .sidebar-subtitle {{
                color: var(--muted);
                font-size: 0.84rem;
                margin-top: 0.1rem;
                line-height: 1.45;
            }}

            .sidebar-section-label {{
                color: var(--muted);
                font-size: 0.76rem;
                font-weight: 800;
                letter-spacing: 0.12em;
                text-transform: uppercase;
                margin: 1.05rem 0 0.55rem;
            }}

            div[role="radiogroup"] > label {{
                background: transparent;
                border: 1px solid transparent;
                border-radius: 16px;
                margin-bottom: 0.35rem;
                padding: 0.5rem 0.55rem;
                transition: all 180ms ease;
            }}

            div[role="radiogroup"] > label:hover {{
                background: rgba(17, 135, 216, 0.08);
                border-color: rgba(17, 135, 216, 0.16);
            }}

            .sidebar-stat {{
                padding: 0.9rem 1rem;
                border-radius: 18px;
                background: rgba(17, 135, 216, 0.06);
                border: 1px solid var(--border);
                margin-bottom: 0.65rem;
            }}

            @media (max-width: 1024px) {{
                .hero-grid,
                .footer-grid {{
                    grid-template-columns: 1fr;
                }}

                .footer-meta {{
                    justify-content: flex-start;
                }}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
