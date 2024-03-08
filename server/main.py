from sanic import Sanic
from sanic.request import Request
from sanic.response import text
from sanic.response import json

from sanic_ext import Extend

from utils import action_policy_table_lookup
from utils import mctsHint

from postgres import Postgres

user = ""

password = ""

port = "5432"
server = "localhost"
db = "blackjack"

db = Postgres("postgres://"+user+":"+password+"@"+server+":"+port+"/"+db)

app = Sanic("Blackjack")
app.config.CORS_ORIGINS="*"
Extend(app)

@app.post("/qlearning")
async def qlearning(request):
  game_state = request.json
  action = action_policy_table_lookup(game_state['state'])
  return json({"action":action})

@app.post("/mcts")
async def mcts(request):
  print("Request is",request)
  game_state= request.json
  action = mctsHint(game_state['state'])
  print('action is',action)
  return json({"action":action})

@app.post("/history")
async def write_history(request):
  game_state = str(request.json)
  print("str gamestate is",str(game_state))
  db.run("INSERT INTO history(state) VALUES (%s)",(game_state,))

@app.get("/getHistory")
async def get_history(request):
  res =  db.all("SELECT * FROM history")
  return json(res)

@app.post("/login")  
async def login(request):
  formValues = request.json
  username = formValues['username']
  password = formValues['password']
  print('username and password',username,password)
  userNameExists = db.all("SELECT * FROM gameuser where name=(%s)",(username,))

  print('Hello',userNameExists,len(userNameExists))

  if(len(userNameExists) == 0):
    return json({"res":-1})

  userNamePasswordMatch = db.all('SELECT * FROM gameuser where name=(%s) and password=(%s)',(username,password))

  if(len(userNamePasswordMatch) == 0):
    return json({"res":-2})
  else:
    return json({"res":1})
  

@app.post('/signup')
async def signup(request):
  formValues = request.json
  email = formValues['email']
  username = formValues['username']
  password = formValues['password']
  print("email,username,password",email,username,password)
  db.run("INSERT INTO gameuser(name,password,email) VALUES (%s,%s,%s)",(username,password,email))
  return json({"res":'success'})


if __name__ == "__main__":
    app.run(debug=True,auto_reload=True)

