from flask import request, make_response, jsonify
from flask.views import View
from . import decorators, json_read

def get_projects():
    projects = json_read.get("projects")
    for i in projects:
        yield i, projects.get(i)

class ListAllProjectsView(View):
    methods = ['GET']
    decorators = [decorators.restricted]

    def dispatch_request(self):
        try:
            limit = int(request.args.get("limit"))
        except:
            limit = 10
        
        projects = get_projects()
        response = []
        for i in range(limit):
            try:
                projectname, details = next(projects)
                response.append(
                    {
                        "name": projectname,
                        "details": details
                    }
                )
            except StopIteration:
                break

        return make_response(jsonify(response))