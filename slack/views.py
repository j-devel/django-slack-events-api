from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
from django.core.exceptions import PermissionDenied
import json

import logging
logging.getLogger().setLevel(logging.INFO)


# uncomment for the slackclient API client (https://github.com/slackapi/python-slackclient)
from .adapter_slackclient import slack_events_adapter, SLACK_VERIFICATION_TOKEN
#----
# uncomment for the slacker API client (https://github.com/os/slacker)
# from .adapter_slacker import slack_events_adapter, SLACK_VERIFICATION_TOKEN
#----
# uncomment for a urllib2-based client implemented in client_urllib2.py
# This should work with Google App Engine.
# from .adapter_urllib2 import slack_events_adapter, SLACK_VERIFICATION_TOKEN


def render_json_response(request, data, status=None, support_jsonp=False):
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    callback = request.GET.get("callback")
    if not callback:
        callback = request.POST.get("callback")  # in case of POST and JSONP

    if callback and support_jsonp:
        json_str = "%s(%s)" % (callback, json_str)
        response = HttpResponse(json_str, content_type="application/javascript; charset=UTF-8", status=status)
    else:
        response = HttpResponse(json_str, content_type="application/json; charset=UTF-8", status=status)
    return response


@csrf_exempt
def slack_events(request, *args, **kwargs):  # cf. https://api.slack.com/events/url_verification
    # logging.info(request.method)
    if request.method == "GET":
        raise Http404("These are not the slackbots you're looking for.")

    try:
        # https://stackoverflow.com/questions/29780060/trying-to-parse-request-body-from-post-in-django
        event_data = json.loads(request.body.decode("utf-8"))
    except ValueError as e:  # https://stackoverflow.com/questions/4097461/python-valueerror-error-message
        logging.info("ValueError: "+str(e))
        return HttpResponse("")
    logging.info("event_data: "+str(event_data))

    # Echo the URL verification challenge code
    if "challenge" in event_data:
        return render_json_response(request, {
            "challenge": event_data["challenge"]
        })

    # Parse the Event payload and emit the event to the event listener
    if "event" in event_data:
        # Verify the request token
        request_token = event_data["token"]
        if request_token != SLACK_VERIFICATION_TOKEN:
            slack_events_adapter.emit('error', 'invalid verification token')
            message = "Request contains invalid Slack verification token: %s\n" \
                      "Slack adapter has: %s" % (request_token, SLACK_VERIFICATION_TOKEN)
            raise PermissionDenied(message)

        event_type = event_data["event"]["type"]
        logging.info("event_type: "+event_type)
        slack_events_adapter.emit(event_type, event_data)
        return HttpResponse("")

    # default case
    return HttpResponse("")
