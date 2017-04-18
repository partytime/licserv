# A license server clone

import socket
import threading
import Queue
import time

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

# the key is the productkey
totalLicenses = {"soft1":10,"soft2":1,"soft3":2}
checkedOut = {"soft1":0,"soft2":0,"soft3":0}
#checkedOut = {"soft1":["10.82.4.5","10.82.4.7"]}

class run_server(threading.Thread):
    def __init__ (self, conn, gq):
        self.conn = conn
        self.socket = socket
        self.gq = gq
        threading.Thread.__init__(self)

    def checkLicenseAvail(host, productKey):
        # We already have a license checked out
        if host in checkedOut["productKey"]:
            return True
        elif len(checkedOut["productKey"]) < totalLicenses["productKey"]:
            return True


    ##def clientConn(self):
    def run(self):
        print threading.currentThread().getName()
        print "global queue is", self.gq
        # lock and update the clients list
        lock.acquire()
        clients.append(self)
        lock.release()
        #n = g.Navigation()
        #p = g.Player()
        self.conn.send("Ready for data: ")
        self.data = self.conn.recv(1024).decode("latin1")
        self.textin = str(self.data).strip()
        user = self.textin
        if not p.checkUserExists(user):
            self.conn.send("Your name doesn't seem to be on our list. Creating new user!\n")
            p.addUser(user, "A new user with no description")
        self.conn.send("***************************************\n")
        self.conn.send("WELCOME " + self.textin.upper() + "\n")
        if u.users[user]['wizard']:
            self.conn.send("It's a pleasure to see a managing wizard around.\n")
        self.conn.send("***************************************\n")
        self.conn.send("Enjoy the trip, my dear friend.\n")
        self.conn.send("(If you are lost, type 'help' for a command list)\n")
        self.conn.send("***************************************\n")
        lock.acquire()
        usersOnline.append(user)
        lock.release()

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
