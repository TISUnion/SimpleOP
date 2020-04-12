# SimpleOP

这是一个可以在你自己的Minecraft服务器中在服务端进行``OP权限获取``、``重启服务器``、``关闭服务器``的插件，需配合[MCDReforged](https://github.com/Fallen-Breath/MCDReforged)使用。

使用``!!op``来给你op权限（记得自己deop掉）

使用``!!restart``来重启服务器

使用``!!stop``来关闭服务器

重启和关闭服务器的时间可以自由设定，打开``simpleOP.py``文件，在最顶上有个``waiting_time``，将这个数字改成任意正整数即可，单位是秒

如果你不需要``!!stop``（避免熊孩子滥用），你可以将以下内容删除或注释掉

```python
if info.content == '!!stop':
	stop_message=''
	while True:
		stop_message='Server will close in {} second(s), please save your work!'.format(time_left)
		server.say(stop_message)
		if(time_left==0):
			server.stop()
			break
		else:
			time.sleep(1)
			time_left=time_left-1
```

---

This is a plugin which can help you get OP permission, restart your server, close your server in game. Just input the following contents. Remember, using [MCDReforged](https://github.com/Fallen-Breath/MCDReforged) is essentials.

`!!op` give you op

`!!restart` restart the server

``!!stop`` stop the server

The time can be set at the line 3, just edit the number behind the variable ``waiting_time`` in seconds.

If you want to disable ``!!stop`` command, you can delete or remark the content below

```python
if info.content == '!!stop':
	stop_message=''
	while True:
		stop_message='Server will close in {} second(s), please save your work!'.format(time_left)
		server.say(stop_message)
		if(time_left==0):
			server.stop()
			break
		else:
			time.sleep(1)
			time_left=time_left-1
```



