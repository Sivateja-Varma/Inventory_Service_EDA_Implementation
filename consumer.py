from first_service import Product
from redis_om import get_redis_connection
import time

redis = get_redis_connection(host="localhost",
                             port=6378,
                             decode_responses=True
                             )

key ="order_completed"
group="inventory-group"

try:
  redis.xgroup_create(key,group)
except:
  print("group already exists")  

while True:
  try:
    results = redis.xreadgroup(group,key,{key:'>'},count=1)  
    if results!=[]:
        for result in results:
          print(result)
          obj = result[1][0][1]
          try:
            product = Product.get(obj['product_id'])
            # print(product)
            product.quantity=product.quantity - int(obj['quantity']) 
            product.save()
          except:
            redis.xadd('refund_order',obj,'*')  
  except Exception as e:
    print(str(e))  
  time.sleep(1)  
