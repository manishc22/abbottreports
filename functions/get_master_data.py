import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text, URL
import psycopg2


load_dotenv()


def sql_engine():
    engine = create_engine(
        "postgresql://postgres.menngmczcnnppczwxokk:z8sbaqh10domUZS3@aws-0-us-east-1.pooler.supabase.com:5432/postgres")

    return engine


@st.cache_data(ttl=7200)
def master_view():
    engine = sql_engine()
    
    with engine.begin() as conn:
        sql = text(
            """select * from master_view_new
               """)
        data = pd.read_sql_query(
            sql, conn)
        
        conn.close()
    return data


@st.cache_data(ttl=7200)
def total_count():
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """select count(*) from store_audits
               """)
        data = pd.read_sql_query(
            sql, conn)
        conn.close()
        st.session_state.counter = 0
        st.session_state.win_counter = 0
    return data


@st.cache_data(ttl=7200)
def overview_data():
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """select * from overview_report
               """)
        data = pd.read_sql_query(
            sql, conn)
        conn.close()
    return data


@st.cache_data(ttl=7200)
def audit_data():
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """select * from audit_review
               """)
        data = pd.read_sql_query(
            sql, conn)
        conn.close()
    return data


@st.cache_data(ttl=7200)
def daily_forms():
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """select * from daily_forms
               """)
        data = pd.read_sql_query(
            sql, conn)
        conn.close()
    return data


@st.cache_data(ttl=7200)
def sales_team():
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """select * from sales_team_final
               """)
        data = pd.read_sql_query(
            sql, conn)
        conn.close()
    return data


@st.cache_data(ttl=7200)
def sales_count():
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """select * from sales_count
               """)
        data = pd.read_sql_query(
            sql, conn)
        conn.close()
    return data


@st.cache_data(ttl=7200)
def sales_team_total():
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """select * from sales_team
               """)
        data = pd.read_sql_query(
            sql, conn)
        conn.close()
    return data


@st.cache_data(ttl=7200)
def sales_store_master():
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """select "SalesmanPositionID", "StoreName" from abbott_master_jan
               """)
        data = pd.read_sql_query(
            sql, conn)
        conn.close()
    return data


@st.cache_data(ttl=7200)
def total_sales_visits():
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """select * from total_sales_visits
               """)
        data = pd.read_sql_query(
            sql, conn)
        conn.close()
    return data

@st.cache_data(ttl=7200)
def weekly_forms():
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """WITH weekly_forms as
            (Select "RegionName", created_at, month, DATE_PART('week', created_at)::int as Week
            from store_audits where month = 'Jan')
            select "RegionName", week, count(*)
            from weekly_forms
            group by "RegionName", week
            order by week, "RegionName"
            """)
        data = pd.read_sql_query(
            sql, conn)
        conn.close()
    return data