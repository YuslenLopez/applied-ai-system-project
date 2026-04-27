import random
import streamlit as st

from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score
from coach import get_coach_response, extract_strategy_name

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

# Show balloons if player won
if "status" in st.session_state and st.session_state.status == "won":
    st.balloons()

st.sidebar.header("🤖 AI Coach")

# Placeholder for coach content - will be filled after show_hint is defined
coach_placeholder = st.sidebar.empty()

st.sidebar.divider()
st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "suggested_strategies" not in st.session_state:
    st.session_state.suggested_strategies = []

if "last_coach_response" not in st.session_state:
    st.session_state.last_coach_response = None

if "show_hints" not in st.session_state:
    st.session_state.show_hints = True

if "last_hint_message" not in st.session_state:
    st.session_state.last_hint_message = None

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)
    st.write("Suggested Strategies:", st.session_state.suggested_strategies)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    st.session_state.show_hints = st.checkbox("Show hint", value=st.session_state.show_hints)

# Coach section in sidebar - update placeholder after show_hint is defined
if st.session_state.status == "playing" and st.session_state.attempts > 0:
    with coach_placeholder.container():
        st.caption("Need help?")
        if st.button("Best Move? 🎯", use_container_width=True, key="best_move_btn"):
            with st.spinner("Coach thinking..."):
                response = get_coach_response(
                    query_type="best_move",
                    low=low,
                    high=high,
                    guess_history=st.session_state.history,
                    difficulty=difficulty,
                    suggested_strategies=st.session_state.suggested_strategies,
                    show_hints=st.session_state.show_hints,
                    last_outcome=st.session_state.last_hint_message,
                )
                st.session_state.last_coach_response = response
                st.rerun()
        
        if st.button("New Strategy? 💡", use_container_width=True, key="strategy_btn"):
            with st.spinner("Coach thinking..."):
                response = get_coach_response(
                    query_type="new_strategy",
                    low=low,
                    high=high,
                    guess_history=st.session_state.history,
                    difficulty=difficulty,
                    suggested_strategies=st.session_state.suggested_strategies,
                    show_hints=st.session_state.show_hints,
                    last_outcome=st.session_state.last_hint_message,
                )
                st.session_state.suggested_strategies.append(
                    extract_strategy_name(response)
                )
                st.session_state.last_coach_response = response
                st.rerun()
        
        if st.session_state.last_coach_response:
            st.caption("💬 Coach says:")
            st.info(st.session_state.last_coach_response)
else:
    with coach_placeholder.container():
        st.caption("Make a guess to unlock help!")

if new_game:
    # Reset game state for the current difficulty
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.suggested_strategies = []
    st.session_state.last_coach_response = None
    st.session_state.last_hint_message = None
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        if st.session_state.attempts % 2 == 0:
            secret = str(st.session_state.secret)
        else:
            secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        # Store hint message for coach (always, regardless of show_hints setting)
        st.session_state.last_hint_message = message

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )
    
    st.rerun()

# Display hint if available and enabled
if st.session_state.last_hint_message and st.session_state.show_hints:
    st.warning(st.session_state.last_hint_message)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
