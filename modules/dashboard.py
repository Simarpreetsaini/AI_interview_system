
import streamlit as st
import matplotlib.pyplot as plt

def show_dashboard(df):

    st.subheader("Interview Analytics Dashboard")

    fig = plt.figure()
    plt.bar(range(len(df)), df["score"])
    plt.xlabel("Question")
    plt.ylabel("Score")

    st.pyplot(fig)

    final_score = df["score"].mean()

    st.metric("Final Interview Score", round(final_score,2))

    if final_score > 60:
        st.success("Selected")
    else:
        st.error("Rejected")
