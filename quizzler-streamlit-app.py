import streamlit as st
import requests


# Function to fetch questions from the API
def fetch_questions():
    url = "https://opentdb.com/api.php?amount=20&category=9&type=boolean"
    parameters = {
        "amount": 25,
        "category": 9,
        "type": "boolean"
    }
    response = requests.get(url, params=parameters)
    if response.status_code == 200:
        return response.json()["results"]
    else:
        st.error("Failed to fetch questions")


# Function to update the session state
def update_session_state():
    if 'index' not in st.session_state:
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.questions = fetch_questions()
        st.session_state.answered = False

# Main function to run the app
def main():
    st.title("Quizzler!")
    update_session_state()

    # Display current question and get user's answer
    if st.session_state.index < len(st.session_state.questions):
        current_question = st.session_state.questions[st.session_state.index]
        st.write(f"Question {st.session_state.index + 1}: {current_question['question']}")

        # Get user's answer using buttons
        left, right, middle = st.columns((5, 5, 5))
        with left:
            true_button = st.button("True")
        with right:
            false_button = st.button("False")
        with middle:
            continue_button = st.button("Continue")

        correct_answer = current_question['correct_answer'].lower()

        # Check if both buttons were clicked and update score
        if true_button or false_button:
            if not st.session_state.answered:
                st.session_state.answered = True
                if (true_button and correct_answer == 'true') or (false_button and correct_answer == 'false'):
                    st.success("Correct!")
                    st.session_state.score += 1
                else:
                    st.error("Incorrect!")
            else:
                st.write("Please click anywhere on the screen to move to the next question.")

    # Display final score
    else:
        st.write("Quiz completed!")
        st.write(f"Final Score: {st.session_state.score}/{len(st.session_state.questions)}")

    # Move to the next question
    if st.session_state.answered:
        st.session_state.index += 1
        st.session_state.answered = False

if __name__ == "__main__":
    main()