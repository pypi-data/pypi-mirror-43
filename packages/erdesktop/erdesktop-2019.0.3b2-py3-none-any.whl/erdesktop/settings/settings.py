from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QPoint, QSettings

from erdesktop.settings.default import *
from erdesktop.settings.theme import dark_theme_palette, light_theme_palette


class Settings:
	"""
	Implements methods for application settings storage access.
	"""

	def __init__(self, autocommit=True, settings_file=SETTINGS_FILE):
		self.__settings = QSettings(settings_file, QSettings.IniFormat)
		self.__is_dark_theme = self.__settings.value('app_user/is_dark_theme', APP_IS_DARK_THEME)
		self.__autocommit = autocommit

	def autocommit(self, val: bool):
		self.__autocommit = val

	def commit(self):
		self.__autocommit = True
		self.__settings.sync()

	def _commit(self):
		if self.__autocommit:
			self.__settings.sync()

	@property
	def app_size(self):
		return self.__settings.value('app/size', QSize(APP_WIDTH, APP_HEIGHT))

	@property
	def app_pos(self):
		return self.__settings.value('app/pos', QPoint(APP_POS_X, APP_POS_Y))

	@property
	def app_last_backup_path(self):
		return self.__settings.value('app/last_backup_path', './')

	@property
	def app_last_restore_path(self):
		return self.__settings.value('app/last_restore_path', '')

	# noinspection PyMethodMayBeStatic
	def app_icon(self, is_ico=False, q_icon=True, small=False):
		icon = ''
		if small and is_ico:
			icon = APP_ICON_SMALL_ICO
		elif small and not is_ico:
			icon = APP_ICON_SMALL
		elif not small and is_ico:
			icon = APP_ICON_DEFAULT_ICO
		elif not small and not is_ico:
			icon = APP_ICON_DEFAULT
		if q_icon:
			return QIcon(icon)
		return icon

	@property
	def app_theme(self):
		return dark_theme_palette() if self.is_dark_theme else light_theme_palette()

	@property
	def is_dark_theme(self):
		return self.__settings.value('app_user/is_dark_theme', APP_IS_DARK_THEME) == 'true'

	@property
	def is_always_on_top(self):
		return self.__settings.value('app_user/is_always_on_top', ALWAYS_ON_TOP) == 'true'

	@property
	def app_font(self):
		return int(self.__settings.value('app_user/font', FONT))

	@property
	def app_lang(self):
		return self.__settings.value('app_user/lang', LANG)

	@property
	def app_max_backups(self):
		return int(self.__settings.value('app_user/max_backups', MAX_BACKUPS))

	@property
	def badge_color(self):
		return self.__settings.value('app/badge_color', BADGE_COLOR)

	@property
	def badge_letter_color(self):
		return self.__settings.value('app/badge_letter_color', BADGE_LETTER_COLOR)

	@property
	def remove_event_after_time_up(self):
		return self.__settings.value('event_user/remove_event_after_time_up', REMOVE_EVENT_AFTER_TIME_UP) == 'true'

	@property
	def start_in_tray(self):
		return self.__settings.value('app_user/start_in_tray', START_IN_TRAY) == 'true'

	@property
	def run_with_system_start(self):
		return self.__settings.value('app_user/run_with_system_start', RUN_WITH_SYSTEM_START) == 'true'

	@property
	def notification_duration(self):
		return int(self.__settings.value('event_user/notification_duration', NOTIFICATION_DURATION))

	@property
	def remind_time_before_event(self):
		return int(self.__settings.value('event_user/remind_time_before_event', REMIND_TIME))

	@property
	def include_settings_backup(self):
		return self.__settings.value('app_user/include_settings_backup', INCLUDE_SETTINGS_BACKUP) == 'true'

	def _set_value(self, key, value):
		self.__settings.setValue(key, value)
		self._commit()

	def set_size(self, size: QSize):
		self._set_value('app/size', size)

	def set_pos(self, pos: QPoint):
		self._set_value('app/pos', pos)

	def set_last_backup_path(self, path: str):
		self._set_value('app/last_backup_path', path)

	def set_last_restore_path(self, path: str):
		self._set_value('app/last_restore_path', path)

	def set_theme(self, is_dark: bool):
		self._set_value('app_user/is_dark_theme', 'true' if is_dark else 'false')

	def set_is_always_on_top(self, value: bool):
		self._set_value('app_user/is_always_on_top', 'true' if value else 'false')

	def set_font(self, value: int):
		self._set_value('app_user/font', value)

	def set_lang(self, value: str):
		self._set_value('app_user/lang', value)

	def set_max_backups(self, value: int):
		self._set_value('app_user/max_backups', value)

	def set_remove_event_after_time_up(self, value: bool):
		self._set_value('app_user/remove_event_after_time_up', 'true' if value else 'false')

	def set_start_in_tray(self, value: bool):
		self._set_value('app_user/start_in_tray', 'true' if value else 'false')

	def set_run_with_system_start(self, value: bool):
		self._set_value('app_user/run_with_system_start', 'true' if value else 'false')

	def set_notification_duration(self, value: int):
		self._set_value('event_user/notification_duration', value)

	def set_remind_time_before_event(self, value: int):
		self._set_value('event_user/remind_time_before_event', value)

	def set_include_settings_backup(self, value: bool):
		self._set_value('app_user/include_settings_backup', 'true' if value else 'false')

	def to_dict(self):
		return {
			'is_dark_theme': self.is_dark_theme,
			'is_always_on_top': self.is_always_on_top,
			'font': self.app_font,
			'remove_event_after_time_up': self.remove_event_after_time_up,
			'start_in_tray': self.start_in_tray,
			'notification_duration': self.notification_duration,
			'remind_time_before_event': self.remind_time_before_event,
			'lang': self.app_lang
		}

	def from_dict(self, data):
		keys = [
			'is_dark_theme', 'is_always_on_top', 'font',
			'remove_event_after_time_up', 'start_in_tray',
			'notification_duration', 'remind_time_before_event', 'lang'
		]
		for key in keys:
			if key not in data:
				raise KeyError('Settings failure: backup is invalid.')
		self.set_theme(data['is_dark_theme'])
		self.set_is_always_on_top(data['is_always_on_top'])
		self.set_font(data['font'])
		self.set_remove_event_after_time_up(data['remove_event_after_time_up'])
		self.set_start_in_tray(data['start_in_tray'])
		self.set_notification_duration(data['notification_duration'])
		self.set_remind_time_before_event(data['remind_time_before_event'])
		self.set_lang(data['lang'])
		self.commit()
