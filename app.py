import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import pickle
from dotenv import load_dotenv
import os
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback



#Sidebar

with st.sidebar:
    st.title('YMGK PROJE')
    st.markdown('''
    ## Hakkında
    Bu uygulama LLM kullanarak aşağıdaki uygulamalar ile yazılmıştır.
    - [Streamlit](https://streamlit.io/)
    - [Langchain](https://python.langchain.com/en/latest/index.html)
    - [OpenAi](https://openai.com/)

    ''')

    add_vertical_space(5)
    st.write('16541021 G. Efe Kaplan')


    def main():
        st.header("PDF ile konuş")
        #Upload pdf 
        pdf= st.file_uploader("PDF yükleyin",type='pdf')

        load_dotenv()

        if pdf is not None:
            pdf_reader=PdfReader(pdf)
            #st.write(pdf_reader)

            text=""
            for page in pdf_reader.pages:
                text += page.extract_text()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            chunks=text_splitter.split_text(text=text)


            #embedding

            store_name = pdf.name[:-4]

            if os.path.exists(f"{store_name}.pkl"):
                with open(f"{store_name}.pkl", "wb") as f:
                    VectorStore = pickle.load(f)
            else:
                embeddings = OpenAIEmbeddings()
                VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
                with open(f"{store_name}.pkl", "wb") as f:
                    pickle.dump(VectorStore, f)

            #Accept questions

            query= st.text_input('Yüklediğiniz belgeye sorular sorun:')

            st.write(query)

            if query:
                docs = VectorStore.similarity_search(query=query)
                
                llm = OpenAI(temperature=0)
                chain= load_qa_chain(llm=llm,chain_type="stuff")

                with get_openai_callback() as cb:

                    response = chain.run(input_documents=docs, question=query)
                    print(cb)


if __name__ == '__main__':
    main()