import streamlit as st
from graph import app

# ─── Page Config ──────────────────────────────────────
st.set_page_config(
    page_title="AI Cold Email Agent",
    page_icon="📧",
    layout="centered"
)

# ─── Header ───────────────────────────────────────────
st.title("📧 AI Cold Email Agent")
st.caption("Multi-Agent system powered by LangGraph + Groq")

st.divider()

# ─── Input Form ───────────────────────────────────────
st.subheader("🎯 Target Company")

company_name = st.text_input("Company Name", placeholder="e.g. Shopify")
website_url = st.text_input("Company Website", placeholder="e.g. https://www.shopify.com")
your_service = st.text_area("Your Service", placeholder="e.g. AI Chatbot for customer support", height=80)

st.divider()

st.subheader("👤 Your Details")

col1, col2 = st.columns(2)
with col1:
    your_name = st.text_input("Your Name", placeholder="e.g. Abdul Samad")
with col2:
    your_role = st.text_input("Your Role", placeholder="e.g. AI Solutions Lead")

st.divider()

# ─── Run Button ───────────────────────────────────────
if st.button("🚀 Generate Email", use_container_width=True, type="primary"):

    # Validation
    if not all([company_name, website_url, your_service, your_name, your_role]):
        st.error("Please fill all fields!")
        st.stop()

    # ─── Agent Pipeline ───────────────────────────────
    with st.status("🤖 Agents running...", expanded=True) as status:

        st.write("🔍 Research Agent: Researching company...")
        st.write("🎯 Pain Point Agent: Identifying problems...")
        st.write("✍️ Email Writer: Crafting personalized email...")
        st.write("✅ Review Agent: Reviewing and improving...")

        result = app.invoke({
            "company_name": company_name,
            "website_url": website_url,
            "your_service": your_service,
            "your_name": your_name,
            "your_role": your_role,
            "research": "",
            "pain_points": "",
            "email_subject": "",
            "email_body": "",
            "review": ""
        })

        status.update(label="✅ Email Ready!", state="complete")

    st.divider()

    # ─── Research Output ──────────────────────────────
    with st.expander("🔍 Company Research", expanded=False):
        st.markdown(result["research"])

    # ─── Pain Points Output ───────────────────────────
    with st.expander("🎯 Pain Points Identified", expanded=False):
        st.markdown(result["pain_points"])

    st.divider()

    # ─── Final Email Output ───────────────────────────
    st.subheader("📧 Generated Email")

    st.markdown(f"**Subject:** {result['email_subject']}")
    st.divider()
    st.markdown(result["email_body"])

    # ─── Copy Button ──────────────────────────────────
    full_email = f"Subject: {result['email_subject']}\n\n{result['email_body']}"
    st.download_button(
        label="📋 Download Email",
        data=full_email,
        file_name=f"{company_name}_cold_email.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.divider()

    # ─── Review Output ────────────────────────────────
    with st.expander("📝 Agent Review & Scores", expanded=True):
        st.markdown(result["review"])