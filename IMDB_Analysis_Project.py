
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="IMDB Movie Analysis", layout="wide")

# 2. Read CSV and assign to dataframe 'df'
df = pd.read_csv("Cleaned_df.csv",index_col=0) 

# 3. Dashboard Header
st.title("IMDB Movie Analysis Dashboard")
st.markdown("Explore insights from top IMDB movies, analyzing revenue, runtimes, and ratings.")
st.markdown("---")

# 4. Create Tabs for Organization 
tab1, tab2, tab3, tab4 = st.tabs(["Data Overview", "Univariate Analysis", "Bivariate Analysis", "Multivariate Analysis"])

# --- TAB 1: Data Overview ---
with tab1:
    st.subheader("Dataset Preview")
    st.dataframe(df.head(15), use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Movies", len(df))
    with col2:
        st.metric("Total Directors", df['Director'].nunique())
    with col3:
        st.metric("Unique Certificates", df['Certificate'].nunique())

# --- TAB 2: Univariate Analysis ---
with tab2:
    st.subheader("Univariate Analysis")
    st.markdown("Select any column from the dataset to view its distribution.")
    
    # Selectbox for a cleaner UI
    selected_col = st.selectbox("Choose a column to analyze:", df.columns)
    
    # Generate histogram for selected column
    fig_uni = px.histogram(
        df, 
        x=selected_col, 
        title=f'Distribution of {selected_col}',
        color_discrete_sequence=['#636EFA']
    )
    st.plotly_chart(fig_uni, use_container_width=True)

# --- TAB 3: Bivariate Analysis ---
with tab3:
    st.subheader("Bivariate Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # fig1: Average Runtime for top 10 Directors
        avg_runtime_director = df.groupby('Director')['Runtime'].mean().sort_values(ascending=False).reset_index().head(10)
        
        fig1 = px.bar(
            avg_runtime_director,
            x='Director',
            y='Runtime',
            title='Top 10 Directors by Average Runtime (Minutes)',
            text_auto='.1f',
            labels={'Runtime': 'Average Runtime (mins)'},
            color='Runtime',
            color_continuous_scale='Viridis'
        )
        fig1.update_traces(textposition='outside')
        st.plotly_chart(fig1, use_container_width=True)
        
    with col2:
        # fig2: Top 10 Years by Total Gross Revenue
        top_years_gross = df.groupby('Released_Year')['Gross'].sum().sort_values(ascending=False).reset_index().head(10)
        
        fig2 = px.bar(
            top_years_gross,
            x='Released_Year',
            y='Gross',
            title='Top 10 Years by Total Gross Revenue',
            text_auto='.2s',
            labels={'Released_Year': 'Released Year', 'Gross': 'Total Gross Revenue'},
            color='Gross',
            color_continuous_scale='Blues'
        )
        fig2.update_traces(textposition='outside')
        fig2.update_layout(xaxis_type='category')
        st.plotly_chart(fig2, use_container_width=True)
        
    st.markdown("---")
    
    # fig3: Top 5 Directors with highest number of votes in 2000s
    top_5_directors_2000 = df[df['Released_Year'] >= 2000]
    top_5_directors_2000 = top_5_directors_2000.groupby('Director')['No_of_Votes'].sum().sort_values(ascending=False).reset_index().head(5)
    
    fig3 = px.bar(
        top_5_directors_2000,
        x='Director',
        y='No_of_Votes',
        title='Top 5 Directors by Total Number of Votes (2000 - 2020)',
        text_auto='.2s',
        labels={'No_of_Votes': 'Total Number of Votes'},
        color='No_of_Votes',
        color_continuous_scale='Magma'
    )
    fig3.update_traces(textposition='outside')
    st.plotly_chart(fig3, use_container_width=True)

# --- TAB 4: Multivariate Analysis ---
with tab4:
    st.subheader("Multivariate Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # fig4: Average Gross by Certificate (based on IMDB Rating)
        cert_stats = df.groupby('Certificate')[['Gross', 'IMDB_Rating']].mean().sort_values(by='Gross', ascending=False).reset_index()
        
        fig4 = px.bar(
            cert_stats,
            x='Certificate',
            y='Gross',
            color='IMDB_Rating',
            title='Average Gross by Certificate (based on IMDB Rating)',
            text_auto='.2s',
            color_continuous_scale='Blues'
        )
        fig4.update_traces(textposition='outside')
        st.plotly_chart(fig4, use_container_width=True)

    with col2:
        # fig5: Top 10 Highest Grossing Movies (2000 - 2020)
        df_filtered = df[df['Released_Year'] >= 2000][['Series_Title', 'Released_Year', 'Gross']]
        df_filtered = df_filtered.sort_values(by='Gross', ascending=False).head(10)
        
        fig5 = px.bar(
            df_filtered,
            x='Series_Title',
            y='Gross',
            title='Top 10 Highest Grossing Movies (2000 - 2020)',
            text_auto='.2s',
            labels={'Gross': 'Gross Revenue', 'Series_Title': 'Movie Title'},
            color='Released_Year',
            color_continuous_scale='Sunset'
        )
        fig5.update_traces(textposition='outside')
        fig5.update_xaxes(tickangle=45)
        st.plotly_chart(fig5, use_container_width=True)
