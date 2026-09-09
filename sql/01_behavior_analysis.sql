-- 1. 用户行为漏斗分析
SELECT
    behavior_type,
    COUNT(*) AS behavior_count
FROM user_behavior
GROUP BY behavior_type
ORDER BY behavior_count DESC;


-- 2. 高频购买用户Top10
SELECT
    user_id,
    COUNT(*) AS buy_count
FROM user_behavior
WHERE behavior_type='buy'
GROUP BY user_id
ORDER BY buy_count DESC
LIMIT 10;