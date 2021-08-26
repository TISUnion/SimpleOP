import time
from threading import Lock

from mcdreforged.api.all import *


class Config(Serializable):
	restart_delay: int = 5


PLUGIN_METADATA = ServerInterface.get_instance().as_plugin_server_interface().get_self_metadata()
restart_lock = Lock()
config = Config.get_default()


def tr(translation_key: str, *args, **kwargs) -> RTextMCDRTranslation:
	return ServerInterface.get_instance().rtr('{}.{}'.format(PLUGIN_METADATA.id, translation_key), *args, **kwargs)


@new_thread(PLUGIN_METADATA.name + ' - restart')
def restart(source: CommandSource):
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
	server.register_help_message('!!op', tr('help.op'))
	server.register_help_message('!!restart', tr('help.restart', config.restart_delay))
	server.register_command(Literal('!!op').runs(give_op))
	server.register_command(Literal('!!restart').runs(restart))
