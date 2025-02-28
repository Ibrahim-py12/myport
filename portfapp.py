import streamlit as st
from matplotlib.pyplot import title

about_page = st.Page(

    page = "aboutme.py",
    title = "About me",
    default = True,

)
pr1 = st.Page(
    page = "webscrap.py",
    title = "Automated WecScrapper",

)
#
# pr2 = st.Page(
#     page="mathgesai.py",
#     title="Math Gesture AI"
#
#
# )

pg = st.navigation(pages=[about_page,pr1])

pg.run()





#            streamlit run portfapp.py