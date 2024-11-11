from rq import Queue
from redis import Redis

redis_conn = Redis(host="localhost", port=6379)
queue = Queue(connection=redis_conn)
