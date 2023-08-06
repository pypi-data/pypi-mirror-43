import time
from flask import g, request
from flask.signals import got_request_exception
from pybrake.utils import logger

try:
    from flask_login import current_user
except ImportError:
    flask_login_imported = False
else:
    flask_login_imported = True

from .notifier import Notifier


def init_app(app):
    if "pybrake" in app.extensions:
        raise ValueError("pybrake is already injected")
    if "PYBRAKE" not in app.config:
        raise ValueError("app.config['PYBRAKE'] is not defined")

    notifier = Notifier(**app.config["PYBRAKE"])

    app.extensions["pybrake"] = notifier
    got_request_exception.connect(_handle_exception, sender=app)

    app.before_request(_before_request())
    app.after_request(_after_request(notifier))

    return app


def _before_request():
    def before_request_middleware():
        g.request_start_time = time.time()

    return before_request_middleware


def _after_request(notifier):
    def after_request_middleware(response):
        if not hasattr(g, "request_start_time"):
            logger.error("request_start_time is empty")
            return response

        notifier.routes.notify(
            method=request.method,
            route=request.url_rule.rule,
            status_code=response.status_code,
            start_time=g.request_start_time,
            end_time=time.time(),
        )

        return response

    return after_request_middleware


def _handle_exception(sender, exception, **_):
    notifier = sender.extensions["pybrake"]

    notice = notifier.build_notice(exception)
    ctx = notice["context"]
    ctx["method"] = request.method
    ctx["url"] = request.url
    ctx["route"] = str(request.endpoint)

    try:
        user_addr = request.access_route[0]
    except IndexError:
        user_addr = request.remote_addr
    if user_addr:
        ctx["userAddr"] = user_addr

    if flask_login_imported and current_user.is_authenticated:
        user = dict(id=current_user.get_id())
        for s in ["username", "name"]:
            if hasattr(current_user, s):
                user[s] = getattr(current_user, s)
        ctx["user"] = user

    notice["params"]["request"] = dict(
        form=request.form,
        json=request.json,
        files=request.files,
        cookies=request.cookies,
        headers=dict(request.headers),
        environ=request.environ,
        blueprint=request.blueprint,
        url_rule=request.url_rule,
        view_args=request.view_args,
    )

    notifier.send_notice(notice)
