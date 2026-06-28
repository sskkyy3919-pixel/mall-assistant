import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="مساعد الراشد الذكي | Alrashid Mall Assistant", layout="centered")

# تنسيق المربعات وتصميم الواجهة عبر CSS ليطابق الرسمة
st.markdown("""
    <style>
    .shop-box {
        background-color: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        font-weight: bold;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }
    .main-title {
        font-size: 28px;
        font-weight: bold;
        color: #b39256;
    }
    </style>
""", unsafe_allowed_code=True)

@st.cache_data
def load_data():
    return pd.read_excel('shops.xlsx')

df = load_data()

# 🌐 إدارة حالة اللغة
if 'lang' not in st.session_state:
    st.session_state.lang = 'ar'

# 📝 إعداد الترجمة والنصوص بناءً على اللغة المفضلة
if st.session_state.lang == 'ar':
    title_text = "مُستشارك للتسوق"
    lbl_target = "اختر الفئة المستهدفة:"
    lbl_category = "اختر التصنيف الرئيسي:"
    lbl_price = "مستوى الأسعار:"
    lbl_btn = "اقترح المحلات المناسبة ✨"
    lbl_success = "المحلات المقترحة لك:"
    lbl_warning = "للأسف، لا توجد محلات تطابق هذه الاختيارات."
    
    targets_opts = ["نساء", "رجال", "أطفال", "الكل"]
    price_opts = ["اقتصادي", "متوسط", "مرتفع", "الكل"]
    all_word = "الكل"
    
    col_name = 'اسم المحل'
    col_target = 'الفئة المستهدفة'
    col_cat = 'التصنيف الرئيسي'
    col_price = 'مستوى الأسعار'
else:
    title_text = "Shopping Assistant"
    lbl_target = "Select Target Audience:"
    lbl_category = "Select Main Category:"
    lbl_price = "Price Level:"
    lbl_btn = "Suggest Shops ✨"
    lbl_success = "Recommended Shops for you:"
    lbl_warning = "Unfortunately, no shops match these criteria."
    
    targets_opts = ["Women", "Men", "Children", "All"]
    price_opts = ["Affordable", "Medium", "Premium", "All"]
    all_word = "All"
    
    col_name = 'Shop_Name'
    col_target = 'Target_Audience'
    col_cat = 'Category'
    col_price = 'Price_Level'

# 🏛️ تصميم الهيدر (الشعار على اليسار والعنوان على اليمين ليطابق الرسمة)
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
    
    st.markdown(f"<div class='main-title'>{title_text}</div>", unsafe_allowed_code=True)

with header_col2:
    # 🎯 هنا عدلناها لتبحث عن ملف الـ jpg بدقة
    if os.path.exists('logo.jpg'):
        st.image('logo.jpg', width=130)

st.write("---")

# 1. اختيار الفئة المستهدفة
target_sel = st.selectbox(lbl_target, targets_opts)

# 2. فلترة البيانات بناءً على الفئة المستهدفة
if target_sel in ["نساء", "Women"]:
    filtered_df = df[df[col_target].isin(["نساء", "الكل", "Women", "All"])]
    available_categories = sorted(filtered_df[col_cat].unique())
elif target_sel in ["رجال", "Men"]:
    filtered_df = df[df[col_target].isin(["رجال", "الكل", "Men", "All"])]
    excluded = ["عبايات", "لانجري وملابس داخلية", "انجري وملابس داخلية", "Abayas", "Lingerie"]
    filtered_df = filtered_df[~filtered_df[col_cat].isin(excluded)]
    available_categories = sorted(filtered_df[col_cat].unique())
elif target_sel in ["أطفال", "Children"]:
    filtered_df = df[df[col_target].isin(["أطفال", "الكل", "Children", "All"])]
    excluded = ["عبايات", "لانجري وملابس داخلية", "انجري وملابس داخلية", "Abayas", "Lingerie"]
    filtered_df = filtered_df[~filtered_df[col_cat].isin(excluded)]
    available_categories = sorted(filtered_df[col_cat].unique())
else:
    filtered_df = df
    available_categories = [all_word]

# 3. اختيار التصنيف الرئيسي
category_sel = st.selectbox(lbl_category, available_categories)

# 4. اختيار مستوى الأسعار
price_sel = st.selectbox(lbl_price, price_opts)

# 🧠 تطبيق منطق الأسعار التراكمي
if price_sel in ["اقتصادي", "Affordable"]:
    price_filter = ["اقتصادي", "Affordable"]
elif price_sel in ["متوسط", "Medium"]:
price_filter = ["متوسط", "اقتصادي", "Medium", "Affordable"]
elif price_sel in ["مرتفع", "Premium"]:
    price_filter = ["مرتفع", "متوسط", "اقتصادي", "Premium", "Medium", "Affordable"]
else:
    price_filter = df[col_price].unique().tolist()

# 5. الفلترة النهائية وعرض النتائج للمستخدم
if category_sel == all_word:
    final_df = filtered_df[filtered_df[col_price].isin(price_filter)]
else:
    final_df = filtered_df[(filtered_df[col_cat] == category_sel) & 
                           (filtered_df[col_price].isin(price_filter))]

st.write("")

# زر عرض الاقتراحات والمحلات
if st.button(lbl_btn, use_container_width=True):
    if not final_df.empty:
        st.success(lbl_success)
        
        # تقسيم المحلات إلى شبكة مربعات (Grid) متناسقة
        shops = final_df[col_name].unique()
        for i in range(0, len(shops), 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j < len(shops):
                    with cols[j]:
                        st.markdown(f"<div class='shop-box'>{shops[i+j]}</div>", unsafe_allowed_code=True)
    else:
        st.warning(lbl_warning)
