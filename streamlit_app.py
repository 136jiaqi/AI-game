from __future__ import annotations

import base64
import json
import os
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


ROOT = Path(__file__).parent
H5_ROOT = ROOT / "public" / "h5"
DEFAULT_API_BASE = "https://xmodhub-ai-evaluation-api-288906-10-1411444327.sh.run.tcloudbase.com"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def image_data_uri(path: Path) -> str:
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{data}"


def configured_api_base() -> str:
    secret_value = ""
    try:
        secret_value = st.secrets.get("XMODHUB_API_BASE", "")
    except Exception:
        secret_value = ""
    return (os.getenv("XMODHUB_API_BASE") or secret_value or DEFAULT_API_BASE).rstrip("/")


def build_activity_page() -> str:
    html = read_text(H5_ROOT / "index.html")
    css = read_text(H5_ROOT / "styles.css")
    js = read_text(H5_ROOT / "app.js")

    api_base = configured_api_base()
    js = js.replace(
        'const DEPLOYED_API_BASE = "https://xmodhub-ai-evaluation.lijiaqi13648060.chatgpt.site";\n'
        'const API_BASE = window.location.protocol === "file:" ? DEPLOYED_API_BASE : window.location.origin;',
        f"const DEPLOYED_API_BASE = {json.dumps(api_base)};\n"
        "const API_BASE = DEPLOYED_API_BASE;",
    )

    guide_image = image_data_uri(H5_ROOT / "assets" / "steam-store-link-guide.png")
    html = html.replace("./assets/steam-store-link-guide.png", guide_image)
    html = html.replace('<link rel="stylesheet" href="./styles.css?v=20260728-steps" />', f"<style>{css}</style>")
    html = html.replace('<link rel="stylesheet" href="./styles.css" />', f"<style>{css}</style>")
    html = html.replace('<script src="./app.js?v=20260721-payment-click"></script>', f"<script>{js}</script>")
    html = html.replace('<script src="./app.js"></script>', f"<script>{js}</script>")
    return html


def main() -> None:
    st.set_page_config(
        page_title="XMODhub AI免费评估",
        page_icon="X",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    st.markdown(
        """
        <style>
          #MainMenu, header, footer { display: none !important; }
          .stApp { background: #090f19; }
          .block-container {
            max-width: none;
            padding: 0;
          }
          iframe {
            display: block;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

    components.html(build_activity_page(), height=1450, scrolling=True)


if __name__ == "__main__":
    main()
