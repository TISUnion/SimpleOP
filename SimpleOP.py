import time
from threading import Lock

from mcdreforged.api.all import *

PLUGIN_METADATA = {
	'id': 'simple_op',
	'version': '1.0.0',
	'name': 'Simple OP',
	'description': '!!op to get op, !!restart to restart the server',
	'author': 'Fallen_Breath',
	'link': 'https://github.com/MCDReforged/SimpleOP'
}

restart_lock = Lock()


@new_thread(PLUGIN_METADATA['name'] + ' - restart')
def restart(source: CommandSource):
	acq = restart_lock.acquire(blocking=False)
	if not acq:
		source.reply('已经在重启了')
		return
	try:
		for i in range(5):
			source.get_server().say(RText('{} 秒后重启服务器!'.format(5 - i), color=RColor.red))
			time.sleep(1)
		source.get_server().restart()
	finally:
		restart_lock.release()


def give_op(source: CommandSource):
	if isinstance(source, PlayerCommandSource):
		source.get_server().execute('op {}'.format(source.player))


def on_load(server: ServerInterface, prev):
	try:
		global restart_lock
		restart_lock = prev.restart_lock
	except AttributeError:
		pass

	server.register_help_message('!!op', '给我op')
	server.register_help_message('!!restart', '重启服务器，延迟5秒')
	server.register_command(Literal('!!op').runs(give_op))
	server.register_command(Literal('!!restart').runs(restart))
