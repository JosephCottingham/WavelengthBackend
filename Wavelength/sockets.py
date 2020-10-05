import json
from datetime import timedelta, datetime
from Wavelength import socketio, db

from .models.database.sql_models import Message, Room

from flask_socketio import join_room, leave_room, send


@socketio.on('connect')
def connection():
    print('connected')

#will implement later for now use join_room from bottom
@socketio.on('join')
def on_join(data):
    print('received join request')
    room = data['room']
    photo_url = data['photo_url']
    my_room = Room.query.filter_by(token=data['room'], finalized=True).first()
    if my_room != None:
        join_room(room)
        payload = {
            'message' : {
                'sent_datetime' : str(datetime.now()), 
                'gen_msg' : True,
                'username' : data['username'],
                'photo_url' : data['photo_url'],
                'msg' : '{0} has joined the room.'.format(data['username']),
                'video_url' : data['video_url'],
                'is_playing' : my_room.is_playing,
                'time' : my_room.time_stamp,
                'code' : 200
            }
        }
        send(json.dump(payload), room=data['room'])
    payload = {
            'message' : {
                'sent_datetime' : str(datetime.now()), 
                'code' : 404
            }
        }
    send(json.dump(payload), room=data['room'])

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    photo_url = data['photo_url']
    leave_room(room)
    payload = {
        'data' : {
            'sent_datetime' : str(datetime.now()),
            'gen_msg' : True,
            'name' : data['username'],
            'picture' : data['photo_url'],
            'message' : '{0} has left the room.'.format(data['username']),
            'code' : 200
        }
    }
    send(json.dump(payload), room=room)

@socketio.on('message')
def on_message(data):
    room = data['room']
    photo_url = data['photo_url']
    msg = data['msg']
    payload = {
        'data' : {
            'sent_datetime' : str(datetime.now()),
            'gen_msg' : False,
            'name' : data['username'],
            'picture' : data['photo_url'],
            'message' : msg,
            'code' : 200
        }
    }
    send(json.dump(payload), room=room)

@socketio.on('video_url_change')
def on_message(data):
    my_room = Room.query.filter_by(token=data['room'], finalized=True).first()
    if my_room != None:
        my_room.time_stamp = 0
        my_room.time_stamp_set_datetime = datetime.now()
        my_room.video_url = data['video_url']
        db.session.commit()
        payload = {
            'message' : {
                'sent_datetime' : str(datetime.now()),
                'gen_msg' : True,
                'name' : data['username'],
                'picture' : data['photo_url'],
                'message' : 'Video URL Changed',
                'video_url' : data['video_url'],
                'is_playing' : my_room.is_playing,
                'time' : my_room.time_stamp,
                'code' : 200
            }
        }
        send(json.dump(payload), room=data['room'])
    payload = {
            'message' : {
                'sent_datetime' : str(datetime.now()), 
                'code' : 404
            }
        }
    send(json.dump(payload), room=data['room'])

@socketio.on('video_loc_change')
def on_message(data):
    my_room = Room.query.filter_by(token=data['room'], finalized=True).first()
    if my_room != None:
        my_room.time_stamp = data['video_time']
        db.session.commit()
        my_room
        payload = {
            'message' : {
                'sent_datetime' : str(datetime.now()), 
                'gen_msg' : True,
                'name' : data['username'],
                'picture' : data['photo_url'],
                'message' : 'Video Location Changed',
                'time' : data['video_time'],
                'is_playing' : my_room.is_playing,
                'code' : 200
            }
        }
        send(json.dump(payload), room=data['room'])
    payload = {
            'message' : {
                'sent_datetime' : str(datetime.now()), 
                'code' : 404
            }
        }
    send(json.dump(payload), room=data['room'])
    
        
@socketio.on('video_pause')
def on_message(data):
    my_room = Room.query.filter_by(token=data['room'], finalized=True).first()
    if my_room != None:
        if my_room.is_playing:
            my_room.time_stamp = data['video_time'] 
            my_room.time_stamp_set_datetime = datetime.now()
            my_room.is_playing = False
            db.session.commit()
            payload = {
                'message' : {
                    'sent_datetime' : str(datetime.now()),
                    'gen_msg' : True,
                    'name' : data['username'],
                    'picture' : data['photo_url'],
                    'message' : '{0} Hit Pause'.format(data['username']),
                    'video_url' : data['video_url'],
                    'is_playing' : my_room.is_playing,
                    'code' : 200
                }
            }
            send(json.dump(payload), room=data['room'])
        payload = {
            'message' : {
                'sent_datetime' : str(datetime.now()), 
                'code' : 400
            }
        }
        send(json.dump(payload), room=data['room'])
    payload = {
            'message' : {
                'sent_datetime' : str(datetime.now()), 
                'code' : 404
            }
        }
    send(json.dump(payload), room=data['room'])

@socketio.on('video_play')
def on_message(data):
    my_room = Room.query.filter_by(token=data['room'], finalized=True).first()
    if my_room != None:
        if not my_room.is_playing:
            my_room.time_stamp = data['video_time'] 
            my_room.time_stamp_set_datetime = datetime.now()
            my_room.is_playing = True
            db.session.commit()
            payload = {
                'message' : {
                    'sent_datetime' : str(datetime.now()),
                    'gen_msg' : True,
                    'name' : data['username'],
                    'picture' : data['photo_url'],
                    'message' : '{0} Hit Play'.format(data['username']),
                    'video_url' : data['video_url'],
                    'is_playing' : my_room.is_playing,
                    'code' : 200
                }
            }
            send(json.dump(payload), room=data['room'])
        payload = {
            'message' : {
                'sent_datetime' : str(datetime.now()), 
                'code' : 400
            }
        }
        send(json.dump(payload), room=data['room'])
    payload = {
            'message' : {
                'sent_datetime' : str(datetime.now()), 
                'code' : 404
            }
        }
    send(json.dump(payload), room=data['room'])

@socketio.on('sync')
def on_sync(data):
    my_room = Room.query.filter_by(token=data['room'], finalized=True).first()
    if my_room != None:
        if my_room.time_stamp_set_datetime < (datetime.now()-timedelta(sec=10)):
            my_room.time_stamp_set_datetime = datetime.now()
            my_room.time_stamp = data['video_time'] 
            my_room.is_playing = data['is_playing']
            my_room.video_url = data['video_url']

            payload = {
                'message' : {
                    'sent_datetime' : str(datetime.now()), 
                    'gen_msg' : True,
                    'username' : data['username'],
                    'photo_url' : data['photo_url'],
                    'msg' : '{0} has synced video'.format(data['username']),
                    'video_url' : data['video_url'],
                    'is_playing' : data['is_playing'],
                    'time' : data['video_time'] ,
                    'code' : 200
                }
            }
            send(json.dump(payload), room=data['room'])
        payload = {
            'message' : {
                'sent_datetime' : str(datetime.now()), 
                'code' : 400
            }
        }
        send(json.dump(payload), room=data['room'])
    payload = {
            'message' : {
                'sent_datetime' : str(datetime.now()), 
                'code' : 404
            }
        }
    send(json.dump(payload), room=data['room'])


@socketio.on('join_room')
def join_room_and_notify(data):
    room = data['room']
    join_room(room)

    socketio.emit('connection_message', {
        'username': data['username'],
        'photo_url': data['photo_url'],
    }, room)

@socketio.on('chat_message')
def handle_message(data):
    socketio.emit('chat_message', {
        'username': data['username'],
        'photo_url': data['photo_url'],
        'message': data['message']
    })

@socketio.on('update_link')
def update_link(data):
    socketio.emit('update_link', {
        'link': data['link']
    })