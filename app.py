import streamlit as st
import pandas as pd

# 1. إعداد واجهة الصفحة
st.set_page_config(page_title="مساعد المول الذكي", page_icon="🛍️", layout="centered")
st.title("مساعدك الذكي في المول 🤖✨")

# 2. قراءة جدولك من سطح المكتب (المسار العربي اللي ضبط معكِ)
df = pd.read_excel('shops.xlsx')

# 3. تنظيف البيانات من الفواصل والمسافات الزائدة تلقائياً خلف الكواليس
for col in ['التصنيف الرئيسي', 'الفئة المستهدفة', 'مستوى الأسعار']:
    df[col] = df[col].astype(str).str.replace('،', ',').apply(lambda x: [i.strip() for i in x.split(',')])

st.write("اختر ما تبحث عنه اليوم لتجد ما يناسبك:")

# 4. تصميم عناصر الواجهة (القوائم المنسدلة وأزرار الاختيار للزائر)
user_target = st.selectbox("👤 الفئة المستهدفة:", ["نساء", "رجال", "أطفال", "عوائل", "افراد"])
user_category = st.selectbox("🏬 التصنيف الرئيسي:", ["مطاعم", "كافيهات", "ملابس", "عطور", "مستحضرات تجميل", "سوبرماركت"])
user_budget = st.radio("💰 مستوى الأسعار:", ["اقتصادي", "متوسط", "مرتفع"])

# 5. زر الضغط (الفلتر الذكي اللي يشتغل أول ما الزائر يضغط الزر)
if st.button("✨ اقترح لي المحلات الان"):
    
    # الفلترة الذكية (تبحث بمرونة داخل القوائم عن الكلمة اللي اختارها الزائر)
    filtered_df = df[
        df['الفئة المستهدفة'].apply(lambda x: any(user_target in s for s in x)) &
        df['التصنيف الرئيسي'].apply(lambda x: any(user_category in s for s in x)) &
        df['مستوى الأسعار'].apply(lambda x: any(user_budget in s for s in x))
    ]
    
    # عرض النتائج بشكل تفاعلي وجميل في الصفحة
    st.subheader("🛍️ المحلات المقترحة:")
    if not filtered_df.empty:
        for index, row in filtered_df.iterrows():
            st.success(f"**{row['اسم المحل']}**")
    else:
        st.warning("❌ عذراً، لا توجد محلات تطابق هذه الاختيارات بالضبط حالياً في المول. جرب تغيير مستوى الأسعار أو الفئة!")
