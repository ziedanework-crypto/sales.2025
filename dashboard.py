import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# تحميل البيانات
df = pd.read_csv("sales.csv")

# استخراج أسماء الشهور
months = df.columns[1:]

# تنظيف الأرقام
for col in months:
    df[col] = df[col].astype(str).str.replace(",", "").str.strip()
    df[col] = pd.to_numeric(df[col], errors="coerce")

# إعداد الصفحة
st.set_page_config(page_title="لوحة تحليل المشتريات", layout="wide")
st.title("📊 لوحة تحليل المشتريات حسب طرق الدفع والشهور")

# ===== 🎛️ الفلاتر =====
st.sidebar.header("خيارات العرض")
selected_methods = st.sidebar.multiselect("اختر طرق الدفع", options=df["حالة الدفع"].unique(), default=df["حالة الدفع"].unique())
selected_months = st.sidebar.multiselect("اختر الشهور", options=months, default=list(months))
compare_methods = st.sidebar.multiselect("قارن بين طريقتين دفع", options=df["حالة الدفع"].unique(), default=[])

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

# ===== 🥧 رسوم دائرية جنب بعض =====
st.subheader("🥧 توزيع المشتريات حسب طريقة الدفع لكل شهر")
chunk_size = 3
month_chunks = [selected_months[i:i+chunk_size] for i in range(0, len(selected_months), chunk_size)]

for chunk in month_chunks:
    cols = st.columns(len(chunk))
    for i, month in enumerate(chunk):
        with cols[i]:
            month_data = filtered_df[["حالة الدفع", month]].dropna()
            fig_pie = px.pie(
                month_data, names="حالة الدفع", values=month,
                title=f"{month}",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig_pie, use_container_width=True)

# ===== 📊 تحليل إحصائي شامل =====
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

# ===== 🆚 مقارنة بين طريقتين دفع =====
if len(compare_methods) == 2:
    st.subheader(f"🆚 مقارنة مباشرة بين {compare_methods[0]} و {compare_methods[1]}")
    df_compare = df[df["حالة الدفع"].isin(compare_methods)][["حالة الدفع"] + list(selected_months)]
    df_compare_long = df_compare.melt(id_vars=["حالة الدفع"], var_name="الشهر", value_name="القيمة")
    fig_compare = px.line(
        df_compare_long, x="الشهر", y="القيمة", color="حالة الدفع", markers=True,
        title="مقارنة الأداء بين طريقتين دفع",
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    st.plotly_chart(fig_compare, use_container_width=True)

# ===== 📆 أعلى وأقل شهر لكل طريقة دفع =====
st.subheader("📆 أعلى وأقل شهر لكل طريقة دفع")
for method in selected_methods:
    row = df[df["حالة الدفع"] == method][selected_months].T
    row.columns = ["القيمة"]
    row["الشهر"] = row.index
    max_row = row.loc[row["القيمة"].idxmax()]
    min_row = row.loc[row["القيمة"].idxmin()]
    st.markdown(f"""
    - **{method}**  
      أعلى شهر: {max_row['الشهر']} بمشتريات {int(max_row['القيمة']):,}  
      أقل شهر: {min_row['الشهر']} بمشتريات {int(min_row['القيمة']):,}
    """)

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