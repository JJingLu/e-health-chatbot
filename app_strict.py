import streamlit as st
import streamlit.components.v1 as components
from typing import Optional, Dict, Any


st.set_page_config(page_title="E-Health Preventive Check-Up (Strict Script)", page_icon="🩺", layout="centered")


def init_state():
    if "init" in st.session_state:
        return
    st.session_state.init = True
    st.session_state.stage = "receptionist_intro"
    st.session_state.messages = []
    st.session_state._need_scroll = False  # 新消息出现时触发滚动
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


def say(role: str, text: str):
    # 仅记录消息，渲染统一在 render_messages 中完成（支持左右对齐与气泡样式）
    st.session_state.messages.append({"role": role, "text": text})
    st.session_state._need_scroll = True


def chat_input(label_key: str, placeholder: str = "Type here...") -> Optional[str]:
    return st.chat_input(placeholder=placeholder, key=label_key)


def buttons(options, key_prefix: str) -> Optional[str]:
    cols = st.columns(min(4, len(options)))
    chosen = None
    for i, opt in enumerate(options):
        if cols[i % len(cols)].button(opt, key=f"{key_prefix}_{i}"):
            chosen = opt
            # 按钮点击也触发滚动标记（下一次渲染后滚动到底部）
            try:
                st.session_state._need_scroll = True
            except Exception:
                pass
    return chosen


def set_stage(next_stage: str) -> None:
    st.session_state.stage = next_stage
    # 阶段切换通常意味着新消息将出现，先置位滚动标记
    try:
        st.session_state._need_scroll = True
    except Exception:
        pass
    st.rerun()


def scroll_to_bottom():
    # 恢复为页面级滚动：滚动到文档底部与锚点
    st.markdown("<div id='bottom-anchor'></div>", unsafe_allow_html=True)
    components.html(
        """
        <script>
        const go = () => {
          try {
            const el = document.getElementById('bottom-anchor');
            if (el && typeof el.scrollIntoView === 'function') {
              el.scrollIntoView({ behavior: 'instant', block: 'end' });
            }
            window.scrollTo({ top: document.body.scrollHeight, behavior: 'instant' });
          } catch (e) {}
        };
        go();
        if (window && window.requestAnimationFrame) {
          window.requestAnimationFrame(go);
          window.requestAnimationFrame(() => setTimeout(go, 0));
        }
        setTimeout(go, 30);
        setTimeout(go, 80);
        setTimeout(go, 180);
        setTimeout(go, 320);
        </script>
        """,
        height=0,
    )


