"""
Library page.
"""
import urwid
from clay.gp import GP
from clay.songlist import SongListBox
from clay.notifications import NotificationArea


class MyLibrary(urwid.Columns):
    """
    My library page.

    Displays :class:`clay.songlist.SongListBox` with all songs in library.
    """
    name = 'Library'
    key = 1

    def __init__(self, app):
        self.app = app
        self.songlist = SongListBox(app)
        self.notification = None

        GP.get().auth_state_changed += self.auth_state_changed

        super(MyLibrary, self).__init__([
            self.songlist
        ])

    def on_get_all_songs(self, tracks, error):
        """
        Called when all library songs are fetched from server.
        Populate song list.
        """
        if error:
            NotificationArea.notify('Failed to load my library: {}'.format(str(error)))
            return
        # self.notification.close()
        self.songlist.populate(tracks)
        self.app.redraw()

    def auth_state_changed(self, is_auth):
        """
        Called when auth state changes.
        If *is_auth* is true, load all library songs.
        """
        if is_auth:
            self.songlist.set_placeholder(u'\n \uf01e Loading song list...')

            GP.get().get_all_tracks_async(callback=self.on_get_all_songs)
            # self.notification = NotificationArea.notify('Loading library...')
