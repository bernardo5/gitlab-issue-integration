from flask import Flask, render_template, request, make_response, redirect, abort

from wtforms import Form, TextField, validators, SubmitField, TextAreaField

from services import AuthenticateWithGitlab, GetIssueInformation, CreateIssue, FetchIssueTemplates

import os

from os.path import join, dirname

from dotenv import load_dotenv
 
app=Flask(__name__)

# Create .env file path.
dotenv_path = join(dirname(__file__), '.env')
 
# Load file from the path.
load_dotenv(dotenv_path)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

class reusableForm(Form):
	token = TextField('Gitlab user token:', validators = [validators.required()])
	team = TextField('Team name:', validators = [validators.required()])
	project = TextField('Gitlab Project name:', validators = [validators.required()])

class issueForm(Form):
	issue_title = TextField('Issue Title:', validators = [validators.required()])
	issue_description = TextAreaField('Issue Description:', validators = [validators.required()], id='issue_description_inner_form')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/input/issues/list/form/<btntype>', methods=['GET'])
def form_page(btntype):
	form = reusableForm(request.form)
	creation_form = issueForm(request.form)
	if btntype == 'view':
		return render_template('form.html', form = form)
	else:
		return render_template('newIssue.html', form = form, creation_form=creation_form)

@app.route('/input/issues/list/', methods = ['POST'])
def show_issues():
	auth = AuthenticateWithGitlab(request.form['token'])

	gl = auth.call()
	fetched_issue = GetIssueInformation('issue', gl, request.form['project'], request.form['team'])
	returned_issues = fetched_issue.call()

	return render_template('issues.html', issues = returned_issues)

@app.route('/create/issue/templating/', methods=['POST'])
def templating():
	token = request.form['token']
	team = request.form['team']
	project = request.form['project']
	template_service = FetchIssueTemplates(token, team, project)
	templates_map = template_service.call()
	creation_form = issueForm(request.form)
	return render_template('createIssue.html', templates_map=templates_map, creation_form=creation_form, token=token, team=team, project=project)

@app.route('/create/issue/', methods = ['POST'])
def projects():
	auth = AuthenticateWithGitlab(request.form['token'])

	gl = auth.call()

	projs = CreateIssue(gl, request.form['team'], request.form['project'], request.form['issue_title'], request.form['issue_description'])

	result_issue = projs.call()

	if result_issue == 'error':
		return render_template('error.html')
	else:
		return render_template('created_issue.html', name=result_issue)

if __name__=="__main__":
	app.run()