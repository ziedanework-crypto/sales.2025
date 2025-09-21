import streamlit as st
import pandas as pd
import plotly.express as px

# تحميل وتنظيف البيانات
df = pd.read_csv("sales.csv")
months = [col for col in df.columns if col.startswith("Sales")]
for col in months:
    df[col] = df[col].astype(str).str.replace(",", "").str.strip()
    df[col] = pd.to_numeric(df[col], errors="coerce")

# إعداد الصفحة
st.set_page_config(page_title="تحليل مبيعات المناطق - رسوم دائرية", layout="wide")
st.title("تحليل مبيعات المناطق عبر الشهور - رسوم دائرية")

# ===== 🎛️ الفلاتر =====
st.sidebar.header("خيارات العرض")
selected_regions = st.sidebar.multiselect("اختر المناطق", options=df["المنطقة"].unique(), default=df["المنطقة"].unique())
selected_months = st.sidebar.multiselect("اختر الشهور", options=months, default=months)

# تصفية البيانات
filtered_df = df[df["المنطقة"].isin(selected_regions)][["المنطقة"] + selected_months]

# ===== 📋 جدول البيانات =====
st.subheader("📋 البيانات بعد التنظيف والتصفية")
st.dataframe(filtered_df)

# ===== 🥧 رسم دائري لكل شهر: توزيع المبيعات حسب المناطق =====
st.subheader("📆 توزيع المبيعات حسب المناطق لكل شهر")
for month in selected_months:
    month_data = filtered_df[["المنطقة", month]].dropna()
    fig_pie_month = px.pie(
        month_data, names="المنطقة", values=month,
        title=f"توزيع المبيعات حسب المناطق - {month}",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_pie_month, use_container_width=True)

# ===== 🥧 رسم دائري لكل منطقة: توزيع المبيعات عبر الشهور =====
st.subheader("🏘️ توزيع المبيعات حسب الشهور لكل منطقة")
for region in selected_regions:
    region_data = filtered_df[filtered_df["المنطقة"] == region][selected_months].T
    region_data.columns = ["المبيعات"]
    region_data["الشهر"] = region_data.index
    fig_pie_region = px.pie(
        region_data, names="الشهر", values="المبيعات",
        title=f"توزيع المبيعات عبر الشهور - {region}",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig_pie_region, use_container_width=True)

# ===== 💬 ملاحظات تحفيزية =====
st.subheader("💬 ملاحظات تحفيزية حسب الأداء")
for region in selected_regions:
    region_data = filtered_df[filtered_df["المنطقة"] == region][selected_months].values.flatten()
    avg = region_data.mean()
    std = region_data.std()
    rng = region_data.max() - region_data.min()
    if avg > df[months].mean().mean() and std < df[months].std().mean():
        st.markdown(f"- {region}: أداء قوي ومتزن، حافظ على الاستقرار وابدأ التوسع بثقة.")
    elif avg > df[months].mean().mean():
        st.markdown(f"- {region}: أداء مرتفع، لكن راقب التذبذب لضمان الاستدامة.")
    elif std < df[months].std().mean():
        st.markdown(f"- {region}: أداء متوسط لكن مستقر، فرصة ممتازة للتجريب.")
    else:
        st.markdown(f"- {region}: التذبذب واضح، راجع نقاط الضعف وركّز على التحسين التدريجي.")