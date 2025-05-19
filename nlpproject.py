import pytextrank
import spacy
import streamlit as st





# ---------- One-time initialisation ----------
# (spaCy model is cached so it loads only once per session)
if "nlp" not in st.session_state:
    st.session_state.nlp = spacy.load("en_core_web_lg")
    st.session_state.nlp.add_pipe("textrank")

# ---------- Session-persistent chat history ----------
if "history" not in st.session_state:
    st.session_state.history = []           # list of {"prompt": ..., "summary": ...}

# ---------- User input ----------
prompt = st.chat_input("Enter a text")

# ---------- Process the turn ----------
if prompt is not None:
    if prompt.strip() == "":
        st.warning("Please enter a description.")
    else:
        with st.spinner("Processing…"):
            try:
                doc = st.session_state.nlp(prompt)
                summary = " ".join(sent.text for sent in doc._.textrank.summary())
                st.session_state.history.append(
                    {"prompt": prompt, "summary": summary}
                )
            except Exception as e:
                st.error(f"Error: {e}")

# ---------- Display full conversation ----------
st.divider()
st.subheader("Natural Language Processing (NLP)")
st.header("longe text---> summary")

for i, turn in enumerate(st.session_state.history, 1):
    st.markdown(f" User Enter  text {turn['prompt']}")
    st.markdown(f"**Summary:** {turn['summary']}")
    st.divider()

# ---------- Optional clear-chat button ----------
if st.button("Clear history"):
    st.session_state.history.clear()
