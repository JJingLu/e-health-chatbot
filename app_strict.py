import streamlit as st
import streamlit.components.v1 as components
from typing import Optional, Dict, Any


st.set_page_config(page_title="E-Health Preventive Check-Up (Strict Script)", page_icon="🩺", layout="centered")


def init_state():
    if "init" in st.session_state:
        return
    st.session_state.init = True
    st.session_state.stage = "landing"
    st.session_state.visit_round = "first"  # first | second_social | second_medical | second_non_medical | second_non_social
    st.session_state.condition = "human"  # human | ai | ai_assisted
    st.session_state.messages = []
    st.session_state._need_scroll = False  # 新消息出现时触发滚动
    st.session_state.profile = {
        "preferred_name": None,
        "first_time_online": None,
        "topics": [],
        "ongoing_issues": None,
        "issues_detail": None,
        "occupation": None,
        "work_busy": None,
        "stress_0_10": None,
        "relax": None,
        "smoke_now": None,
        "smoke_6m": None,
        "smoke_12m": None,
        "drink": None,
        "drink_freq": None,
        "exercise_freq": None,
        "exercise_types": None,
        "family_good": None,
        "companionship": None,
        "fruit_freq": None,
        "veg_freq": None,
        "grain_freq": None,
        "protein_freq": None,
        "dairy_freq": None,
        "food_allergy": None,
        "allergy_items": None,
        "cook_at_home": None,
        "try_new_recipes": None,
        "sleep_quality_1_5": None,
        "screen_before_bed": None,
        "fall_asleep_latency": None,
        "diff_fall_asleep": None,
        "night_wake_diff": None,
        "morning_tired": None,
        "family_sleep_history": None,
        # second visit
        "mturk_id": None,
        "depressed_level": None,
        "weight_change": None,
        "favorite_activity": None,
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
    st.title("🩺 E-Health Preventive Check-Up (Strict Script)")
    st.caption("All texts follow the provided English script verbatim.")

    st.session_state.visit_round = st.selectbox(
        "Visit Round",
        [
            "first",
            "second_social",
            "second_medical",
            "second_non_medical",
            "second_non_social",
        ],
        format_func=lambda x: {
            "first": "First Doctor Visit",
            "second_social": "Second Visit (Individuation: Social Info)",
            "second_medical": "Second Visit (Individuation: Medical Info)",
            "second_non_medical": "Second Visit (No Individuation Based on Medical Info)",
            "second_non_social": "Second Visit (No Individuation Based on Social Info)",
        }[x],
    )
    st.session_state.condition = st.selectbox(
        "Doctor Condition",
        ["human", "ai", "ai_assisted"],
        format_func=lambda x: {
            "human": "Human doctor condition",
            "ai": "AI doctor condition",
            "ai_assisted": "AI-assisted human doctor condition",
        }[x],
    )

    c1, c2 = st.columns(2)
    if c1.button("Start"):
        set_stage("receptionist_intro")
    if c2.button("Reset"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        init_state()
        st.rerun()


# ---------------- First Visit (Strict English Script) -----------------
def receptionist_intro_first():
    say("receptionist", "Hi, welcome to the e-health platform")
    say("receptionist", "How can I help you today?")
    if buttons(["[wellness checkup]"], "wel_btn"):
        if st.session_state.condition == "human":
            say("receptionist", "Sure. Please bear with me until I connect you to Dr. Alex. Meanwhile, you can read a brief introduction of Dr. Alex.")
            say(
                "receptionist",
                "\nDr. Alex received a medical degree from the University of Pittsburgh School of Medicine in 2005 and has been board certified in preventive care and medicine. Dr. Alex’s particular expertise includes nutrition, fitness, and lifestyle.",
            )
        elif st.session_state.condition == "ai":
            say("receptionist", "Thanks for completing the form. Please bear with us until we connect you to AI Dr. Alex. Meanwhile, you can read a brief introduction of AI Dr. Alex.")
            say(
                "receptionist",
                "\nDr. Alex is an AI medical system developed at the University of Pittsburgh School of Medicine. It has been trained based on deep learning algorithms for providing preventive care and medicine. AI Dr. Alex’s particular expertise includes nutrition, fitness, and lifestyle.",
            )
        else:
            say("receptionist", "Thanks for completing the form. Please bear with us until we connect you to Dr. Alex that will be assisted by an AI medical system. Meanwhile you can read a brief introduction of Dr. Alex and the AI medical system.")
            say(
                "receptionist",
                "\nDr. Alex is a board-certified preventive medicine specialist who received a medical degree from the University of Pittsburgh School of Medicine in 2005. Dr. Alex’s particular expertise includes nutrition, fitness, and lifestyle.\n\nThe AI medical system assisting Dr. Alex is based on deep learning algorithms for providing preventive care and medicine.",
            )
        set_stage("doctor_first_greet")


def doctor_first_flow():
    stage = st.session_state.stage
    p = st.session_state.profile

    if stage == "doctor_first_greet":
        say("doctor", "Hi, I am Dr. Alex. How would you like to be addressed?")
        name = chat_input("name_first", "[preferred name input]")
        if name:
            p["preferred_name"] = name
            say("patient", f"[{name}]")
            say("doctor", f"{name}, nice to meet you.")
            say("doctor", "How are you doing lately?")
            set_stage("doctor_first_feel")
    elif stage == "doctor_first_feel":
        clicked = buttons(["[good]", "[bad]", "[hard to say]"], "first_feel")
        if clicked:
            say("patient", clicked)
            say("doctor", "Is this your first-time consulting doctors online for wellness?")
            set_stage("doctor_first_online")

    elif stage == "doctor_first_online":
        clicked = buttons(["[yes]", "[no]"], "first_online")
        if clicked:
            say("patient", clicked)
            say("doctor", "Well, lots of people have consulted me about wellness. What topics do you want to know more about today?")
            set_stage("doctor_first_topics")

    elif stage == "doctor_first_topics":
        opts = ["[diet]", "[fitness]", "[sleep]", "[lifestyle]"]
        st.write("Select topics (click all that apply), then press Continue:")
        cols = st.columns(4)
        chosen = []
        for i, o in enumerate(opts):
            if cols[i].checkbox(o, key=f"topic_{i}"):
                chosen.append(o)
        if st.button("Continue", key="first_topics_go"):
            p["topics"] = chosen
            say("patient", ", ".join(chosen) if chosen else "[]")
            say("doctor", "Great. I will be sure to cover it in this checkup.")
            say("doctor", "Do you have any ongoing health issues that I should be aware of?")
            set_stage("doctor_first_ongoing")

    elif stage == "doctor_first_ongoing":
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
                    set_stage("doctor_first_job")
            else:
                say("doctor", "What do you do for a living?")
                set_stage("doctor_first_job")

    elif stage == "doctor_first_job":
        ans = chat_input("job", "[answer input]")
        if ans:
            p["occupation"] = ans
            say("patient", f"[{ans}]")
            say("doctor", "[If employed] How busy are you at work?")
            set_stage("doctor_first_busy")

    elif stage == "doctor_first_busy":
        ans = chat_input("busy", "[answer input]")
        if ans:
            p["work_busy"] = ans
            say("patient", f"[{ans}]")
            say("doctor", "How stressful is your job? From 0-10, can you give me a number?")
            set_stage("doctor_first_stress")

    elif stage == "doctor_first_stress":
        nums = [f"[{i}]" for i in range(0, 11)]
        clicked = buttons(nums, "stress")
        if clicked:
            say("patient", clicked)
            say("doctor", "Got it. Managing stress is an important and challenging task. But you know, stress isn’t always bad. Sometimes it can motivate us to get things done.")
            say("doctor", "What do you often do to relax yourself?")
            set_stage("doctor_first_relax")

    elif stage == "doctor_first_relax":
        ans = chat_input("relax", "[answer input]")
        if ans:
            p["relax"] = ans
            say("patient", f"[{ans}]")
            say("doctor", "I am glad that you know how to wind down.")
            say("doctor", "Do you currently smoke cigarettes?")
            set_stage("doctor_first_smoke_now")

    elif stage == "doctor_first_smoke_now":
        clicked = buttons(["[Yes]", "[No]"], "smoke_now")
        if clicked:
            say("patient", clicked)
            if clicked == "[Yes]":
                say("doctor", "[if Yes] Were you smoking 6 months ago?")
                set_stage("doctor_first_smoke_6")
            else:
                say("doctor", "Do you drink alcohol?")
                set_stage("doctor_first_drink")

    elif stage == "doctor_first_smoke_6":
        clicked = buttons(["[Yes]", "[No]"], "smoke_6")
        if clicked:
            say("patient", clicked)
            say("doctor", "[if Yes] Were you smoking 12 months ago?")
            set_stage("doctor_first_smoke_12")

    elif stage == "doctor_first_smoke_12":
        clicked = buttons(["[Yes]", "[No]"], "smoke_12")
        if clicked:
            say("patient", clicked)
            say("doctor", "Do you drink alcohol?")
            set_stage("doctor_first_drink")

    elif stage == "doctor_first_drink":
        clicked = buttons(["[Yes]", "[No]"], "drink")
        if clicked:
            say("patient", clicked)
            if clicked == "[Yes]":
                say("doctor", "[if Yes] How often do you drink alcohol?")
                set_stage("doctor_first_drink_freq")
            else:
                say("doctor", "You know people have used alcohol and cigarettes to relieve stress for centuries. But, research results are mixed in terms of whether it can really reduce stress.")
                say("doctor", "Do you exercise recently? How often do you exercise?")
                set_stage("doctor_first_exercise")

    elif stage == "doctor_first_drink_freq":
        clicked = buttons([
            "[1-2 days a week]",
            "[3-5 days a week]",
            "[6-7 days a week]",
        ], "drink_freq")
        if clicked:
            say("patient", clicked)
            say("doctor", "You know people have used alcohol and cigarettes to relieve stress for centuries. But, research results are mixed in terms of whether it can really reduce stress.")
            say("doctor", "Do you exercise recently? How often do you exercise?")
            set_stage("doctor_first_exercise")

    elif stage == "doctor_first_exercise":
        clicked = buttons([
            "[never]",
            "[1-2 days per week]",
            "[3-5 days per week]",
            "[6+ days per week]",
        ], "exercise")
        if clicked:
            say("patient", clicked)
            if clicked == "[never]":
                set_stage("doctor_first_family")
            else:
                say("doctor", "[If not “never”] What are some of the exercises you enjoy?")
                # 跳转到独立阶段，避免重复追加提示
                set_stage("doctor_first_exercise_types")

    elif stage == "doctor_first_exercise_types":
        ans = chat_input("exercise_types", "[answer input]")
        if ans:
            say("patient", f"[{ans}]")
            set_stage("doctor_first_family")

    elif stage == "doctor_first_family":
        clicked = buttons(["[Yes]", "[No]"], "family")
        if clicked:
            say("patient", clicked)
            say("doctor", "How often do you feel that you lack companionship?")
            set_stage("doctor_first_lonely")

    elif stage == "doctor_first_lonely":
        clicked = buttons([
            "[Hardly ever or never]",
            "[some of the time]",
            "[often]",
        ], "lonely")
        if clicked:
            say("patient", clicked)
            if clicked == "[often]":
                say("doctor", "[high loneliness] It seems like you are quite lonely. I'll suggest you talk to your friends and family more frequently. It may help.")
            elif clicked == "[some of the time]":
                say("doctor", "[medium loneliness] It seems like you are a little bit lonely. I'll suggest you talk to your friends and family more frequently. It may help.")
            else:
                say("doctor", "[low loneliness] It seems like you are not lonely at all. I am glad that you feel supported and fulfilled in your relationship,")
            say("doctor", "Next, I would like to know what you’re currently eating.")
            say("doctor", "You probably know that most foods can be categorized into five major groups, namely Fruit, Vegetables, Grains, Protein, and Dairy. I would like to know how often you eat from each group.")
            set_stage("doctor_first_food_fruit")

    elif stage == "doctor_first_food_fruit":
        say("doctor", "How often do you eat fruits, such as apples, bananas, or oranges? The fruit can be fresh, frozen, canned, or dried. 100% fruit juice also counts as fruit.")
        clicked = buttons([
            "[0-2 days per week]",
            "[3-5 days per week]",
            "[6+ days per week]",
        ], "fruit")
        if clicked:
            say("patient", clicked)
            say("doctor", "How about vegetables, like broccoli and cabbage?")
            set_stage("doctor_first_food_veg")

    elif stage == "doctor_first_food_veg":
        clicked = buttons([
            "[0-2 days per week]",
            "[3-5 days per week]",
            "[6+ days per week]",
        ], "veg")
        if clicked:
            say("patient", clicked)
            say("doctor", "How often do you eat grains, such as wheat, bread, and pasta? Foods such as popcorn, rice, and oatmeal are also included as grains.")
            set_stage("doctor_first_food_grain")

    elif stage == "doctor_first_food_grain":
        clicked = buttons([
            "[0-2 days per week]",
            "[3-5 days per week]",
            "[6+ days per week]",
        ], "grain")
        if clicked:
            say("patient", clicked)
            say("doctor", "How about protein foods, such as seafood, meat, poultry, eggs, beans, peas, lentils, nuts, seeds, or soy products?")
            set_stage("doctor_first_food_protein")

    elif stage == "doctor_first_food_protein":
        clicked = buttons([
            "[0-2 days per week]",
            "[3-5 days per week]",
            "[6+ days per week]",
        ], "protein")
        if clicked:
            say("patient", clicked)
            say("doctor", "How often do you eat dairy products, such as dairy milk, yogurt, and cheese?")
            set_stage("doctor_first_food_dairy")

    elif stage == "doctor_first_food_dairy":
        clicked = buttons([
            "[0-2 days per week]",
            "[3-5 days per week]",
            "[6+ days per week]",
        ], "dairy")
        if clicked:
            say("patient", clicked)
            say("doctor", "Do you have any food allergies?")
            set_stage("doctor_first_allergy")

    elif stage == "doctor_first_allergy":
        clicked = buttons(["[yes]", "[no]"], "allergy")
        if clicked:
            say("patient", clicked)
            if clicked == "[yes]":
                say("doctor", "[if yes] What food are you allergic to?")
                ans = chat_input("allergy_items", "[answer input]")
                if ans:
                    say("patient", f"[{ans}]")
                    say("doctor", "I will take this into account when providing suggestions.")
                    say("doctor", "Do you usually cook at home?")
                    set_stage("doctor_first_cook")
            else:
                say("doctor", "I will take this into account when providing suggestions.")
                say("doctor", "Do you usually cook at home?")
                set_stage("doctor_first_cook")

    elif stage == "doctor_first_cook":
        clicked = buttons(["[Yes]", "[No]"], "cook")
        if clicked:
            say("patient", clicked)
            say("doctor", "How often do you try new recipes?")
            set_stage("doctor_first_new_recipes")

    elif stage == "doctor_first_new_recipes":
        clicked = buttons(["[Never]", "[ Rarely]", "[ Sometimes]", "[ Often]", "[ Always]"], "new_recipes")
        if clicked:
            say("patient", clicked)
            say("doctor", "How is your sleep quality lately? If 1 means very bad and 5 means very good, can you give me a number?")
            set_stage("doctor_first_sleep_quality")

    elif stage == "doctor_first_sleep_quality":
        ans = chat_input("sleep_q", "[Answer input]")
        if ans:
            say("patient", f"[{ans}]")
            say("doctor", "Any screen time before bed? That is, do you look at a smartphone or tablet before falling asleep?")
            set_stage("doctor_first_screen")

    elif stage == "doctor_first_screen":
        clicked = buttons(["[Yes]", "[No]"], "screen")
        if clicked:
            say("patient", clicked)
            say("doctor", "How long after getting in bed do you usually fall asleep?")
            set_stage("doctor_first_latency")

    elif stage == "doctor_first_latency":
        clicked = buttons(["[immediately]", "[10-15 minutes]", "[20-40 minutes]", "[longer]"], "latency")
        if clicked:
            say("patient", clicked)
            say("doctor", "How often do you have difficulty falling asleep (1 hour or longer)?")
            set_stage("doctor_first_diff_fall")

    elif stage == "doctor_first_diff_fall":
        clicked = buttons(["[never]", "[every once in a while]", "[pretty often]", "[most nights]"], "diff_fall")
        if clicked:
            say("patient", clicked)
            say("doctor", "Do you ever wake in the night and have trouble getting back to sleep?")
            set_stage("doctor_first_wake_trouble")

    elif stage == "doctor_first_wake_trouble":
        clicked = buttons(["[never]", "[every once in a while]", "[pretty often]", "[most nights]"], "wake_trouble")
        if clicked:
            say("patient", clicked)
            say("doctor", "How often do you wake up in the morning still feeling tired?")
            set_stage("doctor_first_morning_tired")

    elif stage == "doctor_first_morning_tired":
        clicked = buttons(["[never]", "[every once in a while]", "[pretty often]", "[most nights]"], "morning_tired")
        if clicked:
            say("patient", clicked)
            say("doctor", "Some people have problems sleeping due to genetic reasons. Do you have a family history of sleep disorders, such as narcolepsy or sleep apnea?")
            set_stage("doctor_first_family_sleep")

    elif stage == "doctor_first_family_sleep":
        clicked = buttons(["[yes]", "[no]"], "family_sleep")
        if clicked:
            say("patient", clicked)
            say("doctor", "Based on our chat, I think you are doing fine. But, you can always do better. After considering the recommendation from the AI system, here is my advice for you (adopted from CDC exercise guideline):\n\n\u25CFExercise at least 150 minutes a week. Choose moderate intensity activity such as brisk walking. \n\u25CFImprove your strength and flexibility. Practice muscle-strengthening activities at least 2 days a week, such as squats. \n\u25CFCustomize and enjoy nutrient-dense food and beverage choices to reflect your personal preferences, cultural traditions, and budgetary considerations.\n\u25CFChoose a mix of healthy foods you like from each of the five groups: whole fruit, veggies, whole grains, proteins, and dairy.\n\u25CFLimit foods and beverages that are higher in added sugars, saturated fat, and sodium (salt).")
            say("doctor", "Our receptionist will send you pamphlets of good practices of exercise and diet.")
            say("doctor", "Thanks for your visit.")
            say("receptionist", "You can right-click to save the pamphlets.")
            say("receptionist", "This is the end of your first doctor's visit. Here’s the access code for you to continue the questionnaire: 9087. Please copy the code and return it to the questionnaire page to proceed.")
            st.session_state.stage = "end"


# ---------------- Second Visits -----------------
def receptionist_common_second():
    say("receptionist", "Hi, welcome to the e-health platform")
    say("receptionist", "How can I help you today?")
    if not buttons(["[Wellness Checkup]"], "wel2"):
        return False
    say("receptionist", "Have you used our platform before?")
    used = buttons(["[Yes]", "[No]"], "used")
    if not used:
        return False
    say("patient", used)
    if used == "[No]":
        say("receptionist", "[If No] This platform only opens for registered users who visited this platform previously. Thanks for visiting us.")
        set_stage("end")
        return False
    say("receptionist", "[If Yes] Thanks for visiting us again. What is your MTurk ID?")
    mturk = chat_input("mturk", "[ID input]")
    if not mturk:
        return False
    st.session_state.profile["mturk_id"] = mturk
    say("patient", f"[{mturk}]")
    say("receptionist", "Thanks for the information. I will connect you with the doctor you visited last time.")

    # Condition intros
    if st.session_state.condition == "ai":
        say("receptionist", "\nAI doctor condition\n\nThanks for completing the form. Please bear with us until we connect you to AI Dr. Alex. Meanwhile, you can read a brief introduction of AI Dr. Alex.\n\nDr. Alex is an AI medical system developed at the University of Pittsburgh School of Medicine. It has been trained based on deep learning algorithms for providing preventive care and medicine. AI Dr. Alex’s particular expertise includes nutrition, fitness, and lifestyle.")
    elif st.session_state.condition == "human":
        say("receptionist", "\nHuman doctor condition\n\nThanks for completing the form. Please bear with us until we connect you to Dr. Alex. Meanwhile, you can read a brief introduction of Dr. Alex.\n\nDr. Alex received a medical degree from the University of Pittsburgh School of Medicine in 2005 and has been board certified in preventive care and medicine. Dr. Alex’s particular expertise includes nutrition, fitness, and lifestyle.")
    else:
        say("receptionist", "\nAI-assisted human doctor condition\n\nThanks for completing the form. Please bear with us until we connect you to Dr. Alex that will be assisted by an AI medical system. Meanwhile you can read a brief introduction of Dr. Alex and the AI medical system. \n\nDr. Alex is a board-certified preventive medicine specialist who received a medical degree from the University of Pittsburgh School of Medicine in 2005. Dr. Alex’s particular expertise includes nutrition, fitness, and lifestyle.\n\nThe AI medical system assisting Dr. Alex is based on deep learning algorithms for providing preventive care and medicine.")
    return True


def second_social_flow():
    if not receptionist_common_second():
        return
    name = st.session_state.profile.get("preferred_name") or "[insert patient’s preferred name]"
    say("doctor", f"Hi, {name}. How is everything going since your last visit?")
    g = buttons(["[good]", "[bad]"], "2s_goodbad")
    if not g:
        return
    say("patient", g)
    say("doctor", "I hope your family is doing well.  Are they?")
    fam = buttons(["[Yes]", "[No]"], "2s_fam")
    if not fam:
        return
    say("patient", fam)
    if fam == "[Yes]":
        say("doctor", "[if yes] That’s good.")
    else:
        say("doctor", "[if no] I’m sorry to hear that.")

    say("doctor", "[Individuation 1]\n\nIt seems like you were [not very/very] busy at work two weeks ago. How about now? Any changes in your working schedule?")
    chg = buttons(["[Yes]", "[No]"], "2s_busy_change")
    if not chg:
        return
    say("patient", chg)
    say("doctor", "[If still not very busy] Good. I am glad that you are not overwhelmed by your work.\n\n[If become very busy] Yeah, same here. I hope you still have time to take care of yourself.")

    say("doctor", "[Individuation 2]\n\nLast time, you mentioned that you [have/do not have] a good relationship with your family. Is it still the case?")
    fam2 = buttons(["[yes]", "[no]"], "2s_rel")
    if not fam2:
        return
    say("patient", fam2)
    say("doctor", "[Have a good relationship] Great! Having a good family relationship is beneficial to your health. \n\n[Do not have a good relationship] I see. I hope you have friends to talk to about these issues.")

    say("doctor", "[Individuation 3]\n\nI remember you [were/were not] cooking at home. Is it still the case?")
    c = buttons(["[Yes]", "[No]"], "2s_cook")
    if not c:
        return
    say("patient", c)
    say("doctor", "You know it is healthier to cook at home since you have control over what you are eating.")

    say("doctor", "[Individuation 4]\n\nEarlier, you said that you [did not have/had] screen time before bed. Any changes?")
    sc = buttons(["[Yes]", "[No]"], "2s_screen")
    if not sc:
        return
    say("patient", sc)
    say("doctor", "It is better not using electronic devices two hours before bed because it can interfere with your sleep.")

    say("doctor", "[Individuation 5]\n\nHave you been able to [insert the patient’s favorite activity] lately?")
    fav = buttons(["[Yes]", "[No]"], "2s_fav")
    if not fav:
        return
    say("patient", fav)
    if fav == "[Yes]":
        say("doctor", "[If yes] Great! I am glad that you have time to do things you enjoy.")
    else:
        say("doctor", "[If no] I understand. I hope you have time to do things you enjoy.")

    say("doctor", "Based on our chat, I think you are making improvements. Here is some advice for you (adopted from CDC exercise guideline):\n\n\u25CFExercise at least 150 minutes a week. Choose moderate intensity activity such as brisk walking. \n\u25CFImprove your strength and flexibility. Practice muscle-strengthening activities at least 2 days a week, such as squats. \n\u25CFCustomize and enjoy nutrient-dense food and beverage choices to reflect your personal preferences, cultural traditions, and budgetary considerations.\n\u25CFChoose a mix of healthy foods you like from each of the five groups: whole fruit, veggies, whole grains, proteins, and dairy.\n\u25CFLimit foods and beverages that are higher in added sugars, saturated fat, and sodium (salt).")
    say("doctor", "Our receptionist will send you pamphlets of good practices of exercise and diet. It is the same pamphlets we offered you last time.")
    say("doctor", "[Provision of privacy control]\n\nDo you want me to put today’s visit in your record?")
    r = buttons(["[Yes]", "[No]"], "2s_record")
    if not r:
        return
    say("patient", r)
    say("doctor", "OK. Do you want to keep your personal medical information on our platform?")
    k = buttons(["[Yes]", "[No]"], "2s_keep")
    if not k:
        return
    say("patient", k)
    say("doctor", "Ok, [insert patient’s name], thanks for the visit. Please feel free to contact me if you have any concerns or questions.")
    say("receptionist", "You can right-click to save the pamphlets.")
    say("receptionist", "This is the end of the conversation with the doctor. Here’s the access code for you to continue the questionnaire: 9246. Please copy the code and return it to the questionnaire page to proceed.")
    st.session_state.stage = "end"


def second_medical_flow():
    if not receptionist_common_second():
        return
    name = st.session_state.profile.get("preferred_name") or "[insert patient’s preferred name]"
    say("doctor", f"Hi, {name}. How is everything going since your last visit?")
    g = buttons(["[good]", "[bad]"], "2m_goodbad")
    if not g:
        return
    say("patient", g)
    say("doctor", "I hope your family is doing well.  Are they?")
    fam = buttons(["[Yes]", "[No]"], "2m_fam")
    if not fam:
        return
    say("patient", fam)
    if fam == "[Yes]":
        say("doctor", "[if yes] That’s good.")
    else:
        say("doctor", "[if no] I’m sorry to hear that.")

    say("doctor", "[Individuation 1]\n\nIt seems like you were [a little bit/somewhat/very] depressed about two weeks ago. How about now?")
    dep = buttons(["[feel better]", "[feel worse]", "[nothing changed]"], "2m_dep")
    if not dep:
        return
    say("patient", f"{dep} []")
    say("doctor", "[If still depressed] Sorry to hear that you are not feeling good. Depression and other mental issues may be hard to solve in a short period of time. You may want to talk with a therapist or psychological counselor after today’s visit.\n\n[If not depressed] I am glad that you are feeling better. Mental issues such as depression come and go. It may be advisable to talk with a therapist or psychological counselor after today’s visit, just to be on the safe side.")

    say("doctor", "[Individuation 2]\n\nI remember you [do not have/have] a family history of sleep disorder, right?")
    fh = buttons(["[Yes]", "[No]"], "2m_sleep_fh")
    if not fh:
        return
    say("patient", fh)

    say("doctor", "[Individuation 3]\n\nIt seems that you did not consume much from the [fruit/vegetable/grain/protein/diary] group last time. Have you followed the recommendation to eat from all five food groups?")
    all5 = buttons(["[Yes]", "[No]"], "2m_all5")
    if not all5:
        return
    say("patient", all5)
    if all5 == "[Yes]":
        say("doctor", "[If yes] Great! Keep doing that. It is good to have a balanced diet.")
    else:
        say("doctor", "[If no] I see. It is always difficult to get it started. Once you get started, you will feel the benefit from a balanced diet.")

    say("doctor", "[Individuation 4]\n\nLast time, you mentioned that you [have/do not have] food allergies. Is this correct?")
    fa = buttons(["[yes]", "[no]"], "2m_fa")
    if not fa:
        return
    say("patient", fa)
    say("doctor", "[If no food allergy]  Good. I would recommend you to eat from all five food groups. It is good to have a balanced diet.\n[if still have food allergy] Generally, I would recommend people to eat from all five groups. But, this is not the case for you. As you know, you should avoid food that can trigger your allergy.")

    say("doctor", "[Individuation 5]\n\nI remember you [are/are not] in a healthy weight range. Any changes in your weight recently?")
    wc = buttons([
        "[Largely increased]",
        "[slightly increased]",
        "[the same]",
        "[slightly decreased]",
        "[largely decreased]",
    ], "2m_wchange")
    if not wc:
        return
    say("patient", wc)
    say("doctor", "[If changes slightly] Weight change is very normal. As long as you are in a healthy range, you are good.\n[If changes significantly] It is very unusual to experience significant weight change in about two weeks. You may want to talk to a psychological counselor about this.\n[if healthy but no change] Great. You are on a good track.\n[if unhealthy but no change] It is challenging to lose weight. I believe having a balanced diet and exercising more can help.")

    say("doctor", "Based on our chat, I think you are making improvements. Here is some advice for you (adopted from CDC exercise guidelines):\n\n\u25CFExercise at least 150 minutes a week. Choose moderate intensity activity such as brisk walking. \n\u25CFImprove your strength and flexibility. Practice muscle-strengthening activities at least 2 days a week, such as squats. \n\u25CFCustomize and enjoy nutrient-dense food and beverage choices to reflect your personal preferences, cultural traditions, and budgetary considerations.\n\u25CFChoose a mix of healthy foods you like from each of the five groups: whole fruit, veggies, whole grains, proteins, and dairy.\n\u25CFLimit foods and beverages that are higher in added sugars, saturated fat, and sodium (salt).")
    say("doctor", "Our receptionist will send you pamphlets of good practices of exercise and diet. It is the same pamphlets we offered you last time.")
    say("doctor", "[Provision of privacy control]\n\nDo you want me to put today’s visit in your record?")
    r = buttons(["[Yes]", "[No]"], "2m_record")
    if not r:
        return
    say("patient", r)
    say("doctor", "OK. Do you want to keep your personal medical information on our platform?")
    k = buttons(["[Yes]", "[No]"], "2m_keep")
    if not k:
        return
    say("patient", k)
    say("doctor", "Sure. [insert patient’s name], thanks for the visit. Please feel free to contact me if you have any health concerns or questions.")
    say("receptionist", "You can right-click to save the pamphlets.")
    say("receptionist", "This is the end of the conversation with the doctor. Here’s the access code for you to continue the questionnaire: 9246. Please copy the code and return it to the questionnaire page to proceed.")
    st.session_state.stage = "end"


def second_non_medical_flow():
    if not receptionist_common_second():
        return
    say("doctor", "Hi, how is everything going since your last visit?")
    g = buttons(["[good]", "[bad]"], "2nm_goodbad")
    if not g:
        return
    say("patient", g)
    say("doctor", "I hope your family is doing well.  Are they?")
    fam = buttons(["[Yes]", "[No]"], "2nm_fam")
    if not fam:
        return
    say("patient", fam)
    if fam == "[Yes]":
        say("doctor", "[if yes] That’s good.")
    else:
        say("doctor", "[if no] I’m sorry to hear that.")
    say("patient", "[good/bad]")
    say("doctor", "May I know how you would like to be addressed?")
    name = chat_input("2nm_name", "[name input]")
    if not name:
        return
    say("patient", f"[{name}]")

    say("doctor", "[Non-Individuation 1]\n\nI do not remember whether we discussed your diet previously. Is it ok if I ask a few questions about it?")
    if not buttons(["[sure]"], "2nm_ok"):
        return
    say("patient", "[sure]")

    say("doctor", "How often do you eat from the Fruit group, such as apples, bananas, and oranges? The fruit can be fresh, frozen, canned, or dried. Also, 100% fruit juice also counts as fruit.")
    buttons(["[0-2 days per week]", "[3-5 days per week]", "[6+ days per week]"], "2nm_fruit")
    say("doctor", "How about the Vegetable group, like broccoli and cabbage?")
    buttons(["[0-2 days per week]", "[3-5 days per week]", "[6+ days per week]"], "2nm_veg")
    say("doctor", "How often do you eat grains, such as wheat, bread, and pasta? Foods such as popcorn, rice, and oatmeal are also included as grains.")
    buttons(["[0-2 days per week]", "[3-5 days per week]", "[6+ days per week]"], "2nm_grain")
    say("doctor", "How about protein foods, such as seafood, meat, poultry, eggs, beans, peas, lentils, nuts, seeds, and soy products?")
    buttons(["[0-2 days per week]", "[3-5 days per week]", "[6+ days per week]"], "2nm_protein")
    say("doctor", "How often do you eat from the Dairy group, such as dairy milk, yogurt, and cheese?")
    buttons(["[0-2 days per week]", "[3-5 days per week]", "[6+ days per week]"], "2nm_dairy")

    say("doctor", "[Non-Individuation 2]\n\nI do not recall our discussion of food allergies last time. \nAre you allergic to any food?")
    fa = buttons(["[Yes]", "[No]", "[]"], "2nm_fa")
    if not fa:
        return
    say("patient", fa)
    if fa == "[Yes]":
        say("doctor", "[If yes] What food are you allergic to?")
        ans = chat_input("2nm_fa_items", "[Answer input]")
        if not ans:
            return
        say("patient", f"[{ans}]")

    say("doctor", "[Non-Individuation 3]\n\nCould you please remind me of your weight?")
    w = chat_input("2nm_weight", "[weight input]")
    if not w:
        return
    say("patient", f"[{w}]")
    say("doctor", "Did you gain any weight during Covid?")
    wg = buttons(["[Yes]", "[No]"], "2nm_wg")
    if not wg:
        return
    say("patient", wg)

    say("doctor", "Do you feel down, depressed, or hopeless in the past two weeks?")
    dep = buttons([
        "[Not at all]",
        "[several days]",
        "[more than half of the days]",
        "[nearly every day]",
    ], "2nm_dep")
    if not dep:
        return
    say("patient", dep)
    say("doctor", "[Non-Individuation 4]\n\n[If answer “not at all” or “several days”] I do not have your depression history on top of my head. But I think you are doing fine.\n\n[If answer “more than half of the days” or “nearly every day”] I do not have your depression history on top of my head. If you feel the need to talk to a psychological consultor, I can provide you with a reference.")

    say("Doctor", "How do you sleep lately? If 1 means very bad and 5 means very good, can you give me a number?")
    sl = chat_input("2nm_sleep_q", "[answer input]")
    if not sl:
        return
    say("Patient", f"[{sl}]")

    say("doctor", "[Non-Individuation 5]\n\nRefresh my memory. Do any of your relatives have a sleep disorder?")
    buttons(["[never]", "[rarely]", "[sometimes]", "[often]", "[always]"], "2nm_sleep_rel")
    say("doctor", "OK. Based on our chat, I think you are doing fine. But, you can always do better. Here is some advice for you (adopted from CDC exercise guidelines):\n\n\u25CFExercise at least 150 minutes a week. Choose moderate intensity activity such as brisk walking. \n\u25CFImprove your strength and flexibility. Practice muscle-strengthening activities at least 2 days a week, such as squats. \n\u25CFCustomize and enjoy nutrient-dense food and beverage choices to reflect your personal preferences, cultural traditions, and budgetary considerations.\n\u25CFChoose a mix of healthy foods you like from each of the five groups: whole fruit, veggies, whole grains, proteins, and dairy.\n\u25CFLimit foods and beverages that are higher in added sugars, saturated fat, and sodium (salt).")
    say("doctor", "Our receptionist will send you pamphlets of good practices of exercise, diet, and mental health.")
    say("doctor", "[Provision of privacy control]\n\nDo you want me to put today’s visit in your record?")
    r = buttons(["[Yes]", "[No]"], "2nm_record")
    if not r:
        return
    say("patient", r)
    say("doctor", "OK. Do you want to keep your personal medical information on our platform?")
    k = buttons(["[Yes]", "[No]"], "2nm_keep")
    if not k:
        return
    say("patient", k)
    say("doctor", "Sure. [insert patient’s name], thanks for the visit. Please feel free to contact me if you have any health concerns or questions.")
    say("receptionist", "You can right-click to save the pamphlets.")
    say("receptionist", "This is the end of the conversation with the doctor. Here’s the access code for you to continue the questionnaire: 9246. Please copy the code and return it to the questionnaire page to proceed.")
    st.session_state.stage = "end"


def second_non_social_flow():
    if not receptionist_common_second():
        return
    say("doctor", "Hi, how is everything going since your last visit?")
    g = buttons(["[good]", "[bad]"], "2ns_goodbad")
    if not g:
        return
    say("patient", g)
    say("doctor", "I hope your family is doing well.  Are they?")
    fam = buttons(["[Yes]", "[No]"], "2ns_fam")
    if not fam:
        return
    say("patient", fam)
    if fam == "[Yes]":
        say("doctor", "[if yes] That’s good.")
    else:
        say("doctor", "[if no] I’m sorry to hear that.")
    say("patient", "[good/bad]")
    say("doctor", "May I know how you would like to be addressed?")
    name = chat_input("2ns_name", "[name input]")
    if not name:
        return
    say("patient", f"[{name}]")

    say("doctor", "[Non-Individuation 1]\n\nCould you please remind me what you do for a living?")
    occ = chat_input("2ns_occ", "[occupation input]")
    if not occ:
        return
    say("patient", f"[{occ}]")
    say("doctor", "If 0 means no stress at all and 5 means a lot of stress, may I know how stressful you are lately?")
    s = buttons(["[0]", "[1]", "[2]", "[3]", "[4]", "[5]"], "2ns_stress")
    if not s:
        return
    say("patient", s)

    say("doctor", "[Non-Individuation 2]\n\nI do not remember whether we discussed it previously. What do you do to relax?")
    relax = chat_input("2ns_relax", "[answer input]")
    if not relax:
        return
    say("patient", f"[{relax}]")
    say("doctor", "Do you also use electronic devices right before sleep?")
    buttons(["[Yes]", "[No]", "[]"], "2ns_screen")
    say("doctor", "[Non-Individuation 3]\n\nI do not remember whether I mentioned the negative influence of screen time before bed last time. Just a reminder, it is better not using smartphone or tablet 2 hours before bed as it can influence your sleep quality.")
    say("patient", "[Got it]")
    say("doctor", "Let’s talk about your diet. Do you like cooking?")
    buttons(["[Yes]", "[No]"], "2ns_like_cook")
    say("doctor", "[Non-Individuation 4]\n\nI do not have this information on top of my head. How often do you cook by yourself?")
    buttons(["[never]", "[rarely]", "[sometimes]", "[often]", "[always]"], "2ns_cook_freq")
    say("1doctor", "[Non-Individuation 5]\n\nRefresh my memory. How often do you contact your family and friends?")
    buttons(["[hardly ever or never]", "[some of the time]", "[always]"], "2ns_contact")

    say("doctor", "Based on our chat, I think you are doing fine. But, you can always do better. Here is some advice for you (adopted from CDC exercise guidelines):\n\n\u25CFExercise at least 150 minutes a week. Choose moderate intensity activity such as brisk walking. \n\u25CFImprove your strength and flexibility. Practice muscle-strengthening activities at least 2 days a week, such as squats. \n\u25CFCustomize and enjoy nutrient-dense food and beverage choices to reflect your personal preferences, cultural traditions, and budgetary considerations.\n\u25CFChoose a mix of healthy foods you like from each of the five groups: whole fruit, veggies, whole grains, proteins, and dairy.\n\u25CFLimit foods and beverages that are higher in added sugars, saturated fat, and sodium (salt).")
    say("doctor", "Our receptionist will send you pamphlets of good practices of exercise and diet.")
    say("doctor", "[Provision of privacy control]\n\nDo you want me to put today’s visit in your record?")
    r = buttons(["[Yes]", "[No]"], "2ns_record")
    if not r:
        return
    say("patient", r)
    say("doctor", "OK. Do you want to keep your personal medical information on our platform?")
    k = buttons(["[Yes]", "[No]"], "2ns_keep")
    if not k:
        return
    say("patient", k)
    say("doctor", "Sure. [insert patient’s name], thanks for the visit. Please feel free to contact me if you have any health concerns or questions.")
    say("receptionist", "You can right-click to save the pamphlets.")
    say("receptionist", "This is the end of the conversation with the doctor. Here’s the access code for you to continue the questionnaire: 9246. Please copy the code and return it to the questionnaire page to proceed.")
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

    if st.session_state.visit_round == "first":
        if st.session_state.stage == "receptionist_intro":
            receptionist_intro_first()
        else:
            doctor_first_flow()
        # 处理完阶段后滚动
        scroll_to_bottom()
        return

    # second visits
    if st.session_state.stage == "receptionist_intro":
        # start the appropriate flow immediately after receptionist phase
        pass

    if st.session_state.visit_round == "second_social":
        second_social_flow()
    elif st.session_state.visit_round == "second_medical":
        second_medical_flow()
    elif st.session_state.visit_round == "second_non_medical":
        second_non_medical_flow()
    elif st.session_state.visit_round == "second_non_social":
        second_non_social_flow()

    if st.session_state.stage == "end":
        st.success("Dialogue ended. Thank you!")

    # 在全部渲染后统一滚动到底部
    if st.session_state.get("_need_scroll"):
        scroll_to_bottom()
        st.session_state._need_scroll = False


if __name__ == "__main__":
    main()


