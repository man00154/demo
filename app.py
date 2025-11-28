import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="BMS Anomaly Dashboard", layout="wide")

st.title("Data Center BMS – Anomaly FAQ & Power Trend Demo")

st.markdown("""
This UI provides:
- A dropdown menu to select anomaly-related queries  
- Auto-generated explanations  
- A demo time-series graph of power consumption  
""")

# ----------------------- FAQ ANSWERS -----------------------
faq_answers = {
    "Higher ambient temperature": """
Higher ambient temperature increases heat load on the cooling system.
Expected impacts:
- Higher chiller/CRAC runtime
- Higher cooling power usage
- Increased anomaly score if values drift beyond normal baseline
""",

    "Increase in IT load": """
IT load increase causes rise in:
- Rack-level power
- Heat generation
- Cooling demand

If cooling does not scale proportionally, anomaly score increases.
""",

    "Increase in chilled water inlet temperature": """
Higher inlet temperature reduces cooling efficiency and may trigger:
- Higher room temperatures
- Longer chiller runtimes
- Energy inefficiencies

Model flags this as anomaly when deviation is large.
""",

    "What exactly triggers a high anomaly score": """
A high anomaly score occurs when real-time behavior deviates significantly
from baseline patterns for similar environmental and load conditions.
""",

    "How the operations team should interpret each category": """
Green = Normal  
Amber = Monitor closely  
Red = Immediate investigation needed  
""",

    "What actions need to be taken for different anomaly levels": """
Low: Monitor  
Medium: Check sensors & logs  
High: Immediate investigation, raise incident  
""",

    "Which parameters the model uses (runtime, performance degradation, fleet score, etc.)": """
Model commonly uses:
- Power, runtime, temperatures
- Cooling/airflow data
- Fleet comparison metrics
- Performance degradation indicators
""",

    "How operations should decide on maintenance priority": """
Focus on:
1. High anomaly assets  
2. Redundancy level  
3. SLA impact  
4. CMMS history  
""",

    "Also, since we have CMMS–Anavaya with full history of PPM records (available via API), please confirm if this data can be integrated for better accuracy": """
Yes, CMMS–Anavaya PPM data can be integrated.
Use API history to enrich anomaly prediction and maintenance actions.
""",

    "Health KPIs and thresholds": """
Common KPIs:
- COP/EER
- Rack inlet temperature compliance
- UPS efficiency
- PUE & energy KPIs
""",

    "What conditions require immediate escalation by the operations team": """
Escalate when:
- Critical temperature breaches  
- Loss of N+1 redundancy  
- Repeated high anomalies  
""",

    "What triggers an internal alert from the model": """
Alert is triggered when:
- Anomaly > threshold  
- Sudden spike  
- Persistent moderate anomalies  
"""
}

# ----------------------- UI LAYOUT -----------------------
col1, col2 = st.columns([1.3, 1])

with col1:
    st.subheader("Anomaly Explanation – FAQ")

    question = st.selectbox(
        "Select a query:", 
        list(faq_answers.keys())
    )

    st.markdown("### Answer")
    st.markdown(faq_answers[question])

with col2:
    st.subheader("Demo: Power Consumption (kW) vs Time")

    end_time = datetime.now()
    start_time = end_time - timedelta(hours=24)
    timestamps = pd.date_range(start=start_time, end=end_time, freq="15min")

    base_kw = 500
    noise = np.random.normal(0, 15, len(timestamps))
    bump = np.exp(-((np.arange(len(timestamps)) - len(timestamps)/2)**2)
                 / (2 * (len(timestamps)/10)**2)) * 80

    power_kw = base_kw + noise + bump

    df_power = pd.DataFrame({"Timestamp": timestamps, "Power_kW": power_kw})
    df_power = df_power.set_index("Timestamp")

    st.line_chart(df_power, y="Power_kW")
    st.caption("DEMO")
