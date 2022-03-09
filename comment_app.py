from datetime import datetime
import pandas as pd
from sklearn import utils
import streamlit as st
import db
#from utils import db

COMMENT_TEMPLATE_MD = """{} - {}
> {}"""


def space(num_lines=1):
    """Adds empty lines to the Streamlit app."""
    for _ in range(num_lines):
        st.write("")


# Title
st.title("💬 Commenting Application")



# Comments part

conn = db.connector()

query = "Select * from comments;"
result_dataFrame = pd.read_sql(query,conn)
comments = result_dataFrame

with st.expander("💬 Open comments"):

    # Show comments

    st.write("**Comments:**")

    for index, entry in enumerate(comments.itertuples()):
        st.markdown(COMMENT_TEMPLATE_MD.format(entry.name, entry.date, entry.comment))

        is_last = index == len(comments) - 1
        is_new = "just_posted" in st.session_state and is_last
        if is_new:
            st.success("☝️ Your comment was successfully posted.")

    space(2)

    # Insert comment

    st.write("**Add your own comment:**")
    form = st.form("comment")
    name = form.text_input("Name")
    comment = form.text_area("Comment")
    submit = form.form_submit_button("Add comment")

    if submit:
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        mysql_query = "INSERT INTO comments (name,comment,date)  VALUES ('"+ name +"','"+ comment +"','"+ date +"') "                  
                          
        mycursor = conn.cursor()
        result = mycursor.execute(mysql_query)
        conn.commit()
        if "just_posted" not in st.session_state:
            st.session_state["just_posted"] = True
        st.experimental_rerun()