import streamlit as st
import streamlit.components.v1 as components
from typing import Optional, Dict, Any
import base64
import mimetypes
from pathlib import Path


st.set_page_config(
    page_title="E-Health Preventive Check-Up (Strict Script)", 
    page_icon="🩺", 
    layout="centered",
    initial_sidebar_state="expanded"
)


def init_state():
    if "init" in st.session_state:
        return
    st.session_state.init = True
    st.session_state.stage = "receptionist_welcome"
    st.session_state.messages = []
    st.session_state.profile = {
        "preferred_name": None,
        "first_time_online": None,
        "topics": [],
        "ongoing_issues": None,
        "issues_detail": None,
        "occupation": None,
        "work_stress": None,
        "relax": None,
        "smoke_now": None,
        "smoke_6m": None,
        "drink": None,
        "drink_freq": None,
        "exercise_freq": None,
        "exercise_types": None,
        "companionship": None,
        "fruit_freq": None,
        "veg_freq": None,
        "grain_freq": None,
        "protein_freq": None,
        "dairy_freq": None,
        "cook_at_home": None,
        "try_new_recipes": None,
        "sleep_quality_1_5": None,
        "screen_before_bed": None,
        "diff_fall_asleep": None,
        "night_wake_diff": None,
        "morning_tired": None,
        "family_sleep_history": None,
    }


def say(role: str, text: str, delay: float = 0):
    # 仅记录消息，渲染统一在 render_messages 中完成（支持左右对齐与气泡样式）
    st.session_state.messages.append({"role": role, "text": text, "delay": delay})


def say_image(role: str, image_path: str, caption: str = "", delay: float = 0):
    # 记录图片消息
    st.session_state.messages.append({"role": role, "type": "image", "image_path": image_path, "caption": caption, "delay": delay})


def to_data_url(image_path: str) -> Optional[str]:
    """将本地图片路径转换为 base64 data URL，便于在自定义组件 iframe 中稳定显示。"""
    candidate_paths = [
        Path(image_path),
        Path(__file__).parent / image_path,
        Path.cwd() / image_path,
    ]
    resolved_path: Optional[Path] = None
    for p in candidate_paths:
        try:
            if p.is_file():
                resolved_path = p
                break
        except Exception:
            continue
    if resolved_path is None:
        return None
    mime, _ = mimetypes.guess_type(str(resolved_path))
    if not mime:
        mime = "image/png"
    try:
        data_bytes = resolved_path.read_bytes()
    except Exception:
        return None
    b64 = base64.b64encode(data_bytes).decode("ascii")
    return f"data:{mime};base64,{b64}"


def say_multiple(role: str, texts: list, delays: list = None):
    """发送多条消息，支持逐条延迟显示"""
    if delays is None:
        delays = [0.5] * len(texts)  # 默认每条消息间隔0.5秒
    
    for i, text in enumerate(texts):
        delay = delays[i] if i < len(delays) else delays[-1] if delays else 0.5
        say(role, text, delay)


def chat_input(label_key: str, placeholder: str = "Type here...") -> Optional[str]:
    return st.chat_input(placeholder=placeholder, key=label_key)


def buttons(options, key_prefix: str) -> Optional[str]:
    cols = st.columns(min(4, len(options)))
    chosen = None
    for i, opt in enumerate(options):
        if cols[i % len(cols)].button(opt, key=f"{key_prefix}_{i}"):
            chosen = opt
    return chosen


def set_stage(next_stage: str) -> None:
    st.session_state.stage = next_stage
    st.rerun()




