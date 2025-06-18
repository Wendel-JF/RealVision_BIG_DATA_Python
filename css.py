# CSS personalizado com Flexbox
import streamlit as st


def Styles():
    # CSS personalizado com Flexbox
    # background-color: #0D1B2A;
    st.markdown("""
        <style>
        .main {
            display: flex;
            flex-direction: column;
            max-width: 800px;
        }

        .metric-container {
            display: flex;
            width: 100%;
            height: 200px;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 30px;
            background-color: #2d3748;
            margin-bottom: 20px;
        }

         .metric-label {
        font-size: 24px !important;
        font-weight: bold;
        margin-bottom: 4px;
    }
                
         .metric-value {
                font-weight: 100;
                color: #dbdbdb;
        font-size: 26px;
     }

       
                
</style>
""", unsafe_allow_html=True)
