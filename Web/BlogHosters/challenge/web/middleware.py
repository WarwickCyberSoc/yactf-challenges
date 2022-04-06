from functools import wraps
from flask import g, session, redirect, url_for


def is_authenticated():
    def _is_authenticated(f):
        @wraps(f)
        def __is_authenticated(*args, **kwargs):
            if not hasattr(g, "user") or g.user is None:
                return redirect(url_for("login_page"))

            return f(*args, **kwargs)

        return __is_authenticated

    return _is_authenticated
