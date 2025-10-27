import streamlit as st
import math

st.set_page_config(page_title="Scientific Calculator", layout="centered")

# ---- THEME TOGGLE ----
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

dark = st.session_state.dark_mode
bg_color = "#0f172a" if dark else "#f9fafb"
text_color = "#f8fafc" if dark else "#0f172a"
btn_color = "#1e293b" if dark else "#e2e8f0"

st.markdown(
    f"""
    <style>
        body {{
            background-color: {bg_color};
            color: {text_color};
        }}
        div.stButton > button {{
            background-color: {btn_color};
            color: {text_color};
            border: none;
            border-radius: 10px;
            padding: 12px 18px;
            margin: 4px;
            font-size: 16px;
        }}
        div.stButton > button:hover {{
            background-color: #3b82f6;
            color: white;
        }}
        div.calc-display {{
            background-color: {'#1e293b' if dark else '#e2e8f0'};
            padding: 15px;
            border-radius: 10px;
            text-align: right;
            font-size: 22px;
            font-weight: 500;
            word-wrap: break-word;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🧮 Scientific Calculator")

# ---- STATE ----
if "expression" not in st.session_state:
    st.session_state.expression = ""
if "result" not in st.session_state:
    st.session_state.result = ""


def append(value):
    st.session_state.expression += value


def clear():
    st.session_state.expression = ""
    st.session_state.result = ""


def backspace():
    st.session_state.expression = st.session_state.expression[:-1]


def calculate():
    try:
        expr = st.session_state.expression.replace("×", "*").replace("÷", "/").replace("π", str(math.pi)).replace("e", str(math.e))
        # Replace sqrt, log, ln, etc.
        expr = expr.replace("√", "math.sqrt").replace("ln", "math.log").replace("log", "math.log10")
        expr = expr.replace("sin", "math.sin").replace("cos", "math.cos").replace("tan", "math.tan")
        expr = expr.replace("^", "**")

        # Factorial support
        expr = expr.replace("!", ")")  # temporary
        if "!" in st.session_state.expression:
            expr = f"math.factorial({expr}"

        result = eval(expr)
        st.session_state.result = str(result)
        st.session_state.expression = str(result)
    except Exception:
        st.session_state.result = "Error"


# ---- DISPLAY ----
st.markdown('<div class="calc-display">' + (st.session_state.expression or "0") + "</div>", unsafe_allow_html=True)
st.markdown(
    f"<div style='text-align:right;font-size:18px;color:#94a3b8'>{st.session_state.result}</div>",
    unsafe_allow_html=True,
)

# ---- BUTTONS ----
cols = st.columns(5)
buttons = [
    ["sin", "cos", "tan", "ln", "log"],
    ["7", "8", "9", "(", ")"],
    ["4", "5", "6", "×", "÷"],
    ["1", "2", "3", "+", "-"],
    ["0", ".", "^", "π", "e"],
    ["√", "!", "C", "DEL", "="],
]

for row in buttons:
    c = st.columns(5)
    for i, b in enumerate(row):
        if c[i].button(b, use_container_width=True):
            if b == "C":
                clear()
            elif b == "DEL":
                backspace()
            elif b == "=":
                calculate()
            else:
                append(b)

# ---- THEME TOGGLE ----
st.markdown("---")
if st.button(("🌞 Light Mode" if dark else "🌙 Dark Mode"), use_container_width=True):
    st.session_state.dark_mode = not st.session_state.dark_mode
    st.rerun()


