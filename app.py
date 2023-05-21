import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space

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


if __name__ == '__main__':
    main()