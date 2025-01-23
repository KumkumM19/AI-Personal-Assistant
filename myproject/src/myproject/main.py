#!/usr/bin/env python
import sys
import warnings
import pyttsx3
from crew import Myproject
from datetime import datetime
import speech_recognition as sr
import streamlit as st
import traceback
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def get_text_query():
    """
    Get query input from the user via text.
    """
    return input("Enter your query: ")

def get_audio_query():
    """
    Get query input from the user via audio using speech recognition.
    """
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    print("Listening... Please speak your query.")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjust to ambient noise
        audio = recognizer.listen(source)
    
    try:
        # Convert audio to text
        query = recognizer.recognize_google(audio)
        print(f"Detected query: {query}")
        return query
    except sr.UnknownValueError:
        print("Sorry, could not understand the audio. Please try again.")
    except sr.RequestError as e:
        print(f"Speech Recognition API error: {e}")
    return None

def text_to_speech(text):
    """
    Convert text to speech.
    """
    engine = pyttsx3.init()  # Initialize the text-to-speech engine
    engine.setProperty('rate', 150)  # Set speech rate
    engine.setProperty('volume', 1)  # Set volume level (0.0 to 1.0)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Use the default voice
    print("Speaking the result...")
    engine.say(text)  # Convert text to speech
    engine.runAndWait()  # Play the speech

# def run():
#     """
#     Run the AI Personal Assistant crew.
#     """
#     print("Choose input method:")
#     print("1. Text")
#     print("2. Audio")
#     choice = input("Enter your choice (1 or 2): ").strip()

#     if choice == "1":
#         query = get_text_query()
#         print(query)
#     elif choice == "2":
#         query = get_audio_query()
#         if not query:  # Retry if audio input fails
#             print("Switching to text input due to audio error.")
#             query = get_text_query()
#     else:
#         print("Invalid choice. Defaulting to text input.")
        

#     inputs = {
#         'query': query,
#         'date': datetime.now().strftime("%Y-%m-%d"),
#         'timezone': datetime.now().astimezone().tzname()
#     }

#     try:
#         result = Myproject().crew().kickoff(inputs=inputs)
#         print("print1")
#         print(crew.usage_metrics)
#         print("Task completed. Result:", result)
#         print("print2")

#         print("Press 1 if you want sound:")
#         output_choice = input("Enter your choice (1 or 0): ").strip()

#         if output_choice == "1":
#             text_to_speech(result.raw)
#         else:
#             print("Invalid choice. Defaulting to text output.")
#             print("Result as text:")
#             print(result.raw)
#     except Exception as e:
#         print(f"An error occurred while running the crew: {e}")
#         traceback.print_exc()

# if __name__ == "__main__":
#     run()


# # Streamlit app
# def main():
#     st.title("AI Personal Assistant")
#     st.write("An intelligent assistant to handle your queries efficiently.")

#     # Sidebar controls
#     st.sidebar.title("Voice and Speaker Options")
#     use_voice_input = st.sidebar.button("Use Voice Input")
#     use_speaker_output = st.sidebar.button("Use Speaker Output")

#     # Input method: Text by default, but Voice if selected
#     if use_voice_input:
#         query = get_audio_query()
#         st.write(f"Voice Input Detected: {query}")
#     else:
#         query = st.text_input("Enter your query:")

#     # Run processing when query is submitted
#     if st.button("Submit"):
#         if not query:
#             st.error("Please enter a query before submitting!")
#             return
        
#         inputs = {
#             "query": query,
#             "date": datetime.now().strftime("%Y-%m-%d"),
#             "timezone": datetime.now().astimezone().tzname()
#         }

#         try:
#             st.info("Processing your query...")
#             result = Myproject().crew().kickoff(inputs=inputs)
#             st.success("Task completed successfully!")

#             # Display result
#             st.write("**Result:**", result["raw"])

#             # Use Speaker Output if selected
#             if use_speaker_output:
#                 text_to_speech(result.raw)
#         except Exception as e:
#             st.error("An error occurred while processing your query.")
#             st.error(f"Error details: {e}")
#             st.write(traceback.format_exc())

# if __name__ == "__main__":
#     main()


import streamlit as st
from datetime import datetime
import traceback

import streamlit as st
from datetime import datetime
import traceback

def main():
    st.title("AI Personal Assistant")
    st.write("An intelligent assistant to handle your queries efficiently.")

    # Sidebar controls
    st.sidebar.title("Voice and Speaker Options")

    # Voice and Speaker Options
    if st.sidebar.button("Use Voice Input"):
        # Capture voice input and save it in session state
        st.session_state["query"] = get_audio_query()
        st.write(f"Voice Input Detected: {st.session_state['query']}")

    if st.sidebar.button("Use Speaker Output"):
        # Set flag for speaker output
        st.session_state["use_speaker_output"] = True

    # Default query handling
    if "query" not in st.session_state:
        st.session_state["query"] = ""
    
    query = st.text_input("Enter your query:", value=st.session_state["query"])

    # Run processing when query is submitted
    if st.button("Submit"):
        if not query:
            st.error("Please enter a query before submitting!")
            return

        # Update session state with current query
        st.session_state["query"] = query
        
        inputs = {
            "query": query,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "timezone": datetime.now().astimezone().tzname()
        }

        try:
            st.info("Processing your query...")
            result = Myproject().crew().kickoff(inputs=inputs)
            st.success("Task completed successfully!")
            
             # Save the result in session state
            st.session_state["result"] = result.raw

            # Display result
            st.write("**Result:**", result.raw)

            # Use Speaker Output if selected
            if st.session_state.get("use_speaker_output", True):
                text_to_speech(result.raw)
        except Exception as e:
            st.error("An error occurred while processing your query.")
            st.error(f"Error details: {e}")
            st.write(traceback.format_exc())

if __name__ == "__main__":
    # Initialize session state
    if "query" not in st.session_state:
        st.session_state["query"] = ""
    if "use_speaker_output" not in st.session_state:
        st.session_state["use_speaker_output"] = False
    main()



# def train():
#     """
#     Train the crew for a given number of iterations.
#     """
#     inputs = {
#         "topic": "AI LLMs"
#     }
#     try:
#         Myproject().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while training the crew: {e}")

# def replay():
#     """
#     Replay the crew execution from a specific task.
#     """
#     try:
#         Myproject().crew().replay(task_id=sys.argv[1])

#     except Exception as e:
#         raise Exception(f"An error occurred while replaying the crew: {e}")

# def test():
#     """
#     Test the crew execution and returns the results.
#     """
#     inputs = {
#         "topic": "AI LLMs"
#     }
#     try:
#         Myproject().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while replaying the crew: {e}")
