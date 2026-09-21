"""
FleetOps AI - Agent Logic (Day 5)
===================================
يربط سؤال المستخدم (Natural Language) بالأدوات في tools.py عبر إحدى طريقتين:

1) REAL MODE  -> يستخدم OpenAI API (Chat Completions + function/tool calling الحقيقي).
                 يتفعّل تلقائيًا لو لقى OPENAI_API_KEY في البيئة.

2) TEST MODE  -> Router بسيط (keyword-based) بيحاكي نفس سلوك اختيار الأداة،
                 يستخدم عشان نقدر نختبر الـ pipeline كامل دلوقتي بدون ما نحتاج API key.
                 لما تحطوا مفتاحكم، الكود هيستخدم REAL MODE تلقائيًا بنفس الأدوات بالظبط.

الأدوات المستخدمة: openai (Chat Completions API - Function Calling), python-dotenv, json, os
"""

import os
import json
from dotenv import load_dotenv

import tools
import ml_anomaly

load_dotenv()

# ---------------------------------------------------------------------------
# تعريف الأدوات بصيغة OpenAI Function Calling Schema
# ---------------------------------------------------------------------------
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_top_downtime_equipment",
            "description": "يرجع المعدات الأكثر توقفًا (Downtime) في الأسطول",
            "parameters": {
                "type": "object",
                "properties": {
                    "top_n": {"type": "integer", "description": "عدد المعدات المطلوبة", "default": 5}
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_equipment_needing_attention",
            "description": "يحدد المعدات التي تحتاج تدخل صيانة/تشغيل فوري بناءً على Downtime وكفاءة الوقود وتكرار الصيانة",
            "parameters": {
                "type": "object",
                "properties": {
                    "downtime_threshold_pct": {"type": "number", "default": 15.0}
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "explain_utilization_trend",
            "description": "يحلل سبب ارتفاع أو انخفاض معدل استخدام المعدات (Utilization) عبر الوقت، لكل الأسطول أو لمشروع محدد",
            "parameters": {
                "type": "object",
                "properties": {
                    "project": {"type": "string", "description": "اسم المشروع (اختياري)"}
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_fuel_consumption",
            "description": "يكتشف الارتفاع أو الانخفاض غير الطبيعي في استهلاك الوقود لمعدة معينة أو لكل الأسطول",
            "parameters": {
                "type": "object",
                "properties": {
                    "equipment_id": {"type": "string", "description": "معرّف المعدة (اختياري)"}
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "generate_fleet_report",
            "description": "يولد تقرير أداء شامل عن كل الأسطول (استخدام، توقف، وقود، مشاكل رئيسية)",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "compute_attention_scores",
            "description": "يحسب درجة أولوية موحدة (0-100) لكل معدة بناءً على كل المؤشرات مجتمعة (Downtime + Fuel + Maintenance + ML Anomaly)، لترتيب المعدات حسب أولوية التدخل",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]

TOOL_FUNCTIONS = {
    "get_top_downtime_equipment": tools.get_top_downtime_equipment,
    "get_equipment_needing_attention": tools.get_equipment_needing_attention,
    "explain_utilization_trend": tools.explain_utilization_trend,
    "analyze_fuel_consumption": tools.analyze_fuel_consumption,
    "generate_fleet_report": tools.generate_fleet_report,
    "compute_attention_scores": ml_anomaly.compute_attention_scores,
}

SYSTEM_PROMPT = """أنت FleetOps AI، مساعد ذكي لعمليات أسطول معدات الإنشاء.
مهمتك: فهم سؤال المستخدم، اختيار الأداة (tool) المناسبة، تنفيذها، ثم تلخيص النتيجة
في إجابة واضحة وقابلة للتنفيذ (Insight + توصية عملية) بنفس لغة سؤال المستخدم.
لا تخترع أرقامًا؛ استخدم فقط البيانات التي ترجعها الأدوات."""


# ---------------------------------------------------------------------------
# REAL MODE: استدعاء OpenAI API فعليًا (Function Calling)
# ---------------------------------------------------------------------------
def ask_agent_real(user_question: str) -> str:
    from openai import OpenAI
    client = OpenAI()  # يقرأ OPENAI_API_KEY من البيئة تلقائيًا

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_question},
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=TOOLS_SCHEMA,
        tool_choice="auto",
    )
    msg = response.choices[0].message

    if msg.tool_calls:
        messages.append(msg)
        for call in msg.tool_calls:
            fn_name = call.function.name
            fn_args = json.loads(call.function.arguments or "{}")
            result = TOOL_FUNCTIONS[fn_name](**fn_args)
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(result, ensure_ascii=False, default=str),
            })
        final = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
        return final.choices[0].message.content

    return msg.content


# ---------------------------------------------------------------------------
# TEST MODE: Router بسيط بدون LLM (للتجربة الآن بدون API key)
# ---------------------------------------------------------------------------
def _route_question(question: str) -> tuple[str, dict]:
    q = question.lower()
    if any(k in q for k in ["أولوية موحد", "attention score", "ترتيب شامل", "priority score", "درجة الأولوية"]):
        return "compute_attention_scores", {}
    if any(k in q for k in ["تدخل فوري", "أولوية", "attention", "urgent", "priority"]):
        return "get_equipment_needing_attention", {}
    if any(k in q for k in ["وقود", "fuel", "استهلاك"]):
        return "analyze_fuel_consumption", {}
    if any(k in q for k in ["انخفض", "استخدام", "utilization", "قلّ", "قل معدل"]):
        return "explain_utilization_trend", {}
    if any(k in q for k in ["تقرير", "report", "أداء الأسطول"]):
        return "generate_fleet_report", {}
    if any(k in q for k in ["downtime", "توقف", "أعلى المعدات"]):
        return "get_top_downtime_equipment", {"top_n": 5}
    return "generate_fleet_report", {}


def _summarize(tool_name: str, result: dict) -> str:
    """توليد إجابة نصية مبسّطة من نتيجة الأداة (محاكاة تلخيص الـ LLM في وضع الاختبار)."""
    if "error" in result:
        return f"⚠️ {result['error']}"

    if tool_name == "get_top_downtime_equipment":
        lines = [f"🔧 أعلى المعدات من حيث التوقف:"]
        for r in result["data"]:
            lines.append(f"  • {r['equipment_id']} ({r['equipment_type']}, {r['project']}) — "
                         f"توقف {r['downtime_rate_%']}% | صيانة {r['maintenance_events']} مرة")
        return "\n".join(lines)

    if tool_name == "get_equipment_needing_attention":
        if not result["data"]:
            return "✅ لا توجد معدات تحتاج تدخل فوري حاليًا."
        lines = ["🚨 معدات تحتاج تدخل فوري:"]
        for r in result["data"]:
            lines.append(f"  • {r['equipment_id']} ({r['equipment_type']}, {r['project']}) — السبب: {r['reason']}")
        return "\n".join(lines)

    if tool_name == "explain_utilization_trend":
        direction = "انخفاض 📉" if result["change_%"] < 0 else "ارتفاع/استقرار 📈"
        return (
            f"📊 معدل الاستخدام في ({result['scope']}): من {result['first_3_weeks_avg_%']}% "
            f"إلى {result['last_3_weeks_avg_%']}% ({direction}, تغيّر {result['change_%']}%).\n"
            f"السبب الأرجح: توقف مرتفع في معدات نوع '{result['likely_driver_equipment_type']}' مؤخرًا."
        )

    if tool_name == "analyze_fuel_consumption":
        if result["anomalies_found"] == 0:
            return "✅ لا توجد قفزات غير طبيعية في استهلاك الوقود حاليًا."
        lines = [f"⛽ تم اكتشاف {result['anomalies_found']} حالة شذوذ في استهلاك الوقود:"]
        for r in result["data"]:
            lines.append(f"  • {r['equipment_id']} ({r['equipment_type']}) — {r['flag']} بنسبة {r['change_%']}% "
                         f"({r['baseline_l_per_hr']} → {r['recent_l_per_hr']} لتر/ساعة)")
        lines.append("💡 التوصية: فحص ميكانيكي فوري (تسريب/فلتر/محرك) للمعدات المذكورة.")
        return "\n".join(lines)

    if tool_name == "generate_fleet_report":
        lines = [
            f"📋 تقرير أداء الأسطول ({result['period']})",
            f"  • عدد المعدات: {result['fleet_size']}",
            f"  • معدل الاستخدام العام: {result['overall_utilization_%']}%",
            f"  • إجمالي ساعات التشغيل: {result['total_operating_hours']} | التوقف: {result['total_downtime_hours']}",
            f"  • إجمالي استهلاك الوقود: {result['total_fuel_l']} لتر",
            "  • أهم 3 مشاكل توقف: " + ", ".join(d["equipment_id"] for d in result["top_downtime_equipment"]),
        ]
        if result["fuel_anomalies"]:
            lines.append("  • تنبيه وقود: " + ", ".join(a["equipment_id"] for a in result["fuel_anomalies"]))
        return "\n".join(lines)

    if tool_name == "compute_attention_scores":
        lines = ["🎯 ترتيب المعدات حسب درجة الأولوية الموحدة (0-100):"]
        for r in result["data"][:10]:
            lines.append(f"  • {r['equipment_id']} ({r['equipment_type']}, {r['project']}) — "
                         f"Attention Score: {r['attention_score']}/100")
        return "\n".join(lines)

    return json.dumps(result, ensure_ascii=False, default=str)


def ask_agent_test(user_question: str) -> str:
    tool_name, args = _route_question(user_question)
    result = TOOL_FUNCTIONS[tool_name](**args)
    return _summarize(tool_name, result)


# ---------------------------------------------------------------------------
# نقطة الدخول الموحدة: يختار real أو test تلقائيًا
# ---------------------------------------------------------------------------
def ask_agent(user_question: str) -> str:
    if os.getenv("OPENAI_API_KEY"):
        return ask_agent_real(user_question)
    return ask_agent_test(user_question)


if __name__ == "__main__":
    questions = [
        "ما المعدات التي لديها أعلى Downtime؟",
        "أي المعدات تحتاج إلى تدخل فوري؟",
        "لماذا انخفض معدل استخدام المعدات؟",
        "ما أسباب ارتفاع استهلاك الوقود؟",
        "أنشئ لي تقريرًا عن أداء الأسطول",
    ]
    for q in questions:
        print(f"\n❓ السؤال: {q}")
        print(ask_agent(q))
        print("-" * 60)
