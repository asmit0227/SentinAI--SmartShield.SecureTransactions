import time
from src.redis import redis_client

VELOCITY_TIME =300 #5MINUTES

def record_transaction_velocity(
        card_id=str,
        transaction_id=str
):
     current_time=time.time()
    
     key=f"velocity:{card_id}"
    
     latest_time_velocity = (current_time-VELOCITY_TIME)

     pipe=redis_client.pipeline()

     pipe.zremrangebyscore(
          key,
          0,
          latest_time_velocity
     )

     pipe.zadd(
          key,
          {transaction_id : current_time}
     )

     pipe.zcard(key)

     pipe.expire(
          key,
          VELOCITY_TIME*2
     )

     results=pipe.execute()
     transaction_count=results[2]
     return transaction_count

