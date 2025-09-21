import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# تحميل وتنظيف البيانات
df = pd.read_csv("sales.csv")
months = [col for col in df.columns if col.startswith("Sales")]
for col in months:
    df[col] = df[col].astype(str).str.replace(",", "").str.strip()
    df[col] = pd.to_numeric(df[col], errors="coerce")

# إعداد الصفحة
st.set_page_config(page_title="تحليل مبيعات المناطق", layout="wide")
st.title("تحليل مبيعات المناطق عبر الشهور")

# تحويل البيانات
df_long = df.melt(id_vars=["المنطقة"], var_name="الشهر", value_name="المبيعات")

# ===== 🎛️ الفلاتر =====
st.sidebar.header("خيارات العرض")
selected_regions = st.sidebar.multiselect("اختر المناطق", options=df["المنطقة"].unique(), default=df["المنطقة"].unique())
selected_months = st.sidebar.multiselect("اختر الشهور", options=months, default=months)
compare_regions = st.sidebar.multiselect("قارن بين منطقتين", options=df["المنطقة"].unique(), default=[])

# تصفية البيانات
filtered_df = df[df["المنطقة"].isin(selected_regions)][["المنطقة"] + selected_months]
filtered_long = filtered_df.melt(id_vars=["المنطقة"], var_name="الشهر", value_name="المبيعات")

# ===== 📋 جدول البيانات =====
st.subheader("📋 البيانات بعد التنظيف والتصفية")
st.dataframe(filtered_df)

# ===== 📈 تطور المبيعات =====
fig_line = px.line(
    filtered_long, x="الشهر", y="المبيعات", color="المنطقة", markers=True,
    title="تطور المبيعات حسب الفلاتر",
    color_discrete_sequence=px.colors.qualitative.Set2
)
st.plotly_chart(fig_line, use_container_width=True)

# ===== 📊 مقارنة المناطق =====
fig_bar = px.bar(
    filtered_long, x="الشهر", y="المبيعات", color="المنطقة", barmode="group",
    title="مقارنة المبيعات بين المناطق",
    color_discrete_sequence=px.colors.qualitative.Pastel
)
st.plotly_chart(fig_bar, use_container_width=True)

# ===== 🌡️ خريطة حرارية =====
pivot = filtered_long.pivot_table(index="المنطقة", columns="الشهر", values="المبيعات")
fig_heatmap = px.imshow(
    pivot, text_auto=True, aspect="auto",
    title="خريطة حرارية لأداء المبيعات",
    color_continuous_scale="Viridis"
)
st.plotly_chart(fig_heatmap, use_container_width=True)

# ===== 🆚 مقارنة منطقتين =====
if len(compare_regions) == 2:
    st.subheader(f"📊 مقارنة مباشرة بين {compare_regions[0]} و {compare_regions[1]}")
    df_compare = df[df["المنطقة"].isin(compare_regions)][["المنطقة"] + selected_months]
    df_compare_long = df_compare.melt(id_vars=["المنطقة"], var_name="الشهر", value_name="المبيعات")
    fig_compare = px.line(
        df_compare_long, x="الشهر", y="المبيعات", color="المنطقة", markers=True,
        title="مقارنة الأداء بين منطقتين",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    st.plotly_chart(fig_compare, use_container_width=True)

# ===== 🥇 أعلى وأقل منطقة شهريًا =====
st.subheader("🏆 تحليل شهري لأعلى وأقل منطقة")
for month in selected_months:
    month_data = filtered_df[["المنطقة", month]].dropna()
    if not month_data.empty:
        top = month_data.loc[month_data[month].idxmax()]
        low = month_data.loc[month_data[month].idxmin()]
        st.markdown(f"""
        **{month}:**
        - الأعلى مبيعًا: {top['المنطقة']} بمبيعات {int(top[month]):,}
        - الأقل مبيعًا: {low['المنطقة']} بمبيعات {int(low[month]):,}
        """)

# ===== 📊 متوسط وتذبذب ومدى =====
st.subheader("📊 تحليل متوسط الأداء والتذبذب والمدى")
summary = filtered_long.groupby("المنطقة")["المبيعات"].agg(["mean", "std", "min", "max"])
summary["range"] = summary["max"] - summary["min"]
summary["change_rate"] = summary["range"] / summary["mean"]
summary = summary.sort_values(by="mean", ascending=False)
st.dataframe(summary.style.format("{:,.0f}"))

# ===== 📉 متوسط المبيعات =====
fig_avg = px.bar(
    summary.reset_index(), x="المنطقة", y="mean",
    title="متوسط المبيعات لكل منطقة",
    color="المنطقة", color_discrete_sequence=px.colors.qualitative.Bold
)
st.plotly_chart(fig_avg, use_container_width=True)

# ===== 📉 التذبذب =====
fig_std = px.bar(
    summary.reset_index(), x="المنطقة", y="std",
    title="تذبذب الأداء (الانحراف المعياري)",
    color="المنطقة", color_discrete_sequence=px.colors.qualitative.Prism
)
st.plotly_chart(fig_std, use_container_width=True)

# ===== 📈 الاتجاه العام =====
st.subheader("📈 الاتجاه العام للمبيعات")
trend = filtered_long.groupby(["المنطقة", "الشهر"])["المبيعات"].mean().reset_index()
fig_trend = px.line(
    trend, x="الشهر", y="المبيعات", color="المنطقة",
    title="الاتجاه العام عبر الشهور",
    color_discrete_sequence=px.colors.qualitative.Dark24
)
st.plotly_chart(fig_trend, use_container_width=True)

# ===== 💬 التحفيز الذكي =====
st.subheader("💬 ملاحظات تحفيزية حسب الأداء")
for index, row in summary.iterrows():
    avg = row["mean"]
    std = row["std"]
    rng = row["range"]
    rate = row["change_rate"]
    if avg > filtered_long["المبيعات"].mean() and std < filtered_long["المبيعات"].std():
        st.markdown(f"- {index}: أداء قوي ومتزن، حافظ على الاستقرار وابدأ التوسع بثقة.")
    elif rate < 0.2:
        st.markdown(f"- {index}: أداء مستقر جدًا، جرّب استراتيجيات جديدة بثقة.")
    elif avg > filtered_long["المبيعات"].mean():
        st.markdown(f"- {index}: أداء مرتفع، لكن راقب التذبذب لضمان الاستدامة.")
    elif std < filtered_long["المبيعات"].std():
        st.markdown(f"- {index}: أداء متوسط لكن مستقر، فرصة ممتازة للتجريب.")
    else:
        st.markdown(f"- {index}: التذبذب واضح، راجع نقاط الضعف وركّز على التحسين التدريجي.")