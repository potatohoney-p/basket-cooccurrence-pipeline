def recommend(db,customer,limit=5,min_support=1):
    if limit<0 or min_support<1: raise ValueError('Invalid query limits')
    scores={}
    owned=set(r[0] for r in db.execute('SELECT item FROM baskets WHERE customer=?',(customer,)))
    for item in owned:
        for left,right,support in db.execute('SELECT left_item,right_item,support FROM pairs WHERE (left_item=? OR right_item=?) AND support>=?',(item,item,min_support)):
            candidate=right if left==item else left
            if candidate not in owned: scores[candidate]=scores.get(candidate,0)+support
    return sorted(scores.items(),key=lambda p:(-p[1],p[0]))[:limit]
def coverage(db):
    customers=db.execute('SELECT COUNT(DISTINCT customer) FROM baskets').fetchone()[0]
    items=db.execute('SELECT COUNT(DISTINCT item) FROM baskets').fetchone()[0]
    return {'customers':customers,'items':items,'events':db.execute('SELECT COUNT(*) FROM baskets').fetchone()[0]}
