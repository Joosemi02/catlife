import os

from dotenv import load_dotenv
from motor import motor_tornado

load_dotenv()
client = motor_tornado.MotorClient(os.getenv("MONGODB_URI"))
db: motor_tornado.core.AgnosticDatabase = client["catlife"]
