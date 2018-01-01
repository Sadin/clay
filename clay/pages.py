import urwid
from clay.settings import Settings
from clay.gp import gp
from clay.meta import VERSION


class StartUp(urwid.Filler):
    def __init__(self, app):
        self.app = app

        super(StartUp, self).__init__(
            urwid.Pile([
                urwid.Padding(
                    urwid.AttrWrap(urwid.BigText(
                        'Clay'.format(VERSION),
                        urwid.font.HalfBlock5x4Font()
                    ), 'logo'),
                    'center',
                    None
                ),
                urwid.AttrWrap(urwid.Text('Version {}'.format(VERSION), align='center'), 'line1'),
                urwid.AttrWrap(urwid.Text('Authorizing...', align='center'), 'line2')
            ])
            # urwid.Text('Loading...'),
            # valign='top'
        )

        self.start()

    def on_login(self, success, error):
        if error:
            self.app.set_page(
                'Error',
                'Failed to log in: {}'.format(str(error))
            )
            return
        if not success:
            self.app.set_page(
                'Error',
                'Google Play Music login failed '
                '(API returned false)'
            )
            return

        self.app.set_page('MyLibrary')

    def start(self):
        if Settings.is_config_valid():
            config = Settings.get_config()
            gp.login(
                config['username'],
                config['password'],
                config['device_id'],
                callback=self.on_login
            )
        else:
            self.app.set_page(
                'Error',
                'Please set your credentials on the settings page.'
            )


class Error(urwid.Filler):
    def __init__(self, app):
        self.text = urwid.Text('Error'),
        super(Error, self).__init__(
            self.text,
            valign='top'
        )

    def set_error(self, error):
        self.text = 'Error:\n\n{}'.format(str(error))
