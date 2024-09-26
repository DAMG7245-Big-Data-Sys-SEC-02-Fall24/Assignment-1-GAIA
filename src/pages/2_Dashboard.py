import sys
import os
import streamlit as st
import pandas as pd
import plotly.express as px
import metrics as mt

# Set page config as the first Streamlit function
st.set_page_config(page_title="LLM Performance Dashboard", layout="wide")


# Title and Intro
st.title("LLM Performance Dashboard")
st.write("""
This dashboard provides insights into the performance of various Large Language Models (LLMs) based on the responses generated.
Explore various metrics such as accuracy, improvement rate, and performance across task levels.
""")

st.subheader("Category counts")
response_counts = mt.response_count_by_category()
df_response_counts = pd.DataFrame(response_counts, columns=['Category', 'Count'])
fig_response_counts = px.bar(df_response_counts, x='Category', y='Count', 
                             title="Response Count by Category",
                             labels={'Count':'Count','Category':'Category'},
                             text='Count')
fig_response_counts.update_traces(
            texttemplate='<b>%{text:.0f}</b>',  # Make text bold and round to 2 decimal places
            textposition='inside',            # Position text outside the bars
            textfont_size=26,                   # Increase font size
            textfont_color='Black'
    )
#fig_response_counts.update_layout(yaxis_range=[0, 200])
st.plotly_chart(fig_response_counts)

st.subheader(f"Response Breakdown for different task levels")
response_breakdown = mt.response_breakdown_by_task_level()
df_response_breakdown = pd.DataFrame(response_breakdown, columns=['Task Level', 'Result Category', 'Count'])

def plot_donut_charts_for_levels(df_response_breakdown):
    levels = df_response_breakdown['Task Level'].unique()
    sorted_levels = sorted(df_response_breakdown['Task Level'].unique())
    for level in sorted_levels:
        st.subheader(f"Task Level: {level}")
        df_level = df_response_breakdown[df_response_breakdown['Task Level'] == level]
        # Create a donut chart for this task level
        fig = px.pie(df_level, names='Result Category', values='Count', 
                     title=f"Response Breakdown for Task Level {level}",
                     hole=0.3)  # hole=0.3 makes it a donut chart
        

        st.plotly_chart(fig)

# Call the function to generate and display the charts
plot_donut_charts_for_levels(df_response_breakdown)


# Overall Accuracy per LLM
st.subheader("Overall Accuracy per LLM (As Is)")
overall_accuracy = mt.overall_accuracy_per_llm()
if overall_accuracy:
    df_overall_accuracy = pd.DataFrame(overall_accuracy, columns=['LLM ID', 'Accuracy'])
    # Formatting the accuracy to 2 decimal places
    df_overall_accuracy['Accuracy'] = df_overall_accuracy['Accuracy'].round(2)
    # Create vertical bar chart (default orientation)
    fig_overall_accuracy = px.bar(df_overall_accuracy, x='LLM ID', y='Accuracy', 
                                  title="Overall Accuracy per LLM", 
                                  labels={'Accuracy': 'Accuracy (%)', 'LLM ID': 'LLM'},
                                  text='Accuracy',orientation='v',text_auto='.2f')
    fig_overall_accuracy.update_traces(
            texttemplate='<b>%{text:.2f}</b>',  # Make text bold and round to 2 decimal places
            textposition='inside',            # Position text outside the bars
            textfont_size=26,                   # Increase font size
            textfont_color='Black'
        )
    fig_overall_accuracy.update_layout(yaxis_range=[0, 100])
    st.plotly_chart(fig_overall_accuracy)
else:
    st.write("No data available for overall accuracy.")

