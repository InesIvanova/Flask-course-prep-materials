from resources.auth import RegisterComplainer, LoginComplainer

routes = (
    (RegisterComplainer, "/register"),
    (LoginComplainer, "/login")
)
