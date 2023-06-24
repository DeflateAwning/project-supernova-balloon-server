from flask import Flask, request, jsonify, render_template
import firebirdsql

from . import secrets

app = Flask(__name__)

# create db connection
conn = firebirdsql.connect(
	database=secrets.db_database,
	user=secrets.db_user,
	password=secrets.db_password,
	host=secrets.db_host,
	port=secrets.db_port,
)

# Endpoint to receive and store the helium packet
@app.route('/api/v1/receive_helium_packet', methods=['POST'])
def receive_helium_packet():
	...

# Route to display packet metadata
@app.route('/')
def packet_metadata():
	
	cursor = conn.cursor()

	# Fetch the packet metadata from the "incoming_packets" table
	query = "SELECT id, app_eui, dev_eui FROM incoming_packets"
	cursor.execute(query)
	packets = cursor.fetchall()

	# Close the database connection
	cursor.close()
	conn.close()

	return render_template('index.html', packets=packets)

if __name__ == '__main__':
	app.run()
