import streamlit as st
import requests
import base64
import os
import subprocess

st.set_page_config(
    page_title="Resume Parser",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://talentxpert.com/',
        'About': "Generative AI Powered Resume Parser"
    }
)

# Create folders if they don't exist
if not os.path.exists("input_pdf"):
    os.makedirs("input_pdf")

# Streamlit UI
st.title("Resume Parser")

# Upload PDF file
uploaded_pdf = st.file_uploader("Upload a file", type=["pdf", ".doc", ".docx"])

try:
    if uploaded_pdf is not None:
        left_column, right_column = st.columns(2)

        if uploaded_pdf.name.lower().endswith(".doc") or uploaded_pdf.name.lower().endswith(".docx"):
            if uploaded_pdf.name.lower().endswith(".docx"):
                pdf_filename = uploaded_pdf.name.lower().replace(".docx", ".pdf")
            elif uploaded_pdf.name.lower().endswith(".doc"):
                pdf_filename = uploaded_pdf.name.lower().replace(".doc", ".pdf")
            else:
                raise "The file can't be supported"

            with open("input_pdf/" + uploaded_pdf.name.lower(), "wb") as write_file:
                write_file.write(uploaded_pdf.read())
            st.text(str(uploaded_pdf.name.lower()))
            command = ['libreoffice', '--headless', '--convert-to', 'pdf', "input_pdf/" + str(uploaded_pdf.name.lower()),
                       '--outdir', 'input_pdf/']

            completed_process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if completed_process.returncode == 0:

                with open('input_pdf/' + pdf_filename, "rb") as f:
                    pdf_data = f.read()

                with left_column:
                    st.header("Input Document")
                    pdf_display = f'<iframe src="data:application/pdf;base64,{base64.b64encode(pdf_data).decode("utf-8")}" width="100%" height="1000" type="application/pdf"></iframe>'
                    st.markdown(pdf_display, unsafe_allow_html=True)
                pdf_filename = 'input_pdf/' + pdf_filename
            else:
                raise "The file can't be supported"

        else:
            # Display the PDF in the left column while waiting for processing

            # Save the uploaded PDF to the "input_pdf" folder
            pdf_filename = f"input_pdf/{uploaded_pdf.name}"
            with open(pdf_filename, "wb") as pdf_file:
                pdf_file.write(uploaded_pdf.read())

            with left_column:
                st.header("Input Document")
                with open(pdf_filename, "rb") as f:
                    pdf_data = f.read()
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64.b64encode(pdf_data).decode("utf-8")}" width="100%" height="1000" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)

        # Process the uploaded PDF file using the REST API
        with st.spinner("Processing..."):
            with open(pdf_filename, "rb") as f:
                files = {"file": f}
                response = requests.post("http://localhost:8001/api/v1/parse", files=files, data={"timestamps": "s"})

        if response.status_code == 200:
            data = response.json()

            JSON_output = data["ParserResults"]

            # Display the OpenAI output in the right column after processing
            with right_column:
                st.header("Json Output")
                st.json(JSON_output)
            time_output = data["ProcessTimes"]
            st.header("Processing Latency")
            st.json(time_output)
        else:
            st.error("An error occurred while processing the PDF.", icon="🚨")



except:
    st.error('Please try a different file', icon="🚨")
