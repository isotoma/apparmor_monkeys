apparmor_monkeys
================

.. image:: https://codecov.io/github/Jc2k/apparmor_monkeys/coverage.svg?branch=master
   :target: https://codecov.io/github/Jc2k/apparmor_monkeys?branch=master


Monkeypatches to minimize the permissions required to run python under AppArmor.


What does this do?
------------------

Imagine you've written a simple Django application. Maybe you just followed the
Django tutorial. All your code does is a bit of database querying. Then you
deploy it under AppArmor and::

    type=AVC msg=audit(1443087838.797:1078): apparmor="DENIED" operation="exec" profile="helloworld-application" name="/bin/dash" pid=8202 comm="python" requested_mask="x" denied_mask="x" fsuid=999 ouid=0

Suddenly your audit log is full of messages complaining that your application
is trying to run a shell. You certainly didn't write code to do that. Whats
going on? Did you get hacked?

You (probably ;)) didn't get hacked.

Turns out python shells out when doing some fairly mundane stuff. Up until now
you could:

 * Ignore it. Let your audit log have ``DENIED`` entries that you have to
   ignore. Now it's hard to spot suspicious behaviour in your monitoring.
   Thinks might be broken, thinks might not be broken.
   Hope you don't have to go through that log with a security professional.

 * Allow it. Now your profile is broader than it needs to be. You are throwing
   away the security you gain in the first place. Hope you don't have to go
   through that profile with a security professional.

This package patches several stdlib API's to avoid ``subprocess`` usage,
letting you keep your simple profiles and clean audit logs. The patching is
automatic, using a ``pth`` file. These are loaded by ``site.py`` when python is
starting.


ctypes vs ldconfig
~~~~~~~~~~~~~~~~~~

One of the first things I caught by application doing was trying to run
``gcc``. This turned out to be a fallback for when an earlier attempt to run
``ldconfig`` had failed.

This turned out to be how ``ctypes.util.find_library`` works. This can be used
in a few places:

 * Gunicorn uses it for its sendfile implementation.
 * Python's ``uuid`` module uses for ``uuid4``. Just importing the ``uuid``
   module triggers this, even if you aren't using ``uuid4``.


platform.uname vs os.uname
~~~~~~~~~~~~~~~~~~~~~~~~~~

``platform.uname`` is mostly the same as ``os.uname``, but there is an extra
field. The field is sourced by shelling out and running ``uname -p``::

    sh -c "uname %s 2>%s"

This is used in several places:

 * A command trick for getting your own version number is
   ``pkg_resources.require('myapp')[0].version``, which triggers it.
 * Gunicorn triggers it via a ``platform.system()`` in
   ``gunicorn.workers.workertmp`` before it even loads your code.


Switching profiles
------------------

You can harden your AppArmor profiles further using ``change_profile`` to switch into a different profile after initialising your app.

If using multiprocess gunicorn (i.e. synchronous gunicorn) then you can wrap
your workers in their own specific profile. In your gunicorn config you can add
a hook to do this::

    from apparmor_monkeys import change_profile

    def post_fork(server, worker):
        change_profile("myapplication//worker")


You can do this for celery too::

    from apparmor_monkeys import change_profile
    from celery import signals

    @signals.worker_process_init.connect
    def switch_apparmor_profile(sender=None, signal=None):
        change_profile("tenselfservice-worker//worker")
