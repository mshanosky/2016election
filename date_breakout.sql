#ALTER TABLE tweets MODIFY tweet_num int(11) AUTO_INCREMENT;
#SET NAMES utf8mb4;
#ALTER DATABASE election CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
#ALTER TABLE tweets CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
#ALTER TABLE tweets CHANGE  text text VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
#SHOW VARIABLES WHERE Variable_name LIKE 'character\_set\_%' OR Variable_name LIKE 'collation%';
#ALTER TABLE tweets ADD COLUMN tweet_num INT AFTER id
#CREATE UNIQUE INDEX tweet_index ON tweets(tweet_num);
#ALTER TABLE tweets MODIFY text VARCHAR(170labels);
#SELECT text FROM election.tweets_a WHERE text LIKE '% immigration %' AND DATE(date) = '2016-09-06'word_cntst10 LIMIT 100;
#SELECT date_format(date, '%Y-%m-%d') as date, count(*) FROM election.tweets_t GROUP BY date_format(date, '%Y-%m-%d');
#SELECT text FROM election.tweets_a WHERE DATE(date) = '2016-09-06' LIMIT 100;
/* SELECT	
	date_format(date, '%Y-%m-%d') as date,
	sum(if (senti_score > 0.1,1,0))   as '1',
    sum(if (senti_score <= 0.1,1,0) and if (senti_score >=  -0.1,1,0)) as '0',	
    sum(if (senti_score < -0.1,1,0))   as '-1',	
	count(*) as 'count'
FROM tweets_a
JOIN users ON tweets_a.usr_id = users.usr_id
where trump=0 AND russian_usr=1 	
GROUP BY date_format(date, '%Y-%m-%d');	
*/
#SELECT	
#    date_format(date, '%Y-%m-%d') as date,
#    sum(if (trump=1,senti_score,0))   as 'trump',
#    sum(if (clinton=1,senti_score,0))   as 'clinton'
#FROM tweets_a	
#GROUP BY date_format(date, '%Y-%m-%d') LIMIT 100;	
/* SELECT		
date_format(date, '%Y-%m-%d') as date,		
sum(if (wc_score > 0,1,0))   as '1',		
    sum(if (wc_score = 0,1,0))   as '0',		
    sum(if (wc_score < 0,1,0))   as '-1',		
count(*) as 'count'		
FROM tweets_a	
JOIN users ON tweets_a.usr_id = users.usr_id
where trump=0 AND current_usr=1 
GROUP BY date_format(date, '%Y-%m-%d');	
*/
SELECT	
	trump,
    sum(if (senti_score > 0.6,1,0))   as '3',
	sum(if (senti_score <= 0.6,1,0) and if (senti_score >  0.3,1,0)) as '2',	
	sum(if (senti_score <= 0.3,1,0) and if (senti_score >  0.1,1,0)) as '1',	
    sum(if (senti_score <= 0.1,1,0) and if (senti_score >=  -0.1,1,0)) as '0',	
	sum(if (senti_score < -0.1,1,0) and if (senti_score >=  -0.3,1,0)) as '-1',	
    sum(if (senti_score < -0.3,1,0) and if (senti_score >=  -0.6,1,0)) as '-3',	
    sum(if (senti_score < -0.6,1,0))   as '-3',	
	count(*) as 'count'
FROM tweets_a
 group by trump
;	

	
