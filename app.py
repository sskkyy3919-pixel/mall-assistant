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

# 2. فلترة البيانات الذكية بناءً على الفئة المستهدفة بشكل صارم
if target == "نساء":
    # يعرض محلات النساء + محلات الكل، لكن يستبعد تصنيفات الرجال الصريحة إن وجدت
    filtered_df = df[df['الفئة المستهدفة'].isin(["نساء", "الكل"])]
    # نضمن استبعاد أي تصنيف رئيسي لا يناسب النساء
    excluded_categories = [] 
elif target == "رجال":
    # يعرض محلات الرجال + محلات الكل
    filtered_df = df[df['الفئة المستهدفة'].isin(["رجال", "الكل"])]
    # ❌ هنا السر: نستبعد تماماً تصنيفات العبايات واللانجري من قائمة الرجال
    filtered_df = filtered_df[~filtered_df['التصنيف الرئيسي'].isin(["عبايات", "لانجري وملابس داخلية", "انجري وملابس داخلية"])]
elif target == "أطفال":
    # يعرض محلات الأطفال + محلات الكل
    filtered_df = df[df['الفئة المستهدفة'].isin(["أطفال", "الكل"])]
    # ❌ نستبعد العبايات واللانجري من قائمة الأطفال أيضاً
    filtered_df = filtered_df[~filtered_df['التصنيف الرئيسي'].isin(["عبايات", "لانجري وملابس داخلية", "انجري وملابس داخلية"])]
else:
    # إذا اختار "الكل" يظهر المول كاملاً بكل تصنيفاته
    filtered_df = df

# 3. جلب التصنيفات المتاحة المفلترة بدقة الآن (ستختفي العبايات واللانجري للرجال والأطفال!)
available_categories = sorted(filtered_df['التصنيف الرئيسي'].unique())

# 4. اختيار التصنيف الرئيسي
category = st.selectbox("🛍️ اختر التصنيف الرئيسي:", available_categories)

# 5. اختيار مستوى الأسعار المفضّل
price = st.selectbox("💰 مستوى الأسعار المفضّل:", ["اقتصادي", "متوسط", "مرتفع"])

# 🧠 تطبيق منطق الأسعار التراكمي المتفق عليه
if price == "اقتصادي":
    price_filter = ["اقتصادي"]
elif price == "متوسط":
    price_filter = ["متوسط", "اقتصادي"]
else:
    price_filter = ["مرتفع", "متوسط", "اقتصادي"]

# الفلترة النهائية بناءً على التصنيف والسعر
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
