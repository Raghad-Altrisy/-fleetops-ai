"""
FleetOps AI - Streamlit Dashboard (Day 6)
============================================
واجهة واحدة فيها:
  1) Overview: نظرة عامة على الأسطول (KPIs + رسومات)
  2) Chat: محادثة طبيعية مع الـ AI Agent (يستخدم agent.ask_agent)
  3) Reports: تقرير أداء شامل قابل للعرض

للتشغيل محليًا: streamlit run app/main.py
للنشر السحابي: ادفع المشروع على GitHub وانشره على share.streamlit.io
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import streamlit as st
import pandas as pd
import plotly.express as px

import tools
import agent
import ml_anomaly

st.set_page_config(page_title="FleetOps AI", page_icon="🚜", layout="wide")

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("🚜 FleetOps AI")
    st.caption("AI Operations Agent for Construction Equipment")

    st.divider()
    api_key = st.text_input("OpenAI API Key (اختياري)", type="password",
                             help="لو حطيت مفتاح، الشات هيستخدم LLM حقيقي. لو سبته فاضي، هيشتغل بوضع Test Mode.")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        st.success("✅ Real Mode مفعّل (OpenAI)")
    else:
        st.info("ℹ️ شغّال بـ Test Mode (بدون LLM حقيقي)")

    st.divider()
    st.caption("مسابقة الابتكار وريادة الأعمال — مسار AI + Operation")

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab_overview, tab_chat, tab_report = st.tabs(["📊 نظرة عامة", "💬 اسأل الـ Agent", "📋 تقرير الأداء"])

# ============================== TAB 1: OVERVIEW ==============================
with tab_overview:
    report = tools.generate_fleet_report()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("عدد المعدات", report["fleet_size"])
    c2.metric("معدل الاستخدام العام", f"{report['overall_utilization_%']}%")
    c3.metric("إجمالي ساعات التشغيل", f"{report['total_operating_hours']:,.0f}")
    c4.metric("إجمالي استهلاك الوقود (لتر)", f"{report['total_fuel_l']:,.0f}")

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("أعلى المعدات من حيث التوقف")
        top_downtime = pd.DataFrame(tools.get_top_downtime_equipment(8)["data"])
        fig = px.bar(top_downtime, x="equipment_id", y="downtime_rate_%",
                     color="equipment_type", text="downtime_rate_%")
        fig.update_layout(showlegend=True, height=380)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("معدل الاستخدام حسب المشروع")
        by_project = pd.DataFrame(report["by_project"])
        fig2 = px.bar(by_project, x="project", y="utilization_%", color="project", text="utilization_%")
        fig2.update_layout(showlegend=False, height=380)
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.subheader("🚨 معدات تحتاج تدخل فوري")
    attention = pd.DataFrame(tools.get_equipment_needing_attention()["data"])
    if attention.empty:
        st.success("لا توجد معدات تحتاج تدخل فوري حاليًا ✅")
    else:
        st.dataframe(attention[["equipment_id", "equipment_type", "project", "reason"]],
                     use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("🎯 ترتيب الأولوية الموحد (Attention Score)")
    st.caption("يجمع Downtime + انحراف الوقود + تكرار الصيانة + كشف الشذوذ بالـ Machine Learning في رقم واحد (0-100)")
    scores = pd.DataFrame(ml_anomaly.compute_attention_scores()["data"])
    fig3 = px.bar(scores, x="equipment_id", y="attention_score", color="attention_score",
                  color_continuous_scale=["#2a9d8f", "#e9c46a", "#e76f51"])
    fig3.update_layout(height=350, coloraxis_showscale=False)
    st.plotly_chart(fig3, use_container_width=True)

# ============================== TAB 2: CHAT ==============================
with tab_chat:
    st.subheader("اسأل الـ AI Agent عن أسطولك")
    st.caption("أمثلة: ما المعدات التي لديها أعلى Downtime؟ / أي المعدات تحتاج تدخل فوري؟ / ما أسباب ارتفاع استهلاك الوقود؟")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for role, msg in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(msg)

    user_q = st.chat_input("اكتب سؤالك هنا...")
    if user_q:
        st.session_state.chat_history.append(("user", user_q))
        with st.chat_message("user"):
            st.markdown(user_q)

        with st.chat_message("assistant"):
            with st.spinner("جاري التحليل..."):
                answer = agent.ask_agent(user_q)
                st.markdown(answer)
        st.session_state.chat_history.append(("assistant", answer))

# ============================== TAB 3: REPORT ==============================
with tab_report:
    st.subheader("📋 تقرير أداء الأسطول الشامل")
    report = tools.generate_fleet_report()

    st.markdown(f"**الفترة:** {report['period']}")
    st.markdown(f"**عدد المعدات:** {report['fleet_size']}")
    st.markdown(f"**معدل الاستخدام العام:** {report['overall_utilization_%']}%")

    st.markdown("### أداء المشاريع")
    st.dataframe(pd.DataFrame(report["by_project"]), use_container_width=True, hide_index=True)

    st.markdown("### أهم 3 مشاكل توقف")
    st.dataframe(pd.DataFrame(report["top_downtime_equipment"]), use_container_width=True, hide_index=True)

    if report["fuel_anomalies"]:
        st.markdown("### ⚠️ تنبيهات استهلاك الوقود")
        st.dataframe(pd.DataFrame(report["fuel_anomalies"]), use_container_width=True, hide_index=True)

    st.download_button(
        "⬇️ تحميل التقرير كـ CSV",
        pd.DataFrame(report["by_project"]).to_csv(index=False).encode("utf-8-sig"),
        file_name="fleet_performance_report.csv",
    )
