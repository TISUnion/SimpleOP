# -*- coding: utf-8 -*-


def on_info(server, info):
	if info.is_user and info.content == '!!op':
		server.execute('op ' + info.player)
	if info.content == '!!restart':
		server.restart()
