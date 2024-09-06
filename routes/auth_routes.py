# routes/auth_routes.py

from flask import Blueprint

auth_bp = Blueprint('auth_bp', __name__)

# @auth_bp.route("/login")
# def login():
#     authorization_url, state = app.flow.authorization_url()
#     session["state"] = state
#     return redirect(authorization_url)


# @auth_bp.route("/callback")
# def callback():
#     app.flow.fetch_token(authorization_response=request.url)

#     if not session["state"] == request.args["state"]:
#         abort(500)  # State does not match!

#     credentials = app.flow.credentials
#     request_session = requests.session()
#     cached_session = cachecontrol.CacheControl(request_session)
#     token_request = google.auth.transport.requests.Request(session=cached_session)

#     id_info = id_token.verify_oauth2_token(
#         id_token=credentials._id_token,
#         request=token_request,
#         audience=app.config['GOOGLE_CLIENT_ID']
#     )

#     session["google_id"] = id_info.get("sub")
#     session["name"] = id_info.get("name")
#     return redirect("/protected_area")


# @auth_bp.route("/protected_area")
# def protected_area():
#     return f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>"


# @auth_bp.route("/logout")
# def logout():
#     session.clear()
#     return redirect("/")
