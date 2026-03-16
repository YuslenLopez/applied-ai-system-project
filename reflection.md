# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
1.The game looked like a simple guessing the number game with a handful of options to select difficulty, apply hints and an area to enter guesses. 

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
1.The hint was guiding me in the wrong direction from the secret. 
2.The new game button was not letting me immediately start a new game without refreshing the page. 
3.The difficulty setting seemed to be flipped because the harder setting mathmatically had higher odds than the normal mode at least that is what was displayed. 
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
1.Copilot 

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
1.The AI suggested that the hints where incorrect due to incorrect positioning of conditional checking for the the go higher or go lower hints.I verified the results by reading the code and making the change and then testing the game again.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
1.The Ai did not mention anything inherently incorrect but it did explain some of the errors found in a somewhat confusing manner that could result in more errors if not properly understood. Like it mentions String vs. int comparison causes lexicographic “glitch" which could lead the developer to beleive that the randomization between two strings was intended and just incorrect instead of reworking the whole section of code to a functioning form. 
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
1.Can never be 100% certain but after testing the specific fix area with a couple of use cases that would not have worked before. Then if it works like it should the issue was resolved. 

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
1.On my first test I wanted to see if the enter bar would let me enter things outside of the range and it did. Then after that I looked at playing the game as intended and noticed a few things immediately wrong with the intended version versus the current version. 

- Did AI help you design or understand any tests? How?
1.Yes it helped me understand certain errors by providing a example that can be seen as a test case. For example mentioning that the range being set to a string could lead to funky comparisons with a int or float that can lead to incorrect results.
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
1.Streamlit reruns basically means that the way in which it is designed Streamlit will rerun all the scripts again when certain actions like button clicks , changes a slider, types in a text input, uploads a file and selects from a dropdown are performed. This can reset variables back to default values and throw off the current state of things. So we need to use things like session state to store variables across reruns and make sure the data is saved accordingly. 
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
1.Definitley would like to use AI more to develope test cases for my projects and to also find test cases that could break my existing code.
  - This could be a testing habit, a prompting strategy, or a way you used Git.

- What is one thing you would do differently next time you work with AI on a coding task?
1.I will do more planning with the AI to understand the current status of the code and see what needs fixing. 

- In one or two sentences, describe how this project changed the way you think about AI generated code.

