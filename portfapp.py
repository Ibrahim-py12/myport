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

pr2 = st.Page(
    page="todo.py",
    title="TO-DO",


)

pg = st.navigation(pages=[about_page,pr1,pr2])

pg.run()





#            streamlit run portfapp.py