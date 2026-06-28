import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="مساعد الراشد", 
    layout="centered"
)

# 🎨 كود سحري قصير ومضمون لجعل كل شيء محاذي لليمين
st.markdown(
    "<style>"
    ".stApp { direction: RTL; text-align: right; }"
    "div[data-baseweb='select'] { direction: RTL; text-align: right; }"
    "label { text-align: right !important; display: block !important; }"
    "</style>", 
    unsafe_allowed_code=True
)

@st.cache_data
def load_data():
    return pd.read_excel('shops.xlsx')

df = load_data()

if 'lang' not in st.session_state:
    st.session_state.lang = 'ar'

if st.session_state.lang == 'ar':
    title_text = "✨ مُستشارك للتسوق في الراشد ميجا مول"
    lbl_target = "👤 اختر الفئة المستهدفة:"
    lbl_category = "🛍️ اختر التصنيف الرئيسي:"
    lbl_price = "💰 مستوى الأسعار:"
    lbl_btn = "اقترح المحلات المناسبة ✨"
    lbl_success = "📌 المحلات المقترحة لك:"
    lbl_warning = "للأسف، لا توجد محلات تطابق هذه الاختيارات."
    targets_opts = ["نساء", "رجال", "أطفال", "الكل"]
    price_opts = ["اقتصادي", "متوسط", "مرتفع", "الكل"]
    all_word = "الكل"
    col_name = 'اسم المحل'
    col_target = 'الفئة المستهدفة'
    col_cat = 'التصنيف الرئيسي'
    col_price = 'مستوى الأسعار'
else:
    title_text = "✨ Your Shopping Assistant"
    lbl_target = "👤 Select Target Audience:"
    lbl_category = "🛍️ Select Main Category:"
    lbl_price = "💰 Price Level:"
    lbl_btn = "Suggest Shops ✨"
    lbl_success = "📌 Recommended Shops:"
    lbl_warning = "No shops match these criteria."
    targets_opts = ["Women", "Men", "Children", "All"]
    price_opts = ["Affordable", "Medium", "Premium", "All"]
    all_word = "All"
    col_name = 'Shop_Name'
    col_target = 'Target_Audience'
    col_cat = 'Category'
    col_price = 'Price_Level'

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

target_sel = st.selectbox(lbl_target, targets_opts)

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

if target_sel == all_word:
    available_categories = [all_word]
else:
    available_categories = sorted(filtered_df[col_cat].unique())

category_sel = st.selectbox(lbl_category, available_categories)
price_sel = st.selectbox(lbl_price, price_opts)

price_map = {
    "اقتصادي": ["اقتصادي"], 
    "Affordable": ["Affordable"],
    "متوسط": ["اقتصادي", "متوسط"], 
    "Medium": ["Affordable", "Medium"],
    "مرتفع": ["اقتصادي", "متوسط", "مرتفع"], 
    "Premium": ["Affordable", "Medium", "Premium"]
}
price_filter = price_map.get(price_sel, df[col_price].unique().tolist())

if category_sel == all_word:
    final_df = filtered_df[filtered_df[col_price].isin(price_filter)]
else:
    final_df = filtered_df[
        (filtered_df[col_cat] == category_sel) & 
        (filtered_df[col_price].isin(price_filter))
    ]

st.write("")

# زر مقسم بعناية ومقاوم لتقطيع السطور
search_clicked = st.button(
    lbl_btn, 
    use_container_width=True
)

if search_clicked:
    if not final_df.empty:
        st.success(lbl_success)
        shops = final_df[col_name].unique()
        for i in range(0, len(shops), 4):
            cols = st.columns(4)
            for j in range(4):
if i + j < len(shops):
                    with cols[j]:
                        # سطر قصير ومحمي تماماً من التقطيع
                        st.button(
                            shops[i+j], 
                            key=f"sh_{i+j}", 
                            disabled=True,
                            use_container_width=True
                        )
    else:
        st.warning(lbl_warning)

# 💡 حيلة ذكية: مسافات إضافية بالأسفل لتجبر القوائم على الفتح لأسفل دائماً
for _ in range(10):
    st.write("")
