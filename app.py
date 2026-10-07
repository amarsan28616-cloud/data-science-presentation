from pathlib import Path

import streamlit as st

BASE = Path(__file__).parent
SLIDES = sorted((BASE / "slides").glob("slide-*.jpg"))
PPTX = BASE / "Shorat_Innovative_Presentation.pptx"

# Speaker notes (slide number -> text), taken from the original deck
NOTES = {
    3: "Today, Data rules the world. This has resulted in a huge demand for Data Scientists. "
       "A Data Scientist helps companies with data-driven decisions, to make their business better.",
}

st.set_page_config(page_title="Data Science Presentation", page_icon="📊", layout="wide")

total = len(SLIDES)
if "idx" not in st.session_state:
    st.session_state.idx = 0


def go(delta=0, to=None):
    new = to if to is not None else st.session_state.idx + delta
    st.session_state.idx = max(0, min(total - 1, new))


# ---------- Sidebar ----------
with st.sidebar:
    st.title("📊 Data Science")
    st.caption("Presented by Amarja S")
    st.selectbox(
        "Jump to slide",
        range(total),
        index=st.session_state.idx,
        format_func=lambda i: f"Slide {i + 1}",
        key="jump",
        on_change=lambda: go(to=st.session_state.jump),
    )
    st.download_button(
        "⬇️ Download PPTX",
        data=PPTX.read_bytes(),
        file_name=PPTX.name,
        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        width="stretch",
    )
    show_thumbs = st.toggle("Show thumbnails", value=False)
    if show_thumbs:
        for i, p in enumerate(SLIDES):
            st.image(str(p), caption=f"Slide {i + 1}", width="stretch")
            st.button("Open", key=f"open{i}", on_click=go, kwargs={"to": i})

# ---------- Main viewer ----------
st.header("Data Science Presentation")

st.image(str(SLIDES[st.session_state.idx]), width="stretch")

prev_col, mid_col, next_col = st.columns([1, 2, 1])
prev_col.button("⬅️ Previous", on_click=go, kwargs={"delta": -1},
                disabled=st.session_state.idx == 0, width="stretch")
mid_col.markdown(
    f"<div style='text-align:center;padding-top:0.4rem'>Slide <b>{st.session_state.idx + 1}</b> of {total}</div>",
    unsafe_allow_html=True,
)
next_col.button("Next ➡️", on_click=go, kwargs={"delta": 1},
                disabled=st.session_state.idx == total - 1, width="stretch")
st.progress((st.session_state.idx + 1) / total)

note = NOTES.get(st.session_state.idx + 1)
if note:
    with st.expander("🗒️ Speaker notes"):
        st.write(note)
