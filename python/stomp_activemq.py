# pip install stomp.py
import stomp
import time

class MessageListener(stomp.ConnectionListener):

    def on_error(self, headers, message):
        print('received an error "%s"' % message)

    def on_message(self, headers, message):
        print('received a message "%s"' % message)

con = stomp.Connection([('ba-server.com', 61613)])
con.set_listener('', MessageListener())
con.start()
con.connect('admin', 'admin', wait=True)
con.subscribe(destination='/queue/test', id=1, ack='auto')

while True:
    time.sleep(1)
