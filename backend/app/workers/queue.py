import redis
from rq import Queue, Worker
from app.core.config import settings

# Initialize Redis connection
redis_conn = redis.from_url(settings.REDIS_URL)

# Redis RQ Task Queue
task_queue = Queue("sheetpilot", connection=redis_conn)

def start_worker():
    """
    Launches the RQ Background Worker listener.
    """
    print("⚡ Starting SheetPilot RQ Background Worker...")
    worker = Worker([task_queue], connection=redis_conn)
    worker.work()

if __name__ == "__main__":
    start_worker()
