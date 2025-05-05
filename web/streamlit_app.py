import streamlit as st

main_page = st.Page("main.py", title="Главная"
# , icon=":material/add_circle:"
)
service_page = st.Page("service.py", title="Сервис"
# , icon=":material/delete:"
)

pg = st.navigation(
    {
            "Main": [main_page, service_page],
            # "Reports": []
        }
)
st.set_page_config(page_title="Mimika AI"
# , page_icon=":material/edit:"
)
pg.run()




