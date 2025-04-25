import streamlit as st 
from features.apikeys import SEARCH_ID, GOOGLE_API_KEY
import requests
from features.logger import log_action
from urllib.parse import urlparse


def GET_MATERIAL(username=''):
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

    col1, col2, col3 = st.columns(3)
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
        log_action(username, f"Researching on '{search_query}'")
        response = requests.get(url, params=params)
        print(response.json())
        results = response.json().get('items', [])
        pdf_links = []

        if results:
            log_action(username, "Research results found")
            for item in results:
                pdf_links.append({
                    'title': item['title'],
                    'link': item['link']
                })
        else:
            log_action(username, f"Error: 'API expired'")

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
            for pdf in pdf_links:
                log_action(username, f"URL : '{pdf['link']}'")
                domain_name = get_domain_name(pdf['link'])
                st.subheader(f"[{pdf['title']}]({pdf['link']}) - [{domain_name}]")
                # Optional: You could also display the domain or additional info if needed
                # st.write(f"[Link]({pdf['link']})")

        st.write(":green[Here are the materials that we have found online related to your query]👇👇")
        log_action(username, "Research Papers List ")
        display_pdf_links(pdf_links)
