import streamlit as st
import pandas as pd
import plotly.express as px

# إعداد الصفحة
st.set_page_config(page_title="لوحة تحليل المناطق", layout="wide")
st.title("📊 لوحة تحليل المناطق حسب الأشهر")

# البيانات الأصلية
data = {
    "المنطقة": [
        "بينين القطار", "الخانكة", "قليوب", "القناطر الخيرية", "بهتيم",
        "طوخ", "مشكل السوق", "كبار العملاء", "مخازن"
    ],
    "يوليو": [1826209, 1700581, 1922788, 2635189, 1922788, 1196735, 9, 2, 5],
    "أغسطس": [1826639, 1728044, 1933102, 2586612, 1933102, 1196735, 11, 4, 6],
    "سبتمبر": [1872665, 1775200, 1954452, 2568287, 1954452, 1278903, 22, 2, 4]
}
df = pd.DataFrame(data)

# تحويل البيانات إلى شكل طويل
df_melted = df.melt(id_vars="المنطقة", var_name="الشهر", value_name="القيمة")

# الفلاتر
selected_regions = st.multiselect("اختر المناطق", options=df["المنطقة"].unique(), default=df["المنطقة"].unique())
selected_months = st.multiselect("اختر الأشهر", options=["يوليو", "أغسطس", "سبتمبر"], default=["يوليو", "أغسطس", "سبتمبر"])

# تصفية البيانات حسب الفلاتر
filtered_df = df_melted[
    df_melted["المنطقة"].isin(selected_regions) &
    df_melted["الشهر"].isin(selected_months)
]

# 🎨 رسم بياني شريطي
st.subheader("📈 الرسم البياني الشريطي")
fig_bar = px.bar(
    filtered_df,
    x="المنطقة",
    y="القيمة",
    color="الشهر",
    barmode="group",
    text_auto=True,
    title="مقارنة المناطق حسب الأشهر"
)
st.plotly_chart(fig_bar, use_container_width=True)

# 📉 رسم بياني خطي
st.subheader("📉 الرسم البياني الخطي")
fig_line = px.line(
    filtered_df,
    x="الشهر",
    y="القيمة",
    color="المنطقة",
    markers=True,
    title="تطور القيم عبر الأشهر"
)
st.plotly_chart(fig_line, use_container_width=True)

# 📋 جدول البيانات
st.subheader("📋 جدول البيانات")
pivot_df = filtered_df.pivot(index="المنطقة", columns="الشهر", values="القيمة")
st.dataframe(pivot_df.style.highlight_max(axis=1, color="lightgreen").highlight_min(axis=1, color="salmon"))

# 🧮 مؤشرات الأداء
st.subheader("📌 مؤشرات الأداء")
for month in selected_months:
    max_row = df.loc[df[month].idxmax()]
    min_row = df.loc[df[month].idxmin()]
    st.markdown(f"🔹 في شهر **{month}**:")
    st.markdown(f"- أعلى قيمة: **{max_row['المنطقة']}** بـ **{max_row[month]:,}**")
    st.markdown(f"- أقل قيمة: **{min_row['المنطقة']}** بـ **{min_row[month]:,}**")

# 🤖 مساعد افتراضي بيعلق على البيانات
st.subheader("🤖 مساعد التحليل الذكي")
for region in selected_regions:
    row = df[df["المنطقة"] == region].iloc[0]
    diff = row["سبتمبر"] - row["يوليو"]
    trend = "📈 زيادة" if diff > 0 else "📉 انخفاض"
    st.markdown(f"- المنطقة **{region}** شهدت {trend} بمقدار **{abs(diff):,}** بين يوليو وسبتمبر.")

# ✨ لمسة جمالية
st.markdown("---")
st.markdown("🎨 تم تنفيذ هذه اللوحة بواسطة محمد، فنان البيانات وصانع البوتات الساحرة 💡")