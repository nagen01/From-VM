from neomodel import config
config.DATABASE_URL = 'bolt://neo4j:neo4j@localhost:7687'
from neomodel import db
db.set_connection('bolt://neo4j:neo4j@localhost:7687')

