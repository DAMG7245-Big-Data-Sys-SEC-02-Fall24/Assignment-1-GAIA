
import os
import sys
# Add the 'src' directory to the Python path dynamically
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.data_layer.data_access import data_access_instance
from src.data_layer.models import Task
from src.utils.gpt import evaluate


import streamlit as st

# Streamlit UI for LLM management
def llm_management_ui():
    st.sidebar.title("LLM Management")

    # Fetch all LLMs
    llms = data_access_instance.get_all_llms()

    # Extract the names of LLMs for dropdown
    llm_options = [f"{llm.llmname} (Version: {llm.version}, ID: {llm.llmid})" for llm in llms]

    # Handle the selected LLM in session state
    if 'selected_llm' not in st.session_state:
        st.session_state['selected_llm'] = llm_options[0] if llm_options else None

    # Sidebar dropdown to select the current LLM
    st.sidebar.subheader("Select LLM")
    selected_llm = st.sidebar.selectbox(
        "Select from available LLMs",
        llm_options,
        index=llm_options.index(st.session_state['selected_llm']) if st.session_state['selected_llm'] in llm_options else 0
    )

    # Save selected LLM in session state
    st.session_state['selected_llm'] = selected_llm

    # Display the currently selected LLM
    st.sidebar.write(f"**Currently Selected LLM:** {selected_llm}")



def get_random_task():
    task: Task | None = data_access_instance.get_random_task()
    clear_session_storage()
    print("🧹🧹🧹🧹Got random question nd cleared storage 🧹🧹🧹🧹")
    return task


def clear_session_storage():
    print("Clearing storage")
    st.session_state["Task"] = None
    st.session_state["Response"] = None
    st.session_state["Reprompt"] = False
    st.session_state["Re_Response"] = None
    st.session_state["File_Path"] = None
    st.session_state['selected_llm'] = None


def parse_response(response):
    # Split the response into explanation and final answer
    parts = response.split("Final Answer:", 1)

    if len(parts) == 2:
        explanation = parts[0].strip()
        final_answer = parts[1].strip()
        return explanation, final_answer
    else:
        return None, None


def display_response(response):
    explanation, final_answer = parse_response(response)

    if explanation is not None and final_answer is not None:
        # Display the explanation in an expander
        with st.expander("Thought Process", expanded=False):
            st.write(explanation)

        # Display the final answer
        st.success(f"Final Answer: {final_answer}")
    else:
        # Backup: Display the whole response if parsing fails
        st.warning("Couldn't parse the response into separate parts. Displaying the full response:")
        st.success(response)


st.title("LLM Prompting 🤖")
if "Task" not in st.session_state:
    st.session_state["Task"] = None
if "Response" not in st.session_state:
    st.session_state["Response"] = None
if "Reprompt" not in st.session_state:
    st.session_state["Reprompt"] = False
if "Re_Response" not in st.session_state:
    st.session_state["Re_Response"] = None
if "File_Path" not in st.session_state:
    st.session_state["File_Path"] = None
if "selected_llm" not in st.session_state:
    st.session_state['selected_llm'] = None


llm_management_ui()

if st.button("Pick a random question 🎲"):
    task: Task | None = get_random_task()
    st.session_state["Task"] = task

if st.session_state["Task"]:
    task = st.session_state["Task"]
    st.text_area(label="Question", value=task.question)
    st.text_input(label="Expected Answer", value=task.expectedanswer)
    if task.filename and st.session_state["File_Path"] is None:
        with st.spinner("Getting required files"):
            from src.data_layer.object_store import download_file_from_gcs

            file_path = download_file_from_gcs(task.filename)
            st.session_state["File_Path"] = file_path

if st.session_state["File_Path"]:
    file_path = st.session_state["File_Path"]
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            file_bytes = file.read()
            file_name = os.path.basename(file_path)

            # Display download button
            st.download_button(
                label=f"Download {file_name}",
                data=file_bytes,
                file_name=file_name,
                mime="application/octet-stream"
            )
    else:
        st.warning(f"File {file_path} not found.")

if st.session_state["Response"] is None and st.session_state["Task"] is not None and st.session_state[
    "Response"] is None:
    if st.button("Prompt LLM", type="primary"):
        task: Task = st.session_state["Task"]
        with st.spinner("Generating Response..."):
            st.session_state["Response"] = evaluate(task, st.session_state["File_Path"])
            display_response(st.session_state["Response"])

if st.session_state["Response"] is not None and st.session_state["Re_Response"] is None:
    if st.button("Mark as correct", type="secondary"):
        data_access_instance.mark_task_as_correct(st.session_state["Task"])
