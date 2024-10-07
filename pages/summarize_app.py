# CORE PACKAGES
import streamlit as st

# ADDITIONAL PACKAGES / SUMMARIZATION PACKAGES
from transformers import pipeline

# LexRak Algorithm
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import nltk
import os

# EDA Packages
import pandas as pd

# Data Visualization
import matplotlib.pyplot as plt
import matplotlib
import altair as alt
matplotlib.use('Agg') #Tkagg #Backend

# Carregar o pipeline de sumarização
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


# Caminho para a pasta do ambiente virtual 
venv_path = os.path.join(os.getcwd(), '.venv', 'nltk_data')


# Crie a pasta 'nltk_data' dentro do venv, se não existir
if not os.path.exists(venv_path):
    os.makedirs(venv_path)


# Defina o caminho para o NLTK
nltk.data.path.append(venv_path)


# Baixe o pacote 'punkt' para o diretório dentro do venv
nltk.download('punkt_tab', download_dir=venv_path)
nltk.download('punkt', download_dir=venv_path)


def sumy_summarizer(paragraph, sentences_count=2):
    parser = PlaintextParser.from_string(paragraph, Tokenizer("english"))

    summarizer = LsaSummarizer(Stemmer("english"))
    summarizer.stop_words = get_stop_words("english")

    summary = summarizer(parser.document, sentences_count)
    return summary

# Evaluate Summary
from rouge import Rouge

def evaluate_summary(summary, reference):
    r = Rouge()
    eval_score = r.get_scores(summary, reference)
    eval_score_df = pd.DataFrame(eval_score[0])
    return eval_score_df

def main():
    st.title("Summarize App")
    menu = ['Home','About']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == "Home":
        st.subheader("Summarization")
        raw_text = st.text_area("Enter Text Here")

        if st.button("Summarize"):
            with st.expander("Original Text"):
                st.write(raw_text)
            
            # Layout
            c1, c2 = st.columns(2)

            with c1:
                with st.expander("LexRank Summary"):
                    my_summary = sumy_summarizer(raw_text)
                    extracted_text = [str(sentence) for sentence in my_summary]
                    full_text = ' '.join(extracted_text)
                    document_len = {"Original": len(raw_text), "Summary":len(full_text)}

                    st.write(document_len)
                    st.write(full_text)
                    st.info("Rouge Score")
                    eval_df = evaluate_summary(full_text, raw_text)

                    st.dataframe(eval_df.T)
                    eval_df['metrics'] = eval_df.index
                    c = alt.Chart(eval_df).mark_bar().encode(x='metrics', y = 'rouge-1')
                    st.altair_chart(c)

            with c2:
                with st.expander("TextRank Summary"):
                    my_summary = summarizer(raw_text, max_length=130, min_length=30, do_sample=False)
                    full_text = my_summary[0]["summary_text"]
                    document_len = {"Original": len(raw_text), "Summary":len(full_text)}

                    st.write(document_len)
                    st.write(full_text)
                    st.info("Rouge Score")
                    eval_df = evaluate_summary(full_text, raw_text)
                    
                    st.dataframe(eval_df.T)
                    eval_df['metrics'] = eval_df.index
                    c = alt.Chart(eval_df).mark_bar().encode(x='metrics', y = 'rouge-1')
                    st.altair_chart(c)
    else:
        st.subheader("About")


if __name__ == '__main__':
    main()
