import json

import requests

import gitlab

import base64

from ast import literal_eval

class AuthenticateWithGitlab(object):
	"""docstring for AuthenticateWithGitlab"""
	def __init__(self, token):
		super(AuthenticateWithGitlab, self).__init__()
		self.token = token

	def call(self):
		gl = gitlab.Gitlab('https://gitlab.com', self.token)
		gl.auth()
		return gl

class GetIssueInformation(object):
	"""docstring for GetIssueInformation"""
	def __init__(self, issue, gl, project_name, team):
		super(GetIssueInformation, self).__init__()
		self.issue = issue
		self.gl = gl
		self.project_name = project_name
		self.team = team

	def call(self):
		#get project
		project = self.gl.projects.get(self.team+'/'+self.project_name)

		#get issue
		issue_list = project.issues.list()

		processed_issues = []

		for single_issue in issue_list:
			processed_issues.append({'url':single_issue.web_url, 'title':single_issue.title, 'number':single_issue.iid})

		return processed_issues

class CreateIssue(object):
	"""docstring for CreateIssue"""
	def __init__(self, gl, team, project, issue_title, issue_description):
		super(CreateIssue, self).__init__()
		self.gl = gl
		self.team = team
		self.project = project
		self.issue_title = issue_title
		self.issue_description = issue_description

	def call(self):
		project_list = self.gl.projects.get(self.team+'/'+self.project)

		issue = project_list.issues.create({'title': self.issue_title, 'description': self.issue_description})

		try:
			return issue.iid
		except (RuntimeError, TypeError, NameError, ValueError):
			return 'error'
		return
		
class FetchIssueTemplates(object):
	"""docstring for FetchIssueTemplates"""
	def __init__(self, token, team, project):
		super(FetchIssueTemplates, self).__init__()
		self.token = token
		self.team = team
		self.project = project

	def call(self):
		auth = AuthenticateWithGitlab(self.token)
		gl = auth.call()
		project = gl.projects.get(self.team+'/'+self.project)
		files = project.repository_tree(path='.gitlab/issue_templates/', ref='master')
		file_map=[]
		for d in files:
			file_info = project.repository_blob(d['id'])
			file_map.append({'name' : d['name'], 'content' : base64.b64decode(file_info['content']).decode("utf-8")})
		return file_map
		