from resources.auth import RegisterComplainer, LoginComplainer
from resources.complaint import ComplaintListCreate

routes = (
    (RegisterComplainer, "/register"),
    (LoginComplainer, "/login"),
    (ComplaintListCreate, "/complainers/complaints")
)
