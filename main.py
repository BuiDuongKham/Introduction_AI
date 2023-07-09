import numpy as np
from fastapi import FastAPI
from othello import Othello
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    # "http://localhost",
    # "http://localhost:3000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
   board: object
   move: object
   turn: int

@app.get("/")
async def root():
    md = dict()
    md.update({"mess": 'Hello World'})
    return md
@app.post("/")
async def post_root(item: Item):
    print(item.board)
    print(item.move)
    board = np.array(item.board)
    othello = Othello(board, depth=4 ,turn=item.turn)
    othello.make_move(item.move[0], item.move[1])
    move = othello.alpha_beta()[1]
    print(move)
    return_dict = dict()
    if move is None:
        return_dict.update({"board": board.tolist()})
        return_dict.update({"possible_moves": othello.get_legal_moves()})
        # return_dict.update({"is_game_over": othello.game_over})
        # return_dict.update({"winner": othello.winner})
        return return_dict
    othello.make_move(move[0], move[1])
    new_board = np.array(othello.board, dtype=int).tolist()
    return_dict.update({"board": new_board})
    return_dict.update({"possible_moves": othello.get_legal_moves()})
    # return_dict.update({"is_game_over": othello.game_over})
    # return_dict.update({"winner": othello.winner})
    # return_dict.update({"move": move})
    return return_dict