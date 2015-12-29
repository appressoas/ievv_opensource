import platform
from ievv_opensource.utils.desktopnotifications import mocknotification
from ievv_opensource.utils.desktopnotifications import osxnotification
from ievv_opensource.utils.desktopnotifications import linuxnotification


if platform.system().lower() == 'darwin':
    _notificationbackend = osxnotification.Notification()
elif platform.system().lower() == 'linux':
    _notificationbackend = linuxnotification.Notification()
else:
    _notificationbackend = mocknotification.Notification()


def show_message(title, message):
    """
    Show a message in the desktop notification system of the OS.

    Examples::

        Show a message::

            desktopnotifications.show_message(
                title='Hello world',
                message='This is a test')

    Currently this only works in OSX, but we would be happy
    to accept patches for other operating systems/desktop managers.
    See https://github.com/appressoas/ievv_opensource/issues/12.

    Args:
        title (str): The title of the notification.
        message (str): The notification message.
    """
    _notificationbackend.show_message(title=title, message=message)


# if __name__ == '__main__':
#     show_message('Hello world', 'Testing "d\'s\'ad')