def ensure_styles():
    # 注入Landbot风格的样式
    st.markdown(
        """
        <style>
        .block-container { max-width: 700px; padding-left: 0 !important; padding-right: 0 !important; }
        
        /* Landbot风格的按钮样式 */
        .stButton > button { 
            border-radius: 25px !important; 
            padding: 12px 24px !important; 
            border: none !important; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important; 
            color: white !important; 
            font-weight: 600 !important; 
            font-size: 14px !important;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important; 
            transition: all 0.3s ease !important;
            margin: 4px 8px 4px 0 !important;
            min-width: 120px !important;
        }
        .stButton > button:hover { 
            transform: translateY(-2px) !important; 
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important; 
        }
        
        /* 输入框样式 */
        .stTextInput > div > div > input {
            border-radius: 25px !important;
            border: 2px solid #e2e8f0 !important;
            padding: 12px 20px !important;
            font-size: 14px !important;
            transition: all 0.3s ease !important;
        }
        .stTextInput > div > div > input:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        }
        
        /* 聊天输入框样式 */
        .stChatInput > div > div > div > textarea {
            border-radius: 25px !important;
            border: 2px solid #e2e8f0 !important;
            padding: 12px 20px !important;
            font-size: 14px !important;
            resize: none !important;
        }
        
        /* 隐藏Streamlit默认元素 */
        .stApp > header { visibility: hidden; }
        .stApp > div:first-child { padding-top: 0 !important; }
        
        /* 消息气泡样式优化 */
        .bubble-text, .bubble-text * { margin-top: 0 !important; margin-bottom: 0 !important; }
        .bubble-text p, .bubble-text ul, .bubble-text ol, .bubble-text pre, .bubble-text blockquote, .bubble-text code,
        .bubble-text h1, .bubble-text h2, .bubble-text h3, .bubble-text h4, .bubble-text h5, .bubble-text h6 { margin: 0 !important; }
        .bubble-text > * + * { margin-top: 4px !important; }
        .bubble-text ul, .bubble-text ol { padding-left: 1.1em !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_messages():
    # 这个函数现在被 render_custom_chat() 替代
    pass

def render_custom_chat():
    """使用自定义组件渲染聊天界面 - 支持逐条延迟显示和打字机效果"""
    
    # 获取当前消息数量，用于增量更新
    current_message_count = len(st.session_state.messages)
    
    # 准备消息数据，简化显示逻辑
    messages_html = ""
    for i, m in enumerate(st.session_state.messages):
        role = m.get("role", "")
        message_type = m.get("type", "text")
        delay = m.get("delay", 0)
        is_right = role == "patient"
        
        # 为每条消息添加唯一ID，便于增量更新
        message_id = f"msg-{i}"
        
        # Landbot风格的样式
        if is_right:
            bubble_bg = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
            text_color = "#FFFFFF"
            role_align = "right"
            wrap_align = "flex-end"
            row_style = f"display:flex; align-items:flex-start; justify-content:flex-end; gap:12px; margin:16px 0; animation: slideInRight 0.4s ease-out;"
        else:
            bubble_bg = "#FFFFFF"
            text_color = "#2D3748"
            role_align = "left"
            wrap_align = "flex-start"
            row_style = f"display:flex; align-items:flex-start; justify-content:flex-start; gap:12px; margin:16px 0; animation: slideInLeft 0.4s ease-out;"
        
        # 更精致的头像和角色标签
        avatar_html = "🩺" if role == "doctor" else ("🧑‍💼" if role == "receptionist" else "🙂")
        role_label = role.capitalize()
        
        avatar_style = (
            "width:40px; height:40px; border-radius:50%; display:flex; align-items:center; justify-content:center; "
            "font-size:18px; background:linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color:white; "
            "box-shadow:0 2px 8px rgba(0,0,0,0.15); flex-shrink:0; animation: bounceIn 0.5s ease-out;"
        )
        
        role_style = (
            f"font-size:12px; font-weight:600; color:#718096; margin-bottom:6px; text-align:{role_align}; "
            "text-transform:uppercase; letter-spacing:0.8px; opacity:0.8;"
        )
        
        avatar_box = f'<div style="{avatar_style}">{avatar_html}</div>'
        role_box = f'<div style="{role_style}">{role_label}</div>'
        
        # 根据消息类型生成内容
        if message_type == "image":
            image_path = m.get("image_path", "")
            caption = m.get("caption", "")
            
            # 图片样式
            image_style = (
                "max-width:300px; max-height:400px; border-radius:12px; "
                "box-shadow:0 4px 12px rgba(0,0,0,0.15); margin:8px 0;"
            )
            
            # 图片容器样式
            bubble_style = (
                "display:inline-block; max-width:75%; padding:14px 18px; border-radius:20px; line-height:1.5; "
                "box-shadow:0 2px 12px rgba(0,0,0,0.15); word-break:break-word; white-space:pre-wrap; "
                f"background:{bubble_bg}; color:{text_color}; border:none; position:relative; "
                "font-size:15px; font-weight:400;"
            )
            
            # 生成图片HTML
            src = to_data_url(image_path) or image_path
            image_html = f'<img src="{src}" style="{image_style}" alt="{caption}">'
            if caption:
                image_html += f'<div style="font-size:12px; color:#666; margin-top:4px; text-align:center;">{caption}</div>'
            
            bubble_box = f'<div style="{bubble_style}">{image_html}</div>'
        else:
            # 文本消息
            text = (m.get("text", "") or "").lstrip()
            bubble_style = (
                "display:inline-block; max-width:75%; padding:14px 18px; border-radius:20px; line-height:1.5; "
                "box-shadow:0 2px 12px rgba(0,0,0,0.15); word-break:break-word; white-space:pre-wrap; "
                f"background:{bubble_bg}; color:{text_color}; border:none; position:relative; "
                "font-size:15px; font-weight:400;"
            )
            bubble_box = f'<div style="{bubble_style}">{text}</div>'
        
        wrap_style = f"display:flex; flex-direction:column; align-items:{wrap_align}; max-width:100%;"
        
        if is_right:
            messages_html += f"""
            <div id="{message_id}" class="message-row" style="{row_style}">
                <div style="{wrap_style}">{role_box}{bubble_box}</div>
                {avatar_box}
            </div>
            """
        else:
            messages_html += f"""
            <div id="{message_id}" class="message-row" style="{row_style}">
                {avatar_box}
                <div style="{wrap_style}">{role_box}{bubble_box}</div>
            </div>
            """
    
    # 创建Landbot风格的聊天组件
    chat_html = f"""
    <style>
        @keyframes slideInLeft {{
            from {{ transform: translateX(-30px); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}
        @keyframes slideInRight {{
            from {{ transform: translateX(30px); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}
        @keyframes bounceIn {{
            0% {{ transform: scale(0.3); opacity: 0; }}
            50% {{ transform: scale(1.05); }}
            70% {{ transform: scale(0.9); }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}
        @keyframes fadeInUp {{
            from {{ transform: translateY(20px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}
        @keyframes typing {{
            0%, 20% {{ opacity: 0; }}
            50% {{ opacity: 1; }}
            100% {{ opacity: 0; }}
        }}
        .typing-indicator {{
            display: flex;
            align-items: center;
            gap: 4px;
            padding: 12px 18px;
            background: #f7fafc;
            border-radius: 20px;
            margin: 8px 0;
            animation: fadeInUp 0.3s ease-out;
        }}
        .typing-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #a0aec0;
            animation: typing 1.4s infinite;
        }}
        .typing-dot:nth-child(2) {{ animation-delay: 0.2s; }}
        .typing-dot:nth-child(3) {{ animation-delay: 0.4s; }}
    </style>
    
    <div id="chat-container" style="
        max-width: 700px; 
        margin: 0 auto; 
        height: 75vh; 
        overflow-y: auto; 
        padding: 24px;
        border: none;
        border-radius: 20px;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        box-sizing: border-box;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
    ">
        <div id="messages-container" style="min-height: 100%;">
            {messages_html}
        </div>
        <div id="scroll-anchor"></div>
    </div>
    
    <script>
        // 简化的滚动逻辑
        function scrollToBottom() {{
            const container = document.getElementById('chat-container');
            if (container) {{
                container.scrollTop = container.scrollHeight;
            }}
        }}
        
        // 检查是否有新消息
        function checkForNewMessages() {{
            const currentCount = {current_message_count};
            if (currentCount > window.lastMessageCount) {{
                window.lastMessageCount = currentCount;
                // 延迟滚动，确保新内容已渲染
                setTimeout(scrollToBottom, 100);
                
                // 检查是否是医生建议消息，如果是则设置10秒延迟
                const lastMessage = document.querySelector('.message-row:last-child');
                if (lastMessage) {{
                    const messageText = lastMessage.textContent || '';
                    if (messageText.includes('Based on our chat, I think you are doing fine')) {{
                        // 10秒后触发延迟内容显示
                        setTimeout(() => {{
                            // 这里可以触发一个事件或直接调用Streamlit的rerun
                            window.parent.postMessage({{type: 'streamlit:rerun'}}, '*');
                        }}, 10000);
                    }}
                }}
            }}
        }}
        
        // 初始化
        function initializeChat() {{
            window.lastMessageCount = {current_message_count};
            scrollToBottom();
        }}
        
        // 页面加载完成后初始化
        document.addEventListener('DOMContentLoaded', function() {{
            initializeChat();
        }});
        
        // 定期检查新消息
        setInterval(checkForNewMessages, 1000);
        
        // 简化的DOM监听
        const observer = new MutationObserver(function(mutations) {{
            let hasNewContent = false;
            mutations.forEach(function(mutation) {{
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {{
                    hasNewContent = true;
                }}
            }});
            
            if (hasNewContent) {{
                setTimeout(scrollToBottom, 200);
            }}
        }});
        
        // 开始观察
        const messagesContainer = document.getElementById('messages-container');
        if (messagesContainer) {{
            observer.observe(messagesContainer, {{ childList: true, subtree: true }});
        }}
    </script>
    """
    
    # 使用自定义组件渲染，调整高度
    components.html(chat_html, height=600)


def landing():
    st.title("🩺 E-Health Preventive Check-Up")
    st.caption("Welcome to your wellness consultation with Dr. Alex")
    
    if st.button("Start Consultation"):
        # 与 Reset 一致：清空消息并回到接待员欢迎阶段
        st.session_state.messages = []
        st.session_state.stage = "receptionist_welcome"
        st.rerun()
    if st.button("Reset"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        init_state()
        st.rerun()


# ---------------- Single Visit (Strict English Script) -----------------
def receptionist_intro():
    stage = st.session_state.stage
    
    if stage == "receptionist_welcome":
        # 检查是否已经显示过欢迎消息
        if not any(msg.get("text") == "Hi, welcome to the e-health platform" for msg in st.session_state.messages):
            say("receptionist", "Hi, welcome to the e-health platform")
        
        # 显示Hi按钮
        if buttons(["[Hi]"], "hi_btn"):
            say("patient", "[Hi]")
            set_stage("receptionist_help")
    
    elif stage == "receptionist_help":
        # 检查是否已经显示过帮助消息
        if not any(msg.get("text") == "How can I help you today?" for msg in st.session_state.messages):
            say("receptionist", "How can I help you today?")
        
        if buttons(["[wellness checkup]"], "wel_btn"):
            say("patient", "[wellness checkup]")
            set_stage("receptionist_intro")
    
    elif stage == "receptionist_intro":
        # 检查是否已经显示过介绍消息
        if not any(msg.get("text") == "Sure. Please bear with me until I connect you to Dr. Alex. Meanwhile, you can read a brief introduction of Dr. Alex." for msg in st.session_state.messages):
            say("receptionist", "Sure. Please bear with me until I connect you to Dr. Alex. Meanwhile, you can read a brief introduction of Dr. Alex.")
            say("receptionist", "Dr. Alex received a medical degree from the University of Pittsburgh School of Medicine in 2005 and has been board certified in preventive care and medicine. Dr. Alex's particular expertise includes nutrition, fitness, and lifestyle.")
        set_stage("doctor_greet")


def doctor_flow():
    stage = st.session_state.stage
    p = st.session_state.profile

    if stage == "doctor_greet":
        # 检查是否已经显示过问候消息
        if not any(msg.get("text") == "Hi, I am Dr. Alex. How would you like to be addressed?" for msg in st.session_state.messages):
            say("doctor", "Hi, I am Dr. Alex. How would you like to be addressed?")
            set_stage("doctor_name_input")
    
    elif stage == "doctor_name_input":
        name = chat_input("name_input", "[preferred name input]")
        if name:
            p["preferred_name"] = name
            say("patient", f"[{name}]")
            say("doctor", f"{name}, nice to meet you.")
            say("doctor", "How are you doing lately?")
            set_stage("doctor_feel")
    elif stage == "doctor_feel":
        clicked = buttons(["[good]", "[bad]", "[hard to say]"], "feel")
        if clicked:
            say("patient", clicked)
            say("doctor", "Is this your first-time consulting doctors online for wellness?")
            set_stage("doctor_online")

    elif stage == "doctor_online":
        clicked = buttons(["[yes]", "[no]"], "online")
        if clicked:
            say("patient", clicked)
            say("doctor", "Well, lots of people have consulted me about wellness. What topics do you want to know more about today?")
            set_stage("doctor_topics")

    elif stage == "doctor_topics":
        clicked = buttons(["[diet]", "[fitness]", "[sleep]"], "topics")
        if clicked:
            say("patient", clicked)
            say("doctor", "Great. I will be sure to cover it in this checkup.")
            say("doctor", "Do you have any ongoing health issues that I should be aware of?")
            set_stage("doctor_ongoing")

    elif stage == "doctor_ongoing":
        clicked = buttons(["[Yes]", "[No]"], "ongoing")
        if clicked:
            say("patient", clicked)
            if clicked == "[Yes]":
                say("doctor", "What are some health problems you have?")
                set_stage("doctor_issues_detail")
            else:
                say("doctor", "What do you do for a living?")
                set_stage("doctor_job")
    
    elif stage == "doctor_issues_detail":
        ans = chat_input("issues_detail", "[answer input]")
        if ans:
            p["issues_detail"] = ans
            say("patient", f"[{ans}]")
            say("doctor", "Thanks for letting me know. I will take your health status into account when providing suggestions.")
            say("doctor", "What do you do for a living?")
            set_stage("doctor_job")

    elif stage == "doctor_job":
        ans = chat_input("job", "[answer input]")
        if ans:
            p["occupation"] = ans
            say("patient", f"[{ans}]")
            # 检查是否失业
            job_lower = ans.lower()
            unemployed_keywords = ["unemployed", "not working", "no job", "student", "retired", "stay at home", "homemaker"]
            is_unemployed = any(keyword in job_lower for keyword in unemployed_keywords)
            
            if is_unemployed:
                # 如果失业，跳过工作压力问题
                # 使用逐条显示效果
                say_multiple("doctor", [
                    "Got it. Managing stress is an important and challenging task. But you know, stress isn't always bad. Sometimes it can motivate us to get things done.",
                    "What do you often do to relax yourself?"
                ], [0, 0.5])
                set_stage("doctor_relax")
            else:
                # 如果就业，询问工作压力
                say("doctor", "How stressful are you at work? From 0-10, can you give me a number?")
                set_stage("doctor_stress")

    elif stage == "doctor_stress":
        ans = chat_input("stress", "[answer input]")
        if ans:
            p["work_stress"] = ans
            say("patient", f"[{ans}]")
            # 使用逐条显示效果
            say_multiple("doctor", [
                "Got it. Managing stress is an important and challenging task. But you know, stress isn't always bad. Sometimes it can motivate us to get things done.",
                "What do you often do to relax yourself?"
            ], [0, 0.5])
            set_stage("doctor_relax")

    elif stage == "doctor_relax":
        ans = chat_input("relax", "[answer input]")
        if ans:
            p["relax"] = ans
            say("patient", f"[{ans}]")
            say("doctor", "I am glad that you know how to wind down.")
            set_stage("doctor_smoke_question")

    elif stage == "doctor_smoke_question":
        # 检查是否已经显示过吸烟问题
        if not any(msg.get("text") == "Do you currently smoke cigarettes?" for msg in st.session_state.messages):
            say("doctor", "Do you currently smoke cigarettes?")
        set_stage("doctor_smoke")

    elif stage == "doctor_smoke":
        clicked = buttons(["[Yes]", "[No]"], "smoke")
        if clicked:
            say("patient", clicked)
            if clicked == "[Yes]":
                say("doctor", "Were you smoking 6 months ago?")
                set_stage("doctor_smoke_6m")
            else:
                say("doctor", "Do you drink alcohol?")
                set_stage("doctor_drink")

    elif stage == "doctor_smoke_6m":
        clicked = buttons(["[Yes]", "[No]"], "smoke_6m")
        if clicked:
            say("patient", clicked)
            say("doctor", "Do you drink alcohol?")
            set_stage("doctor_drink")

    elif stage == "doctor_drink":
        clicked = buttons(["[Yes]", "[No]"], "drink")
        if clicked:
            say("patient", clicked)
            if clicked == "[Yes]":
                say("doctor", "How often do you drink alcohol?")
                set_stage("doctor_drink_freq")
            else:
                # 使用逐条显示效果
                say_multiple("doctor", [
                    "You know people have used alcohol and cigarettes to relieve stress for centuries. But, research results are mixed in terms of whether it can actually reduce stress.",
                    "How often do you exercise?"
                ], [0, 0.5])
                set_stage("doctor_exercise")

    elif stage == "doctor_drink_freq":
        clicked = buttons([
            "[1-2 days a week]",
            "[3-5 days a week]",
            "[6-7 days a week]",
        ], "drink_freq")
        if clicked:
            say("patient", clicked)
            say("doctor", "You know people have used alcohol and cigarettes to relieve stress for centuries. But, research results are mixed in terms of whether it can actually reduce stress.")
            say("doctor", "How often do you exercise?")
            set_stage("doctor_exercise")

    elif stage == "doctor_exercise":
        clicked = buttons([
            "[never]",
            "[1-2 days per week]",
            "[3-5 days per week]",
            "[6+ days per week]",
        ], "exercise")
        if clicked:
            say("patient", clicked)
            if clicked != "[never]":
                say("doctor", "What are some of the exercises you enjoy?")
                set_stage("doctor_exercise_types")
            else:
                say("doctor", "How often do you feel that you lack companionship?")
                set_stage("doctor_companionship")

    elif stage == "doctor_exercise_types":
        ans = chat_input("exercise_types", "[answer input]")
        if ans:
            say("patient", f"[{ans}]")
            say("doctor", "How often do you feel that you lack companionship?")
            set_stage("doctor_companionship")

    elif stage == "doctor_companionship":
        clicked = buttons([
            "[Hardly ever or never]",
            "[some of the time]",
            "[often]",
        ], "companionship")
        if clicked:
            say("patient", clicked)
            if clicked == "[often]":
                say("doctor", "It seems like you are quite lonely. I'll suggest you talk to your friends and family more frequently. It may help.")
            elif clicked == "[some of the time]":
                say("doctor", "It seems like you are a little bit lonely. I'll suggest you talk to your friends and family more frequently. It may help.")
            else:
                say("doctor", "It seems like you are not lonely at all. I am glad that you feel supported and fulfilled in your relationship,")
            # 使用逐条显示效果
            say_multiple("doctor", [
                "Next, I would like to know what you're currently eating.",
                "You probably know that most foods can be categorized into five major groups, namely Fruit, Vegetables, Grains, Protein, and Dairy. I would like to know how often you eat from each group."
            ], [0, 0.5])
            set_stage("doctor_diet_intro")

    elif stage == "doctor_diet_intro":
        clicked = buttons(["[OK]"], "diet_intro")
        if clicked:
            say("patient", clicked)
            say("doctor", "How often do you eat fruits, such as apples, bananas, or oranges? The fruit can be fresh, frozen, canned, or dried. 100% fruit juice also counts as fruit.")
            set_stage("doctor_fruit")

    elif stage == "doctor_fruit":
        clicked = buttons([
            "[0-2 days per week]",
            "[3-5 days per week]",
            "[6+ days per week]",
        ], "fruit")
        if clicked:
            say("patient", clicked)
            say("doctor", "How about vegetables, like broccoli and cabbage?")
            set_stage("doctor_vegetables")

    elif stage == "doctor_vegetables":
        clicked = buttons([
            "[0-2 days per week]",
            "[3-5 days per week]",
            "[6+ days per week]",
        ], "vegetables")
        if clicked:
            say("patient", clicked)
            say("doctor", "How often do you eat grains, such as wheat, bread, and pasta? Foods such as popcorn, rice, and oatmeal are also included as grains.")
            set_stage("doctor_grains")

    elif stage == "doctor_grains":
        clicked = buttons([
            "[0-2 days per week]",
            "[3-5 days per week]",
            "[6+ days per week]",
        ], "grains")
        if clicked:
            say("patient", clicked)
            say("doctor", "How about protein foods, such as seafood, meat, poultry, eggs, beans, peas, lentils, nuts, seeds, or soy products?")
            set_stage("doctor_protein")

    elif stage == "doctor_protein":
        clicked = buttons([
            "[0-2 days per week]",
            "[3-5 days per week]",
            "[6+ days per week]",
        ], "protein")
        if clicked:
            say("patient", clicked)
            say("doctor", "How often do you eat dairy products, such as dairy milk, yogurt, and cheese?")
            set_stage("doctor_dairy")

    elif stage == "doctor_dairy":
        clicked = buttons([
            "[0-2 days per week]",
            "[3-5 days per week]",
            "[6+ days per week]",
        ], "dairy")
        if clicked:
            say("patient", clicked)
            say("doctor", "Do you usually cook at home?")
            set_stage("doctor_cook")

    elif stage == "doctor_cook":
        clicked = buttons(["[Yes]", "[No]"], "cook")
        if clicked:
            say("patient", clicked)
            say("doctor", "How often do you try new recipes?")
            set_stage("doctor_recipes")

    elif stage == "doctor_recipes":
        clicked = buttons(["[Never]", "[ Rarely]", "[ Sometimes]", "[ Often]", "[ Always]"], "recipes")
        if clicked:
            say("patient", clicked)
            say("doctor", "How is your sleep quality lately? If 1 means very bad and 5 means very good, can you give me a number?")
            set_stage("doctor_sleep_quality")

    elif stage == "doctor_sleep_quality":
        ans = chat_input("sleep_quality", "[Answer input]")
        if ans:
            say("patient", f"[{ans}]")
            say("doctor", "Any screen time before bed? That is, do you look at a smartphone or tablet before falling asleep?")
            set_stage("doctor_screen")

    elif stage == "doctor_screen":
        clicked = buttons(["[Yes]", "[No]"], "screen")
        if clicked:
            say("patient", clicked)
            say("doctor", "How often do you have difficulty falling asleep (1 hour or longer)?")
            set_stage("doctor_fall_asleep")

    elif stage == "doctor_fall_asleep":
        clicked = buttons(["[never]", "[every once in a while]", "[pretty often]", "[most nights]"], "fall_asleep")
        if clicked:
            say("patient", clicked)
            say("doctor", "Do you ever wake in the night and have trouble getting back to sleep?")
            set_stage("doctor_wake_trouble")

    elif stage == "doctor_wake_trouble":
        clicked = buttons(["[never]", "[every once in a while]", "[pretty often]", "[most nights]"], "wake_trouble")
        if clicked:
            say("patient", clicked)
            say("doctor", "How often do you wake up in the morning still feeling tired?")
            set_stage("doctor_morning_tired")

    elif stage == "doctor_morning_tired":
        clicked = buttons(["[never]", "[every once in a while]", "[pretty often]", "[most nights]"], "morning_tired")
        if clicked:
            say("patient", clicked)
            say("doctor", "Some people have problems sleeping due to genetic reasons. Do you have a family history of sleep disorders, such as narcolepsy or sleep apnea?")
            set_stage("doctor_family_sleep")

    elif stage == "doctor_family_sleep":
        # 检查是否已经处理了用户选择
        if "family_sleep_processed" not in st.session_state:
            st.session_state.family_sleep_processed = False
        
        if not st.session_state.family_sleep_processed:
            clicked = buttons(["[yes]", "[no]"], "family_sleep")
            if clicked:
                st.session_state.family_sleep_processed = True
                say("patient", clicked)
                # 立即显示医生建议
                say("doctor", "Based on our chat, I think you are doing fine. But, you can always do better. After reviewing the AI system's recommendation, here is my advice for you:\n\n●Exercise at least 150 minutes a week. Choose moderate intensity activity such as brisk walking.\n●Improve your strength and flexibility. Practice muscle-strengthening activities at least 2 days a week, such as squats.\n●Customize and enjoy nutrient-dense food and beverage choices to reflect your personal preferences, cultural traditions, and budgetary considerations.\n●Choose a mix of healthy foods you like from each of the five groups: whole fruit, veggies, whole grains, proteins, and dairy.\n●Limit foods and beverages that are higher in added sugars, saturated fat, and sodium (salt).")
                # 设置阶段为等待用户确认
                st.session_state.stage = "doctor_final_advice_confirm"
    
    elif stage == "doctor_final_advice_confirm":
        # 直接显示OK按钮，不使用标志位
        clicked = buttons(["[OK]"], "final_advice_confirm")
        if clicked:
            say("patient", clicked)
            # 逐条显示后续内容
            say("doctor", "Our receptionist will send you pamphlets of good practices of exercise and diet.")
            say("doctor", "Thanks for your visit.")
            say("doctor", "[The doctor has left the chat]")
            # Receptionist分享两张图
            say_image("receptionist", "图片1.png", "Exercise Guidelines Pamphlet")
            say_image("receptionist", "图片2.png", "Mental Health Self-Care Guide")
            say("receptionist", "You can right-click to save the pamphlets.")
            say("receptionist", "This is the end of your first doctor's visit. Here's the access code for you to continue the questionnaire: 9087. Please copy the code and return it to the questionnaire page to proceed.")
            st.session_state.stage = "end"




# ---------------- Router -----------------
def main():
    init_state()

    with st.sidebar:
        st.markdown("**Controls**")
        if st.button("Home"):
            # Reset conversation messages when going Home
            st.session_state.messages = []
            set_stage("landing")
        st.divider()
        st.markdown("Run this strict English script app with: \n`streamlit run app_strict.py`")

    # 确保样式总是注入（即使当前还没有消息）
    ensure_styles()

    if st.session_state.stage == "landing":
        landing()
        return

    # --- 方案 4：自定义聊天组件 ---
    render_custom_chat()
    
    # 在聊天区域下方显示交互元素
    if st.session_state.stage in ["receptionist_welcome", "receptionist_help", "receptionist_intro"]:
        receptionist_intro()
    else:
        doctor_flow()

    if st.session_state.stage == "end":
        st.success("Dialogue ended. Thank you!")


if __name__ == "__main__":
    main()


