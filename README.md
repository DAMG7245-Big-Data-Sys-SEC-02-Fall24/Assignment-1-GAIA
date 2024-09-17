# GAIA Benchmark Validation Application

## Abstract
This project is focused on building an evaluation tool for the GAIA dataset using Streamlit. The application allows users to select test cases from a multi-model validation dataset, send queries to the OpenAI model, and evaluate its responses. The application enables users to compare model outputs with expected answers, providing options to correct and re-evaluate the model performance. A final summary of results is generated to track performance across various test cases.

## Checklist of Deliverables
- [x] Diagrams illustrating system architecture
- [x] Fully documented CodeLab
- [x] 5-minute video submission
- [x] Link to a working Streamlit application
- [x] GitHub repository with project files and documentation

## Architecture
The architecture includes the following components:
1. **GAIA Dataset**: Provides structured metadata for validation purposes. The multi-model dataset includes metadata for test cases.
2. **Streamlit Application**: A multi-page UI built to explore test cases one at a time.
3. **Interaction with OpenAI API**: Sends test case data to OpenAI, receives responses, and allows user comparison with expected outputs.
4. **Editable Annotations**: Provides a mechanism for users to adjust test case annotations if OpenAI’s answer is incorrect, then re-evaluate.
5. **Feedback and Reporting**: Records user feedback, visualizes test case performance, and generates a summary report.

## Tech Stack
- **Streamlit**: Front-end for multi-page application development
- **OpenAI API**: For generating model responses
- **GAIA Dataset**: For test case and validation data
- **Python**: Core language for backend logic and integration
- **S3 Bucket (or alternative)**: Suggested for data storage and staging

## Dataset
- **GAIA Dataset**: A multi-model validation dataset accessible via Hugging Face [GAIA Datasets](https://huggingface.co/datasets/gaia-benchmark/GAIA). It contains structured metadata essential for validation and test cases. The dataset is used to compare OpenAI model responses with predefined answers.

## Features
- Select specific test cases from GAIA validation dataset.
- Send test case queries to OpenAI API for evaluation.
- Compare OpenAI responses with expected answers.
- Annotate and re-evaluate test cases in case of incorrect responses.
- Generate summary reports visualizing the performance of test cases.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your OpenAI API key in the environment:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

## Usage
1. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
2. Select a test case from the GAIA validation dataset.
3. Submit the test case to OpenAI and compare the response.
4. Annotate incorrect responses and re-submit for evaluation.
5. View summary results and feedback.

## Data Storage
The data storage design involves a staging phase, where test case data and model responses are stored in an S3 bucket or an alternative cloud storage solution. This ensures efficient data handling and retrieval for evaluation purposes.

## License
This project is licensed under the MIT License.

---

Feel free to modify any sections or add additional details!
