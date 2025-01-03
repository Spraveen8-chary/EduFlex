import streamlit as st
from features.apikeys import SEARCH_ID, GOOGLE_API_KEY
import requests
from urllib.parse import urlparse


def GET_MATERIAL():
    
    api_key = GOOGLE_API_KEY

    search_engine_id = SEARCH_ID

    markdown_text = """
    # Course Materials

    Welcome to our Course Materials section! Here, you can find a wealth of resources tailored to your learning needs. Whether you're a beginner, intermediate, or advanced learner, we've got you covered. Simply enter your query below, and we'll provide you with relevant materials to help you excel in your studies.

    ## How to Use

    1. **Enter Your Query**: Type your topic or keyword of interest in the search box below.
    2. **Explore Resources**: Once you've entered your query, hit the "Search" button, and we'll fetch the most relevant materials for you.
    3. **Learn and Grow**: Dive into the materials provided, including articles, videos, tutorials, and more, to enhance your understanding and mastery of the subject.

    """

    # Display Markdown text in the app
    st.markdown(markdown_text)

    col1,col2,col3 = st.columns(3)
    with col2:
        search_query = st.text_input("On which topic do you need materials")

    url = 'https://www.googleapis.com/customsearch/v1'

    params = {
        'q': search_query,
        'key': api_key,
        'cx': search_engine_id,
        'fileType': 'pdf'
    }

    if search_query:
        response = requests.get(url, params=params)
        print(response.json())
        results = response.json()['items']
        pdf_links = []
        for item in results:
            # print(item['link'])
            pdf_links.append(item['link'])



        def get_domain_name(url):
            """
            Extracts the domain name from a given URL and removes the "www" prefix if present.
            """
            parsed_url = urlparse(url)
            domain_name = parsed_url.netloc
            if domain_name.startswith("www."):
                domain_name = domain_name[4:]
            return domain_name


        def display_pdf_links(pdf_links):

            for link in pdf_links:
                domain_name = get_domain_name(link)
                # st.subheader(domain_name)
                st.subheader(f"[{domain_name}]({link})")
                # st.write(f"[Link]({link})")

        st.write(":green[Here are the materials that we have found online related to your query]👇👇")
        display_pdf_links(pdf_links)