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

# 2. منطق الدمج الذكي للخلفية (تجهيز البيانات بناءً على الفئة لتضمين العام)
if target == "نساء":
    filtered_by_target = df[df['الفئة المستهدفة'].isin(["نساء", "الكل"])]
elif target == "رجال":
    filtered_by_target = df[df['الفئة المستهدفة'].isin(["رجال", "الكل"])]
elif target == "أطفال":
    filtered_by_target = df[df['الفئة المستهدفة'].isin(["أطفال", "الكل"])]
else:
    filtered_by_target = df

# 3. جلب التصنيفات المتاحة المفلترة تلقائياً
available_categories = sorted(filtered_by_target['التصنيف الرئيسي'].unique())

# 4. اختيار التصنيف الرئيسي الذكي
category = st.selectbox("🛍️ اختر التصنيف الرئيسي:", available_categories)

# 5. اختيار مستوى الأسعار المفضّل
price = st.selectbox("💰 مستوى الأسعار المفضّل:", ["اقتصادي", "متوسط", "مرتفع"])

# 🧠 تطبيق منطق الأسعار التراكمي المتفق عليه:
if price == "اقتصادي":
    price_filter = ["اقتصادي"]
elif price == "متوسط":
    price_filter = ["متوسط", "اقتصادي"]  # المتوسط يرى المتوسط والاقتصادي
else:
    price_filter = ["مرتفع", "متوسط", "اقتصادي"]  # المرتفع يرى كل المستويات

# الفلترة النهائية وعرض النتائج للمستخدم
final_df = filtered_by_target[(filtered_by_target['التصنيف الرئيسي'] == category) & 
                               (filtered_by_target['مستوى الأسعار'].isin(price_filter))]

# زر عرض واقتراح النتائج
if st.button("اقترح لي المحلات ✨"):
    if not final_df.empty:
        st.success("📌 المحلات المقترحة لك:")
        for shop in final_df['اسم المحل'].unique():
            st.markdown(f"- **{shop}**")
    else:
        st.warning("للأسف، لا توجد محلات تطابق هذه الاختيارات بمستوى السعر المختار حالياً.")
