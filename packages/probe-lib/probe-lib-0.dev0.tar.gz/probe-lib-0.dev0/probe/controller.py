# coding: utf-8
from datetime import datetime

from flask import (Blueprint, render_template, request, redirect, session,
                    url_for, jsonify, abort, current_app, g)

from .buildinfo import version
from .model import Event, MonitorState, create_session_factory
from .monitor import enqueue


app = Blueprint('controller', __name__, template_folder='templates')


@app.before_request
def start_session():
    g.session = create_session_factory(current_app.config['DBURI'])()


@app.after_request
def end_session(response):
    g.session.commit()
    g.session.close()
    return response


@app.before_request
def check_auth():
    token = current_app.config['API_TOKEN']
    if (request.endpoint == 'controller.login'
            or session.get("authenticated")
            or request.args.get('api_token') == token
            or request.args.get('access_token') == token):
        return
    return redirect("/login/")


@app.route('/')
def show_app():
    return render_template('app.html', version=version)


@app.route('/login/', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        if request.form['api_token'] == current_app.config['API_TOKEN']:
            session["authenticated"] = True
            return redirect('/')
    return render_template("login.html", version=version)


@app.route('/hooks/<string:name>/', methods=["POST", "GET"])
def webhook(name):
    if request.method == 'POST':
        enqueue(g.session,
                current_app.registry,
                u'webhook:%s' % name,
                request.get_json(True))

        return jsonify({"accepted": True})
    else:
        return render_template('webhook.html', name=name, version=version)


@app.route('/api/')
def api_root():
    return jsonify({
        "events": "/api/events/",
        "monitors": "/api/monitors/",
    })


@app.route('/api/events/')
def api_events():
    filter = request.args.get('filter')
    since = request.args.get('since', None, type=int)
    until = request.args.get('until', None, type=int)

    events = Event.get_by_filter(g.session, filter, since, until)

    return jsonify({
        "events": [{
            "id": event.id,
            "type": event.type,
            "datetime": event.datetime.isoformat(),
            "description": current_app
                                .registry
                                .get_format(event.type, event.data),
            "body": event.data
        } for event in events]
    })


@app.route('/api/monitors/')
def api_monitors():
    return jsonify({
        "monitors": [
            {
                "name": name,
                "documentation": doc,
                "triggered_by": {
                    "method": trigger,
                    "type": type,
                },
                "state": MonitorState.get_for_monitor(g.session, name),
            }
            for name, doc, trigger, type
            in current_app.registry.get_all_monitors()
        ]
    })


@app.route('/api/monitors/<string:name>/', methods=["PATCH"])
def api_monitor_patch(name):
    MonitorState.set_for_monitor(g.session, name, request.json['state'])
    return jsonify({"success": True})
