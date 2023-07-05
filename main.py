from fastapi import FastAPI
from pydantic import BaseModel
from puzzle import Puzzle
import numpy as np
import json
from fastapi.middleware.cors import CORSMiddleware

class Item(BaseModel):
    initial_state: object
    desired_state: object
    method: object

class Item2(BaseModel):
    num : int

app = FastAPI()


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    print("Hello World")
    return {"message": "Hello World"}

@app.post("/")
async def post_to_root(req: Item):
    print(req)
    puzzle = Puzzle(np.array(req.initial_state), np.array(req.desired_state), iterations=2000)
    if req.method['name'] == 'dfs':
        puzzle.dfs()
    elif req.method['name'] == 'bfs':
        puzzle.bfs()
    elif req.method['name'] == 'lim_dfs':
        puzzle.dfs_with_limited_depth(req.method['option'])
    else:
        puzzle.heuristic1()
    puzzle.retrieve()
    # my_dict = dict()
    # my_dict.update({"result":puzzle.path})
    # print(my_dict)

    my_dict = dict()
    my_dict.update({"is_found":puzzle.found})

    if puzzle.found:
        path_list = list(map(lambda x: x['state'].tolist(), puzzle.path))
        my_dict.update({"result":path_list})
        my_dict.update({"time":puzzle.time})

    return my_dict

@app.post("/test")
async def post_to_test(req: Item2):
    print(req)
    return {"num":req.num}