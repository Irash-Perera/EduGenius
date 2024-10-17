import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

st.header("Explore the :red[Documentation] 📚", divider="red")
col1,col2 = st.columns([1,1.5])

with col1:
  st.markdown("##### :red[Download] the documentation")
  with open("utils/docs/Proposal_Submission.pdf", "rb") as pdf_file:
      PDFbyte = pdf_file.read()
  st.download_button(label="Download Proposal Submission 🧭", 
                      data=PDFbyte,
                      file_name="Project Proposal.pdf",
                      mime='application/octet-stream',
                      use_container_width=True,
                      )

  with open("utils/docs/Software_Requirements_Specification.pdf", "rb") as pdf_file:
      PDFbyte = pdf_file.read()
  st.download_button(label="Download Software Requirements Specification 📝",
                      data=PDFbyte,
                      file_name="Software Requirements Specification.pdf",
                      mime='application/octet-stream',
                      use_container_width=True)

  with open("utils/docs/Software_Architecture_Document.pdf", "rb") as pdf_file:
      PDFbyte = pdf_file.read()
  st.download_button(label="Download Software Architecture Document 🏗️",
                      data=PDFbyte,
                      file_name="Software Architecture Document.pdf",
                      mime='application/octet-stream',
                      use_container_width=True)

  with open("utils/docs/Feasibility_Study.pdf", "rb") as pdf_file:
      PDFbyte = pdf_file.read()
  st.download_button(label="Download Feasibility Study Report 📊",
                      data=PDFbyte,
                      file_name="Feasibility Study Report.pdf",
                      mime='application/octet-stream',
                      use_container_width=True)
  
with col2:
  st.markdown("##### Get an idea about whats happening :red[inside]")
  st.image("utils/docs/chart.png", use_column_width=True)
  
file = st.selectbox("Select a document to preview", ["Proposal Submission", "Software Requirements Specification", "Software Architecture Document", "Feasibility Study Report"])
if file == "Proposal Submission":
  pdf_viewer("utils/docs/Proposal_Submission.pdf")
elif file == "Software Requirements Specification":
  pdf_viewer("utils/docs/Software_Requirements_Specification.pdf")
elif file == "Software Architecture Document":
  pdf_viewer("utils/docs/Software_Architecture_Document.pdf")
else:
  pdf_viewer("utils/docs/Feasibility_Study.pdf")