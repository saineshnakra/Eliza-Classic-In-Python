# Eliza Chatbot: Enhancing a Classic NLP Model

## Objective

The purpose of this project was to create an enhanced version of the classic Eliza chatbot, originally designed by Joseph Weizenbaum. I wanted to maintain Eliza's simple pattern-matching approach to simulate a conversation, but improve on how it handled advanced cases, like fallback responses, keyword prioritization, and memory management.

## 1. Initial Setup and Code Structure
We started by analyzing the existing Eliza chatbot implementation, identifying the core features:

#### Keyword Identification:
Eliza looks for specific keywords in the user’s input and applies decomposition patterns to those keywords.
#### Decomposition and Reassembly: 
Once a keyword is matched, the input is broken into parts and reassembled into a response using predefined templates.
#### Substitution Rules:
Pre-substitution (e.g., changing "I'm" to "I am") and post-substitution rules were added to enhance the flow of conversation.
#### Memory Management: 
Eliza saves some parts of user input to reference in later interactions, giving the impression of memory.

## 2. Algorithm Behind our Chatbot

#### Keyword Matching and Weighting
We designed the system to prioritize higher-weight keywords so that when multiple keywords are found in the user’s input, the most important one is processed first, allowing for more contextually relevant responses.

#### Fallback Responses
I made a fallback mechanism (xnone) to have a natural placeholder for our chatbot conversation when no specific keyword is matched. This guarantees that the chatbot can respond, even when it doesn’t understand the input.

#### Memory and Recall
Eliza has been given the power of memory, allowing it to "remember" and reuse user inputs in future responses. This feature gives the conversation a more cohesive flow by referencing earlier parts of the discussion.

## 3. The File Input
The chatbot’s behavior is driven by an external configuration file (default: doctor.txt). (taken from some other implementation of this project, I couldn't remember which one! ) This file contains:

Initial greetings (tagged as initial).
Final closing statements (tagged as final).
Keywords, decomposition patterns, and responses (tagged as key, decomp, and reasmb).
Quit words (tagged as quit).
We’ve made it easy to customize the script file. So if you want, you can swap the file name to eliza_script.txt in the code, allowing you to easily load a different set of conversation rules or templates.

Through this project, I took an existing Eliza chatbot and enhanced its structure, added a fallback mechanism, and prioritized keyword matching. Additionally, we improved memory management and logging for easier debugging and future extensions. The final result is an improved version of Eliza that can handle a wider variety of inputs, mimicking a more natural conversational agent. But a note to keep in mind, I didn't change any algorithm or didn't use any additional features. I just optimized the keyword matching algorithm and the other underlying algorithms used for a better Eliza.

Have fun playing with it.

## How to Run

Visit my website : https://chatwitheliza.streamlit.app/

If you want to run the repository: 

### Requirements
- Python 3.x
- A terminal or command line interface (CLI)

### Steps to Run the Eliza Chatbot

1. **Clone or Download the Repository**  
   First, clone or download the project files to your local machine.

   ```bash
   git clone https://github.com/saineshnakra/Eliza-Classic-In-Python.git
   cd Eliza-Classic-In-Python
   ```

2. **You Should see these Required Files**  
   Make sure you have the following files in the project directory:
   - `eliza.py` (the main Python script for the chatbot)
   - `doctor.txt` (or your custom conversation script file)


  the basic Eliza chatbot doesn't have any special dependencies.

3. **Run the Chatbot**  
   In your terminal, navigate to the directory where the `eliza.py` script is located. Run the chatbot using the following command:

   ```bash
   python eliza.py
   ```

4. **Customize the Script File (Optional)**  
   If you want to load a custom conversation script, you can modify the script file name in `eliza.py`. For example, change this line in the `main()` function:

   ```python
   eliza.load('doctor.txt')  # Change this to your custom file
   ```

   Then, rerun the chatbot with the new configuration file.

5. **Interact with Eliza**  
   Once the chatbot starts, it will greet you with an initial message. You can then interact with it by typing in the terminal.

   ```bash
   > Hello
   Eliza: How do you do. Please tell me your problem.
   ```

6. **Quit the Chat**  
   To end the conversation, type a quit word (such as "bye", "quit", or another one defined in your script). Eliza will then say goodbye and terminate the program.

