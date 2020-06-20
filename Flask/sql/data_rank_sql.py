def query_video():
    return 'select * from bili_video WHERE DATEDIFF(now(),last_update)=1'

def insert_video_rank():
    return 'INSERT INTO bili_video_rank(video_id,rank,section,uploader_id,create_time)values(%s,%s,%s,%s,now())'

def query_uploader():
    return 'select * from bili_uploader WHERE DATEDIFF(NOW(),last_update)=1'

def query_uploader_video_score(mid):
    return 'select AVG(rank) as video_score from (select rank from bili_video_rank WHERE bili_video_rank.uploader_id = '+str(mid)+' ORDER BY create_time DESC limit 100000) as result LIMIT 0,7'

def insert_uploader_rank():
    return 'INSERT INTO bili_uploader_rank(uploader_id,score,section,create_time)values(%s,%s,%s,now())'

def query_uploader_video_section(mid):
    return 'select tname as name,count(*) as value from (SELECT tname from bili_video WHERE author_mid ='+str(mid)+' GROUP BY video_id) as result GROUP BY tname ORDER By value Desc'