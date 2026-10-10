import streamlit as st
import google.generativeai as genai

reversed_key = "AAvc9SQdb9_cAaKaQvwcsjM6v5MFzf0ZIo04lwhuAtGL6NR8bA."
FULL_API_KEY = reversed_key[::-1]

genai.configure(api_key=FULL_API_KEY)
MODEL = "gemini-1.5-flash"

st.title("=== Exegesis AI ===")
st.write("Your personal scaffolded learning tutor!")

user_question = st.text_input("What question or topic do you want help learning?", placeholder="e.g., 3 multiplied by 6, Photosynthesis, Gravity")

if user_question:
    if 'zonal_round_question' not in st.session_state or st.session_state['zonal_round_question'] != user_question:
        st.session_state['zonal_round_question'] = user_question
        st.session_state['attempt'] = 1
        st.session_state['hints'] = {}
        st.session_state['explanation'] = ""
        
        with st.spinner("Exegesis AI is thinking of a helpful hint..."):
            instructions = (
                "You are a helpful tutor using a scaffolding teaching method for Exegesis AI. "
                "Return your response in EXACTLY this format, separated by double newlines:\n"
                "HINT1: <a subtle first hint>\n\n"
                "HINT2: <a more direct second hint>\n\n"
                "HINT3: <a very obvious third hint>\n\n"
                "EXPLANATION: <the full clear answer and explanation>"
            )
            
            try:
                model = genai.GenerativeModel(
                    model_name=MODEL,
                    system_instruction=instructions
                )
                response = model.generate_content(f"Help me learn about: {user_question}")
                
                response_content = response.text
                parts = response_content.split("\n\n")
                hints = {}
                explanation = ""
                
                for part in parts:
                    if part.startswith("HINT1:"):
                        hints[1] = part.replace("HINT1:", "").strip()
                    elif part.startswith("HINT2:"):
                        hints[2] = part.replace("HINT2:", "").strip()
                    elif part.startswith("HINT3:"):
                        hints[3] = part.replace("HINT3:", "").strip()
                    elif part.startswith("EXPLANATION:"):
                        explanation = part.replace("EXPLANATION:", "").strip()
                
                st.session_state['hints'] = hints
                st.session_state['explanation'] = explanation
                
            except Exception as gemini_error:
                st.error("⚠️ AI Studio Connection Error!")
                st.info(f"Server Response: {gemini_error}")
                st.stop()

    attempt = st.session_state.get('attempt', 1)
    hints = st.session_state.get('hints', {})

    if attempt <= 3 and hints:
        st.info(f"💡 HINT {attempt}: {hints.get(attempt, 'No hint found.')}")
        user_guess = st.text_input("What is your guess?", key=f"guess_{attempt}", placeholder="Type what you think it is...")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Submit Guess", use_container_width=True):
                if user_guess.strip() == "":
                    st.warning("Please type a guess before submitting!")
                else:
                    with st.spinner("Checking your answer..."):
                        check_prompt = f"Question/Topic: {user_question}\nUser Guess: {user_guess}\nIs this correct? Answer only YES or NO."
                        try:
                            model = genai.GenerativeModel(model_name=MODEL)
                            check = model.generate_content(check_prompt)
                            check_text = check.text
                            
                            if "YES" in check_text.upper():
                                st.success("🎉 Awesome job! You figured it out with Exegesis AI!")
                                st.session_state['attempt'] = 4  
                                st.rerun()
                            else:
                                st.error("❌ Not quite, let's try the next step!")
                                st.session_state['attempt'] += 1
                                st.rerun()
                        except Exception as e:
                            st.error(f"Error checking guess: {e}")
        
        with col2:
            if st.button("Need another hint?", use_container_width=True):
                st.session_state['attempt'] += 1
                st.rerun()
                
    else:
        st.warning(f"📚 Here is the full explanation from Exegesis AI:\n\n{st.session_state.get('explanation')}")
        if st.button("Ask Another Question", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
