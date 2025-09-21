import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# تحميل البيانات من sales.csv
df = pd.read_csv("sales.csv")

# استخراج أسماء الشهور
months = df.columns[1:]

# تنظيف الأرقام
for col in months:
    df[col] = df[col].astype(str).str.replace(",", "").str.strip()
    df[col] = pd.to_numeric(df[col], errors="coerce")

# إعداد الصفحة
st.set_page_config(page_title="لوحة تحليل المبيعات", layout="wide")
st.title("📊 لوحة تحليل المبيعات حسب طرق الدفع والشهور")

# ===== 🎛️ الفلاتر =====
st.sidebar.header("خيارات العرض")
selected_methods = st.sidebar.multiselect("اختر طرق الدفع", options=df["حالة الدفع"].unique(), default=df["حالة الدفع"].unique())
selected_months = st.sidebar.multiselect("اختر الشهور", options=months, default=list(months))

# تصفية البيانات
filtered_df = df[df["حالة الدفع"].isin(selected_methods)][["حالة الدفع"] + selected_months]
df_long = filtered_df.melt(id_vars=["حالة الدفع"], var_name="الشهر", value_name="القيمة")

# ===== 📋 جدول البيانات =====
st.subheader("📋 البيانات بعد التنظيف والتصفية")
st.dataframe(filtered_df)

# ===== 📈 تطور طرق الدفع عبر الشهور =====
fig_line = px.line(
    df_long, x="الشهر", y="القيمة", color="حالة الدفع", markers=True,
    title="تطور طرق الدفع عبر الشهور",
    color_discrete_sequence=px.colors.qualitative.Set2
)
st.plotly_chart(fig_line, use_container_width=True)

# ===== 🥧 رسم دائري لكل شهر =====
st.subheader("🥧 توزيع المشتريات حسب طريقة الدفع لكل شهر")
for month in selected_months:
    month_data = filtered_df[["حالة الدفع", month]].dropna()
    fig_pie = px.pie(
        month_data, names="حالة الدفع", values=month,
        title=f"توزيع طرق الدفع - {month}",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ===== 📊 تحليل إحصائي لكل طريقة دفع =====
st.subheader("📊 تحليل متوسط الأداء والتذبذب والمدى")
stats = df_long.groupby("حالة الدفع")["القيمة"].agg(["mean", "std", "min", "max"])
stats["range"] = stats["max"] - stats["min"]
stats["change_rate"] = stats["range"] / stats["mean"]
stats = stats.sort_values(by="mean", ascending=False)
st.dataframe(stats.style.format("{:,.0f}"))

# ===== 📉 متوسط المشتريات =====
fig_avg = px.bar(
    stats.reset_index(), x="حالة الدفع", y="mean",
    title="متوسط المشتريات لكل طريقة دفع",
    color="حالة الدفع", color_discrete_sequence=px.colors.qualitative.Bold
)
st.plotly_chart(fig_avg, use_container_width=True)

# ===== 📉 التذبذب =====
fig_std = px.bar(
    stats.reset_index(), x="حالة الدفع", y="std",
    title="تذبذب الأداء (الانحراف المعياري)",
    color="حالة الدفع", color_discrete_sequence=px.colors.qualitative.Prism
)
st.plotly_chart(fig_std, use_container_width=True)

# ===== 📆 إجمالي المشتريات لكل شهر =====
st.subheader("📆 إجمالي المشتريات لكل شهر")
total_per_month = df[months].sum().reset_index()
total_per_month.columns = ["الشهر", "الإجمالي"]
fig_total = px.bar(
    total_per_month, x="الشهر", y="الإجمالي",
    title="إجمالي المشتريات الشهرية",
    color="الشهر", color_discrete_sequence=px.colors.qualitative.Set1
)
st.plotly_chart(fig_total, use_container_width=True)

# ===== 🥧 رسم دائري للإجمالي حسب طريقة الدفع =====
st.subheader("🥧 توزيع إجمالي المشتريات حسب طريقة الدفع")
total_by_method = df.set_index("حالة الدفع")[months].sum(axis=1).reset_index()
total_by_method.columns = ["حالة الدفع", "الإجمالي"]
fig_pie_total = px.pie(
    total_by_method, names="حالة الدفع", values="الإجمالي",
    title="نسب توزيع طرق الدفع",
    color_discrete_sequence=px.colors.qualitative.Set3
)
st.plotly_chart(fig_pie_total, use_container_width=True)

# ===== 💬 توصيات وتحفيز =====
st.subheader("💬 توصيات مالية وتحفيزية")
for index, row in stats.iterrows():
    avg = row["mean"]
    std = row["std"]
    rate = row["change_rate"]
    if avg > df_long["القيمة"].mean() and std < df_long["القيمة"].std():
        st.markdown(f"- {index}: أداء قوي ومتزن، مناسب للتوسع المالي بثقة.")
    elif rate < 0.2:
        st.markdown(f"- {index}: تذبذب منخفض، مثالي للتخطيط طويل المدى.")
    elif std > df_long["القيمة"].std():
        st.markdown(f"- {index}: تذبذب مرتفع، راقب الأداء الشهري بعناية.")
    else:
        st.markdown(f"- {index}: أداء متوسط، يمكن تحسينه بتعديل شروط الدفع أو التوقيت.")