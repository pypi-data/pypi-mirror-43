import pkg_resources


__version__ = pkg_resources.require("odinuge-django-push-notifications")[0].version


class NotificationError(Exception):
	pass
