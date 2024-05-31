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
            """select * from master_view_new where month not in ('Nov','Dec','Jan','Feb','Mar', 'Apr') order by created_at desc
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


def weekly_data(month):
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """select * from weekly_performance
               where month = :month
               """)
        data = pd.read_sql_query(
            sql, conn, params={"month": month})
    return data


def kyc_total_data():
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """select count(distinct customer_code)
               from kyc_audits
               """)
        data = pd.read_sql_query(
            sql, conn)
    return data


@st.cache_data(ttl=20000)
def kyc_master_data():
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """select "RegionName", "ProgramName", count(distinct "CustomerCode") from kyc_master group by "RegionName", "ProgramName" """)
        data = pd.read_sql_query(sql, conn)
        return data


def kyc_regional_data():
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """select "RegionName", program_name, count(distinct customer_code) from kyc_audits group by "RegionName", program_name  """)
        data = pd.read_sql_query(sql, conn)
        return data


@st.cache_data(ttl=7200)
def kyc_daily_forms():
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """select * from kyc_daily_forms
               """)
        data = pd.read_sql_query(
            sql, conn)
        conn.close()
    return data


@st.cache_data(ttl=7200)
def kyc_master():
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """select * from kyc_master_status
               """)
        data = pd.read_sql_query(
            sql, conn)
        conn.close()
    return data


@st.cache_data(ttl=20000)
def tse_exception():
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """with tse_exceptions as
(select distinct "RegionName", "TSEId", count(*) as "Remaining Stores", 
(select count(distinct("StoreName")) from kyc_master where kyc_master."TSEId" = k."TSEId") as "Total Stores" 
from kyc_master_status k
where "KYC Status" is null group by "RegionName", "TSEId")
select "RegionName", "TSEId", "Remaining Stores", "Total Stores", TRUNC(("Remaining Stores" * 100 / "Total Stores"),1) as "% Remaining" from tse_exceptions 
where "Total Stores" <> 0
and TRUNC(("Remaining Stores" * 100 / "Total Stores"),1) >= 20
order by TRUNC(("Remaining Stores" * 100 / "Total Stores"),1) desc

               """)
        data = pd.read_sql_query(
            sql, conn)
        conn.close()
    return data


@st.cache_data(ttl=20000)
def zero_isr():
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """select * from zero_isr where "ISRPositionID" is not null
               """)
        data = pd.read_sql_query(
            sql, conn)
        conn.close()
    return data
