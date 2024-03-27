# Copyright (c) 2024, CloudGCS Technologies and contributors
# For license information, please see license.txt

import json


from data_sync.data_sync.doctype.event_consumer.event_consumer import register_consumer
from data_sync.data_sync.doctype.event_update_log.event_update_log import get_update_logs_for_consumer
from data_sync.data_sync.doctype.event_producer.event_producer import pull_from_node

from data_sync.data_sync.services.base_app_services import is_client_box
from frappe.utils.background_jobs import get_jobs
import frappe
import time
import requests
from frappe.frappeclient import FrappeClient
from frappe.model.document import Document
from frappe import _
from frappe.utils.data import get_url


class EventServer(Document):
  def is_server_online(self):
    """check connection status for the Event Producer site"""
    retry = 3
    while retry > 0:
      res = requests.get(self.server_url)
      if res.status_code == 200:
        return True
      retry -= 1
      time.sleep(5)
    frappe.throw(_("Failed to connect to the Server site. Retry after some time."))


@frappe.whitelist()
def sync_consumer_event(*args,**kwargs):
  if is_client_box():
    raise Exception("This method is only available for Service Box")
  
  server = frappe.get_doc("Event Server")
  if server.is_server_online():
    server_site = FrappeClient(
        url=server.server_url, api_key=server.api_key, api_secret=server.get_password("api_secret")
      )

    response = server_site.get_api(
      "data_sync.data_sync.doctype.event_producer.event_producer.get_producer",
      params={"producer_url": get_url()},
    )
    if response:
      event_consumer_doc = frappe.get_doc("Event Consumer", server.server_url)
      if event_consumer_doc:
        updated_consumer = server_site.post_request(
          {
            "cmd": "data_sync.data_sync.doctype.event_producer.event_producer.get_producer_updates",
            "producer_url": get_url(),
            "event_consumer": frappe.as_json(event_consumer_doc),
          }
        )
        event_consumer_doc.user = updated_consumer["user"]
        event_consumer_doc.incoming_change = updated_consumer["incoming_change"]

        # first delete all the existing consumer doctypes
        # for consumer_doctype in event_consumer_doc.consumer_doctypes:
        #   frappe.delete_doc("Event Consumer Document Type", consumer_doctype.name)
        
        event_consumer_doc.set("consumer_doctypes", [])

        # then create new consumer doctypes from the updated consumer["consumer_doctypes"]
        consumer_doctypes = []
        for consumer_doctype in updated_consumer["consumer_doctypes"]:
          consumer_doctype_doc = frappe.new_doc("Event Consumer Document Type")
          consumer_doctype_doc.parent = event_consumer_doc.name
          consumer_doctype_doc.parenttype = "Event Consumer"
          consumer_doctype_doc.parentfield = "consumer_doctypes"
          consumer_doctype_doc.ref_doctype = consumer_doctype["ref_doctype"]
          consumer_doctype_doc.status = consumer_doctype["status"]
          consumer_doctype_doc.unsubscribed = consumer_doctype["unsubscribed"]
          consumer_doctype_doc.insert()
          consumer_doctypes.append(consumer_doctype_doc)
          # # add the new consumer doctype to the event_consumer_doc
          # event_consumer_doc.append("consumer_doctypes", consumer_doctype_doc)

        event_consumer_doc.set("consumer_doctypes", consumer_doctypes)
        event_consumer_doc.save()
      else:
        last_update_as_string = register_consumer(response)
        last_update = json.loads(last_update_as_string)["last_update"]

        server_site.post_api(
          "data_sync.data_sync.doctype.event_producer.event_producer.update_producer_after_consumer_creation",
          params={"data": json.dumps({"producer_url": get_url(), "last_update": last_update})},
        )
    else:
      frappe.throw(
        _(
          "Failed to check server or no Event Producer exists for the current site"
        )
      )
  else:
    raise Exception("The server is not online")


@frappe.whitelist()
def sync_producer_event(*args, **kwargs):
  if is_client_box():
    raise Exception("This method is only available for Service Box")
  
  server = frappe.get_doc("Event Server")
  if not server.is_server_online():
        raise Exception("The server is not online")
  server_site = FrappeClient(
        url=server.server_url, api_key=server.api_key, api_secret=server.get_password("api_secret")
      )
  response = server_site.get_api(
    "data_sync.data_sync.doctype.event_consumer.event_consumer.get_consumer",
    params={"consumer_url": get_url()},
  )

  if not response:
    frappe.throw(_("Failed to check server or no Event Consumer exists for the current site"))

  event_producer_doc = frappe.get_doc("Event Producer", server.server_url)
  if not event_producer_doc:
    frappe.throw(_("No Event Producer exists for the current site"))

  updated_producer = server_site.post_request(
    {
      "cmd": "data_sync.data_sync.doctype.event_consumer.event_consumer.get_consumer_updates",
      "consumer_url": get_url(),
      "event_producer": frappe.as_json(event_producer_doc),
    }
  )
  event_producer_doc.user = updated_producer["user"]
  event_producer_doc.incoming_change = updated_producer["incoming_change"]
  
  event_producer_doc.set("producer_doctypes", [])

  # then create new producer doctypes from the updated producer["producer_doctypes"]
  producer_doctypes = []
  for producer_doctype in updated_producer["producer_doctypes"]:
    producer_doctype_doc = frappe.new_doc("Event Producer Document Type")
    producer_doctype_doc.parent = event_producer_doc.name
    producer_doctype_doc.parenttype = "Event Producer"
    producer_doctype_doc.parentfield = "producer_doctypes"
    producer_doctype_doc.ref_doctype = producer_doctype["ref_doctype"]
    producer_doctype_doc.status = producer_doctype["status"]
    producer_doctype_doc.insert()
    producer_doctypes.append(producer_doctype_doc)

  event_producer_doc.set("producer_doctypes", producer_doctypes)
  event_producer_doc.save()
    

@frappe.whitelist()
def pull_data(*args,**kwargs):
  if is_client_box():
    raise Exception("This method is only available for Service Box")
  enqueued_method = ("data_sync.data_sync.doctype.event_producer.event_producer.pull_from_node")
  for event_producer in frappe.get_all("Event Producer"):
    jobs = get_jobs()
    if not jobs or enqueued_method not in jobs[frappe.local.site]:
      # pull_from_node(event_producer.name)
      frappe.enqueue(enqueued_method, queue="default", **{"event_producer": event_producer.name})

@frappe.whitelist()
def push_data(*args,**kwargs):
  if is_client_box():
    raise Exception("This method is only available for Service Box")
  
  server = frappe.get_doc("Event Server")
  if server.is_server_online():
    server_site = FrappeClient(
        url=server.server_url, api_key=server.api_key, api_secret=server.get_password("api_secret")
      )
    response = server_site.get_api(
      "data_sync.data_sync.doctype.event_producer.event_producer.get_update_config",
      params={"producer_url": get_url()},
    )
    if response:
      response = json.loads(response)
      update_logs = get_update_logs_for_consumer(response["event_consumer"], response["doctypes"], response["last_update"])
    else:
      frappe.throw(
        _(
          "Failed to check server or no Event Producer exists for the current site"
        )
      )
    
    server_site.post_request(
      {
        "cmd": "data_sync.data_sync.doctype.event_producer.event_producer.get_pushed_updates",
        "producer_url": get_url(),
        "update_logs": frappe.as_json(update_logs),
      }
	  )
    
  else:
    raise Exception("The server is not online")