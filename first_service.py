from fastapi import FastAPI
from redis_om import get_redis_connection,HashModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:5173",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Product(HashModel,index=True):
  name:str
  price:float
  quantity:int

redis = get_redis_connection(
  host="localhost",
  port=6379,
  decode_responses=True
)


@app.get("/")
def Home():
  return  [format(pk) for pk in Product.all_pks()]

def format(pk:str):
  product= Product.get(pk)
  return {
    'id':product.pk,
    'name':product.name,
    'price':product.price,
    'quantity':product.quantity
  }
@app.post("/products")
def Create(product:Product):
  return product.save()

@app.get("/product/{pk}")
def getProduct(pk:str):
  return Product.get(pk)

@app.delete("/products/{pk}")
def Delete(pk:str):
  return Product.delete(pk)