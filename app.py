import streamlit as st
import prompts as pr
#from langchain import PromptTemplate
from langchain.llms import OpenAI
#import os
import openai

selected_model = "gpt-3.5-turbo"

def basic_generation(user_prompt):
    completion = openai.ChatCompletion.create(
        model=selected_model,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )
    response = completion.choices[0].message.content
    return response

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.5, openai_api_key=openai_api_key)
    return llm


st.set_page_config(page_title="YouTube Title & Video Script Generator", page_icon=":robot:")
st.header("YouTube Title & Video Script Generator")
st.write("### **This tool generates a YouTube video title, thumbnail, script, and a Twitter thread based on the topic you enter.**")
st.write("\n")
col1, col2 = st.columns(2)

with col1:
    st.markdown("##### Don't spend hours trying to generate your YT titles, and scripts. \n ##### This tool is designed to help you generate those ideas, and much more, fast and easy!")
    st.write("\n")
    st.write("\n")
    st.image(image='look down.png', width=100, caption='')

with col2:
    st.image(image='Youtube title and script generator.png', width=300, caption='generated with Microsoft Designer')
    
# generating a sidebar for indserting the parameters
st.sidebar.header('Input')
#step 1: Enter a Topic
user_topic = st.sidebar.text_input(label="Please enter your video topic: ",  placeholder="Topic")
user_minutes= st.sidebar.text_input(label="Please enter your video length (in minutes): ",  placeholder="Length")

def get_api_key():
    input_text = st.sidebar.text_input(label="OpenAI API Key",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key")
    return input_text

openai_api_key = get_api_key()
st.write("\n")
button = st.sidebar.button("Go!")

if openai_api_key:
    llm = load_LLM(openai_api_key=openai_api_key)
    st.markdown("### Here is everything you need for your next Youtube video: ")
    st.write("#### this process may take a few minutes, so please wait...")
    st.write("The AI agent will generate a catchy title first, then it will use the title to generate a thumbnail. \n Next, it will use the title to generate a script... \n and then it will generate a twitter thread from the script. \n")

    #step 2: Generate 10 Catchy Title Ideas
    titles_prompt = pr.youtube_title_generator_prompt.format(topic=user_topic)
    titles = basic_generation(titles_prompt)
    st.write("**Titles Ideas:**")
    st.write("----------------")
    st.write(titles)
    st.write("----------------")

    #step 3: Generate Catchy Thumbnail Ideas
    thumbnail_prompt = pr.youtube_thumbmail_generator_prompt.format(user_titles=titles)
    thumbnails = basic_generation(thumbnail_prompt)
    st.write("**Thumbnail Ideas:**")
    st.write("----------------")
    st.write(thumbnails)
    st.write("----------------")

    #step 4: script
    script_prompt = pr.youtube_script_generator_prompt.format(minutes=user_minutes,topic=user_topic)
    script = basic_generation(script_prompt)
    st.write("**Suggested Script:**")
    st.write("----------------")
    st.write(script)
    st.write("----------------")

    #step 5: Into a twitter thread
    tweet_prompt = pr.tweet_from_youtube_prompt.format(youtube_transcript=script)
    tweet = basic_generation(tweet_prompt)
    st.write("**Twitter Thread:**")
    st.write("----------------")
    st.write(tweet)
    st.write("----------------")

else:
    st.sidebar.write('☝️ Enter Your OpenAI-API-Key and press Go! Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
    st.stop()
