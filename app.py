import streamlit as st
import pandas as pd

st.set_page_config(page_title="SQL Connection Test", layout="wide")

st.title("🧬 Public Database Test: Rfam")
st.markdown("Testing secure SQL connections via `st.connection` using a public MySQL database hosted by the European Bioinformatics Institute.")

# Initialize the connection looking for the [connections.rfam_db] block in secrets.toml
try:
    conn = st.connection('rfam_db', type='sql')
    st.success("Successfully connected to the database server!")
except Exception as e:
    st.error(f"Failed to connect: {e}")
    st.stop()

# Query the database
# We are querying the 'family' table, which lists RNA families
@st.cache_data(ttl=3600)
def fetch_data():
    # Write standard SQL here
    query = """
    SELECT rfam_acc, rfam_id, description, author, number_of_species
    FROM family 
    ORDER BY number_of_species DESC 
    LIMIT 100;
    """
    # conn.query returns a Pandas DataFrame automatically
    return conn.query(query)

with st.spinner("Executing SQL query..."):
    df = fetch_data()

st.subheader("Top 100 RNA Families by Species Count")
st.dataframe(df, use_container_width=True, hide_index=True)
