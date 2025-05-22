from fastapi import FastAPI
import uvicorn 
from pydantic import BaseModel

app = FastAPI() 

@app.get("/")
def sayJoke():
    return {"joke": "How many programmers does it take to screw in one light bulb? Not a single one. In this case, the lack of light is a problem on the iron side."}

@app.get("/{friend}")
def friendSayJoke(friend: str):
    return {"friend" : friend,
            "joke": f"{friend} said: The team requires a python developer, a baby elephant tester, and a team leader monkey."}

jokes = ["Before deleting files, make sure that they are not yours.", "If you start flicking a fly off the monitor using the mouse cursor, it's time to turn off the computer.", "Did the program turn out badly, but the deadlines are on fire, and the customer is swearing? Don't worry, feel free to release the release. Just call it version 1.0.", "do you know the main advantages of IT solutions? Of course, this is arrogance, intolerance and incredible laziness."]

@app.get("/multi/{friend}")
def multiFriendJoke(friend: str, count: int):
    result = ""
    for i in range(count):
        result += f"{friend} said joke number {i}: {jokes[i%len(jokes)]}, "
    return {"friend": friend,
            "jokes": result}

class Joke(BaseModel):
    friend: str
    joke: str

class JokeInput(BaseModel):
    friend:str

@app.post("/", response_model = Joke)
def newJoke(joke_input: JokeInput):
    """Create new joke"""
    return {"friend": joke_input.friend,
            "joke" : joke_input.friend + " tells new joke: " + " — The program is based on the python library blivet. Python rules!!! — Not python, but python, read wikipedia. — Not python, but python, don't read wikipedia. "}

if __name__ == '__main__':
    uvicorn.run(
        "app:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True)