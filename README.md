comment-anything (CA) is a simple commenting system embeddable to any site
(only javascript & iframe support required). Not quite ready yet, but working..

You can see example at http://comment-anything.herokuapp.com/

Example of embedding inside real site (CA was specifically created for it):
http://caryoscelus.github.io/

NOTE: CA is currently being rewritten in PureScript.
Client part is here: https://github.com/caryoscelus/comment-anything-fp-client

Running & configuring
---------------------

You can just run main.py, but you need either config.js & config.py from
examples or to set up environment variables.

    CA_REDIS_SERVER     = server of redis (e.g. localhost)
    CA_REDIS_PORT       = redis port (e.g. 6379)
    CA_REDIS_PASSWORD   = your redis password
    CA_HOST             = host where you run this, only required for js
                          (e.g. http://localhost:5000/)
    CA_SITE_ID          = your site id. This MUST be unique to your site, but
                          can be shared by multiple mirrors, only required for
                          js
                          (e.g. test)
    CA_USE_CONFIG_JS    = if this is set and not empty, config.js will be read
                          from this file (i use it for localhost testing)
    CA_MODERATE_PASS_HASH = if this is set, this is treated as hash for
                          moderator password, which is required to remove
                          comments. Otherwise, removing is impossible

Heroku
------

I'm using this on heroku myself, so installing should be as simple as pushing
and changing environment variables.

API
---

The following API is currently in use:

    /iframe/<site_id>/<page_uri>        = embeddable HTML with related comments
    /get_comments/<site_id>/<page_uri>  = json containing related comments
    /add_comment/<site_id>/<page_uri>   = POST comment (json)
    /dump_comments/<site_id>            = dump all comments for site
    /remove_comment/<site_id>/<comment_id>/<page_uri> = POST remove comment
                                        { "password" = your_password }

Where

    page_uri    = address of page starting with /root (e.g. /root/page.html)
    site_id     = site id

Comment data structure (fields are optional):
    {
        'nick'      : nick,
        'text'      : text,
        'date'      : date,
        'email'     : email,
        'website'   : website
    }

More documentation can arive later. Meanwhile, you can consult source code for
more details.

Tech
----

* redis (db)
* python (server)
* flask (server framework)
* javascript (client)

License
-------

Javascript source (aka client part) is licensed under GPLv3+ (see COPYING.gpl3
for full text), Python source (aka server part) is licensed AGPLv3+ (see
COPYING.agpl3).

.example files and index.html are trivial and could be used without any
restrictions.
