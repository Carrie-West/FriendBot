import sqlite3
import re

def initialize():
  con = sqlite3.connect("server.db")
  cur = con.cursor()
  cur.execute("CREATE TABLE IF NOT EXISTS users (id VARCHAR PRIMARY KEY, name VARCHAR, points INTEGER DEFAULT 0)")
  con.close()

def points(user, score, id):
  initialize()
  con = sqlite3.connect("server.db")
  cur = con.cursor()
  #cur.execute("SELECT * FROM users WHERE name=?", (str(user),))
  #print(user,score)
  #results = cur.fetchall()
  #print(results)
  try:
    cur.execute('''INSERT INTO users (id, name, points)VALUES (?,?,?)''', (id, str(user),score))
    con.commit()
  except:
    cur.execute("UPDATE users SET points = points + ?, name = ? WHERE id=?", (score, str(user), id))
    con.commit()
  con.close()

def slap(user, score):
  con = sqlite3.connect("server.db")
  cur = con.cursor()
  user = re.sub("[^0-9.]", "", user);
  print(user)
  try:
    cur.execute("UPDATE users SET points = points + ? WHERE id LIKE ?", (score, user))
  except Exception as err:
    return err   
  con.commit()
  con.close()
def score(user):
  con = sqlite3.connect("server.db")
  cur = con.cursor()
  cur.execute("SELECT points FROM users WHERE id=?", (user,))
  results = cur.fetchall()
  print(results)
  return results[0][0]

def leaderboard():
  con = sqlite3.connect("server.db")
  cur = con.cursor()
  cur.execute("SELECT name, points FROM users ORDER BY points DESC")
  results = cur.fetchall()

  return results