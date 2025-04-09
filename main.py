import streamlit as st
import pandas as pd
import os
from io import BytesIO


st.set_page_config(page_title = "Data Sweeper",layout="wide")

st.markdown(
    """
    <style>
        
          body {
            background-color: #000000;  /* White background for the entire page */
            font-family: 'Arial', sans-serif;
            color: #333;  /* Dark text color for readability */
        }

        .main {
            background-color: #000000;  /* White background for the main container */
        }

        .block-container {
            padding: 3rem 2rem;  /* Padding around the container for spacing */
            border-radius: 12px;  /* Rounded corners for a smoother look */
            background-color: #ffffff;  /* White background for the block container */
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);  /* Subtle shadow for depth */
        }

        h1, h2, h3, h4, h5, h6 {
            color: #0056b3;  /* Dark blue color for headings to stand out */
            font-family: 'Arial', sans-serif;
        }

        .stButton>button {
            border: none;
            border-radius: 8px;  /* Rounded button edges */
            background-color: #007bff;  /* Blue color for buttons */
            color: white;  /* White text on buttons */
            padding: 0.75rem 1.5rem;  /* Larger button size for better interaction */
            font-size: 1rem;  /* Legible text size */
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);  /* Shadow for depth */
        }

        .stButton>button:hover {
            background-color: #fafafa;  /* White background on hover */
            cursor: pointer;
        }

        .stDataFrame, .stTable {
            border-radius: 10px;  /* Rounded corners for data frames and tables */
            overflow: hidden;  /* Ensures no content overflows */
            background-color: #f9f9f9;  /* Light gray background for data */
        }

        .stDataFrame thead, .stTable thead {
            background-color: #007bff;  /* Blue header for tables */
            color: white;  /* White text on table headers */
        }

        .css-1aumxhk, .css-18e3th9 {
            text-align: left;
            color: #333;  /* Dark text for content */
        }

        .stRadio>label, .stCheckbox>label {
            font-weight: bold;
            color: #333;  /* Dark text for labels */
        }

        .stDownloadButton>button {
            background-color: #28a745;  /* Green color for download buttons */
            color: white;  /* White text on buttons */
        }

        .stDownloadButton>button:hover {
            background-color: #218838;  /* Darker green on hover */
        }

        /* Style for the file uploader */
        .stFileUploader {
            background-color: #e9f7ff;  /* Light blue background for file upload */
            padding: 20px;
            border-radius: 8px;
            border: 2px dashed #007bff;  /* Blue dashed border for the uploader */
            margin-top: 20px;
        }

        .stFileUploader input[type="file"] {
            font-size: 16px;
        }

        /* Customizing the checkboxes and radios */
        .stCheckbox, .stRadio {
            margin-bottom: 15px;
        }

        /* Style for the success message */
        .stSuccess {
            color: #28a745;  /* Green color for success messages */
            font-weight: bold;
            font-size: 18px;
        }

        /* Style for error messages */
        .stError {
            color: #dc3545;  /* Red color for error messages */
            font-weight: bold;
            font-size: 18px;
        }
    </style>
    """,
    unsafe_allow_html=True  # 'unsafe_allow_html' permits raw HTML/CSS embedding in the Streamlit app
)

#Title
st.title("Data Sweeper")
# description
st.write("Transfrorm your files between CSV and Excel formats with built-in data cleaning and visualization")

# file uploader
uploaded_files = st.file_uploader("upload your files (CSV or Excel):", type=["csv","xlsx"], accept_multiple_files=True)



if uploaded_files:
    for file in uploaded_files:  # <-- loop starts here
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue  # <-- now it's correctly inside the loop


            # #display info about the file  
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:**{file.size/1024}")

        #file details
        st.write("Preview the Head of the Dataframe")
        st.dataframe(df.head())

        #Data cleaning options
        st.subheader("Data Cleaning Options")    
        if st.checkbox(f"clean data for {file.name}"):
            col1,col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from the file : {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write(" Duplicates removed")

            with col2:
                if st.button(f"Remove missing values from the file : {file.name}"):
                    numeric_cols  = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values have been filled!") 

    st.subheader ("Select Columns to Convert")   
    columns = st.multiselect(f"choose columns for {file.name}",df.columns ,default=df.columns )    
    df = df[columns]

    #data visualization 
    st.subheader("Data Visualization")
    if st.checkbox(f"show data visualization for {file.name}"):
        st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

   # Conversion options
    st.subheader("Conversion Options")     
    conversion_type  = st.radio(f"convert {file.name} to:",["CSV","Excel"],key=file.name)
    
    if st.button(f"Convert {file.name}"):
        buffer = BytesIO()
        if conversion_type == "CSV":
            df.to_csv(buffer, index=False)
            file_name = file.name.replace(file_ext, ".csv")
            mime_type = "text/csv"
        elif conversion_type == "Excel":
            df.to_excel(buffer, index=False)
            file_name = file.name.replace(file_ext, ".xlsx")
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        buffer.seek(0)

        st.download_button(
            label=f"Download {file.name} as {conversion_type}",
            data=buffer,
            file_name=file_name,
            mime=mime_type
        )

    st.success("All files processed successfully!")