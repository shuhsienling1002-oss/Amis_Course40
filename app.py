import streamlit as st
import time
import random
from io import BytesIO

# --- 1. 核心相容性修復 ---
def safe_rerun():
    """自動判斷並執行重整"""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except:
            st.stop()

def safe_play_audio(text):
    """語音播放安全模式"""
    try:
        from gtts import gTTS
        # 使用印尼語 (id) 發音
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception as e:
        st.caption(f"🔇 (語音生成暫時無法使用)")

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 40: O Widang", page_icon="🤝", layout="centered")

# --- CSS 美化 (友誼暖橙與青綠) ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .source-tag { font-size: 12px; color: #aaa; text-align: right; font-style: italic; }
    .morph-tag { 
        background-color: #FFCC80; color: #E65100; 
        padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold;
        display: inline-block; margin-right: 5px;
    }
    
    /* 單字卡 */
    .word-card {
        background: linear-gradient(135deg, #FFF3E0 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #EF6C00;
    }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #E65100; }
    .chinese-text { font-size: 16px; color: #7f8c8d; }
    
    /* 句子框 */
    .sentence-box {
        background-color: #FFF3E0;
        border-left: 5px solid #FFB74D;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    /* 按鈕 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 20px; font-weight: 600;
        background-color: #FFCC80; color: #E65100; border: 2px solid #EF6C00; padding: 12px;
    }
    .stButton>button:hover { background-color: #FFB74D; border-color: #F57C00; }
    .stProgress > div > div > div > div { background-color: #EF6C00; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 (Unit 40: 18個單字 - 朋友與社交) ---
vocab_data = [
    {"amis": "Widang", "chi": "朋友", "icon": "🧑‍🤝‍🧑", "source": "Row 6", "morph": "Noun"},
    {"amis": "Malawidang", "chi": "成為朋友", "icon": "🤝", "source": "Row 210", "morph": "Mala-Widang"},
    {"amis": "Kapot", "chi": "同伴 / 隊友", "icon": "🤜🤛", "source": "Row 19", "morph": "Noun"},
    {"amis": "Malakapot", "chi": "結伴 / 成為隊友", "icon": "👯", "source": "Standard", "morph": "Mala-Kapot"},
    {"amis": "Cafay", "chi": "同伴 / 伴侶 (詞根)", "icon": "👫", "source": "Standard", "morph": "Root"},
    {"amis": "Malacafay", "chi": "結伴 / 在一起", "icon": "💑", "source": "Row 2888", "morph": "Mala-Cafay"},
    {"amis": "Litemoh", "chi": "遇見 (詞根)", "icon": "👀", "source": "Row 683", "morph": "Root"},
    {"amis": "Malalitemoh", "chi": "相遇 / 碰面", "icon": "🛤️", "source": "Row 683", "morph": "Ma-La-Litemoh"},
    {"amis": "Liso'", "chi": "探望 (詞根)", "icon": "🏠", "source": "Row 3535", "morph": "Root"},
    {"amis": "Miliso'", "chi": "探望 / 拜訪", "icon": "👋", "source": "Row 3535", "morph": "Mi-Liso'"},
    {"amis": "Palafang", "chi": "做客 / 拜訪", "icon": "☕", "source": "Row 992", "morph": "Pa-Lafang"},
    {"amis": "Licay", "chi": "問候 (詞根)", "icon": "❓", "source": "Row 209", "morph": "Root"},
    {"amis": "Milicay", "chi": "問候 / 詢問", "icon": "🙋", "source": "Row 209", "morph": "Mi-Licay"},
    {"amis": "Pa'icela", "chi": "加油 / 鼓勵", "icon": "💪", "source": "Row 326", "morph": "Pa-'Icel-a"},
    {"amis": "Kasasowal", "chi": "交談 / 討論", "icon": "🗣️", "source": "Row 402", "morph": "Ka-Sa-Sowal"},
    {"amis": "Padang", "chi": "幫忙 (詞根)", "icon": "🆘", "source": "Row 384", "morph": "Root"},
    {"amis": "Mipadang", "chi": "幫忙 (主動)", "icon": "🤲", "source": "Row 384", "morph": "Mi-Padang"},
    {"amis": "Romadiw", "chi": "唱歌", "icon": "🎤", "source": "Standard", "morph": "R-om-adiw"},
]

# --- 句子庫 (9句: 嚴格源自 CSV 並移除連字號) ---
sentences = [
    {"amis": "Malalitemoh kita i lalan.", "chi": "我們在路上相遇。", "icon": "🛤️", "source": "Row 683"},
    {"amis": "Tala-cowa ko widang no miso?", "chi": "你的朋友去哪裡？", "icon": "🗺️", "source": "Row 6"},
    {"amis": "Malicay ni ina no miso ko widang no mako.", "chi": "我的朋友被妳的媽媽詢問(問候)。", "icon": "🙋", "source": "Row 209"},
    {"amis": "Takaraw kora a kapot.", "chi": "那位同伴很高。", "icon": "📏", "source": "Row 19"},
    {"amis": "Miliso' to malitengay.", "chi": "探望老人。", "icon": "👴", "source": "Row 3535"},
    {"amis": "Mipadang ci ina to tayal no loma'.", "chi": "媽媽幫忙家務。", "icon": "🧹", "source": "Row 384"},
    {"amis": "Masasowal ko mato'asay.", "chi": "老人互相聊天。", "icon": "🗣️", "source": "Row 402"},
    {"amis": "Malacafay a minokay.", "chi": "結伴回家。", "icon": "🏠", "source": "Standard Pattern"},
    {"amis": "Pa'icelen ko wawa a mitilid.", "chi": "要鼓勵孩子讀書。", "icon": "📚", "source": "Adapted from Row 326"},
]

# --- 3. 隨機題庫 (5題) ---
raw_quiz_pool = [
    {
        "q": "Malalitemoh kita i lalan.",
        "audio": "Malalitemoh kita i lalan",
        "options": ["我們在路上相遇", "我們在路上吵架", "我們在路上賽跑"],
        "ans": "我們在路上相遇",
        "hint": "Malalitemoh (相遇) (Row 683)"
    },
    {
        "q": "Takaraw kora a kapot.",
        "audio": "Takaraw kora a kapot",
        "options": ["那位同伴很高", "那位同伴很矮", "那位同伴很胖"],
        "ans": "那位同伴很高",
        "hint": "Kapot (同伴) (Row 19)"
    },
    {
        "q": "單字測驗：Milicay",
        "audio": "Milicay",
        "options": ["問候/詢問", "罵人", "不理會"],
        "ans": "問候/詢問",
        "hint": "Mi- (做) + Licay (問候)"
    },
    {
        "q": "單字測驗：Malawidang",
        "audio": "Malawidang",
        "options": ["成為朋友", "成為敵人", "成為鄰居"],
        "ans": "成為朋友",
        "hint": "Mala- (成為) + Widang (朋友)"
    },
    {
        "q": "Miliso' to malitengay.",
        "audio": "Miliso' to malitengay",
        "options": ["探望老人", "照顧小孩", "幫助朋友"],
        "ans": "探望老人",
        "hint": "Miliso' (探望) (Row 3535)"
    }
]

# --- 4. 狀態初始化 (洗牌邏輯) ---
if 'init' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q_idx = 0
    st.session_state.quiz_id = str(random.randint(1000, 9999))
    
    # 抽題與洗牌 (5題)
    selected_questions = random.sample(raw_quiz_pool, 5)
    final_questions = []
    for q in selected_questions:
        q_copy = q.copy()
        shuffled_opts = random.sample(q['options'], len(q['options']))
        q_copy['shuffled_options'] = shuffled_opts
        final_questions.append(q_copy)
        
    st.session_state.quiz_questions = final_questions
    st.session_state.init = True

# --- 5. 主介面 ---
st.markdown("<h1 style='text-align: center; color: #E65100;'>Unit 40: O Widang</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>朋友與社交 (Social & Interaction)</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 詞彙與句型", "🎲 隨機挑戰"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字 (構詞分析)")
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
                <div class="morph-tag">{word['morph']}</div>
                <div class="source-tag">src: {word['source']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔊 聽發音", key=f"btn_vocab_{i}"):
                safe_play_audio(word['amis'])

    st.markdown("---")
    st.subheader("🗣️ 實用句型 (Data-Driven)")
    for i, s in enumerate(sentences):
        st.markdown(f"""
        <div class="sentence-box">
            <div style="font-size: 20px; font-weight: bold; color: #E65100;">{s['icon']} {s['amis']}</div>
            <div style="font-size: 16px; color: #555; margin-top: 5px;">{s['chi']}</div>
            <div class="source-tag">src: {s['source']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ 播放句型", key=f"btn_sent_{i}"):
            safe_play_audio(s['amis'])

# === Tab 2: 隨機挑戰模式 ===
with tab2:
    st.markdown("### 🎲 隨機評量")
    
    if st.session_state.current_q_idx < len(st.session_state.quiz_questions):
        q_data = st.session_state.quiz_questions[st.session_state.current_q_idx]
        
        st.progress((st.session_state.current_q_idx) / 5)
        st.markdown(f"**Question {st.session_state.current_q_idx + 1} / 5**")
        
        st.markdown(f"### {q_data['q']}")
        if q_data['audio']:
            if st.button("🎧 播放題目音檔", key=f"btn_audio_{st.session_state.current_q_idx}"):
                safe_play_audio(q_data['audio'])
        
        # 使用洗牌後的選項
        unique_key = f"q_{st.session_state.quiz_id}_{st.session_state.current_q_idx}"
        user_choice = st.radio("請選擇正確答案：", q_data['shuffled_options'], key=unique_key)
        
        if st.button("送出答案", key=f"btn_submit_{st.session_state.current_q_idx}"):
            if user_choice == q_data['ans']:
                st.balloons()
                st.success("🎉 答對了！")
                time.sleep(1)
                st.session_state.score += 20
                st.session_state.current_q_idx += 1
                safe_rerun()
            else:
                st.error(f"不對喔！提示：{q_data['hint']}")
                
    else:
        st.progress(1.0)
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #FFCC80; border-radius: 20px; margin-top: 20px;'>
            <h1 style='color: #E65100;'>🏆 挑戰成功！</h1>
            <h3 style='color: #333;'>本次得分：{st.session_state.score}</h3>
            <p>你已經完成 10 個進階單元的學習了！</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再來一局 (重新抽題)", key="btn_restart"):
            st.session_state.score = 0
            st.session_state.current_q_idx = 0
            st.session_state.quiz_id = str(random.randint(1000, 9999))
            
            new_questions = random.sample(raw_quiz_pool, 5)
            final_qs = []
            for q in new_questions:
                q_copy = q.copy()
                shuffled_opts = random.sample(q['options'], len(q['options']))
                q_copy['shuffled_options'] = shuffled_opts
                final_qs.append(q_copy)
            
            st.session_state.quiz_questions = final_qs
            safe_rerun()
