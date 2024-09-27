
from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.gcp.storage import Storage
from diagrams.gcp.database import SQL
from diagrams.programming.language import Python
from diagrams.onprem.client import User

graph_attr = {
    "fontsize": "45",
    "bgcolor": "white",
    "pad": "0.75"
}

output_path = "../assets/multimodal_llm_benchmarking_application_architecture.png"

with Diagram("Multimodal LLM Benchmarking Application Architecture", filename=output_path, show=False, direction="LR", graph_attr=graph_attr): 
    
    with Cluster("Data Sources"):
        hf = Custom("Hugging Face", "../assets/icons/hf-logo.png")
        local = Custom("Local Machine", "computer")
    
    with Cluster("Google Cloud Platform"):
        gcp_logo = Custom("", "../assets/icons/gcp-logo.png")
        
        with Cluster("Storage"):
            gcs = Storage("GCP Bucket")
            db = SQL("PostgreSQL")
            gcs - Edge(color="black", style="dotted", label="Data\nExchange") - db

        tf = Custom("Terraform", "../assets/icons/terraform.png")

    with Cluster("Data Processing"):
        scripts = Python("Python Scripts")

    with Cluster("User Interface"):
        ui = Custom("Streamlit UI", "../assets/icons/streamlit.png")
        with Cluster("Pages"):
            landing = Custom("Landing Page", "../assets/icons/streamlit.png")
            llm_prompting = Custom("LLM Prompting", "../assets/icons/streamlit.png")
            dashboard = Custom("Metrics Dashboard", "../assets/icons/streamlit.png")

    openai = Custom("OpenAI API", "../assets/icons/openai.png")
    user = User("User")

    # Data flow from sources to processing
    hf >> Edge(color="darkgreen", label="Download") >> local
    local >> Edge(color="darkgreen", label="Process") >> scripts
    scripts >> Edge(color="darkgreen", style="dashed", label="Load") >> gcs
    scripts >> Edge(color="darkgreen", style="dashed", label="Load") >> db

    # Terraform manages GCP resources
    tf >> Edge(color="orange", style="dotted", label="Manage") >> gcs
    tf >> Edge(color="orange", style="dotted", label="Manage") >> db

    # User interactions with the UI
    user >> Edge(color="blue", label="Interact") >> ui
    ui >> Edge(color="blue") >> landing
    ui >> Edge(color="blue") >> llm_prompting
    ui >> Edge(color="blue") >> dashboard

    # LLM prompting interactions with data sources
    llm_prompting >> Edge(color="red", label="Query") >> db
    llm_prompting >> Edge(color="red", label="Fetch") >> gcs
    llm_prompting >> Edge(color="purple", label="Request") >> openai

    # Dashboard metrics fetching
    dashboard >> Edge(color="darkblue", style="bold", label="Fetch Metrics") >> db
