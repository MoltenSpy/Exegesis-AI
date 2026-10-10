import streamlit as st
import time

st.title("=== Exegesis AI ===")
st.write("Your personal scaffolded learning tutor!")

# Get the user's question or topic
user_question = st.text_input("What question or topic do you want help learning?", placeholder="e.g., Photosynthesis, Gravity, Robotics")

if user_question:
    # Initialize session state for a new question with a completely new variable name
    if 'zonal_round_question' not in st.session_state or st.session_state['zonal_round_question'] != user_question:
        st.session_state['zonal_round_question'] = user_question
        st.session_state['attempt'] = 1
        
        with st.spinner("Exegesis AI is crafting your learning scaffolding..."):
            time.sleep(1) # Simulates real AI thinking time smoothly

        # Local scaffolding data for your presentation
        st.session_state['hints'] = {
            1: f"It involves exploring the core mechanics, active steps, or deep nature of '{user_question}'.",
            2: f"Think about the primary inputs, structural laws, or basic rules that make '{user_question}' function.",
            3: f"You are looking for the absolute fundamental concept or building blocks behind '{user_question}'."
        }
        st.session_state['explanation'] = (
            f"Great job exploring! '{user_question}' is a vital concept in structured learning. "
            f"Using the scaffolding method, we break down complex architectures into small, "
            f"digestible hints. This builds strong mental models, letting you master the material step-by-step!"
        )

    attempt = st.session_state.get('attempt', 1)
    hints = st.session_state.get('hints', {})

    # Game Loop: Give up to 3 attempts/hints
    if attempt <= 3 and hints:
        st.info(f"💡 HINT {attempt}: {hints.get(attempt)}")
        
        user_guess = st.text_input("What is your guess?", key=f"guess_{attempt}", placeholder="Type what you think it is...")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Submit Guess", use_container_width=True):
                if user_guess.strip() == "":
                    st.warning("Please type a guess before submitting!")
                else:
                    st.success("🎉 Awesome job! You figured it out with Exegesis AI!")
                    st.session_state['attempt'] = 4  
                    st.rerun()
        
        with col2:
            if st.button("Need another hint?", use_container_width=True):
                st.session_state['attempt'] += 1
                st.rerun()
                
    else:
        # Reveal full answer when attempts run out
        st.warning(f"📚 Here is the full explanation from Exegesis AI:\n\n{st.session_state.get('explanation')}")
        
        if st.button("Ask Another Question", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

