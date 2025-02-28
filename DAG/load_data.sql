COPY INTO news_data
        FROM @your_snowflake_stage/newsdata.csv
        FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"');