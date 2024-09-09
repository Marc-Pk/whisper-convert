import os
import whisper

def transcribe_audio_files(folder_path, model):
    # Get all files in the specified folder and the "Downloads" directory
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    
    # Define the supported audio file extensions
    supported_extensions = ['.wav', '.mp3', '.ogg', '.aac']
    
    # Filter audio files based on supported extensions in the Downloads folder
    audio_files = [file for file in os.listdir(downloads_path) if any(file.endswith(ext) for ext in supported_extensions)]
    
    if not audio_files:
        print("No audio files found in the Downloads folder.")
        return
    
    # Iterate over audio files found in the Downloads folder for transcription
    for audio_file in audio_files:
        file_path = os.path.join(downloads_path, audio_file)
        try:
            # Check if a text file with the same name already exists in the current directory
            txt_file_path = os.path.join(folder_path, os.path.splitext(audio_file)[0] + ".txt")
            if os.path.exists(txt_file_path):
                print(f"Skipping transcription for {audio_file}. Text file already exists.")
                continue

            else:
                print(f"Transcribing {audio_file}...")
            
            if model is None:
                # Load the model
                print("Loading model...")
                model = whisper.load_model("large")
                print("Model loaded.")

            # Transcribe each audio file
            transcription = model.transcribe(file_path)["text"]
            print(f"Transcription for {audio_file}: \n{transcription}\n")
            
            # Write the transcription to a text file in the current directory with the same name as the audio file
            with open(txt_file_path, "w") as txt_file:
                txt_file.write(transcription)
                print(f"Transcription saved to {txt_file_path}")
        except Exception as e:
            print(f"Error transcribing {audio_file}: {str(e)}")

def combine_text_files(directory):
    # Get all text files in the specified directory
    text_files = [file for file in os.listdir(directory) if file.endswith(".txt") and file != "combined_text.txt"]
    
    if not text_files:
        print("No text files found in the directory.")
        return
    
    # Sort the text files by creation date in descending order
    text_files.sort(key=lambda x: os.path.getctime(os.path.join(directory, x)), reverse=True)
    
    # Combine the contents of all text files
    combined_text = ""
    for text_file in text_files:
        file_path = os.path.join(directory, text_file)
        with open(file_path, "r") as file:
            combined_text += f"File: {text_file}\n"
            combined_text += file.read()
            combined_text += "\n" + "#" * 20 + "\n\n"
    
    # Write the combined text to a new file
    combined_file_path = os.path.join(directory, "combined_text.txt")
    with open(combined_file_path, "w") as combined_file:
        combined_file.write(combined_text)

if __name__ == "__main__":
    model = None
    folder_path = os.getcwd()
    transcribe_audio_files(folder_path, model)
    combine_text_files(folder_path)
