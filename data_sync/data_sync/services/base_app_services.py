import frappe


def is_service_box():
	box_settings = frappe.get_doc("Box Settings")
	return box_settings.box_type == "Service Box"

def is_client_box():
	box_settings = frappe.get_doc("Box Settings")
	return box_settings.box_type == "Client Box"