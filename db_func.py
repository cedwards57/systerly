from db import User, System, Message

def get_user(username):
    user = User.query.filter_by(username=username).first()
    return user

def verify_user(username,password):
    this_user = User.query.filter_by(username=username).first()
    if this_user != None:
        return password == this_user.password
    return False

def get_sys_name(username):
    this_user = User.query.filter_by(username=username).first()
    return this_user.sysname

def get_message(message_id):
    return Message.query.filter_by(id=message_id).first()

def get_messages(username):
    messages = Message.query.filter_by(username=username).all()
    return [message.id for message in messages]

def get_messages_from(username,alter_id):
    messages = Message.query.filter_by(username=username,alter_id=alter_id).all()
    return [message.id for message in messages]

def get_alter(alter_id):
    return System.query.filter_by(id=alter_id).first()

def get_alter_id(username,alter_name):
    return System.query.filter_by(username=username,alter=alter_name).first()

def get_alter_name(alter_id):
    alter = System.query.filter_by(id=alter_id).first()
    return alter.alter

def get_alters(username):
    sys = System.query.filter_by(username=username).all()
    return [i.id for i in sys]

def is_archived(message_id):
    message = Message.query.filter_by(id=message_id).first()
    return message.archived

def set_user(username,password,sysname):
    return User(username=username, password=password, sysname=sysname)

def set_alter(username,alter):
    high = System.query.order_by(System.id.desc()).first()
    if high == None:
        next = 0
    else:
        next = high.id + 1
    return System(id=next,username=username, alter=alter)

def set_message(username,alter_id,message):
    high = Message.query.order_by(Message.id.desc()).first()
    if high == None:
        next = 0
    else:
        next = high.id + 1
    return Message(id=next,username=username, alter_id=alter_id, message=message, archived=False)