def ensure_styles():
    # 注入基础布局与按钮样式，并彻底收紧气泡内 Markdown 外边距
    st.markdown(
        """
        <style>
        .block-container { max-width: 680px; padding-left: 0 !important; padding-right: 0 !important; }
        .stButton > button { border-radius: 22px !important; padding: 6px 10px !important; border: 2px solid #7C3AED !important; background: #fff !important; color: #7C3AED !important; font-weight: 600 !important; box-shadow: 0 1px 2px rgba(0,0,0,0.06); }
        .stButton > button:hover { background: #F5F3FF !important; }

        /* 取消独立消息视口，使用页面默认滚动 */

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
    ensure_styles()
    # 仅保留宽度居中容器，取消 #chat-viewport 包裹
    st.markdown('<div style="max-width:680px; margin:0 auto;">', unsafe_allow_html=True)
    for m in st.session_state.messages:
        role = m.get("role", ""); text = (m.get("text", "") or "").lstrip()
        is_right = role == "patient"
        row_style = "display:flex; align-items:flex-start; justify-content:flex-end; gap:8px; margin:10px 0;" if is_right else "display:flex; align-items:flex-start; justify-content:flex-start; gap:8px; margin:10px 0;"
        if is_right:
            bubble_bg = "#7C3AED"; bubble_border = "#6D28D9"; text_color = "#FFFFFF"; role_align = "right"; wrap_align = "flex-end"
        else:
            bubble_bg = "#F3F4F6"; bubble_border = "#E5E7EB"; text_color = "#111827"; role_align = "left"; wrap_align = "flex-start"
        bubble_style = (
            "display:inline-block; max-width:80%; padding:8px 12px; border-radius:14px; line-height:1.45; "
            "box-shadow:0 1px 3px rgba(0,0,0,0.04); word-break:break-word; white-space:pre-wrap; "
            f"background:{bubble_bg}; border:1px solid {bubble_border}; color:{text_color};"
        )
        avatar_html = "🩺" if role == "doctor" else ("🧑‍💼" if role == "receptionist" else "🙂")
        role_label = role
        avatar_box = f"<div style=\"font-size:14px; line-height:1;\">{avatar_html}</div>"
        role_box = f"<div style=\"font-size:10px; opacity:.65; margin-bottom:2px; text-align:{role_align};\"><span style=\"font-weight:600;\">{role_label}</span></div>"
        bubble_box = f"<div class=\"bubble-text\" style=\"{bubble_style}\">{text}</div>"
        wrap_style = f"display:flex; flex-direction:column; align-items:{wrap_align}; max-width:100%;"

        if is_right:
            st.markdown(
                f"""
                <div style=\"{row_style}\">
                  <div style=\"{wrap_style}\">{role_box}{bubble_box}</div>
                  {avatar_box}
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div style=\"{row_style}\">
                  {avatar_box}
                  <div style=\"{wrap_style}\">{role_box}{bubble_box}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown('</div>', unsafe_allow_html=True)


def landing():
    st.title("🩺 E-Health Preventive Check-Up")
    st.caption("Welcome to your wellness consultation with Dr. Alex")
    
    if st.button("Start Consultation"):
        set_stage("receptionist_intro")
    if st.button("Reset"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        init_state()
        st.rerun()


# ---------------- Single Visit (Strict English Script) -----------------
def receptionist_intro():
    say("receptionist", "Hi, welcome to the e-health platform")
    say("patient", "[Hi]")
    say("receptionist", "How can I help you today?")
    if buttons(["[wellness checkup]"], "wel_btn"):
        say("receptionist", "Sure. Please bear with me until I connect you to Dr. Alex. Meanwhile, you can read a brief introduction of Dr. Alex.")
        say("receptionist", "Dr. Alex received a medical degree from the University of Pittsburgh School of Medicine in 2005 and has been board certified in preventive care and medicine. Dr. Alex's particular expertise includes nutrition, fitness, and lifestyle.")
        set_stage("doctor_greet")


def doctor_flow():
    stage = st.session_state.stage
    p = st.session_state.profile

    if stage == "doctor_greet":
        say("doctor", "Hi, I am Dr. Alex. How would you like to be addressed?")
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
                say("doctor", "[if yes] What are some health problems you have?")
                ans = chat_input("issues_detail", "[answer input]")
                if ans:
                    p["issues_detail"] = ans
                    say("patient", f"[{ans}]")
                    say("doctor", "Thanks for letting me know. I will take your health status into account when providing suggestions.")
                    say("doctor", "What do you do for a living?")
                    set_stage("doctor_job")
            else:
                say("doctor", "What do you do for a living?")
                set_stage("doctor_job")

    elif stage == "doctor_job":
        ans = chat_input("job", "[answer input]")
        if ans:
            p["occupation"] = ans
            say("patient", f"[{ans}]")
            say("doctor", "[If employed] How stressful are you at work? From 0-10, can you give me a number?")
            set_stage("doctor_stress")

    elif stage == "doctor_stress":
        ans = chat_input("stress", "[answer input]")
        if ans:
            p["work_stress"] = ans
            say("patient", f"[{ans}]")
            say("doctor", "Got it. Managing stress is an important and challenging task. But you know, stress isn't always bad. Sometimes it can motivate us to get things done.")
            say("doctor", "What do you often do to relax yourself?")
            set_stage("doctor_relax")

    elif stage == "doctor_relax":
        ans = chat_input("relax", "[answer input]")
        if ans:
            p["relax"] = ans
            say("patient", f"[{ans}]")
            say("doctor", "I am glad that you know how to wind down.")
            say("doctor", "Do you currently smoke cigarettes?")
            set_stage("doctor_smoke")

    elif stage == "doctor_smoke":
        clicked = buttons(["[Yes]", "[No]"], "smoke")
        if clicked:
            say("patient", clicked)
            if clicked == "[Yes]":
                say("doctor", "[if Yes] Were you smoking 6 months ago?")
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
                say("doctor", "[if Yes] How often do you drink alcohol?")
                set_stage("doctor_drink_freq")
            else:
                say("doctor", "You know people have used alcohol and cigarettes to relieve stress for centuries. But, research results are mixed in terms of whether it can actually reduce stress.")
                say("doctor", "How often do you exercise?")
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
                say("doctor", "[If not \"never\"] What are some of the exercises you enjoy?")
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
                say("doctor", "[high loneliness] It seems like you are quite lonely. I'll suggest you talk to your friends and family more frequently. It may help.")
            elif clicked == "[some of the time]":
                say("doctor", "[medium loneliness] It seems like you are a little bit lonely. I'll suggest you talk to your friends and family more frequently. It may help.")
            else:
                say("doctor", "[low loneliness] It seems like you are not lonely at all. I am glad that you feel supported and fulfilled in your relationship,")
            say("doctor", "Next, I would like to know what you're currently eating.")
            say("doctor", "You probably know that most foods can be categorized into five major groups, namely Fruit, Vegetables, Grains, Protein, and Dairy. I would like to know how often you eat from each group.")
            say("patient", "[OK]")
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
        clicked = buttons(["[yes]", "[no]"], "family_sleep")
        if clicked:
            say("patient", clicked)
            say("doctor", "Based on our chat, I think you are doing fine. But, you can always do better. After reviewing the AI system's recommendation, here is my advice for you:\n\n●Exercise at least 150 minutes a week. Choose moderate intensity activity such as brisk walking.\n●Improve your strength and flexibility. Practice muscle-strengthening activities at least 2 days a week, such as squats.\n●Customize and enjoy nutrient-dense food and beverage choices to reflect your personal preferences, cultural traditions, and budgetary considerations.\n●Choose a mix of healthy foods you like from each of the five groups: whole fruit, veggies, whole grains, proteins, and dairy.\n●Limit foods and beverages that are higher in added sugars, saturated fat, and sodium (salt).")
            say("doctor", "Our receptionist will send you pamphlets of good practices of exercise and diet.")
            say("doctor", "Thanks for your visit.")
            say("doctor", "[The doctor has left the chat]")
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
    render_messages()

    # 后续根据阶段路由可能继续追加消息，先不滚动，等路由处理后统一滚动

    if st.session_state.stage == "landing":
        landing()
        return

    if st.session_state.stage == "receptionist_intro":
        receptionist_intro()
    else:
        doctor_flow()

    if st.session_state.stage == "end":
        st.success("Dialogue ended. Thank you!")

    # 在全部渲染后统一滚动到底部
    if st.session_state.get("_need_scroll"):
        scroll_to_bottom()
        st.session_state._need_scroll = False


if __name__ == "__main__":
    main()


