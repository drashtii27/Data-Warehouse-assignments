# -*- coding: utf-8 -*-
"""a4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xajgwzoest29OScMoqNx1zbEf1NG8EzT
"""

from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from datetime import datetime

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'retries': 0  # No retries on failure
}

# Define the DAG
with DAG('elt_session_summary_dag',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:

    # SQL for joining tables and removing duplicates
    create_session_summary = SnowflakeOperator(
    task_id='create_session_summary',
    sql="""
        CREATE OR REPLACE TABLE analytics.session_summary AS
        WITH ranked_sessions AS (
            SELECT
                session_channel.userId,
                session_channel.sessionId,
                session_channel.channel,
                timestamp.ts AS event_time,
                ROW_NUMBER() OVER (
                    PARTITION BY session_channel.userId, session_channel.sessionId, session_channel.channel
                    ORDER BY timestamp.ts DESC
                ) AS row_num
            FROM
                raw_data.user_session_channel session_channel
            JOIN
                raw_data.session_timestamp timestamp
            ON
                session_channel.sessionId = timestamp.sessionId
            WHERE
                session_channel.duplicate_flag = 'N'
        )
        SELECT
            userId,
            sessionId,
            channel,
            event_time
        FROM
            ranked_sessions
        WHERE
            row_num = 1;
    """,
    snowflake_conn_id='snowflake_default'
)