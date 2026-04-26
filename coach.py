"""AI Coach for the Glitchy Guesser game using ChatGPT and RAG principles."""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_coach_response(
    query_type: str,
    secret: int,
    low: int,
    high: int,
    guess_history: list,
    difficulty: str,
    suggested_strategies: list,
    show_hints: bool = True,
) -> str:
    """
    Get coaching advice from ChatGPT based on game state.
    
    Args:
        query_type: "best_move" or "new_strategy"
        secret: The secret number
        low: Lower bound of range
        high: Upper bound of range
        guess_history: List of guesses the player has made
        difficulty: "Easy", "Normal", or "Hard"
        suggested_strategies: List of previously suggested strategies (for variety)
        show_hints: Whether hints are visible to the player (affects coach context)
    
    Returns:
        Coach response string
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "⚠️ Coach unavailable: Missing OPENAI_API_KEY environment variable."
    
    client = OpenAI(api_key=api_key)
    
    # Calculate game state metrics
    if guess_history:
        last_guess = guess_history[-1]
        off_by = abs(secret - last_guess)
        min_guess = min(guess_history)
        max_guess = max(guess_history)
        guesses_so_far = len(guess_history)
    else:
        last_guess = None
        off_by = None
        min_guess = None
        max_guess = None
        guesses_so_far = 0
    
    # Build context for the prompt
    context = f"""
Game State:
- Secret number: {secret}
- Valid range: {low} to {high}
- Difficulty: {difficulty}
- Guesses made: {guess_history}
- Number of guesses: {guesses_so_far}
- Hints enabled: {show_hints}
"""
    
    if last_guess is not None:
        context += f"- Last guess: {last_guess}\n"
        if show_hints:
            context += f"- How far off: {off_by}\n"
            context += f"- Range of guesses so far: {min_guess} to {max_guess}\n"
        else:
            context += f"- (Hints disabled - coach should not reference how close/far they are)\n"
    
    if suggested_strategies:
        context += f"- Previously suggested strategies in this game: {', '.join(suggested_strategies)}\n"
    
    # Build the prompt based on query type
    if query_type == "best_move":
        prompt = f"""{context}
The player asked: "What's my best move?"

You are a helpful game coach. Based on the game state above:
1. Analyze whether they should guess HIGHER or LOWER
2. Explain WHY and which direction is more strategic
3. Suggest a specific next number or range to try
4. Keep it SHORT (2-3 sentences), actionable, and encouraging
5. Consider previously suggested strategies: {suggested_strategies if suggested_strategies else "None yet"}

Think about: remaining range, how far off they are, and what a binary search approach would suggest.

⚠️ IMPORTANT - DO NOT REVEAL:
- The secret number
- The exact valid range ({low} to {high})
- Specific numbers that are the answer
- How far off they are in absolute terms (e.g., "You're 3 away from the answer")
Instead, use relative guidance like "You're in the upper half" or "Try the middle of your range."

{"⚠️ NOTE: Hints are DISABLED - The player cannot see directional feedback. Base guidance only on guess patterns." if not show_hints else ""}"""
    
    else:  # new_strategy
        prompt = f"""{context}
The player asked: "What is a new strategy I can try?"

You are a helpful game coach teaching number guessing strategies. Based on the game state above:
1. Suggest a DIFFERENT strategy than those already mentioned: {suggested_strategies if suggested_strategies else "None yet"}
2. Explain HOW to apply it to the current range ({low} to {high})
3. Keep it SHORT (2-3 sentences) and actionable
4. Consider that they've guessed: {guess_history}

Good strategies include: binary search (splitting range in half), narrowing the range, using midpoint calculations, etc.

⚠️ IMPORTANT - DO NOT REVEAL:
- The secret number
- The exact valid range ({low} to {high})
- Specific numbers that are the answer
- How far off they are in absolute terms
Teach the strategy in general terms without spoiling the game.

{"⚠️ NOTE: Hints are DISABLED - The player cannot see directional feedback. Suggest strategies that work with only guess history." if not show_hints else ""}"""
    
    try:
        # Make the API call
        response = client.chat.completions.create(
            model="gpt-5.4-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful, encouraging game coach for a number guessing game. Keep responses brief and focused.",
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.7,
            max_completion_tokens=200,
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"⚠️ Coach error: {str(e)}"


def extract_strategy_name(response: str) -> str:
    """Extract a brief strategy name from the coach response for tracking."""
    # Take the first sentence or first 50 chars as the strategy name
    words = response.split()[:8]
    return " ".join(words)
