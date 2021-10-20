from resources.admin import CreateAdmin, CreateApprover, ComplaintManagement
from resources.auth import RegisterComplainer, LoginComplainer, LoginApprover, LoginAdministrator
from resources.complaint import ComplaintListCreate

routes = (
    (RegisterComplainer, "/register"),
    (LoginComplainer, "/login"),
    (LoginApprover, "/approvers/login"),
    (ComplaintListCreate, "/complainers/complaints"),
    (CreateAdmin, "/admins/create-admin"),
    (CreateApprover, "/admins/create-approver"),
    (ComplaintManagement, "/admins/complains/<int:id_>"),
    (LoginAdministrator, "/admins/login"),
)
