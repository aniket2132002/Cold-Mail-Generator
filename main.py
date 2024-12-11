#main code//////////////////////////////////////////////////////
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader 
from evaluate import calculate_cosine_similarity, calculate_bleu_score
import time

from chains import Chain
from Portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:")
   
    submit_button = st.button("Submit")

    if submit_button:
        # List to store time taken for each email generation
        generation_times = []
        
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                
                # Start tracking time for email generation
                start_time = time.time()
                email = llm.write_mail(job, links)
                end_time = time.time()
                
                # Calculate and store the time taken to generate the email
                generation_time = end_time - start_time
                generation_times.append(generation_time)
                
                st.code(email, language='markdown')

                reference_email = """Subject: Unlock Data-Driven Growth with TCS's Expertise

Dear Hiring Manager,

I came across your job posting for a Data Scientist and was impressed by the role's focus on driving business growth through data analysis. As a Business Development Executive at TCS, I'd like to introduce you to our company's capabilities in empowering businesses like yours with tailored AI and software consulting solutions.

At TCS, we've helped numerous enterprises achieve scalability, process optimization, cost reduction, and heightened overall efficiency. Our team of experts excels in Machine Learning, Data Visualization, and Statistics, making us an ideal partner for your data-driven initiatives.

Our portfolio showcases our expertise in Machine Learning and Python, with successful projects that demonstrate our ability to deliver high-quality solutions. You can explore our work at https://example.com/ml-python-portfolio and https://example.com/ml-python-portfolio.

We believe that our capabilities align with your requirements, and we'd be delighted to discuss how TCS can support your business goals. If you're interested in learning more about our services, I'd be happy to schedule a call to explore further.

Please feel free to reply to this email or give me a call at your convenience. I look forward to the opportunity to collaborate and drive growth for your business.

Best regards,

Aniket
Business Development Executive
TCS"""

                # # Cosine Similarity
                # cosine_sim = calculate_cosine_similarity(reference_email, email)
                # st.write(f"Cosine Similarity: {cosine_sim}")

                # # BLEU Score
                # bleu_score = calculate_bleu_score(reference_email, email)
                # # st.write(f"BLEU Score: {bleu_score}")

                # bleu_score_percentage = bleu_score * 100
                # st.write(f"BLEU Score: {bleu_score_percentage}%")

            # Calculate the average email generation time
            if generation_times:
                average_time = sum(generation_times) / len(generation_times)
                st.write(f"Average email generation time: {average_time:.4f} seconds")
        
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
