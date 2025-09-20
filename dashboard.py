import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# تحميل البيانات من ملف CSV
df = pd.read_csv("sales_data.csv")

# تنظيف الأرقام من الفواصل وتحويلها لقيم رقمية
months = [col for col in df.columns if col.startswith("Sales")]
for col in months:
    df[col] = df[col].astype(str).str.replace(",", "").str.strip()
    df[col] = pd.to_numeric(df[col], errors="coerce")

# إعداد الصفحة
st.set_page_config(page_title="تحليل المبيعات حسب المنطقة والشهر", layout="wide")
st.title("تحليل المبيعات حسب المنطقة والشهر")

# عرض البيانات الأصلية بعد التنظيف
st.subheader("البيانات بعد التنظيف")
st.dataframe(df)

# تحويل البيانات من Wide إلى Long لتحليلها
df_long = df.melt(id_vars=["المنطقة"], var_name="الشهر", value_name="المبيعات")

# رسم بياني خطي لتطور المبيعات لكل منطقة
fig_line = px.line(df_long, x="الشهر", y="المبيعات", color="المنطقة", markers=True, title="تطور المبيعات لكل منطقة")
st.plotly_chart(fig_line, use_container_width=True)

# رسم بياني عمودي لمقارنة المبيعات في كل شهر
fig_bar = px.bar(df_long, x="الشهر", y="المبيعات", color="المنطقة", barmode="group", title="مقارنة المبيعات بين المناطق في كل شهر")
st.plotly_chart(fig_bar, use_container_width=True)

# رسم بياني حراري Heatmap لتوضيح الأداء
pivot = df_long.pivot_table(index="المنطقة", columns="الشهر", values="المبيعات")
fig_heatmap = px.imshow(pivot, text_auto=True, aspect="auto", title="خريطة حرارية لأداء المبيعات")
st.plotly_chart(fig_heatmap, use_container_width=True)

# تحليل أعلى وأقل منطقة في كل شهر
st.subheader("تحليل شهري لأعلى وأقل منطقة")
months_unique = df_long["الشهر"].unique()
for month in months_unique:
    month_data = df_long[df_long["الشهر"] == month].dropna()
    if not month_data.empty:
        top = month_data.loc[month_data["المبيعات"].idxmax()]
        low = month_data.loc[month_data["المبيعات"].idxmin()]
        st.markdown(f"""
        **{month}:**
        - الأعلى مبيعًا: {top['المنطقة']} بمبيعات {int(top['المبيعات']):,}
        - الأقل مبيعًا: {low['المنطقة']} بمبيعات {int(low['المبيعات']):,}
        """)

# تحليل المتوسط والتذبذب لكل منطقة
st.subheader("تحليل متوسط الأداء والتذبذب")
summary = df_long.groupby("المنطقة")["المبيعات"].agg(["mean", "std"]).sort_values(by="mean", ascending=False)
st.dataframe(summary.style.format({"mean": "{:,.0f}", "std": "{:,.0f}"}))

# جمل تحفيزية حسب الأداء
st.subheader("ملاحظات تحفيزية")
for index, row in summary.iterrows():
    avg = row["mean"]
    std = row["std"]
    if avg > df_long["المبيعات"].mean() and std < df_long["المبيعات"].std():
        st.markdown(f"- {index}: أداء قوي ومستقر، استمر بنفس القوة.")
    elif avg > df_long["المبيعات"].mean():
        st.markdown(f"- {index}: أداء مرتفع، حافظ على الزخم وراقب التذبذب.")
    elif std < df_long["المبيعات"].std():
        st.markdown(f"- {index}: أداء متوسط لكن مستقر، فرصة ممتازة للتوسع بثقة.")
    else:
        st.markdown(f"- {index}: التذبذب واضح، راجع الاستراتيجية وركز على نقاط القوة.")