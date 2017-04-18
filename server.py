# A license server clone

import socket
import threading
import Queue
import time
import lic

# create a socket to listen for new connections
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# let socket be immidately reused
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind socket to port
s.bind(("", 50007))
# set socket to non blocking; this is weird on BSDs(osx)
# s.setblocking(False)
# listen!
s.listen(1)

gq = Queue.Queue()
lock = threading.Lock()
clients = []
usersOnline = []

#TODO: globals?
# the key is the productkey

class run_server(threading.Thread):
    def __init__ (self, conn, gq):
        self.conn = conn
        self.socket = socket
        self.gq = gq
        threading.Thread.__init__(self)

    def run(self):
        print threading.currentThread().getName()
        print "global queue is", self.gq
        # lock and update the clients list
        lock.acquire()
        clients.append(self)
        lock.release()
        l = lic.LicServ()
        host = str(self.conn.getpeername())
        self.conn.send("Ready for data: ")
        self.data = self.conn.recv(1024).decode("latin1")
        self.textin = str(self.data).strip()
        # rpk is Requested Product Key
        rpk = self.textin
        if l.checkLicenseAvail(host, rpk):
            l.checkOutLic(host, rpk)
            print l.checkedOut
            print l.totalLicenses
        else:
            self.conn.send("There is no license available for %s\n" %rpk )
        self.conn.send("***************************************\n")
        self.conn.send("You got a lic " + host + rpk + "\n")
        self.conn.send("***************************************\n")

        while 1:
            # take only latin strings, cuz italy
            self.data = self.conn.recv(1024).decode("latin1")
            if not self.data: break
            #if not self.gq.empty():
            #    print "A message is in the queue"
            #    shoutMsg = self.gq.get()
            #    self.conn.send(str(shoutMsg))
            #    self.gq.task_done()
            # we need to strip to remove whatever magic comes from telnet
            self.textin = str(self.data).strip()
            print "received ", self.textin, "from client"

        lock.acquire()
        clients.remove(self)
        lock.release()
        self.conn.close()

threads = []
while 1:
    conn, addr = s.accept()
    print "connected", addr
    lq = Queue.Queue()
    world = run_server(conn, gq)
    world.start()
    threads.append(world)
    time.sleep(0.1)

s.close()
