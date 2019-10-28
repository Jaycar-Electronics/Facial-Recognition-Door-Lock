import time
from flask import Flask, jsonify
from multiprocessing import Process, Value

app = Flask(__name__)

@app.route('/names', methods=['POST'])
def get_tasks():
	return jsonify({'tasks': tasks})


def record_loop(loop_on):
	while True:
		if loop_on.value == True:
			print("loop running")
		time.sleep(1)


if __name__ == "__main__":
	recording_on = Value('b', True)
	p = Process(target=record_loop, args=(recording_on,))
	p.start()
	app.run(debug=True, use_reloader=False)
	p.join()
