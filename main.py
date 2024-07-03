from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

fake_db = []

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}

@app.post("/items/")
def create_item(item: dict):
    fake_db.append(item)
    return item

@app.get("/items/")
def read_items():
    return fake_db

@app.put("/items/{item_id}")
def update_item(item_id: int, item: dict):
    for i in range(len(fake_db)):
        if fake_db[i]["item_id"] == item_id:
            fake_db[i] = item
            return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for i in range(len(fake_db)):
        if fake_db[i]["item_id"] == item_id:
            del fake_db[i]
            return {"message": "Item deleted"}

# Lambda handler
handler = Mangum(app)

def lambda_handler(event, context):
    response = handler(event, context)
    return {
        'statusCode': response['statusCode'],
        'body': response['body']
    }
