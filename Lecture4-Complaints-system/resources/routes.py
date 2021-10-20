from resources.admin import CreateAdmin, CreateApprover, ComplaintManagement
from resources.auth import RegisterComplainer, LoginComplainer, LoginApprover, LoginAdministrator
from resources.complaint import ComplaintListCreate, ApproveComplaint, RejectComplainComplaint

routes = (
    (RegisterComplainer, "/register"),
    (LoginComplainer, "/login"),
    (LoginApprover, "/approvers/login"),
    (ApproveComplaint, "/approvers/complaints/<int:id_>/approve"),
    (RejectComplainComplaint, "/approvers/complaints/<int:id_>/reject"),
    (ComplaintListCreate, "/complainers/complaints"),
    (CreateAdmin, "/admins/create-admin"),
    (CreateApprover, "/admins/create-approver"),
    (ComplaintManagement, "/admins/complains/<int:id_>"),
    (LoginAdministrator, "/admins/login"),
)
