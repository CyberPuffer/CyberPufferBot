from utils import log, config
import sqlite3

logger = log.get_logger(name = 'Database')

def init_con(db_file):
	con = None
	con = sqlite3.connect(db_file)
	return con

def check_database():
	con = init_con(config.database_path)
	cur = con.cursor()
	cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users'")
	if (cur.fetchone()[0] == 0):
		logger.warning('Default table not exists, now initializing...',)
		cur.execute("CREATE TABLE users (id INT, role INT, status INT)")
		con.commit()
		con.close()
	else:
		pass

def init_user(user_id):
	con = init_con(config.database_path)
	cur = con.cursor()
	cur.execute("INSERT INTO users VALUES ({user_id}, 0, 0 )".format(user_id = user_id))
	con.commit()
	con.close()

def query(user_id, attrib):
	con = init_con(config.database_path)
	cur = con.cursor()
	result = cur.execute("SELECT {attrib} FROM users WHERE id = {user_id}".format(attrib=attrib, user_id=user_id)).fetchone()
	if result == None:
		init_user(user_id)
		logger.info("New user found: {user_id}".format(user_id = user_id))
		return None
	con.commit()
	con.close()
	return result[0]

def update(user_id, attrib, value):
	con = init_con(config.database_path)
	cur = con.cursor()
	cur.execute("UPDATE users SET {attrib} = {value} WHERE id = {user_id}".format(attrib=attrib, value=value, user_id=user_id))
	con.commit()
	con.close()

def stats(table):
	con = init_con(config.database_path)
	cur = con.cursor()
	num = cur.execute("SELECT COUNT(id) FROM {table}".format(table=table)).fetchone()[0]
	con.commit()
	con.close()
	return num