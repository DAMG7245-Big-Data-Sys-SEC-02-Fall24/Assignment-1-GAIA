import json
import os

from openai import OpenAI
import streamlit as st

from src.data_layer.data_access import data_access_instance
from src.data_layer.models import Task
from src.data_layer.object_store import download_file_from_gcs
from src.utils.tools import tools

from dotenv import load_dotenv
import os

load_dotenv()
# print("-----------------------")
# print(os.getcwd())
# burl = st.secrets["openAI"]["base_url"]
# print(burl)
# print(st.secrets["openAI"]["api_key"])
# print("-----------------------")
client = OpenAI(
    base_url=st.secrets["openAI"]["base_url"],
    api_key=st.secrets["openAI"]["api_key"]
)


def handle_file_reading(task: Task, file_path: str = None):
    if task.filename:
        # Attempt to download the file from GCS

        # Check if the file was downloaded successfully and exists on disk
        if file_path and os.path.exists(file_path):
            # Determine the file type and use the appropriate tool
            _, ext = os.path.splitext(file_path)
            ext = ext.lower()
            tool = None  # Default to None

            # Identify the appropriate tool based on file extension
            if ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
                tool = "ReadImage"
            elif ext in ['.xlsx', '.xls']:
                tool = "ReadExcel"
            elif ext == '.csv':
                tool = "ReadCSV"
            elif ext == '.zip':
                tool = "ReadZIP"
            elif ext == '.pdf':
                tool = "ReadPDF"
            elif ext == '.json':
                tool = "ReadJSON"
            elif ext == '.py':
                tool = "ReadPython"
            elif ext == '.docx':
                tool = "ReadDOCX"
            elif ext == '.pptx':
                tool = "ReadPPTX"
            elif ext in ['.mp3', '.wav']:
                tool = "ReadAudio"
            elif ext == '.pdb':
                tool = "ReadPDB"
            elif ext == '.jsonld':
                tool = "ReadJSONLD"
            elif ext == '.txt':
                tool = "ReadTXT"

            if tool and tool in tools:
                context = tools[tool](file_path)
                # If the tool is ReadAudio, extract transcription
                if tool == "ReadAudio":
                    try:
                        audio_data = json.loads(context)
                        transcription = audio_data.get('transcription', '')
                        context += f"\nTranscription: {transcription}"
                    except json.JSONDecodeError:
                        st.warning("Failed to decode audio metadata.")
                print(context)
                return context
            else:
                # If the tool is unsupported, treat as plain text or return empty string
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
        else:
            # If the file download failed or file does not exist
            st.warning(f"File {task.filename} could not be downloaded or was not found.")
            return ""
    return ""


def evaluate(task: Task, file_path,llm, annotation=False):
    print(f"llm: {llm.llmname}")
    context = handle_file_reading(task, file_path)
    question = task.question
    if annotation:
        print("---Annotation---")
        print(task.annotations)
        question = task.question + task.annotations
    agent_full_answer = get_agent_answer(question, context, llm)
    return agent_full_answer


def get_agent_answer(question, context="", llm=None, additional_prompt=""):
    if llm is None:
        llm = {"llmname": "gpt-4o-mini"}
    prompt = f"""You are a general AI assistant. I will ask you a question. Report your thoughts, and finish your answer with the following template: FINAL ANSWER: [YOUR FINAL ANSWER]. YOUR FINAL ANSWER should be a number OR as few words as possible OR a comma separated list of numbers and/or strings. If you are asked for a number, don't use comma to write your number neither use units such as $ or percent sign unless specified otherwise. If you are asked for a string, don't use articles, neither abbreviations (e.g. for cities), and write the digits in plain text unless specified otherwise. If you are asked for a comma-separated list, apply the above rules depending on whether the element is a number or a string. Answer the following question as best you can, speaking as a general AI assistant. You have access to the following tools:

Search: useful for when you need to answer questions about current events or the current state of the world
ReadImage: useful for reading image files. Input should be the file path to the image.
ReadExcel: useful for reading Excel files. Input should be the file path to the Excel file.
ReadCSV: useful for reading CSV files. Input should be the file path to the CSV file.
ReadZIP: useful for reading ZIP files. Input should be the file path to the ZIP file.
ReadPDF: useful for reading PDF files. Input should be the file path to the PDF file.
ReadJSON: useful for reading JSON files. Input should be the file path to the JSON file.
ReadPython: useful for reading Python files. Input should be the file path to the Python file.
ReadDOCX: useful for reading DOCX files. Input should be the file path to the DOCX file.
ReadPPTX: useful for reading PPTX files. Input should be the file path to the PPTX file.
ReadAudio: useful for reading audio files (MP3, WAV). Input should be the file path to the audio file.
ReadPDB: useful for reading PDB files. Input should be the file path to the PDB file.
ReadJSONLD: useful for reading JSON-LD files. Input should be the file path to the JSON-LD file.
ReadTXT: useful for reading TXT files. Input should be the file path to the TXT file.

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of the tool names
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin Remember to speak as a general AI assistant when giving your final answer.

Context: {context}

Question: {question}

{additional_prompt}
"""
    response = client.chat.completions.create(
        model= llm.llmname or "gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0)

    # Ensure response.choices is a list and access the first element
    if response.choices:
        return response.choices[0].message.content
    else:
        return "No response received from the model."


def get_random_task():
    task: Task | None = data_access_instance.get_random_task()
    return task


if __name__ == "__main__":
    task = data_access_instance.query_by_file_type("xlsx")
    if task.filename:
        download_file_from_gcs(task.filename)
    print(f"{task.taskid}\n"
          f"{task.question}\n"
          f"{task.expectedanswer}\n"
          f"{task.filename}"
          f"\n{task.filepath}")
    evaluate(task)
