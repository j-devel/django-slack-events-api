Slack Events API adapter as a Django app
========================================

**django-slack-events-api** is a minimal Django app for making your Slack bot.

It includes a Django porting of the official Slack Events API adapter:
`python-slack-events-api`_.  The original adapter is based on the `Flask
framework`_; so here's a modular Django app version instead ;-)

.. _python-slack-events-api: https://github.com/slackapi/python-slack-events-api
.. _Flask framework: https://github.com/pallets/flask

This is intended to minimal (devoid of extra model, template, and
module-dependency stuffs) focusing only on `Slack Events`_ handling.  However,
all the features and examples useful for Slack bot creation (such as utilizing
the `python-slackclient`_) found in the original Flask version are retained and
functional.  After working through `the demo section`_, you'll find it easy to
integrate this app into your Django projects as well.

.. _Slack Events: https://api.slack.com/events-api
.. _python-slackclient: https://github.com/slackapi/python-slackclient

**Bonus:** Additionally, django-slack-events-api supports three kinds of Slack client
library integration:

- the official `Slack Developer Kit for Python (aka. python-slackclient)`_ [default],
- the popular `slacker client`_, and
- `a minimal client`_ based on `urllib2`_ (compatible with Google App Engine thanks to no socket module dependency).

.. _Slack Developer Kit for Python (aka. python-slackclient): https://github.com/slackapi/python-slackclient
.. _slacker client: https://github.com/os/slacker
.. _a minimal client: slack/client_urllib2.py
.. _urllib2: https://docs.python.org/2/howto/urllib2.html

**Credits:** Sections marked by 🤖 is a derived work of `python-slack-events-api/example/README.rst`_.

Installation
-----------------

**Tested environment:**

- Python 2.7
- Django 1.8.9

**Install the app and its dependencies:**

.. code::

   $ git clone https://github.com/mm-jay/django-slack-events-api.git
   $ cd django-slack-events-api
   $ pip install -r requirements.txt

.. _the demo section:

Demo: creating a minimal Django project for a Slack bot
-----------------------------------------------------------

In this section, we present a quick demo on how to get a working Django-based
Slack bot on your local computer.  We create a new Django app from scratch and
embed the django-slack app in it.  After configurations, we start the
Django local server on port 3000.  ngrok_ is used to make sure that the local
bot instance is properly communicating with the Slack server on the Internet.

.. _ngrok: https://ngrok.com

**(1) A new django project with a django slack app embedded**

.. code::

   $ django-admin startproject bot  # create a new django project called "bot"
   $ cp -r slack bot/               # copy (embed) the bare django-slack app under the bot project
   $ cd bot                         # move into the root of the bot project

Now the current directory structure should look as follows:
   
.. code::

   $ find .    
   .                               # Root of the new "bot" project
   ./bot
   ./bot/__init__.py
   ./bot/settings.py               # to be modified
   ./bot/urls.py                   # to be modified
   ./bot/wsgi.py
   ./manage.py
   ./slack                         # a copy of django-slack app
   ./slack/__init__.py
   ./slack/adapter_slackclient.py
   ./slack/adapter_slacker.py
   ./slack/adapter_urllib2.py
   ./slack/client_urllib2.py
   ./slack/urls.py
   ./slack/views.py


.. _add the token in bot/settings.py:

**(2) Modify bot/settings.py to add the slack app and tokens.**

For obtaining the ``SLACK_VERIFICATION_TOKEN`` and ``SLACK_BOT_TOKEN`` tokens,
see `Appendix: Setup your bot in Slack`_.

.. code::
   
   INSTALLED_APPS = (
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       'slack',                            # <-- add this
   )

   SLACK_VERIFICATION_TOKEN = "xxxxxxxxXxxXxxXxXXXxxXxxx"  # <-- add this
   SLACK_BOT_TOKEN = "xxxXXxxXXxXXxXXXXxxxX.xXxxxXxxxx"    # <-- add this

**(3) Modify bot/urls.py to configure the endpoint.**

.. code::
   
   urlpatterns = [
       url(r'^admin/', include(admin.site.urls)),
       url(r'^slack/', include('slack.urls', namespace="slack")),  # <-- add this
   ]

**(4) [Optional] Modify slack/urls.py to customize the endpoint (default is /slack/events)**

**(5) [Optional] Select the underlying bot client library**

In ``slack/views.py``, uncomment the adapter corresponding to the client
library of your choice.  (Unmodified, ``adapter_slackclient.py`` is used by
default.)

.. code::

   # uncomment for the slackclient API client (https://github.com/slackapi/python-slackclient)
   from .adapter_slackclient import slack_events_adapter, SLACK_VERIFICATION_TOKEN
   #----
   # uncomment for the slacker API client (https://github.com/os/slacker)
   # from .adapter_slacker import slack_events_adapter, SLACK_VERIFICATION_TOKEN
   #----
   # uncomment for a urllib2-based client implemented in client_urllib2.py
   # This should work with Google App Engine.
   # from .adapter_urllib2 import slack_events_adapter, SLACK_VERIFICATION_TOKEN

