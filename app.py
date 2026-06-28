import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="مساعد الراشد الذكي | Alrashid Mall Assistant", layout="centered")

@st.cache_data
def load_data():
    return pd.read_excel('shops.xlsx')

df = load_data()

# 🌐 إدارة حالة اللغة
if 'lang' not in st.session_state:
    st.session_state.lang = 'ar'
if st.session_state.lang == "ar":
    direction = "rtl"
    align = "right"
else:
    direction = "ltr"
    align = "left"

st.markdown(f"""
<style>

/* اتجاه الصفحة حسب اللغة */
.stApp {{
    direction: {direction};
    text-align: {align};
}}

/* محاذاة النصوص */
h1, h2, h3, p, label {{
    text-align: {align} !important;
}}

/* القوائم المنسدلة */
div[data-baseweb="select"] {{
    direction: {direction};
}}

/* أزرار المحلات */
div.stButton > button {{
    color: black !important;
    font-weight: 700 !important;
    font-size: 18px !important;
}}

div.stButton > button p {{
    text-align: center !important;
    color: black !important;
    font-weight: bold !important;
}}

</style>
""", unsafe_allow_html=True)

# 📝 إعداد نصوص الواجهة
if st.session_state.lang == 'ar':
    title_text = "✨ مُستشارك للتسوق "
    lbl_target = "👤 اختر الفئة المستهدفة:"
    lbl_category = "🛍️ اختر التصنيف الرئيسي:"
    lbl_price = "💰 مستوى الأسعار:"
    lbl_btn = "اقترح المحلات المناسبة ✨"
    lbl_success = "📌 المحلات المقترحة لك:"
    lbl_warning = "للأسف، لا توجد محلات تطابق هذه الاختيارات."
    targets_opts = ["نساء", "رجال", "أطفال", "الكل"]
    price_opts = ["اقتصادي", "متوسط", "مرتفع", "الكل"]
    all_word = "الكل"
    col_name, col_target, col_cat, col_price = 'اسم المحل', 'الفئة المستهدفة', 'التصنيف الرئيسي', 'مستوى الأسعار'
else:
    title_text = "✨Shopping Assistant"
    lbl_target = "👤 Select Target Audience:"
    lbl_category = "🛍️ Select Main Category:"
    lbl_price = "💰 Price Level:"
    lbl_btn = "Suggest Shops ✨"
    lbl_success = "📌 Recommended Shops for you:"
    lbl_warning = "Unfortunately, no shops match these criteria."
    targets_opts = ["Women", "Men", "Children", "All"]
    price_opts = ["Affordable", "Medium", "Premium", "All"]
    all_word = "All"
    col_name, col_target, col_cat, col_price = 'Shop_Name', 'Target_Audience', 'Category', 'Price_Level'

# 🏛️ تصميم الهيدر (الشعار والعنوان وزر اللغة)
header_col1, header_col2 = st.columns([7, 3])
with header_col1:
    if st.session_state.lang == 'ar':
        if st.button("English"):
            st.session_state.lang = 'en'
            st.rerun()
    else:
        if st.button("عربي"):
            st.session_state.lang = 'ar'
            st.rerun()
    st.title(title_text)

with header_col2:
    if os.path.exists('logo.jpg'):
        st.image('logo.jpg', width=130)

st.write("---")

# 1. القوائم المنسدلة للاختيار
target_sel = st.selectbox(lbl_target, targets_opts)

# 2. فلترة الفئة المستهدفة
if target_sel in ["نساء", "Women"]:
    filtered_df = df[df[col_target].isin(["نساء", "الكل", "Women", "All"])]
elif target_sel in ["رجال", "Men"]:
    filtered_df = df[df[col_target].isin(["رجال", "الكل", "Men", "All"])]
    filtered_df = filtered_df[~filtered_df[col_cat].isin(["عبايات", "لانجري وملابس داخلية", "Abayas", "Lingerie"])]
elif target_sel in ["أطفال", "Children"]:
    filtered_df = df[df[col_target].isin(["أطفال", "الكل", "Children", "All"])]
    filtered_df = filtered_df[~filtered_df[col_cat].isin(["عبايات", "لانجري وملابس داخلية", "Abayas", "Lingerie"])]
else:
    filtered_df = df

available_categories = [all_word] if target_sel == all_word else sorted(filtered_df[col_cat].unique())

category_sel = st.selectbox(lbl_category, available_categories)
price_sel = st.selectbox(lbl_price, price_opts)

# 🧠 منطق الأسعار الذكي المختصر (بدون أسطر طويلة)
price_map = {
    "اقتصادي": ["اقتصادي"], "Affordable": ["Affordable"],
    "متوسط": ["اقتصادي", "متوسط"], "Medium": ["Affordable", "Medium"],
    "مرتفع": ["اقتصادي", "متوسط", "مرتفع"], "Premium": ["Affordable", "Medium", "Premium"]
}
price_filter = price_map.get(price_sel, df[col_price].unique().tolist())

# 5. الفلترة النهائية وعرض النتائج
if category_sel == all_word:
    final_df = filtered_df[filtered_df[col_price].isin(price_filter)]
else:
    final_df = filtered_df[(filtered_df[col_cat] == category_sel) & (filtered_df[col_price].isin(price_filter))]

st.write("")

# عرض المحلات على شكل مربعات أنيقة ومقاومة للتلف
if st.button(lbl_btn, use_container_width=True):
    if not final_df.empty:
        st.success(lbl_success)
        shops = final_df[col_name].unique()
        for i in range(0, len(shops), 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j < len(shops):
                   with cols[j]:
                       st.markdown(
                           f"""
                           <div style="
                               border: 1px solid #999;
                               border-radius: 10px;
                               padding: 15px;
                               text-align: center;
                               font-size: 18px;
                               font-weight: bold;
                               color: black;
                               background-color: white;
                               margin-bottom: 10px;
                           ">
                               {shops[i+j]}
                           </div>
                           """,
                           unsafe_allow_html=True
                       )

    else:
        st.warning(lbl_warning)
