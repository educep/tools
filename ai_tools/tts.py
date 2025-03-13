"""
Created by Analitika at 25/11/2024
contact@analitika.fr
"""

# python -m pip install ffmpeg-python==0.2.0
# python -m pip install yt-dlp==2024.11.18

# External imports
import os

import ffmpeg
import yt_dlp
from openai import OpenAI
from pydub import AudioSegment

# Internal imports
from config.settings import DATA_DIR, OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

ext = "mp3"

output_folder = DATA_DIR / "output_tts"


def concat(mp3_files: list[str]) -> None:
    # List of MP3 files to merge
    # Load and merge MP3 files
    combined_audio = AudioSegment.empty()
    for mp3_file in mp3_files:
        audio = AudioSegment.from_file(mp3_file)
        combined_audio += audio

    # Export the merged file as MP3
    combined_audio.export(os.path.join(output_folder, "merged.mp3"), format="mp3")


def segment_text(content: str, max_characters_count: int = 4096) -> list[str]:
    # Split the content into paragraphs
    paragraphs = content.split("\n")
    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        # If adding this paragraph exceeds the limit, finalize the current chunk
        if len(current_chunk) + len(paragraph) + 1 > max_characters_count:  # +1 accounts for "\n"
            chunks.append(current_chunk.strip())
            current_chunk = paragraph  # Start a new chunk with the current paragraph
        else:
            current_chunk += "\n\n" + paragraph if current_chunk else paragraph

    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def segment_audio(input_file: str) -> list[str]:
    # segments audio file to respect whisper size limits
    audio = AudioSegment.from_file(f"{input_file}.{ext}")
    chunk_size = 10 * 60 * 1000  # 10 minutes in milliseconds

    names = []
    for i, chunk in enumerate(audio[::chunk_size]):
        name_ = f"{input_file}_chunk_{i}"
        chunk.export(os.path.join(output_folder, f"{name_}.{ext}"), format=ext)
        names.append(name_)  # no extension
    return names


def extract_audio_from_youtube(video_url: str, output_audio_file: str, ext: str = "mp3") -> None:
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": ext,
                "preferredquality": "64",  # Lower quality to reduce file size (e.g., 64 kbps)
            }
        ],
        "postprocessor_args": [
            "-ar",
            "16000",  # Set sample rate to 16 kHz for lighter files
            "-ac",
            "1",  # Convert to mono audio
        ],
        "outtmpl": output_audio_file,  # Specify output filename
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])


def transcribe_audio(audio_file_path: str) -> str:
    """
    for the available outputs formats:
    https://medium.com/@bezbos./openai-audio-whisper-api-guide-36e7272731dc
     `json`, `text`, `srt`, `verbose_json`, or `vtt`.

    Plain text (response_format=text): directly text
    JSON (response_format=verbose_json):
        transcription.model_dump().keys()
        dict_keys(['text'])
    SubRip File Format (response_format=srt)
    Verbose JSON (response_format=verbose_json):
        transcription.model_dump().keys()
        dict_keys(['text', 'task', 'language', 'duration', 'segments'])
    Web Video Text Tracks (response_format=vtt)"""
    audio_file = os.path.join(output_folder, f"{audio_file_path}.{ext}")
    with open(audio_file, "rb") as audio_file_:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file_,
            response_format="verbose_json",
        )
        output = transcription.model_dump()

    return str(output["text"])


def key_points_extraction(transcription: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": """
                           You are a proficient AI with a specialty in distilling information into key points and summarization.
                           """,
            },
            {
                "role": "user",
                "content": f"""
                           Consider the following *content*, identify the language in which the text is written and give
                           your answer always on solely in spanish from Latin America.
                           Identify and list the main points that were discussed, or brought up, develop the ideas
                           in several phrases so it can be quicly understood.
                           These should be the most important ideas, findings, or topics that are crucial to the
                           essence of the discussion. Your goal is to provide a list that someone could read to
                           quickly understand what was talked about.
                           Give only and directly the text in spanish, do not provide your answer in other language or
                           you will be penalized.

                           # Content
                           {transcription}
                           """,
            },
        ],
    )
    response_ = response.model_dump()
    return str(response_["choices"][0]["message"]["content"])


def text_to_speech(my_text: str, filename: str) -> None:
    # The text to generate audio for. The maximum length is 4096 characters.
    response = client.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=my_text,
        speed=1.02,
    )
    response.stream_to_file(filename)


def read_text(file_path: str) -> str:
    # Open and read a text file
    # file_path = 'example.txt'  # Replace with the path to your file

    try:
        with open(file_path) as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise


if __name__ == "__main__":
    # Replace VIDEO_ID with the actual YouTube video ID
    video_url = "https://www.youtube.com/watch?v=gHfIW47p-lA"
    output_audio_file = "audio_output"  # Desired output file name

    extract_audio_from_youtube(video_url, output_audio_file)
    chunks = segment_audio(output_audio_file)
    # chunks = [f"audio_output_chunk_{_}.mp3" for _ in range(8)]
    transcription = ""
    for chunk in chunks:
        transcription_chunk = transcribe_audio(chunk)
        transcription += transcription_chunk

    with open(os.path.join(output_folder, "transcription.txt"), "w") as file:
        file.write(transcription)

    # transcription = read_text(file_path=r"C:\Users\ecepeda\OneDrive - analitika.fr\Documentos\PROYECTOS\ANALITIKA\PycharmProjects\automat_publisher\data\output_tts\transcription.txt")
    key_points = key_points_extraction(transcription)
    # write key point to a text file
    with open(os.path.join(output_folder, "key_points.txt"), "w") as file:
        file.write(key_points)

    # key_points = read_text(file_path=r"C:\Users\ecepeda\temp\summary.txt")
    file_putput = os.path.join(output_folder, f"audio_summary.{ext}")
    text_to_speech(key_points, file_putput)
    # Convert the merged MP3 to WhatsApp-compatible format (OGG with OPUS codec)
    ffmpeg.input(file_putput).output(
        os.path.join(output_folder, "audio_summary.ogg"),
        acodec="libopus",  # OPUS codec
        audio_bitrate="16k",  # 16kbps bitrate
        ar="24000",  # 24kHz sample rate
    ).run()

    print("Audio file created successfully: output.ogg")
