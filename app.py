import streamlit as st
import pandas as pd

st.set_page_config(page_title="مساعد الراشد الذكي | Alrashid Mall Assistant", layout="centered")

@st.cache_data
def load_data():
    return pd.read_excel('shops.xlsx')

df = load_data()

# 🌐 إدارة حالة اللغة (الافتراضي: عربي)
if 'lang' not in st.session_state:
    st.session_state.lang = 'ar'

# زر تغيير اللغة التبادلي في أعلى الصفحة
col1, col2 = st.columns([8, 2])
with col2:
    if st.session_state.lang == 'ar':
        if st.button("English"):
            st.session_state.lang = 'en'
            st.rerun()
    else:
        if st.button("عربي"):
            st.session_state.lang = 'ar'
            st.rerun()

# 📝 إعداد النصوص والترجمة بناءً على اللغة المختارة
if st.session_state.lang == 'ar':
    title = "✨ 🤖 مساعدك الذكي في الراشد ميجا مول"
    lbl_target = "👤 اختر الفئة المستهدفة:"
    lbl_category = "🛍️ اختر التصنيف الرئيسي:"
    lbl_price = "💰 مستوى الأسعار المفضّل:"
    lbl_btn = "اقترح لي المحلات ✨"
    lbl_success = "📌 المحلات المقترحة لك:"
    lbl_warning = "للأسف، لا توجد محلات تطابق هذه الاختيارات."
    
    # خيارات القوائم بالعربي
    targets_opts = ["نساء", "رجال", "أطفال", "الكل"]
    price_opts = ["اقتصادي", "متوسط", "مرتفع", "الكل"]
    all_word = "الكل"
    
    # أسماء الأعمدة في الإكسل للعربي
    col_name = 'اسم المحل'
    col_target = 'الفئة المستهدفة'
    col_cat = 'التصنيف الرئيسي'
    col_price = 'مستوى الأسعار'
else:
    title = "✨ 🤖 Your Smart Assistant at Alrashid Mega Mall"
    lbl_target = "👤 Select Target Audience:"
    lbl_category = "🛍️ Select Main Category:"
    lbl_price = "💰 Preferred Price Level:"
    lbl_btn = "Suggest Shops ✨"
    lbl_success = "📌 Recommended Shops for you:"
    lbl_warning = "Unfortunately, no shops match these criteria."
    
    # خيارات القوائم بالإنجليزي (تطابق العمود الإنجليزي في ملفكِ)
    targets_opts = ["Women", "Men", "Children", "All"]
    price_opts = ["Affordable", "Medium", "Premium", "All"]
    all_word = "All"
    
    # أسماء الأعمدة في الإكسل للإنجليزي
    col_name = 'Shop_Name'
    col_target = 'Target_Audience'
    col_cat = 'Category'
    col_price = 'Price_Level'

st.title(title)

# 1. اختيار الفئة المستهدفة
target_sel = st.selectbox(lbl_target, targets_opts)

# 2. فلترة البيانات الذكية بناءً على الفئة المستهدفة لتحديد التصنيفات المتاحة
if target_sel in ["نساء", "Women"]:
    filtered_df = df[df[col_target].isin(["نساء", "الكل", "Women", "All"])]
    # استبعاد التجمعات الرجالية الصريحة
    filtered_df = filtered_df[~filtered_df[col_cat].isin(["عبايات", "لانجري وملابس داخلية", "انجري وملابس داخلية", "Abayas", "Lingerie"])] if st.session_state.lang == 'ar' else filtered_df
    available_categories = sorted(filtered_df[col_cat].unique())
elif target_sel in ["رجال", "Men"]:
    filtered_df = df[df[col_target].isin(["رجال", "الكل", "Men", "All"])]
    # استبعاد العبايات واللانجري للرجال
    if st.session_state.lang == 'ar':
        filtered_df = filtered_df[~filtered_df[col_cat].isin(["عبايات", "لانجري وملابس داخلية", "انجري وملابس داخلية"])]
    else:
        filtered_df = filtered_df[~filtered_df[col_cat].isin(["Abayas", "Lingerie"])]
    available_categories = sorted(filtered_df[col_cat].unique())
elif target_sel in ["أطفال", "Children"]:
    filtered_df = df[df[col_target].isin(["أطفال", "الكل", "Children", "All"])]
    if st.session_state.lang == 'ar':
        filtered_df = filtered_df[~filtered_df[col_cat].isin(["عبايات", "لانجري وملابس داخلية", "انجري وملابس داخلية"])]
    else:
        filtered_df = filtered_df[~filtered_df[col_cat].isin(["Abayas", "Lingerie"])]
    available_categories = sorted(filtered_df[col_cat].unique())
else:
    # إذا اختار "الكل"
    filtered_df = df
    available_categories = [all_word]

# 3. اختيار التصنيف الرئيسي
category_sel = st.selectbox(lbl_category, available_categories)

# 4. اختيار مستوى الأسعار (يحتوي على خيار "الكل")
price_sel = st.selectbox(lbl_price, price_opts)

# 🧠 تطبيق منطق الأسعار التراكمي + خيار "الكل" الجديد
if price_sel in ["اقتصادي", "Affordable"]:
    price_filter = ["اقتصادي", "Affordable"]
elif price_sel in ["متوسط", "Medium"]:
price_filter = ["متوسط", "اقتصادي", "Medium", "Affordable"]
elif price_sel in ["مرتفع", "Premium"]:
    price_filter = ["مرتفع", "متوسط", "اقتصادي", "Premium", "Medium", "Affordable"]
else:
    # 🎯 إذا اختار "الكل / All"، نجعل الفلتر يضم كل المستويات المتاحة في العمود
    price_filter = df[col_price].unique().tolist()

# الفلترة النهائية وعرض النتائج
if category_sel == all_word:
    final_df = filtered_df[filtered_df[col_price].isin(price_filter)]
else:
    final_df = filtered_df[(filtered_df[col_cat] == category_sel) & 
                           (filtered_df[col_price].isin(price_filter))]

# زر عرض الاقتراحات
if st.button(lbl_btn):
    if not final_df.empty:
        st.success(lbl_success)
        for shop in final_df[col_name].unique():
            st.markdown(f"- **{shop}**")
    else:
        st.warning(lbl_warning)
