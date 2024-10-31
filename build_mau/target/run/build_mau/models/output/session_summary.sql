
  create or replace   view dev.ANALYTICS.session_summary
  
   as (
    WITH u AS (
    SELECT * FROM dev.ANALYTICS.user_session_channel
), st AS (
    SELECT * FROM dev.ANALYTICS.session_timestamp
)
SELECT u.userId, u.sessionId, u.channel, st.ts
FROM u
JOIN st ON u.sessionId = st.sessionId
  );

