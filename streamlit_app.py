import streamlit as st
from scrape import HEADERS, Tesco

if __name__ == "__main__":

    st.set_page_config(page_title="WhichMart", page_icon="🛒", layout="wide",
                       initial_sidebar_state="collapsed", menu_items=None)

    search = st.text_input(key="search",
                           label="search",
                           label_visibility="visible")

    if not search:
        category = st.selectbox(key="tesco_categories",
                                options=[],
                                index=None,
                                label="tesco categories",
                                label_visibility="visible")
    else:
        tesco = Tesco(HEADERS, search)
        category = st.selectbox(key="tesco_categories",
                                options=tesco.categories.keys(),
                                index=None,
                                label="tesco categories",
                                label_visibility="visible")
        if not category:
            pass
        else:
            products = tesco.standardized_extract(tesco.categories[category])
            st.dataframe(products, hide_index=True, use_container_width=True)