Depending on your choice of the client library, start hacking your bot's logic
by editing one of

- ``adapter_slackclient.py`` (using `python-slackclient`_),
- ``adapter_slacker.py`` (using `slacker`_), and
- ``adapter_urllib2.py`` (using `slack/client_urllib2.py`_).

.. _slacker: https://github.com/os/slacker
.. _slack/client_urllib2.py: slack/client_urllib2.py

**(6) 🤖 Start ngrok**

In order for Slack to contact your local server, you'll need to run a tunnel. We
recommend ngrok or localtunnel. We're going to use ngrok for this example.

If you don't have ngrok, `download it here`_.

.. _download it here: https://ngrok.com


Here's a rudimentary diagream of how ngrok allows Slack to connect to your server

.. image:: https://cloud.githubusercontent.com/assets/32463/25376866/940435fa-299d-11e7-9ee3-08d9427417f6.png


💡  Slack requires event requests be delivered over SSL, so you'll want to
    use the HTTPS URL provided by ngrok.

Run ngrok and copy the **HTTPS** URL

.. code::

  ngrok http 3000

.. code::

  ngrok by @inconshreveable (Ctrl+C to quit)

  Session status                      online
  Version                             2.1.18
  Region                  United States (us)
  Web Interface        http://127.0.0.1:4040

  Forwarding http://h7465j.ngrok.io -> localhost:9292
  Forwarding https://h7465j.ngrok.io -> localhost:9292

**(7) 🤖 Run the app**

You'll need to have your server and ngrok running to complete your app's Event
Subscription setup

.. code::

   $ python manage.py runserver 0.0.0.0:3000

**🎉  Once your app has been installed and subscribed to Bot Events, you will begin receiving event data from Slack**

**(8) Interact with your bot**

Invite your bot to a public channel, then say hi and your bot will respond.

.. image:: https://cloud.githubusercontent.com/assets/29015408/26621593/813a695e-4611-11e7-856d-3c48a31cd906.png

Here are Django console logs showing the interaction with the Slack server.

Case: local server + ngrok:

.. log_local
.. image:: https://cloud.githubusercontent.com/assets/29015408/26621497/27dd11fe-4611-11e7-9729-c2bc596268f1.png

Case: Google App Engine:

.. log_gae 
.. image:: https://cloud.githubusercontent.com/assets/29015408/26621595/814a125a-4611-11e7-80a0-5d9bdfb7237d.png


Appendix: Setup your bot in Slack
-------------------------------------

.. _python-slack-events-api/example/README.rst: https://github.com/slackapi/python-slack-events-api/blob/master/example/README.rst


**🤖 Create a Slack app**

Create a Slack app on https://api.slack.com/apps/

.. image:: https://cloud.githubusercontent.com/assets/32463/24877733/32979776-1de5-11e7-87d4-b5dc9e3e7973.png

**🤖  Add a bot user to your app**

.. image:: https://cloud.githubusercontent.com/assets/32463/24877750/47a16034-1de5-11e7-989b-2a90b9d8e7e3.png

**🤖  Install your app on your team**

Visit your app's **Install App** page and click **Install App to Team**.

.. image:: https://cloud.githubusercontent.com/assets/32463/24877770/61804c36-1de5-11e7-91ef-5cf2e0845729.png

Authorize your app

.. image:: https://cloud.githubusercontent.com/assets/32463/24877792/774ed94c-1de5-11e7-8857-ac8d662c5b27.png

**🤖  Subscribe your app to events**

Add your **Request URL** (your ngrok URL + ``/slack/events``) and subscribe your app to `message.channels` under bot events. **Save** and toggle **Enable Events** to `on`

.. image:: https://cloud.githubusercontent.com/assets/32463/24877867/b39d4384-1de5-11e7-9676-9e47ea7db4e7.png

.. image:: https://cloud.githubusercontent.com/assets/32463/24877931/e119181a-1de5-11e7-8b0c-fcbc3419bad7.png

**🤖  Save your app's credentials**

Once you've authorized your app, you'll be presented with your app's tokens.

.. image:: https://cloud.githubusercontent.com/assets/32463/24877652/d8eebbb4-1de4-11e7-8f75-2cfb1e9d45ee.png

Copy your app's **Bot User OAuth Access Token**, then `add the token in bot/settings.py`_.

.. code::

   SLACK_BOT_TOKEN = "xxxXXxxXXxXXxXXXXxxxX.xXxxxXxxxx"

Next, go back to your app's **Basic Information** page

.. image:: https://cloud.githubusercontent.com/assets/32463/24877833/950dd53c-1de5-11e7-984f-deb26e8b9482.png

Copy your app's **Verification Token**, then `add the token in bot/settings.py`_.

.. code::

   SLACK_VERIFICATION_TOKEN = "xxxxxxxxXxxXxxXxXXXxxXxxx"

