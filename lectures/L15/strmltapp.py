import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

import streamlit as st


st.title("Some app")

@st.cache
def get_df(l):
    return(pd.DataFrame(np.random.normal(loc=l, size=(100,2))))


k = st.slider(label="Mean", min_value=1, max_value=10)

df = get_df(k)
st.line_chart(df[[0,1]])


st.text(str(k))