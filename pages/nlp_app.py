# CORE PACKAGES
import streamlit as st

# ADDITIONAL PACKAGES


# FUNCTIONS



def main():
    st.title("NLP Application with Streamlit 🎈")
    menu = ['Home','NLP (Files)', 'About']

    choice = st.sidebar.selectbox("Menu", menu)
    if choice =="Home":
        st.subheader("Home: Analyze text")
        raw_text = st.text_area("Enter text here")
        num_of_most_common = st.sidebar.number_input("Most common tokens",5,15)
        
        if st.button("Analyze"):
            with st.expander("Original text"):
                st.write(raw_text)
            
            with st.expander("Text Analysis"):
                st.write(raw_text)
            
            with st.expander("Entities"):
                st.write(raw_text)

            # COLUMNS
            col1, col2 = st.columns(2)

            with col1:
                with st.expander("Word stats"):
                    pass
                
                with st.expander("Top Keywords"):
                    pass
                    
                with st.expander("Sentiment"):
                    pass
            
            with col1:
                with st.expander("Plot word frequency"):
                    pass
                
                with st.expander("Plot part of speech"):
                    pass
                    
                with st.expander("Plot worldcloud"):
                    pass

    elif choice=="NLP (files)":
        st.subheader("NLP tasks")
    else:
        st.subheader("About")


if __name__ == '__main__':
    main()