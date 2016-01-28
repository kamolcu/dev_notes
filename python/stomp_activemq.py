# pip install stomp.py
import stomp
import time


class MessageListener(stomp.ConnectionListener):

    def __init__(self, con=None):
        self.con = con

    def on_error(self, headers, message):
        print('received an error "%s"' % message)

    def on_message(self, headers, message):
        print('received a message "%s" and headers "%s"' % (message, headers))
        if(self.con is not None):
            self.con.ack(headers["message-id"], headers["subscription"])


con = stomp.Connection([('ba-server.com', 61613)])
con.set_listener('', MessageListener(con=con))
con.start()
con.connect('admin', 'admin', wait=True)
con.subscribe(destination='/queue/test', id=1, ack='client-individual')

while True:
    time.sleep(1)
