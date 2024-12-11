# Cold-Mail-Generator
Developing a Cold Mail Generator using Langchain and LLMs like Llama 3.1. This  tool automates the process of analyzing job postings and generating relevant cold  emails. By implementing such AI-driven solutions, companies can reach clients with precision and improve their chances of  securing new projects

Objective:
To automate the process of generating cold emails by using LLM (Lama 3.1) and LangChain. 
The tool aims to:
 Automatically extract job roles and skills from clients' career pages.
 Generate tailored emails matching the extracted job details with relevant portfolios.
 Use machine learning to enhance the relevance of the emails to job postings.

Methodology:
1. LangChain Framework: We will use Langchain to extract text from client job portals 
and analyze job descriptions for specific skills and roles.
2. Llama 3.1 LLM: This open-source language model will generate personalized cold 
emails by extracting key information such as job roles, required skills, and job 
descriptions from the extracted text.
3. ChromaDB Vector Store: We will store relevant skills and portfolios in ChromaDB. 
When a job post is analyzed, the system retrieves matching portfolios and generates a 
relevant cold email.
4. Streamlit: This will serve as the frontend, allowing users to input job postings, submit 
them for processing, and receive generated emails.

Project Flow:
1. Input: User submits a job post from a potential client's career page.
2. Data Extraction: Langchain extracts text data from the job post.
3. Skill Identification: Llama 3.1 LLM processes the extracted data to identify required 
skills and roles in JSON format.
4. Portfolio Matching: ChromaDB retrieves the stored portfolios matching the identified 
skills.
5. Cold Email Generation: Llama 3.1 generates a customized cold email based on the 
identified skills, roles, and corresponding portfolios.
6. Output: The email is delivered to the user, ready to be sent to the client.
