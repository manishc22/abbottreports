import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text, URL
import psycopg2


load_dotenv()


def sql_engine():
    engine = create_engine(
        "postgresql://postgres.menngmczcnnppczwxokk:z8sbaqh10domUZS3@aws-0-us-east-1.pooler.supabase.com:6543/postgres")
    return engine


@st.cache_data(ttl=1800)
def master_view():
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """select * from master_view_new
               """)
        data = pd.read_sql_query(
            sql, conn)
    return data


@st.cache_data(ttl=1800)
def total_count():
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """select count(*) from store_audits
               """)
        data = pd.read_sql_query(
            sql, conn)
    return data


@st.cache_data(ttl=1800)
def overview_data():
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """select * from overview_report
               """)
        data = pd.read_sql_query(
            sql, conn)
    return data


@st.cache_data(ttl=1800)
def audit_data():
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """select * from audit_review
               """)
        data = pd.read_sql_query(
            sql, conn)
    return data


@st.cache_data(ttl=1800)
def daily_forms():
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """select * from daily_forms
               """)
        data = pd.read_sql_query(
            sql, conn)
    return data
