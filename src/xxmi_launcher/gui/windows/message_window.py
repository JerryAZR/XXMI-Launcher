import logging

import core.path_manager as Paths
import core.config_manager as Config

from gui.classes.windows import UIToplevel
from gui.classes.containers import UIScrollableFrame
from gui.classes.widgets import UILabel, UIButton

log = logging.getLogger(__name__)


class MessageWindow(UIToplevel):
    def __init__(self, master, icon='info-icon.ico', title='Message', message='< Text >',
                 confirm_text='OK', confirm_command=None, cancel_text='', cancel_command=None,
                 lock_master=True, screen_center=False):
        super().__init__(master, lock_master=lock_master)

        self.response = None

        self.title(title)

        self.cfg.title = title

        if hasattr(Config, 'Active'):
            self.cfg.icon_path = Config.Active.Importer.theme_path / 'MessageWindow' / icon
        else:
            self.cfg.icon_path = Paths.App.Themes / 'Default' / 'MessageWindow' / icon

        self.cfg.width = 640
        self.cfg.height = 225

        # self.transient(master)

        self.apply_config()

        self.center_window(anchor_to_master=not screen_center)

        class MessageScrollableFrame(UIScrollableFrame):
            def __init__(self, master):
                super().__init__(
                    width=600,
                    height=138,
                    corner_radius=0,
                    fg_color="transparent",
                    hide_scrollbar=True,
                    master=master)

                self.put(MessageTextLabel(self, str(message).strip())).pack(pady=(0, 0))

                self.update()

        self.put(MessageScrollableFrame(self)).pack(pady=(20, 20))

        if confirm_text:
            self.put(ConfirmButton(self, confirm_text, confirm_command)).pack(padx=(20, 60), pady=(0, 15), side='right' if cancel_text else 'bottom')

        if cancel_text:
            self.put(CancelButton(self, cancel_text, cancel_command)).pack(padx=(60, 20), pady=(0, 15), side='left')

        self.update()

        self.after(50, self.open)

    def close(self):
        log.debug('Messagebox window closed')
        super().close()


class MessageTextLabel(UILabel):
    def __init__(self, master, message):
        super().__init__(
            text=message,
            wraplength=600,
            height=84,
            justify='center',
            anchor='center',
            font=('Asap', 16),
            master=master)


class ConfirmButton(UIButton):
    def __init__(self, master, confirm_text, confirm_command):
        super().__init__(
            text=confirm_text,
            command=lambda: self.confirm(confirm_command),
            fg_color='#666666',
            text_color='#ffffff',
            hover_color='#888888',
            width=180,
            height=30,
            master=master)

    def confirm(self, confirm_command):
        if confirm_command is not None:
            confirm_command()
        self.master.response = True
        self.master.close()


class CancelButton(UIButton):
    def __init__(self, master, cancel_text, cancel_command):
        super().__init__(
            text=cancel_text,
            command=lambda: self.cancel(cancel_command),
            fg_color='#e5e5e5',
            border_width=1,
            width=180,
            height=30,
            master=master)

    def cancel(self, cancel_command):
        if cancel_command is not None:
            cancel_command()
        self.master.response = False
        self.master.close()
