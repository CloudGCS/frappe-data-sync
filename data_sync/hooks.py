from . import __version__ as app_version

app_name = "data_sync"
app_title = "Data Sync"
app_publisher = "CloudGCS Technologies"
app_description = "Data Sync Module for CloudGCS"
app_email = "hello@cloudgcs.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/data_sync/css/data_sync.css"
# app_include_js = "/assets/data_sync/js/data_sync.js"

# include js, css files in header of web template
# web_include_css = "/assets/data_sync/css/data_sync.css"
# web_include_js = "/assets/data_sync/js/data_sync.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "data_sync/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "data_sync.utils.jinja_methods",
#	"filters": "data_sync.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "data_sync.install.before_install"
# after_install = "data_sync.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "data_sync.uninstall.before_uninstall"
# after_uninstall = "data_sync.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "data_sync.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "*": {
        "after_insert": "data_sync.data_sync.doctype.event_update_log.event_update_log.notify_consumers",
        "on_update": "data_sync.data_sync.doctype.event_update_log.event_update_log.notify_consumers",
        "on_cancel": "data_sync.data_sync.doctype.event_update_log.event_update_log.notify_consumers",
        "on_trash": "data_sync.data_sync.doctype.event_update_log.event_update_log.notify_consumers"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"data_sync.tasks.all"
#	],
#	"daily": [
#		"data_sync.tasks.daily"
#	],
#	"hourly": [
#		"data_sync.tasks.hourly"
#	],
#	"weekly": [
#		"data_sync.tasks.weekly"
#	],
#	"monthly": [
#		"data_sync.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "data_sync.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "data_sync.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "data_sync.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"data_sync.auth.validate"
# ]
