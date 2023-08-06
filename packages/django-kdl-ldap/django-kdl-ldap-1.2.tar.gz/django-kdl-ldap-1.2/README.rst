Django LDAP authentication
==========================

This application uses django-auth-ldap_ to authenticate against KDL's LDAP service. If the LDAP authentication fails it falls back to Django authentication, so it is possible to have local Django accounts.

Configuration
-------------
#. ``pip install django-kdl-ldap``
#. add ``kdl_ldap`` to ``INSTALLED_APPS``
#. import the ``kdl_ldap`` settings into your project's settings ``from kdl_ldap.settings import *  # noqa``.
#. Add the setting ``AUTH_LDAP_REQUIRE_GROUP`` to your project settings and set it to the LDAP group you want to authenticate to: ``AUTH_LDAP_REQUIRE_GROUP = 'cn=PROJECT_GROUP_NAME,' + LDAP_BASE_OU``.
#. Add ``kdl_ldap`` signal handler into your project urls:

        from kdl_ldap.signal_handlers import register_signal_handlers as \
            kdl_ldap_register_signal_hadlers
        kdl_ldap_register_signal_hadlers()

System requirements
-------------------

The python/django LDAP libraries depend on the ``libldap2-dev`` and ``libsasl2-dev`` systemlibraries.

.. _django-auth-ldap: http://pythonhosted.org/django-auth-ldap/
