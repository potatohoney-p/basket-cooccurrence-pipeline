import sqlite3
def connect(path):
    db=sqlite3.connect(path)
    db.execute('CREATE TABLE IF NOT EXISTS baskets (customer TEXT, item TEXT, PRIMARY KEY(customer,item))')
    db.execute('CREATE INDEX IF NOT EXISTS item_index ON baskets(item)')
    return db
def ingest(db,events,batch_size=100):
    if batch_size<1: raise ValueError('Positive batch size required')
    added=0; batch=[]
    def flush(rows):
        before=db.total_changes
        with db: db.executemany('INSERT OR IGNORE INTO baskets VALUES (?,?)',rows)
        return db.total_changes-before
    for event in events:
        customer,item=event
        if not isinstance(customer,str) or not customer or not isinstance(item,str) or not item: raise ValueError('Nonempty customer and item required')
        batch.append((customer,item))
        if len(batch)>=batch_size: added+=flush(batch); batch=[]
    if batch: added+=flush(batch)
    return added
def build_pairs(db):
    with db:
        db.execute('CREATE TABLE IF NOT EXISTS pairs (left_item TEXT, right_item TEXT, support INTEGER, PRIMARY KEY(left_item,right_item))')
        db.execute('DELETE FROM pairs')
        db.execute('INSERT INTO pairs SELECT a.item,b.item,COUNT(*) FROM baskets a JOIN baskets b ON a.customer=b.customer AND a.item<b.item GROUP BY a.item,b.item')
    return db.execute('SELECT COUNT(*) FROM pairs').fetchone()[0]
