import streamlit as st
import streamlit.components.v1 as components
import cv2
from detector import get_hand_landmarks
from model import predict_sign
import os
import pyautogui

st.set_page_config(page_title="Sign Language Recognition System",
layout="wide"
)

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "run_camera" not in st.session_state:
    st.session_state.run_camera = False

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

if "capture_flag" not in st.session_state:
    st.session_state.capture_flag = False

# ---------------- THEME ----------------
if st.session_state.theme == "dark":
    background_style = """
    background: radial-gradient(circle at top, #1e1b2e, #0f0c1a);
    color: white;
    """
else:
    background_style = """
    background: #ffffff;
    color: black;
    """

# ---------------- CSS ----------------
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    {background_style}
    background-image: url("https://www.transparenttextures.com/patterns/cubes.png");
}}

.block-container {{
    padding-top: 0rem !important;
}}

header, footer {{visibility: hidden;}}

.logo {{
    font-size: 24px;
    font-weight: bold;
    color: #c4b5fd;
}}

.stButton>button {{
    background: linear-gradient(90deg, #a5b4fc, #c4b5fd);
    color: #0f0c1a;
    border-radius: 12px;
    height: 42px;
    width: 100%;
    margin: 5px;
    border: none;
}}

.hero {{
    text-align: center;
    margin-top: 10px;
}}

.hero h1 {{
    font-size: 55px;
}}

.gradient {{
    background: linear-gradient(90deg, #a5b4fc, #c4b5fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.subtext {{
    color: {"#d1d5db" if st.session_state.theme=="dark" else "#475569"};
    font-size: 18px;
    margin-top: 10px;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- NAVBAR ----------------
col1, col2 = st.columns([5,5])

with col1:
    st.markdown('<div class="logo">Sign Language Alphabet Recognition System</div>', unsafe_allow_html=True)

with col2:
    n1, n2, n3, n4 = st.columns([1,1,1,0.6])

    if n1.button("Home", use_container_width=True):
        st.session_state.page = "Home"
        st.rerun()

    if n2.button("Features", use_container_width=True):
        st.session_state.page = "Features"
        st.rerun()

    if n3.button("About", use_container_width=True):
        st.session_state.page = "About"
        st.rerun()

    icon = "☾" if st.session_state.theme == "dark" else "☀"
    if n4.button(icon, use_container_width=True):
        st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
        st.rerun()

# ---------------- HOME ----------------
if st.session_state.page == "Home":

    st.markdown("""
    <div class="hero">
        <h1>
            Translate <span class="gradient">Sign Language</span><br>
            Into Text Instantly
        </h1>
        <div class="subtext">
            A real-time computer vision system that detects hand gestures (A–Z)
            and converts them into readable text in real-time.
        </div>
    </div>
    """, unsafe_allow_html=True)

    components.html("""
   <div style="display:flex; justify-content:center; margin-top:20px;">
    <div style="display:flex; gap:20px; width:85%;">

        <div style="flex:1; background: linear-gradient(135deg, #c7d2fe, #ddd6fe); padding:20px; border-radius:15px; text-align:center;">
            <div style="font-size:16px; color:#0f0c1a;">Deaf and Mute People in India</div>
            <div style="font-size:30px; font-weight:bold; color:#000000;">5,000,000</div>
        </div>

        <div style="flex:1; background: linear-gradient(135deg, #c7d2fe, #ddd6fe); padding:20px; border-radius:15px; text-align:center;">
            <div style="font-size:16px; color:#0f0c1a;">Users of Indian Sign Language</div>
            <div style="font-size:30px; font-weight:bold; color:#000000;">2,700,000</div>
        </div>

        <div style="flex:1; background: linear-gradient(135deg, #c7d2fe, #ddd6fe); padding:20px; border-radius:15px; text-align:center;">
            <div style="font-size:16px; color:#0f0c1a;">ISL Translators</div>
            <div style="font-size:30px; font-weight:bold; color:#000000;">339</div>
        </div>

    </div>
</div>
    </div>
    """, height=180)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        b1, b2 = st.columns(2)

        if b1.button("Sign to Text", use_container_width=True):
            st.session_state.page = "camera"
            st.rerun()

        if b2.button("Text to Sign", use_container_width=True):
            st.session_state.page = "learn"
            st.rerun()

# ---------------- CAMERA ----------------
elif st.session_state.page == "camera":

    st.title("Sign to Text")

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("▶ Start Camera"):
            st.session_state.run_camera = True
            st.rerun()

    with c2:
        if st.button("⏹ Stop"):
            st.session_state.run_camera = False
            st.rerun()

    with c3:
        if st.button("Capture"):
            st.session_state.capture_flag = True

    frame_window = st.empty()
    output = st.empty()

    if st.session_state.run_camera:
        cap = cv2.VideoCapture(0)

        while st.session_state.run_camera:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)

            landmarks = get_hand_landmarks(frame)

            if landmarks:
                text = predict_sign(landmarks)
            else:
                text = "No Hand"

            if st.session_state.capture_flag:
                os.makedirs("captures", exist_ok=True)
                screenshot = pyautogui.screenshot()
                screenshot.save(f"captures/capture_{text}.png")
                st.session_state.capture_flag = False

            cv2.putText(frame, f"Prediction: {text}", (20,50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_window.image(frame)

            output.markdown(f"### Output: {text}")

        cap.release()

    if st.button("⬅ Back"):
        st.session_state.page = "Home"
        st.session_state.run_camera = False
        st.rerun()

# ---------------- TEXT TO SIGN ----------------
elif st.session_state.page == "learn":

    from backend import text_to_sign
    from PIL import Image

    st.title("Text to Sign")

    text_input = st.text_input("Enter text")

    if text_input:
        results = text_to_sign(text_input)

        if results:
            cols = st.columns(len(results))

            for i, (char, img_path) in enumerate(results):
                img = Image.open(img_path)
                cols[i].image(img, caption=char)

    if st.button("⬅ Back"):
        st.session_state.page = "Home"
        st.rerun()

# ---------------- FEATURES ----------------
elif st.session_state.page == "Features":

    st.markdown("""
    <div style="text-align:center; margin-top:20px;">
        <h1 style="font-size:40px;">Features</h1>
    </div>
    """, unsafe_allow_html=True)

    components.html("""
    <div style="display:flex; gap:20px; margin-top:30px; padding:10px;">

    <div style="flex:1.5; background: linear-gradient(135deg, #c7d2fe, #ddd6fe); padding:30px; border-radius:20px;">
        <h2 style="color:#000000;">Real-time Translation</h2>
        <p style="color:#000000;">
            Convert hand gestures into text instantly using computer vision and machine learning.
        </p>
    </div>

    <div style="flex:1; display:grid; grid-template-columns:1fr 1fr; gap:20px;">

        <div style="background: linear-gradient(135deg, #c7d2fe, #ddd6fe); padding:20px; border-radius:15px;">
            <h3 style="color:#000000;">High Accuracy</h3>
            <p style="color:#000000;">Reliable predictions using trained model.</p>
        </div>

        <div style="background: linear-gradient(135deg, #c7d2fe, #ddd6fe); padding:20px; border-radius:15px;">
            <h3 style="color:#000000;">Fast Processing</h3>
            <p style="color:#000000;">Real-time detection with low delay.</p>
        </div>

        <div style="background: linear-gradient(135deg, #c7d2fe, #ddd6fe); padding:20px; border-radius:15px;">
            <h3 style="color:#000000;">Secure</h3>
            <p style="color:#000000;">Runs locally without storing data.</p>
        </div>

        <div style="background: linear-gradient(135deg, #c7d2fe, #ddd6fe); padding:20px; border-radius:15px;">
            <h3 style="color:#000000;">User Friendly</h3>
            <p style="color:#000000;">Simple and intuitive interface.</p>
        </div>

    </div>
</div>
    """, height=350)

# ---------------- ABOUT ----------------
elif st.session_state.page == "About":

    st.markdown("""
    <h1 style='text-align:center; margin-bottom:20px;'>About Indian Sign Language</h1>
    """, unsafe_allow_html=True)

    components.html("""
    <div style="
    width:100%;
    display:flex;
    justify-content:center;
">

    <div style="
        width:85%;
        display:flex;
        flex-wrap:wrap;
        gap:25px;
        justify-content:center;
    ">

        <!-- LEFT BIG CARD -->
        <div style="
            flex:1 1 480px;
            max-width:600px;
            background: linear-gradient(135deg, #c7d2fe, #ddd6fe);
            padding:30px;
            border-radius:20px;
        ">
            <h2 style="color:#000000;">Indian Sign Language</h2>
            <p style="color:#000000; line-height:1.6;">
                Indian Sign Language (ISL) is a visual-gestural language used by the deaf community in India.
                It has its own grammar and syntax distinct from spoken languages.
                <br><br>
                ISL serves as a primary means of communication for approximately 5 million deaf individuals across the country.
            </p>
        </div>

        <!-- RIGHT SIDE CARDS -->
        <div style="
            flex:1 1 300px;
            max-width:400px;
            display:flex;
            flex-direction:column;
            gap:20px;
        ">

            <div style="background: linear-gradient(135deg, #c7d2fe, #ddd6fe); padding:20px; border-radius:15px;">
                <h3 style="color:#000000;">Users</h3>
                <p style="color:#000000;">
                    ~5 million deaf individuals use ISL across India.
                </p>
            </div>

            <div style="background: linear-gradient(135deg, #c7d2fe, #ddd6fe); padding:20px; border-radius:15px;">
                <h3 style="color:#000000;">Purpose</h3>
                <p style="color:#000000;">
                    Bridges communication gap between deaf and hearing communities.
                </p>
            </div>

            <div style="background: linear-gradient(135deg, #c7d2fe, #ddd6fe); padding:20px; border-radius:15px;">
                <h3 style="color:#000000;">Goal</h3>
                <p style="color:#000000;">
                    Provide real-time sign language to text translation.
                </p>
            </div>

        </div>

    </div>
</div>
    """, height=500)