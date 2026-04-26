# 🎮 Game Glitch Investigator (Original Project): The Impossible Guesser
## Summary of Original Goals: 
The original goal of the project is a small number guessing game in which a random number is selected between a range determined by difficulty. The user then trys to guess the secret number with the use of hints (if toggled on) in a limited number of attempts. The user can enter numbers, receive accurate hints, see if they guessed correctly and run more than one game as is. 

# 🎮 The Num Gusser Using RAG 
## Summary of Improved Project: 
The new project still uses all of the originals game mechanics and just adds to it by implementing a chat bot that users can interact with to receive more help or work out new strategies. This matters because now the game also can help users learn new strategies while playing a fun little game.

## Architecture Overview:
The system uses streamlit app as a main interface where users can make a guess and submit their answers. The answers are then fed to the logical backend in python which validates and returns results. The user my also select to receive a helpful response from an LLM and this is handled by the python backend as well. 
![alt text](assets\Architecture.png)

## Setup Instructions:
For easy set up of API_KEY and app please look at the COACH_SETUP.md 

## Sample interactions 

Example 1:
![alt text](assets\test1.png)
![alt text](assets\test1-b.png)

Example 2: 


Example 3: 

## Design Decisions: 
Originally I was just going to feed the LLM the secret and ask for a riddle to be returns to provide users with more information to base their guesses on. However this approach was far too simple and did not provide the LLM with enough context to provide a meaningful response to the users each and everytime. As such now the model takes more context like prior guess history and if hints are on or off to give the user a more tailored response. This means there will be more tokens being used per input response but the overall quality of the answer is much better. 

## Testing Summary: 
The LLM at first provided the user with the answer or information not inherently present to the user but given to the AI for reasoning when asked for a best move. This was not the intended response, we want the AI to be helpful but not do the work for the user and ruin the game. As such we then needed to make the guardrails for the model more strict to not return cetain information to the user and to be more general in its response. Besides the need for stricter guardrails the LLM seemed to do rougly what was expected of it and I aim to make it produce better response results with more context based on scenerio of the user.

## Relection 
The project thus far has taught me of the crusial need for guardrails when using AI, especially chat bots which can be abused. A programmer must think about the limit of tokens per response, quality of context, when the context should be given to a cetain response, and even what to tell the AI not to say or do. Although their are lots of limitations impossed by the need for intense guardrails the use of AI can bring new and often times exciting features to a existing project and the opportunities are near endless. Many of these opportunities can even be thought of with the use of AI during brainstorming or planning out the system similar to what I did when asking it if my original idea was good and to suggest a few more ideas for how to implement RAG into the original project.  
One other thing of importance I noticed is that tricky english wording or code that could often make a human stumble can confuse the AI into thinking lines of code containing logic are wrong. AS shown in the following pictures. 

Picture 1 Code in question: 
![alt text](assets\image-1.png)

Picture 2 Response:
![alt text](assets\image-2.png)

Picture 3 Questioned Error: 
![alt text](assets\image-3.png)

## 🚨 The Situation (original Project)

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

