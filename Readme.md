
# FastAPI


FastAPI is a modern, high-performance web framework for building APIs with Python 3.7+ based on standard Python type hints.

## First API 

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```
```

uvicorn filename:app --reload   -> to run the program
```

### Check the Response[](https://realpython.com/fastapi-python-web-apis/#check-the-response "Permanent link")

Open your browser to `http://127.0.0.1:8000`, which will make your browser send a request to your application. It will then send a JSON response with the following:

`{"message": "Hello World"}`



## Path Parameters: Get an Item by ID

```python
# main.py

from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

-the path here is declared by a variable item_id and item_id is passed as an argument to the function


## Request Body: Receiving JSON Data[](https://realpython.com/fastapi-python-web-apis/#request-body-receiving-json-data "Permanent link")

When you need to send data from a client to your API, you send it as a request body.

```python
# main.py

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return item
```

-in this code snippet attributes of Base Model is inherited by the class Item and using the post method we are sending a JSON object and pydantic is used to check if the JSON format matches the format of 'Item'. 
-the same JSON object is returned if it matches the format 


## Building a weather API 

```python
	from fastapi import FastAPI

  

# Define your model

weather_data = {

    "bangalore": {

        "temperature": "28°C",

        "humidity": "65%",

        "condition": "Partly Cloudy"

    },

    "delhi": {

        "temperature": "35°C",

        "humidity": "45%",

        "condition": "Sunny"

    },

    "mumbai": {

        "temperature": "30°C",

        "humidity": "75%",

        "condition": "Humid"

    },

    "chennai": {

        "temperature": "32°C",

        "humidity": "70%",

        "condition": "Hot"

    },

    "kolkata": {

        "temperature": "29°C",

        "humidity": "80%",

        "condition": "Rainy"

    },

    "hyderabad": {

        "temperature": "33°C",

        "humidity": "55%",

        "condition": "Sunny"

    }

}

  

app = FastAPI()

  

@app.get("/weather/{city}")

async def get_weather(city: str):

    city = city.lower()

    if city in weather_data:

        return weather_data[city]

    else:

        return {"error": "City not found"}

  

@app.post("/weather/{city}")

async def update_weather(city: str, data: dict):

    weather_data[city.lower()] = data

    return {"message": "Weather updated", "data": data}
```




# Function calling 

- You can give the model access to your own custom code through **function calling**
- ![[Pasted image 20250702105517.png]]

## function calling steps 

Step 1: Call model with get_weather tool defined

-function is defined under 'tools' and the prompt is passed to the model.
the model responds with a JSON object having the same format as 'tools'

```python
from openai import OpenAI
import json

client = OpenAI()

tools = [{
    "type": "function",
    "name": "get_weather",
    "description": "Get current temperature for provided coordinates in celsius.",
    "parameters": {
        "type": "object",
        "properties": {
            "latitude": {"type": "number"},
            "longitude": {"type": "number"}
        },
        "required": ["latitude", "longitude"],
        "additionalProperties": False
    },
    "strict": True
}]

input_messages = [{"role": "user", "content": "What's the weather like in Paris today?"}]

response = client.responses.create(
    model="gpt-4.1",
    input=input_messages,
    tools=tools,
)
```

Step 2:

response.output

```json
[{
    "type": "function_call",
    "id": "fc_12345xyz",
    "call_id": "call_12345xyz",
    "name": "get_weather",
    "arguments": "{\"latitude\":48.8566,\"longitude\":2.3522}"
}]
```



Step 3: Execute get_weather function

the JSON object is then stored in a variable 'tool_call' and is parsed to get the desired arguments.
this is then passed as parameters to the function and the response is stored in result.

```python
tool_call = response.output[0]
args = json.loads(tool_call.arguments)

result = get_weather(args["latitude"], args["longitude"])
```

Step 4: Supply result and call model again

```python
input_messages.append(tool_call)  # append model's function call message
input_messages.append({                               # append result message
    "type": "function_call_output",
    "call_id": tool_call.call_id,
    "output": str(result)
})

response_2 = client.responses.create(
    model="gpt-4.1",
    input=input_messages,
    tools=tools,
)
print(response_2.output_text)
```
the JSON object and the result is appended to the initial message so that the model has all the required info to generate a final response.



# 🎵 FastAPI + SQLAlchemy: Pagination, Indexing, and DB Commands

## 🔄 Pagination

**What is it?**  
Pagination lets you fetch data in chunks (pages) instead of all at once.

### Typical URL Format
```
GET /songs/?skip=0&limit=10
```

- `skip`: Number of items to skip (offset)
- `limit`: Number of items to return (page size)

### FastAPI Example
```python
@app.get("/songs/")
def get_songs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Song).offset(skip).limit(limit).all()
```

### Paginated JSON Response Example
```json
{
  "total": 100,
  "skip": 0,
  "limit": 10,
  "data": [
    { "id": 1, "title": "Imagine" },
    { "id": 2, "title": "Let It Be" }
  ]
}
```

---

## ⚡ Indexing

**What is it?**  
Indexing improves the performance of database queries, especially search and filtering.

### Add Index in SQLAlchemy
```python
class Song(Base):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)  # indexed column
```

### Optional Custom Index
```python
from sqlalchemy import Index
Index("ix_song_title", Song.title)
```

---

## 🧠 Essential SQLAlchemy DB Commands

| Command        | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `add(obj)`     | Stages a new object to be inserted into the database                        |
| `commit()`     | Commits (writes) all staged changes to the database                         |
| `refresh(obj)` | Reloads the object from the DB, getting updated fields (e.g., auto ID)      |
| `delete(obj)`  | Marks an object for deletion                                                |
| `rollback()`   | Cancels any uncommitted changes (helpful if an error occurs)                |

### Example
```python
new_song = Song(title="Yesterday", artist="The Beatles")
db.add(new_song)         # Stage the object
db.commit()              # Write to DB
db.refresh(new_song)     # Fetch auto-generated ID
print(new_song.id)
```

---

## ✅ Summary

- Use `.add()` to stage data
- Use `.commit()` to write changes
- Use `.refresh()` to get updated fields like `id`
- Use `.delete()` to remove data
- Use `index=True` to speed up filtering
- Use `skip` + `limit` for pagination
