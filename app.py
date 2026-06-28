import streamlit as st
import pandas as pd

st.set_page_config(page_title="مساعد الراشد الذكي", layout="centered")

@st.cache_data
def load_data():
    return pd.read_excel('shops.xlsx')

df = load_data()

st.title("✨ 🤖 مساعدك الذكي في الراشد ميجا مول")

# 1. اختيار الفئة المستهدفة أولاً
target = st.selectbox("👤 اختر الفئة المستهدفة:", ["نساء", "رجال", "أطفال", "الكل"])

# 2. فلترة البيانات الذكية بناءً على الفئة المستهدفة
if target == "نساء":
    filtered_df = df[df['الفئة المستهدفة'].isin(["نساء", "الكل"])]
    available_categories = sorted(filtered_df['التصنيف الرئيسي'].unique())
elif target == "رجال":
    filtered_df = df[df['الفئة المستهدفة'].isin(["رجال", "الكل"])]
    filtered_df = filtered_df[~filtered_df['التصنيف الرئيسي'].isin(["عبايات", "لانجري وملابس داخلية", "انجري وملابس داخلية"])]
    available_categories = sorted(filtered_df['التصنيف الرئيسي'].unique())
elif target == "أطفال":
    filtered_df = df[df['الفئة المستهدفة'].isin(["أطفال", "الكل"])]
    filtered_df = filtered_df[~filtered_df['التصنيف الرئيسي'].isin(["عبايات", "لانجري وملابس داخلية", "انجري وملابس داخلية"])]
    available_categories = sorted(filtered_df['التصنيف الرئيسي'].unique())
else:
    # 🎯 هنا الفكرة: إذا اختار "الكل"، يظهر له خيار واحد فقط في التصنيف الرئيسي وهو "الكل"
    filtered_df = df
    available_categories = ["الكل"]

# 3. اختيار التصنيف الرئيسي (سيظهر "الكل" فقط في حال اختيار الفئة "الكل")
category = st.selectbox("🛍️ اختر التصنيف الرئيسي:", available_categories)

# 4. اختيار مستوى الأسعار المفضّل
price = st.selectbox("💰 مستوى الأسعار المفضّل:", ["اقتصادي", "متوسط", "مرتفع"])

# 🧠 تطبيق منطق الأسعار التراكمي المتفق عليه
if price == "اقتصادي":
    price_filter = ["اقتصادي"]
elif price == "متوسط":
    price_filter = ["متوسط", "اقتصادي"]
else:
    price_filter = ["مرتفع", "متوسط", "اقتصادي"]

# الفلترة النهائية بناءً على التصنيف والسعر
if category == "الكل":
    # إذا كان التصنيف "الكل"، نعرض كل محلات المول التي تطابق السعر المختار فقط بدون تصفية التصنيف
    final_df = filtered_df[filtered_df['مستوى الأسعار'].isin(price_filter)]
else:
    # الفلترة العادية لبقية الفئات والتصنيفات
    final_df = filtered_df[(filtered_df['التصنيف الرئيسي'] == category) & 
                            (filtered_df['مستوى الأسعار'].isin(price_filter))]

# زر عرض واقتراح النتائج
if st.button("اقترح لي المحلات ✨"):
    if not final_df.empty:
        st.success("📌 المحلات المقترحة لك:")
        for shop in final_df['اسم المحل'].unique():
            st.markdown(f"- **{shop}**")
    else:
        st.warning("للأسف، لا توجد محلات تطابق هذه الاختيارات بمستوى السعر المختار حالياً.")
