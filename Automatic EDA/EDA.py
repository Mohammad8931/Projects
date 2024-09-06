import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import nbformat
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell
import base64
import json

def generate_eda(df):
    st.header("Exploratory Data Analysis")

    # Basic Information
    st.subheader("Dataset Information")
    st.write(f"Number of rows: {df.shape[0]}")
    st.write(f"Number of columns: {df.shape[1]}")

    # Data Types
    st.subheader("Data Types")
    st.write(df.dtypes)

    # Missing Values
    st.subheader("Missing Values")
    missing = df.isnull().sum()
    st.write(missing[missing > 0])

    # Basic Statistics
    st.subheader("Basic Statistics")
    st.write(df.describe())

    # Correlation Matrix
    st.subheader("Correlation Matrix")
    corr = df.corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

    # Histograms
    st.subheader("Histograms")
    for col in df.select_dtypes(include=[np.number]).columns:
        fig, ax = plt.subplots()
        df[col].hist(bins=30, ax=ax)
        ax.set_title(f'Histogram of {col}')
        st.pyplot(fig)

    # Box Plots
    st.subheader("Box Plots")
    for col in df.select_dtypes(include=[np.number]).columns:
        fig, ax = plt.subplots()
        df.boxplot(column=col, ax=ax)
        ax.set_title(f'Box Plot of {col}')
        st.pyplot(fig)

    # Scatter Plots
    st.subheader("Scatter Plots")
    num_cols = df.select_dtypes(include=[np.number]).columns
    if len(num_cols) >= 2:
        x_col = st.selectbox("Select X axis", num_cols)
        y_col = st.selectbox("Select Y axis", num_cols)
        fig, ax = plt.subplots()
        df.plot.scatter(x=x_col, y=y_col, ax=ax)
        st.pyplot(fig)

def create_notebook(df):
    nb = new_notebook()
    
    # Add markdown cell with title
    nb.cells.append(new_markdown_cell("# Automated Exploratory Data Analysis"))
    
    # Add code cell with data loading
    nb.cells.append(new_code_cell("import pandas as pd\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nimport numpy as np\n\n"
                                  f"df = pd.read_csv('your_data.csv')  # Replace with actual filename\n"
                                  "df.head()"))
    
    # Add basic information
    nb.cells.append(new_markdown_cell("## Dataset Information"))
    nb.cells.append(new_code_cell(f"print(f'Number of rows: {df.shape[0]}')\n"
                                  f"print(f'Number of columns: {df.shape[1]}')"))
    
    # Add data types
    nb.cells.append(new_markdown_cell("## Data Types"))
    nb.cells.append(new_code_cell("df.dtypes"))
    
    # Add missing values
    nb.cells.append(new_markdown_cell("## Missing Values"))
    nb.cells.append(new_code_cell("df.isnull().sum()"))
    
    # Add basic statistics
    nb.cells.append(new_markdown_cell("## Basic Statistics"))
    nb.cells.append(new_code_cell("df.describe()"))
    
    # Add correlation matrix
    nb.cells.append(new_markdown_cell("## Correlation Matrix"))
    nb.cells.append(new_code_cell("corr = df.corr()\nplt.figure(figsize=(10, 8))\nsns.heatmap(corr, annot=True, cmap='coolwarm')\nplt.title('Correlation Matrix')\nplt.show()"))
    
    # Add histograms
    nb.cells.append(new_markdown_cell("## Histograms"))
    for col in df.select_dtypes(include=[np.number]).columns:
        nb.cells.append(new_code_cell(f"plt.figure()\ndf['{col}'].hist(bins=30)\nplt.title('Histogram of {col}')\nplt.show()"))
    
    # Add box plots
    nb.cells.append(new_markdown_cell("## Box Plots"))
    for col in df.select_dtypes(include=[np.number]).columns:
        nb.cells.append(new_code_cell(f"plt.figure()\ndf.boxplot(column='{col}')\nplt.title('Box Plot of {col}')\nplt.show()"))
    
    # Add scatter plots
    nb.cells.append(new_markdown_cell("## Scatter Plots"))
    num_cols = df.select_dtypes(include=[np.number]).columns
    if len(num_cols) >= 2:
        nb.cells.append(new_code_cell(f"plt.figure()\ndf.plot.scatter(x='{num_cols[0]}', y='{num_cols[1]}')\nplt.title('Scatter Plot')\nplt.show()"))
    
    return nb

def main():
    st.title("Automated Exploratory Data Analysis")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        # Read CSV file
        df = pd.read_csv(uploaded_file)
        
        # Display raw data
        st.subheader("Raw Data")
        st.write(df)

        # Generate EDA
        generate_eda(df)
        
        # Create download button for Jupyter notebook
        if st.button("Download as Jupyter Notebook"):
            notebook = create_notebook(df)
            
            # Convert notebook to JSON string
            notebook_json = json.dumps(nbformat.from_dict(notebook))
            
            # Encode the JSON string to bytes
            notebook_bytes = notebook_json.encode('utf-8')
            
            # Create a BytesIO object
            buffer = BytesIO(notebook_bytes)
            
            # Create download link
            b64 = base64.b64encode(buffer.getvalue()).decode()
            href = f'<a href="data:application/x-ipynb+json;base64,{b64}" download="EDA_results.ipynb">Download Jupyter Notebook</a>'
            st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()