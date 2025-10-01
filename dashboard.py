import streamlit as st
import pandas as pd
import plotly.express as px

# إعداد الصفحة
st.set_page_config(page_title="لوحة تحليل المناطق", layout="wide")
st.title("📊 لوحة تحليل المناطق حسب الأشهر")

# البيانات المصححة
data = {
    "المنطقة": [
        "شبين القناطر", "الخانكة", "قليوب", "القناطر الخيرية", "بنها",
        "طوخ", "مشتول السوق", "كبار العملاء", "المخازن"
    ],
    "يوليو": [1826209, 1700581, 1922788, 2635189, 1922788, 1196735, 9, 2, 5],
    "أغسطس": [1826639, 1728044, 1933102, 2586612, 1933102, 1196735, 11, 4, 6],
    "سبتمبر": [1872665, 1775200, 1954452, 2568287, 1954452, 1278903, 22, 2, 4]
}
df = pd.DataFrame(data)

# إضافة الإجمالي والتغير
df["الإجمالي"] = df[["يوليو", "أغسطس", "سبتمبر"]].sum(axis=1)
df["التغير"] = df["سبتمبر"] - df["يوليو"]

# تحويل البيانات إلى شكل طويل
df_melted = df.melt(id_vars=["المنطقة", "الإجمالي", "التغير"], var_name="الشهر", value_name="القيمة")

# 🎛️ الفلاتر
selected_regions = st.multiselect("اختر المناطق", options=df["المنطقة"].unique(), default=df["المنطقة"].unique())
selected_months = st.multiselect("اختر الأشهر", options=["يوليو", "أغسطس", "سبتمبر"], default=["يوليو", "أغسطس", "سبتمبر"])

# تصفية البيانات حسب الفلاتر
filtered_df = df_melted[
    df_melted["المنطقة"].isin(selected_regions) &
    df_melted["الشهر"].isin(selected_months)
]

# 📊 رسم بياني شريطي
st.subheader("📊 الرسم الشريطي المقارن")
fig_bar = px.bar(
    filtered_df,
    x="المنطقة",
    y="القيمة",
    color="الشهر",
    barmode="group",
    text_auto=True,
    title="مقارنة المناطق حسب الأشهر",
    color_discrete_sequence=px.colors.qualitative.Set2
)
st.plotly_chart(fig_bar, use_container_width=True)

# 📉 رسم بياني خطي
st.subheader("📉 الرسم الخطي لتطور القيم")
fig_line = px.line(
    filtered_df,
    x="الشهر",
    y="القيمة",
    color="المنطقة",
    markers=True,
    title="تطور القيم عبر الأشهر"
)
st.plotly_chart(fig_line, use_container_width=True)

# 🥧 رسم دائري لأعلى 5 مناطق حسب الإجمالي
st.subheader("🥧 الرسم الدائري لأعلى 5 مناطق")
top5 = df[df["المنطقة"].isin(selected_regions)].sort_values("الإجمالي", ascending=False).head(5)
fig_pie = px.pie(
    top5,
    names="المنطقة",
    values="الإجمالي",
    title="نسبة مساهمة المناطق في الإجمالي",
    hole=0.4
)
st.plotly_chart(fig_pie, use_container_width=True)

# 🔵 رسم فقاعي للتغير بين يوليو وسبتمبر
st.subheader("🔵 الرسم الفقاعي للتغير بين يوليو وسبتمبر")
bubble_df = df[df["المنطقة"].isin(selected_regions)].copy()
bubble_df["التغير"] = bubble_df["التغير"].apply(lambda x: max(x, 1))  # منع القيم السالبة أو الصفرية

fig_bubble = px.scatter(
    bubble_df,
    x="يوليو",
    y="سبتمبر",
    size="التغير",
    color="المنطقة",
    hover_name="المنطقة",
    title="تغير القيم بين يوليو وسبتمبر",
    size_max=60
)
st.plotly_chart(fig_bubble, use_container_width=True)

# 📋 جدول البيانات
st.subheader("📋 جدول البيانات")
pivot_df = filtered_df.pivot(index="المنطقة", columns="الشهر", values="القيمة")
st.dataframe(pivot_df.style.highlight_max(axis=1, color="lightgreen").highlight_min(axis=1, color="salmon"))

# 📌 مؤشرات الأداء
st.subheader("📌 مؤشرات الأداء")
for month in selected_months:
    max_row = df.loc[df[month].idxmax()]
    min_row = df.loc[df[month].idxmin()]
    st.markdown(f"🔹 في شهر **{month}**:")
    st.markdown(f"- أعلى قيمة: **{max_row['المنطقة']}** بـ **{max_row[month]:,}**")
    st.markdown(f"- أقل قيمة: **{min_row['المنطقة']}** بـ **{min_row[month]:,}**")

# 🤖 مساعد التحليل الذكي
st.subheader("🤖 مساعد التحليل الذكي")
for region in selected_regions:
    row = df[df["المنطقة"] == region].iloc[0]
    diff = row["سبتمبر"] - row["يوليو"]
    trend = "📈 زيادة" if diff > 0 else "📉 انخفاض"
    emoji = "🔥" if abs(diff) > 50000 else "✨"
    st.markdown(f"- المنطقة **{region}** شهدت {trend} بمقدار **{abs(diff):,}** بين يوليو وسبتمبر {emoji}")

# 🧪 مقارنة خاصة لمنطقة المخازن
st.subheader("🧪 مقارنة خاصة لمنطقة المخازن")
warehouse_row = df[df["المنطقة"] == "المخازن"].iloc[0]
avg_all = df[["يوليو", "أغسطس", "سبتمبر"]].mean().mean()
warehouse_avg = warehouse_row[["يوليو", "أغسطس", "سبتمبر"]].mean()

st.markdown(f"🔍 متوسط منطقة **المخازن** عبر الأشهر: **{warehouse_avg:.2f}**")
st.markdown(f"📊 متوسط باقي المناطق: **{avg_all:.2f}**")
comparison = "أقل من المتوسط العام 📉" if warehouse_avg < avg_all else "أعلى من المتوسط العام 📈"
st.markdown(f"📌 النتيجة: أداء المخازن **{comparison}**")

fig_warehouse = px.bar(
    x=["المخازن", "متوسط باقي المناطق"],
    y=[warehouse_avg, avg_all],
    labels={"x": "المقارنة", "y": "المتوسط"},
    title="📊 مقارنة أداء منطقة المخازن بالمتوسط العام",
    color=["المخازن", "متوسط باقي المناطق"],
    color_discrete_sequence=["#636EFA", "#EF553B"]
)
st.plotly_chart(fig_warehouse, use_container_width=True)

# 🎨 لمسة محمد
st.markdown("---")
st.markdown("🎨 تم تنفيذ هذه اللوحة بواسطة محمد، فنان البيانات وصانع البوتات الساحرة 💡")