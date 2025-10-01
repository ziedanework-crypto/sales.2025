import streamlit as st
import pandas as pd
import plotly.express as px

# إعداد الصفحة
st.set_page_config(page_title="لوحة تحليل الأداء", layout="wide")
st.title("📊 لوحة تحليل المبيعات وعدد العملاء حسب الأشهر")

# بيانات المبيعات
sales_data = {
    "المنطقة": [
        "شبين القناطر", "الخانكة", "قليوب", "القناطر الخيرية", "بنها",
        "طوخ", "مشتول السوق", "كبار العملاء", "مخازن"
    ],
    "يوليو": [1826209, 1700581, 1814119, 2635589, 1922788, 1202928, 173738, 655318, 2072813],
    "أغسطس": [1826639, 1728044, 1585191, 2586612, 1947883, 1196735, 118706, 523933, 1556964],
    "سبتمبر": [1872665, 1775200, 1657736, 2568287, 1823452, 1278903, 102311, 507172, 776063]
}
sales_df = pd.DataFrame(sales_data)

# بيانات عدد العملاء
customers_data = {
    "المنطقة": [
        "شبين القناطر", "الخانكة", "قليوب", "القناطر الخيرية", "بنها",
        "طوخ", "مشتول السوق", "كبار العملاء", "مخازن"
    ],
    "يوليو": [147, 178, 104, 136, 77, 117, 9, 2, 5],
    "أغسطس": [154, 172, 108, 147, 79, 108, 11, 2, 4],
    "سبتمبر": [149, 179, 105, 128, 87, 122, 11, 2, 4]
}
customers_df = pd.DataFrame(customers_data)

# تحويل البيانات إلى شكل طويل
sales_melted = sales_df.melt(id_vars="المنطقة", var_name="الشهر", value_name="المبيعات")
customers_melted = customers_df.melt(id_vars="المنطقة", var_name="الشهر", value_name="عدد العملاء")

# 🎛️ الفلاتر
st.sidebar.header("🎛️ الفلاتر")
selected_regions = st.sidebar.multiselect("اختر المناطق", options=sales_df["المنطقة"].unique(), default=sales_df["المنطقة"].unique())
selected_months = st.sidebar.multiselect("اختر الأشهر", options=["يوليو", "أغسطس", "سبتمبر"], default=["يوليو", "أغسطس", "سبتمبر"])

# تصفية البيانات
filtered_sales = sales_melted[
    sales_melted["المنطقة"].isin(selected_regions) &
    sales_melted["الشهر"].isin(selected_months)
]
filtered_customers = customers_melted[
    customers_melted["المنطقة"].isin(selected_regions) &
    customers_melted["الشهر"].isin(selected_months)
]

# 📈 الجزء العلوي: المبيعات
st.subheader("💰 مقارنة المبيعات حسب الأشهر")
fig_sales = px.bar(
    filtered_sales,
    x="المنطقة",
    y="المبيعات",
    color="الشهر",
    barmode="group",
    text_auto=True,
    title="📊 المبيعات الشهرية لكل منطقة",
    color_discrete_sequence=px.colors.qualitative.Set2
)
st.plotly_chart(fig_sales, use_container_width=True)

# 📉 رسم خطي للمبيعات
fig_sales_line = px.line(
    filtered_sales,
    x="الشهر",
    y="المبيعات",
    color="المنطقة",
    markers=True,
    title="📈 تطور المبيعات عبر الأشهر"
)
st.plotly_chart(fig_sales_line, use_container_width=True)

# 📊 الجزء السفلي: عدد العملاء
st.subheader("👥 مقارنة عدد العملاء حسب الأشهر")
fig_customers = px.bar(
    filtered_customers,
    x="المنطقة",
    y="عدد العملاء",
    color="الشهر",
    barmode="group",
    text_auto=True,
    title="📊 عدد العملاء الشهري لكل منطقة",
    color_discrete_sequence=px.colors.qualitative.Set3
)
st.plotly_chart(fig_customers, use_container_width=True)

# 📉 رسم خطي للعملاء
fig_customers_line = px.line(
    filtered_customers,
    x="الشهر",
    y="عدد العملاء",
    color="المنطقة",
    markers=True,
    title="📈 تطور عدد العملاء عبر الأشهر"
)
st.plotly_chart(fig_customers_line, use_container_width=True)

# 🧠 تحليل ذكي للمخازن
st.subheader("🧪 تحليل خاص لمنطقة المخازن")
warehouse_sales = sales_df[sales_df["المنطقة"] == "مخازن"].iloc[0, 1:]
warehouse_customers = customers_df[customers_df["المنطقة"] == "مخازن"].iloc[0, 1:]

sales_diff = warehouse_sales["سبتمبر"] - warehouse_sales["يوليو"]
customers_diff = warehouse_customers["سبتمبر"] - warehouse_customers["يوليو"]

sales_trend = "📈 زيادة" if sales_diff > 0 else "📉 انخفاض"
customers_trend = "📈 زيادة" if customers_diff > 0 else "📉 انخفاض"

st.markdown(f"- المبيعات في المخازن شهدت {sales_trend} بمقدار **{abs(sales_diff):,}** بين يوليو وسبتمبر.")
st.markdown(f"- عدد العملاء في المخازن شهد {customers_trend} بمقدار **{abs(customers_diff)}** خلال نفس الفترة.")

# 🎨 لمسة محمد
st.markdown("---")
st.markdown("🎨 تم تنفيذ هذه اللوحة بواسطة محمد، فنان البيانات وصانع البوتات الساحرة 💡")