# Accuracy with Annotation
st.subheader("Accuracy with Annotation")
accuracy_annotation = mt.accuracy_with_annotation()
if accuracy_annotation:
    df_accuracy_annotation = pd.DataFrame(accuracy_annotation, columns=['LLM ID', 'Accuracy with Annotation'])
    df_accuracy_annotation['Accuracy with Annotation'] = df_accuracy_annotation['Accuracy with Annotation'].round(2)
    fig_accuracy_annotation = px.bar(df_accuracy_annotation, x='LLM ID', y='Accuracy with Annotation', 
                                     title="Accuracy with Annotation", 
                                     labels={'Accuracy with Annotation': 'Accuracy (%)', 'LLM ID': 'LLM'},
                                     text='Accuracy with Annotation',orientation='v',text_auto='.2f')
    fig_accuracy_annotation.update_traces(
            texttemplate='<b>%{text:.2f}</b>',  # Make text bold and round to 2 decimal places
            textposition='inside',            # Position text outside the bars
            textfont_size=26,                   # Increase font size
            textfont_color='Black'
    )
    fig_accuracy_annotation.update_layout(yaxis_range=[0, 100])
    st.plotly_chart(fig_accuracy_annotation)
else:
    st.write("No data available for accuracy with annotation.")

# Improvement Rate
st.subheader("Improvement Rate")
improvement = mt.improvement_rate()
if improvement:
    df_improvement = pd.DataFrame(improvement, columns=['LLM ID', 'Improvement Rate'])
    df_improvement['Improvement Rate'] = df_improvement['Improvement Rate'].round(2)
    fig_improvement = px.bar(df_improvement, x='LLM ID', y='Improvement Rate', 
                                title="Improvement Rate by LLM", 
                                labels={'Improvement Rate': 'Improvement Rate (%)', 'LLM ID': 'LLM'},
                                text='Improvement Rate', orientation='v', text_auto='.2f')
    fig_improvement.update_traces(
            texttemplate='<b>%{text:.2f}</b>',  # Make text bold and round to 2 decimal places
            textposition='inside',            # Position text outside the bars
            textfont_size=26,                   # Increase font size
            textfont_color='Black'
        )
    fig_improvement.update_layout(yaxis_range=[0, 100])
    st.plotly_chart(fig_improvement)
else:
    st.write("No data available for improvement rate.")

# Failure Rate after Annotation
st.subheader("Failure Rate after Annotation")
failure_rate = mt.failure_rate_after_annotation()
if failure_rate:
    df_failure_rate = pd.DataFrame(failure_rate, columns=['LLM ID', 'Failure Rate'])
    df_failure_rate['Failure Rate'] = df_failure_rate['Failure Rate'].round(2)
    fig_failure_rate = px.bar(df_failure_rate, x='LLM ID', y='Failure Rate', 
                              title="Failure Rate after Annotation", 
                              labels={'Failure Rate': 'Failure Rate (%)', 'LLM ID': 'LLM'},
                              text='Failure Rate',orientation='v',text_auto='.2f')
    fig_failure_rate.update_traces(
            texttemplate='<b>%{text:.2f}</b>',  # Make text bold and round to 2 decimal places
            textposition='inside',            # Position text outside the bars
            textfont_size=26,                   # Increase font size
            textfont_color='Black'
    )
    fig_failure_rate.update_layout(yaxis_range=[0, 100])
    st.plotly_chart(fig_failure_rate)
else:
    st.write("No data available for failure rate after annotation.")

# Performance by Task Level
st.subheader("Performance by Task Level")
performance_task_level = mt.performance_by_task_level()
if performance_task_level:
    df_performance_task_level = pd.DataFrame(performance_task_level, columns=['LLM ID', 'Task Level', 'Performance'])
    df_performance_task_level['Performance'] = df_performance_task_level['Performance'].round(2)
    fig_performance_task_level = px.line(df_performance_task_level, x='Task Level', y='Performance', 
                                         color='LLM ID', title="Performance by Task Level", 
                                         labels={'Performance': 'Performance (%)', 'Task Level': 'Task Level'},
                                         text='Performance',orientation='v')
    fig_performance_task_level.update_traces(mode='lines+markers')
    st.plotly_chart(fig_performance_task_level)
else:
    st.write("No data available for performance by task level.")


# Footer
st.write("Metrics are based on the LLM responses and tasks available in the database.")
