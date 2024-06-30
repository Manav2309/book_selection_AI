import streamlit as st
import pandas as pd
import json
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama

ollama_model = Ollama(model="llama3", temperature=0.02)

try:
    with open('dataset.json', 'r') as f:
        book_data = json.load(f)
except json.JSONDecodeError as e:
    st.error(f"Error reading JSON file: {e}")
    book_data = {}

def get_top_100_books(genre):
    return book_data.get(genre, [])[:100]

def get_top_10_books(books):
    sorted_books = sorted(books, key=lambda x: x.get('Rating', 0), reverse=True)
    top_10_books = sorted_books[:10]
    return top_10_books
template_1 = "give me 'Book titles' and 'Author Names' of 100 different books on {genre} genre."
template_2 = "Give me Book titles, Author Names, Ratings (which must be at least greater than 4 out of 5) on the top 10 books of {genre} genre."
template_details = "Provide genre and other details of the book titled {title}:"

prompt_details = PromptTemplate(input_variables=["title"], template=template_details)
prompt_1 = PromptTemplate(input_variables=["genre"], template=template_1)
prompt_2 = PromptTemplate(input_variables=["genre"], template=template_2)

st.title("Book Recommendation Agent")

if "top_100_books" not in st.session_state:
    st.session_state.top_100_books = []
if "top_10_books" not in st.session_state:
    st.session_state.top_10_books = []
if "selected_genre" not in st.session_state:
    st.session_state.selected_genre = ""
if "selected_genre_1" not in st.session_state:
    st.session_state.selected_genre_1 = ""




genre_1 = st.selectbox("Select a genre:", list(book_data.keys()))
submit_1 = st.button("Get Top 100 Books")
genre = st.text_input("Enter any Genre if it is not given in the box above")
submit = st.button("Generate")

if submit_1 and genre_1:
    st.session_state.top_100_books = get_top_100_books(genre_1)
    st.session_state.selected_genre_1 = genre_1
    st.rerun()

if submit and genre:
    st.session_state.selected_genre=genre
    result_1 = ollama_model.stream(prompt_1.format(genre=genre))
    st.write(result_1)
    result_2 = ollama_model.stream(prompt_2.format(genre=genre))
    st.write(result_2)
    st.stop()
elif submit:
     st.warning("Enter Genre to Generate")       
if st.session_state.top_100_books:
    st.write(f"Top 100 books in {st.session_state.selected_genre_1}:")
    df = pd.DataFrame(st.session_state.top_100_books)
    st.write(df.sample(frac=1))

    st.session_state.top_10_books = get_top_10_books(st.session_state.top_100_books)
    st.write("Top 10 books based on ratings:")
    df = pd.DataFrame(st.session_state.top_10_books)
    st.write(df)

title = st.text_input("Enter the Specific book title of the book you want details for:")
push = st.button("Push")
if push and title:
  response = ollama_model.stream(prompt_details.format(title=title))
  st.write(response)
elif push:
  st.warning("Enter book title to push")
chose=st.button("Choose this book")
if chose and title:
  st.subheader(f"Excellent choice! the book chosen: {title}")  
  st.subheader("Thank you for using the Book Recommendation Agent!")
  st.cache_data.clear()
  st.stop()
elif chose:
  st.warning("write the book title first and then push it to choose")       