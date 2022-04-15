from db import User, System

def get_user(username):
    return User.query.filter_by(username=username).first()

def verify_user(username,password):
    this_user = User.query.filter_by(username=username).first()
    if this_user != None:
        return password == this_user.password
    return False

def get_sys_name(username):
    this_user = User.query.filter_by(username=username).first()
    return this_user.sysname

def get_messages(username):
    messages = Message.query.filter_by(username=username).all()
    return [message.id for message in messages]

def get_messages_from(username,alter):
    messages = Message.query.filter_by(username=username,alter=alter).all()
    return [message.id for message in messages]

def get_alters(username):
    system = System.query.filter_by(username=username).all()
    return [s.alter for s in system]

def is_archived(message_id):
    message = Message.query.filter_by(id=message_id).first()
    return message.archived

def set_user(username,password,sysname):
    return User(username=username, password=password, sysname=sysname)

def set_alter(username,alter):
    return System(username=username, alter=alter)

def set_message(username,alter,message):
    return Message(username=username, alter=alter, message=message, archived=False)