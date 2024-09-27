import streamlit as st
from PIL import Image

# Set page config as the first Streamlit function
st.set_page_config(page_title="LLM Benchmarking Application", layout="centered")

# Load and display a banner or logo (if available)
# Replace 'path_to_logo.png' with the actual path of your logo/banner file
#image = Image.open('./src/Logo.png')  # Add a relevant logo or banner
#st.image(image, use_column_width=True)

# Title and Subtitle
st.title("Welcome to the LLM Benchmarking Application")
st.write("""
The **LLM Benchmarking Application** is designed to analyze and assess the performance of Large Language Models (LLMs) based on their responses to a variety of tasks.
By leveraging cloud-based infrastructure, this platform provides real-time insights and metrics for LLM evaluations.
""")

# Overview of the Features
st.subheader("Main Features")
st.write("""
- **LLM Prompting**: Send prompts to LLMs with or without annotations and gather their responses.
- **Performance Dashboards**: Visualize LLM performance through various metrics such as overall accuracy, improvement rate, and failure rate.
- **Customizable**: Reprompt with annotations for better evaluation, enabling a more robust LLM comparison.
""")
query_params = st.query_params

# def navigate_to(page):
#     st.experimental_set_query_params(page=page)
#
# current_page = query_params.get('page', ['home'])[0]
# # Navigation to Other Pages
# st.subheader("Explore the Application")
# st.write("Navigate to the available pages using the buttons below:")
#
# # Navigation buttons to other pages
# col1, col2, col3 = st.columns(3)
#
# with col1:
#     if st.button('LLM Prompting'):
#         st.write("Navigate to LLM Prompting from the sidebar to explore this feature.")
#         navigate_to("LLM_Prompting")
#
# with col2:
#     if st.button('Dashboard'):
#         st.write("Navigate to the Dashboard for performance metrics.")
#         navigate_to("Dashboard")
#
#
# with col4:
#     if st.button('Documentation'):
#         st.write("For more information and how-to guides, visit the documentation section (if applicable).")

# Instructions for Use
st.subheader("How to Use This Application:")
st.write("""
1. **LLM Prompting**: Go to the LLM Prompting page to select a task, prompt a large language model, and assess its performance. You can either accept the response as is or reprompt with annotations.
2. **Performance Dashboards**: Use the dashboards to visualize various metrics about the LLM's performance.
3. **Interact with the LLM**: Use the application to send real-time requests to LLMs and evaluate their responses based on real-world tasks.
""")

# Optional - Call to Action
st.write("Ready to explore? Use the sidebar to get started!")

# Footer
st.markdown("""
    <style>
    footer {visibility: hidden;}
    footer:after {
        content: '© 2024 LLM Performance Evaluation System. All Rights Reserved.';
        visibility: visible;
        display: block;
        position: relative;
        padding: 10px;
        text-align: center;
        background-color: #f0f0f0;
    }
    </style>
    """, unsafe_allow_html=True)
