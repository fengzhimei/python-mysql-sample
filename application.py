import os
import flask
import MySQLdb

from qiniu import Auth
from qiniu import put_file

import qiniu.config

application = flask.Flask(__name__)
application.debug = True

@application.route('/')
def hello_world():
  return "Hello world Madai!"

@application.route('/env')
def env():
  envs = "Environments: <br>"
  for key in os.environ.keys():
    envs = envs + "%s: %s<br>" % (key,os.environ[key])

  return envs

@application.route('/score')
def score():
  storage = Storage()
  storage.populate()
  score = storage.score()
  return "Hello world, %d!" % score

@application.route('/upload')
def upload():
  access_key = 'RzW0eOSQyuGSqqxAC_RBsyIO3E6q1yi0QhyH033i'
  secret_key = 'EaVes45LAJKd3qzYOn06VTto3f4e8HsFAjwpAQsW'
  bucket_name = 'gftest'
  localfile = '/usr/src/app/a.pptx'
  key = 'test_file'
  mime_type = "text/plain"
  params = {'x:a': 'a'}
  q = Auth(access_key, secret_key)

  token = q.upload_token(bucket_name, key)

  ret, info = put_file(token, key, localfile, mime_type=mime_type, check_crc=True)
  print(info)
  return info

class Storage():
  def __init__(self):
    self.db = MySQLdb.connect(
      user   = os.getenv('MYSQL_USERNAME'),
      passwd = os.getenv('MYSQL_PASSWORD'),
      db     = os.getenv('MYSQL_INSTANCE_NAME'),
      host   = os.getenv('MYSQL_PORT_3306_TCP_ADDR'),
      port   = int(os.getenv('MYSQL_PORT_3306_TCP_PORT'))
    )

    cur = self.db.cursor()
    cur.execute("DROP TABLE IF EXISTS scores")
    cur.execute("CREATE TABLE scores(score INT)")

  def populate(self):
    cur = self.db.cursor()
    sql = "INSERT INTO scores(score) VALUES(1234)"

    try:
      # execute SQL inside a transaction
      cur.execute(sql)
      self.db.commit()
    except:
      # rollback if neccessary
      self.db.rollback()

  def score(self):
    cur = self.db.cursor()
    cur.execute("SELECT * FROM scores")
    row = cur.fetchone()
    return row[0]

if __name__ == "__main__":
  application.run(host='0.0.0.0', port=3000)
