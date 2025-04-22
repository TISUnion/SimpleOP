import time
from threading import Lock

from mcdreforged.api.all import *


class PermissionConfig(Serializable):
	op: int = 1
	restart: int = 1


class Config(Serializable):
	enabled: bool = True
	restart_delay: int = 5
	permissions: PermissionConfig = PermissionConfig()


PLUGIN_METADATA = ServerInterface.get_instance().as_plugin_server_interface().get_self_metadata()
restart_lock = Lock()
config = Config.get_default()
config.enabled = False


def tr(translation_key: str, *args, **kwargs) -> RTextMCDRTranslation:
	return ServerInterface.get_instance().rtr('{}.{}'.format(PLUGIN_METADATA.id, translation_key), *args, **kwargs)


@new_thread(PLUGIN_METADATA.name + ' - restart')
def restart(source: CommandSource):
	if source.get_permission_level() < config.permissions.restart:
		source.reply(tr('permission_denied'))
		return

	acq = restart_lock.acquire(blocking=False)
	if not acq:
		source.reply(tr('restart.spam'))
		return
	try:
		for i in range(config.restart_delay):
			source.get_server().broadcast(RText(tr('restart.countdown', config.restart_delay - i), color=RColor.red))
			time.sleep(1)
		source.get_server().restart()
	finally:
		restart_lock.release()


def give_op(source: CommandSource):
	if source.get_permission_level() < config.permissions.op:
		source.reply(tr('permission_denied'))
		return

	if isinstance(source, PlayerCommandSource):
		source.get_server().execute('op {}'.format(source.player))
	else:
		source.reply(tr('op.needs_player'))


def on_load(server: PluginServerInterface, prev):
	try:
		global restart_lock
		assert type(prev.restart_lock) is type(restart_lock)
		restart_lock = prev.restart_lock
	except (AttributeError, AssertionError):
		pass

	global config
	config = server.load_config_simple(target_class=Config)
	if not config.enabled:
		server.logger.info('{} is disabled by config'.format(PLUGIN_METADATA.name))

	server.register_help_message('!!op', tr('help.op'), permission=config.permissions.op)
	server.register_help_message('!!restart', tr('help.restart', config.restart_delay), permission=config.permissions.restart)
	server.register_command(Literal('!!op').runs(give_op).precondition(Requirements.has_permission(config.permissions.op)))
	server.register_command(Literal('!!restart').runs(restart).precondition(Requirements.has_permission(config.permissions.restart)))
