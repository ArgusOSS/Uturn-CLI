from flask import request, jsonify, make_response
from flask.views import View
from git import GitCommandError
from utility import gitutility, exceptions, decorators

class ListAllBranchesView(View):
    methods = ['GET']
    decorators = [decorators.restricted]

    def dispatch_request(self):
        name = request.args.get("name", None)
        if name is None:
            return make_response(jsonify({"error": ["name parameter is required."]}, 500))
        
        try:
            project = gitutility.Project(name)
        except exceptions.ProjectDoesntExistError:
            return make_response(jsonify({"error":["Invalid path/name."]}, 500))
        
        return make_response(
            jsonify(project.all_branches())
        )

class ListCommitsView(View):
    methods = ['GET']
    decorators = [decorators.restricted]

    def dispatch_request(self):
        name = request.args.get("name", None)
        if name is None:
            return make_response(jsonify({"error": ["name parameter is required."]}, 500))
        
        try:
            project = gitutility.Project(name)
        except exceptions.ProjectDoesntExistError:
            return make_response(jsonify({"error":["Invalid path/name."]}, 500))
        
        try:
            limit = int(request.args.get("limit", 10))
        except ValueError:
            return make_response(
                jsonify(
                    {
                        "errors": ["Invalid limit parameter"]
                    }
                ), 500
            )
        
        response = []
        commits = project.commits()
        for i in range(limit):
            try:
                commit = next(commits)
                r = {
                    "msg": commit.msg,
                    "author_name": commit.author.name,
                    "author_email": commit.author.email,
                    "date": commit.committer_date,
                    "hash": commit.hash,
                }
                response.append(r)
            except StopIteration:
                break
        
        return make_response(jsonify(response))


class RollbackToCommitView(View):
    methods = ['GET']
    decorators = [decorators.restricted]

    def dispatch_request(self):
        hash = request.args.get("hash")
        if hash is None:
            return make_response(jsonify({"error": ["hash parameter is required."]}, 500))

        name = request.args.get("name", None)
        if name is None:
            return make_response(jsonify({"error": ["name parameter is required."]}, 500))
        try:
            project = gitutility.Project(name)
        except exceptions.ProjectDoesntExistError:
            return make_response(jsonify({"error":["Invalid path/name."]}, 500))
        
        try:
            project.rollback(hash)
            return make_response(jsonify({"status": "success"}))
            # add better hash validation!
        except GitCommandError:
            return make_response(jsonify({"error": ["Invalid hash"]}, 500))