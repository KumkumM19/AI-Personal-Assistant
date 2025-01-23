import os
from deepgram import DeepgramClient, PrerecordedOptions

# The API key for Deepgram
DEEPGRAM_API_KEY ='' 

# Replace with your folder path
FOLDER_PATH = 'D:\\Personal_Assistant\\myproject\\recordings'
TRANSCRIBED_PATH='D:\\Personal_Assistant\\myproject'
LOG_FILE = os.path.join(FOLDER_PATH, 'processed_files.log')
OUTPUT_FILE = os.path.join(TRANSCRIBED_PATH, 'combined_transcript.txt')

def get_processed_files():
    """Read the log file and return a set of already processed file names."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as log_file:
            return set(log_file.read().splitlines())
    return set()

def update_log_file(processed_files):
    """Write the updated set of processed files back to the log file."""
    with open(LOG_FILE, 'w') as log_file:
        for file in processed_files:
            log_file.write(file + '\n')

def main():
    deepgram = DeepgramClient(DEEPGRAM_API_KEY)
    final_transcript = ""  # This will store the combined transcript for new files only

    # Get already processed files from the log
    processed_files = get_processed_files()

    # Loop through each file in the folder
    for filename in os.listdir(FOLDER_PATH):
        file_path = os.path.join(FOLDER_PATH, filename)
        
        # Ensure we're only reading unprocessed audio files
        if (file_path.endswith(".wav") or file_path.endswith(".mp3")) and filename not in processed_files:
            with open(file_path, 'rb') as buffer_data:
                payload = {'buffer': buffer_data.read()}  # Read file contents into memory

                options = PrerecordedOptions(
                    smart_format=True, model="nova-2", language="en-US"
                )

            # Transcribe the file
            try:
                response = deepgram.listen.rest.v('1').transcribe_file(payload, options)
                transcript = response['results']['channels'][0]['alternatives'][0]['transcript']
                
                # Append to the new transcript text
                final_transcript += transcript + " "

                # Mark this file as processed
                processed_files.add(filename)
                
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue

    # Append the new transcript to the output file
    if final_transcript:
        with open(OUTPUT_FILE, 'a') as output_file:
            output_file.write(final_transcript.strip() + "\n")

        # Update the log file with newly processed files
        update_log_file(processed_files)

    print("Transcript updated and saved to", OUTPUT_FILE)

if __name__ == '__main__':
    main()
