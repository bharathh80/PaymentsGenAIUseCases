import streamlit as st
from llm.openai import OpenAI
import json

# ------------ SETTINGS ------------
page_title = ' Payments Customer Support Demo ️'
layout = 'wide'

# ------------ PAGE SETUP ------------
st.set_page_config(page_title=page_title, layout=layout)

openai = OpenAI()
with open("customer_emails.json") as f:
    emails_json = json.loads(f.read())
dd_option_1 = "Reminder due to missing return"
dd_option_2 = "General marketplace questions"
dd_option_3 = "Question about delivery date and time"
dd_option_4 = "Complaint about goods/services"
dd_option_5 = "Payment restriction methods"
dd_option_6 = "Payment research"
dd_option_7 = "Questions about payment allocation"
dd_option_8 = "Questions about installment plan / invoice"


def get_dropdown():
    print(st.session_state["dd"])
    st.session_state["customer_text"] = emails_json[st.session_state["dd"]]


def render_page():
    st.title(f"Payments Landing Page")
    dropdown = st.selectbox("",
                            (
                                dd_option_1,
                                dd_option_2,
                                dd_option_3,
                                dd_option_4,
                                dd_option_5,
                                dd_option_6,
                                dd_option_7,
                                dd_option_8
                            ), on_change=get_dropdown, placeholder="Payment customer support choices", key="dd")

    col1, col2 = st.columns(2)

    with col1:
        customer_area = st.text_area(" ", height=500, key="customer_text")

    with col2:
        tab1, tab2 = st.tabs(["Step 1 - Identify customer ticket level", "Step 2 - Respond to ticket"])

    execute_but = st.button("Execute", use_container_width=True)

    if execute_but:
        if st.session_state["dd"]:
            with st.spinner("Processing..."):
                system_prompt = openai.get_system_prompt("determine_ticket_level")
                with tab1:
                    st.write(openai.send_request(system_prompt, st.session_state["customer_text"]))

                system_prompt = openai.get_system_prompt("respond_to_ticket")
                with tab2:
                    st.write(openai.send_request(system_prompt, st.session_state["customer_text"]))


if __name__ == "__main__":
    render_page()