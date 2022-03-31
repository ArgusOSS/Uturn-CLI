from flask import Flask, jsonify, make_response
from utility.decorators import restricted
from utility import ip, gitendpoints, projectendpoints
import platform
import sys

app = Flask(__name__)

@app.route('/')
def home():
    return ""

@app.route('/health')
def ping():
    return make_response(jsonify({"status": "up"}))

@app.route('/verifyconnection')
@restricted
def initconnection():
    OS = platform.platform()
    IP = ip
    json_to_send = {
        "OS": OS,
        "IP": IP
    }
    return make_response(jsonify(json_to_send))

app.add_url_rule('/branches', view_func=gitendpoints.ListAllBranchesView.as_view('branches'))
app.add_url_rule('/commits', view_func=gitendpoints.ListCommitsView.as_view('commits'))
app.add_url_rule('/rollback', view_func=gitendpoints.RollbackToCommitView.as_view('rollback'))
app.add_url_rule('/projects', view_func=projectendpoints.ListAllProjectsView.as_view('projects'))

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8001
    try:
        host = sys.argv[1]
        port = sys.argv[2]
    except:
        pass
    app.run(host=host, port=port)
