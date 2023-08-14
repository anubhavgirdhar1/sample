import streamlit as st
import openai
# from io import BytesIO
import pandas as pd
# from pytrends.request import TrendReq
# import time
# import requests
from newsapi import NewsApiClient

# Load your API key from an environment variable or secret management service
openai.api_key = "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"

# Replace 'YOUR_API_KEY' with your actual NewsAPI key
newsapi = NewsApiClient(api_key='ca7b69a1eeff43e39bb4494edf2149df')

def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    image_url = response['data'][0]['url']
    return image_url

def generate_content(topic, language, country, industry, creativity, audience, tone, words, level):
    # Define the fixed prompt
    prompt = f'As a creative writer, Generate unbiased content on the following headline: {topic}. Target the industry {industry}.Write it in the language {language}. Creativity percentage defines how creative it will be, by creative i mean either way too realisitc or way to fictional so consider the percentage to be {creativity}. Make sure to target the country {country}. Write it targetting specifically the age group of {audience}, also keep the tone {tone}. Dont exceed limit of {words}. Make sure to write in a {level} way.'

    # Initialize the conversation history with the fixed prompt
    messages = [{"role": "user", "content": prompt}]

    # Call the GPT-3.5 model to generate a response
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    content = response['choices'][0]['message']['content']

    return content


def generate_hashtags(topic):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant that generates hashtags."},
                  {"role": "user", "content": f"Generate relevant hashtags for the topic: {topic}"}],
        max_tokens=30
    )
    hashtags = response.choices[0].message['content'].strip()
    return hashtags

def main():
    st.set_page_config(layout="wide")  # Set the page layout to wide by default

    st.markdown(
        """
        <style>
            @font-face {
                font-family: 'Uni Sans';
                src: url('./fonts/unisans-regular.woff2') format('woff2'),
                     url('./fonts/unisans-regular.woff') format('woff');
                font-weight: normal;
                font-style: normal;
            }
            .st-au, .st-ax, .st-av, .st-aw, .st-be, .st-bg, .st-b8, .st-b3, .st-b4, .st-bh,
            .st-bi, .st-bj, .st-bk, .st-bl, .st-bm, .st-bn, .st-bo, .st-bp, .st-bq, .st-b1,
            .st-br, .st-bs, .st-bt, .st-bu, .st-bv, .st-bw, .st-bx {
                background-color: transparent;
                color: white;
                border-color: white;
                border-radius: 10px;
            }
            .css-1avcm0n.e8zbici2 {
                border-color: white;
                background-color: transparent;
            }
            .css-uf99v8.egzxvld5 {
                background-image: linear-gradient(to right, #C33764, #1D2671);
            }
            .css-5uatcg.edgvbvh10 {
                background-color: transparent;
                border-radius: 10px;
                color: white;
                border-color: white;
            }
            .css-5uatcg.edgvbvh10:hover {
                background-color: black;
            }
            .css-ocqkz7.e1tzin5v3 {
                border: black;
                border-width: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Topic Extractor")

    # Create a wide layout with three columns
    col1, col2, col3 = st.columns(3)

    # Fetch related keywords for the input keyword
    with col1:
        st.subheader("Latest topics")

        # Input text area to enter the query
        query_input = st.text_input("Enter query for Latest topics", "Neom")

        # Fetch recent AI-related news articles based on the entered query
        ai_news = newsapi.get_everything(q=query_input, sort_by='relevancy', language='en', from_param='2023-08-01', to='2023-08-09')

        # Extract relevant information from the news response
        news_articles = ai_news['articles']

        def format_newsletter(articles):
            ls = []
            newsletter_content = "<h1>Trending topics</h1>"
            for article in articles:
                title = article['title']
                newsletter_content += f"<p>{title}</p>"
                ls.append(title)
            return ls[:15]

        formatted_titles = format_newsletter(news_articles)

        # Display the formatted news titles in a table
        st.table(pd.DataFrame(formatted_titles, columns=['News Title']))

    with col2:
        st.subheader("AI Content Generator")

        col4, col5, col6, col11 = st.columns(4)

        language = col4.selectbox("Target Language", ["English", "Hindi", "Arabic", "Hinglish"])
        industry = col5.selectbox("Target Industry", ["Retail", "Hospitality", "Healthcare"])
        country = col6.selectbox("Target Country", ["Saudi Arabia", "United States of America", "India"])
        level = col11.selectbox("Grammar level", ["Sophisticated", "Layman"])

        col7, col8, col9, col10 = st.columns(4)

        creativity = col7.text_input("creativity %", "50%")
        audience = col8.selectbox("Target audience", ["Adults", "Teens", "Kids", "Old Age"])
        tone = col9.selectbox("Tone", ["Formal", "Casual", "Professional", "Funny", "Serious"])
        words = col10.text_input("word count", "500")

        topic_name = st.text_input("Enter a topic", "Neom")

        filename = ""


        if st.button("Generate Content"):
            if topic_name.strip():
                generated_content = generate_content(topic_name, language, country, industry, creativity, audience, tone, words, level)
                st.text_area("Generated Content", generated_content, height=600)
                

                generated_hashtags = generate_hashtags(generated_content)
                st.text_area("Generated Hashtags", generated_hashtags, height=100)

                
    with col3:
        st.header("Image Generation")
        if st.button("Generate image"):
            st.subheader("Generated Image")

            image_url = generate_image(topic_name)  # Generate image directly from the topic text

            # Display the generated image in an iframe
            if image_url:
                st.image(image_url, caption='Generated Image', use_column_width=True)
            else:
                st.text("Image not available")
   
if __name__ == "__main__":
    main()
