import sys, os

import uvicorn

import socketio
# create a Socket.IO server
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins = 'http://localhost:8000')

# wrap with ASGI application
app = socketio.ASGIApp(sio)

"""
class ChatServer(socketio.AsyncNamespace):
    def on_connect(self, sid, environ):
        print('Somebody connected')
        pass

    def on_disconnect(self, sid):
        print('Somebody disconnected')
        pass

    async def on_chat_message(self, sid, data):
        print('Inside on_chat_message', data)
        await self.emit('my_response', data)

sio.register_namespace(ChatServer('/chat'))


"""
@sio.event
def connect(sid, environ):
    print('connect ', sid)
    

@sio.event
async def begin_chat(sid, room, user):
    sio.enter_room(sid, room)
    if room == 'Lobby':
        data = dict(to_room=room, isMine=True, author='Websaw Chat Server',
                    text='%s has entered the %s.  Please be nice' % (user, room))
    else:
        data = dict(to_room=room, isMine=True, author='Websaw Chat Server',
                text='%s has entered the %s room.  Please be nice' % (user, room))
    await sio.emit('message', data, room)  
    print('should have sent message from join chat ', data)


@sio.event
async def leave_chat(sid, room, user):
    sio.leave_room(sid, 'chat_users')
    if room == 'Lobby':
        data = dict(to_room=room, isMine=True, author='Websaw Chat Server',
                    text='%s has left the %s. Hope to see you soon' % (user, room))
    else:
        data = dict(to_room=room, isMine=True, author='Websaw Chat Server',
                text='%s has left %s. Hope to see you soon' % (user, room))
    
    await sio.emit('message', data, room)  
    print('should have sent message from leave chat ', data)

@sio.event
async def in_message(sid, data):
    print('message received', sid, data)
    await sio.emit('message', data, room=data['to_room'], skip_sid = sid)  
    print('sent "message', sid, data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == "__main__":
    # https://www.fatalerrors.org/a/uvicorn-a-lightweight-and-fast-python-asgi-framework.html
    uvicorn.run(app=app, host="127.0.0.1", port=8080, log_level="info")
    #uvicorn.run(
    #    app=SERV_APP_FILE,
    #    host=HOST,
    #    port=PORT,
    #    reload=True,
    #    workers=1,
    #    debug=False,
    #)