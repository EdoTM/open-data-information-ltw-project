select p.*, coalesce(sum(v.value), 0) as score, coalesce(v2.value, 0) as userVote
from posts p left join votes v on p.id = v.post
             left join votes v2 on p.id = v2.post and v2.email = 'a@a'
group by p.id