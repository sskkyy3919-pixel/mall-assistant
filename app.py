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

# 📝 إعداد نصوص الواجهة بناءً على اللغة المفضلة
if st.session_state.lang == 'ar':
    title_text = "مُستشارك للتسوق"
    lbl_target = "👤 اختر الفئة المستهدفة:"
    lbl_category = "🛍️ اختر التصنيف الرئيسي:"
    lbl_price = "💰 مستوى الأسعار المفضّل:"
    lbl_btn = "اقترح لي المحلات المناسبة ✨"
    lbl_success = "📌 المحلات المقترحة لك:"
    lbl_warning = "للأسف، لا توجد محلات تطابق هذه الاختيارات."
    targets_opts = ["نساء", "رجال", "أطفال", "الكل"]
    price_opts = ["اقتصادي", "متوسط", "مرتفع", "الكل"]
    all_word = "الكل"
    col_name, col_target, col_cat, col_price = 'اسم المحل', 'الفئة المستهدفة', 'التصنيف الرئيسي', 'مستوى الأسعار'
else:
    title_text = "Shopping Assistant"
    lbl_target = "👤 Select Target Audience:"
    lbl_category = "🛍️ Select Main Category:"
    lbl_price = "💰 Preferred Price Level:"
    lbl_btn = "Suggest Shops ✨"
    lbl_success = "📌 Recommended Shops for you:"
    lbl_warning = "Unfortunately, no shops match these criteria."
    targets_opts = ["Women", "Men", "Children", "All"]
    price_opts = ["Affordable", "Medium", "Premium", "All"]
    all_word = "All"
    col_name, col_target, col_cat, col_price = 'Shop_Name', 'Target_Audience', 'Category', 'Price_Level'

# 🏛️ توزيع الواجهة: التصنيفات على اليمين والشعار موازي لها على اليسار (تدعم اليمين تلقائياً)
main_layout_col1, main_layout_col2 = st.columns([7, 3])

with main_layout_col1:
    # زر اللغة
    if st.session_state.lang == 'ar':
        if st.button("English"):
            st.session_state.lang = 'en'
            st.rerun()
    else:
        if st.button("عربي"):
            st.session_state.lang = 'ar'
            st.rerun()
            
    # العنوان بلون الشعار الفخم عبر كود آمن وبسيط
    st.write(f"### :brown[{title_text}]")
    
    # 1. القوائم المنسدلة للاختيار
    target_sel = st.selectbox(lbl_target, targets_opts)

with main_layout_col2:
    st.write("") 
    if os.path.exists('logo.jpg'):
        st.image('logo.jpg', width=140)

# باقي القوائم منسقة بشكل ممتاز ومريح
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

# 🧠 منطق الأسعار الذكي
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

# زر عرض الاقتراحات والمحلات ممتد
if st.button(lbl_btn, use_container_width=True):
    if not final_df.empty:
        st.success(lbl_success)
        shops = final_df[col_name].unique()
        for i in range(0, len(shops), 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j < len(shops):
with cols[j]:
    # أزرار واضحة وبارزة للمحلات
    st.button(f"**{shops[i+j]}**", key=f"sh_{i+j}", disabled=True, use_container_width=True)
    else:
        st.warning(lbl_warning)

# مساحات بالأسفل لتجبر القوائم المنسدلة على الفتح لأسفل دائماً
for _ in range(8):
    st.write("")
