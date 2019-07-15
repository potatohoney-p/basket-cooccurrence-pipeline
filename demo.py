import json
from core import connect,ingest,build_pairs
from features import recommend,coverage
with open('examples/input.json') as stream: data=json.load(stream)
db=connect(':memory:')
try:
    ingest(db,iter(data['events']),2); build_pairs(db)
    print(json.dumps({'coverage':coverage(db),'recommendations':recommend(db,data['customer'])},sort_keys=True))
finally: db.close()
