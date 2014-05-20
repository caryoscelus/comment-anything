Easy commenting system storing everything in Redis. Not quite ready yet, but
working..

Running & configuring
---------------------

You can just run main.py, but you need either config.js & config.py from
examples or to set up environment variables.

    CA_REDIS_SERVER     = server of redis (e.g. localhost)
    CA_REDIS_PORT       = redis port (e.g. 6379)
    CA_REDIS_PASSWORD   = your redis password
    CA_HOST             = host where you run this, only required for js
    CA_SITE_ID          = your site id. This MUST be unique to your site, but
                          can be shared by multiple mirrors

Heroku
------

I'm using this on heroku myself, so installing should be as simple as pushing
and changing environment variables.

Tech
----

* redis
* python
* flask
* javascript (for client part)
