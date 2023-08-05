#!/usr/bin/env python3
import socket
import selectors
import types

sel = selectors.DefaultSelector()

class socketClient(object):
    current_conns_id = 0
    break_flag = 0
    def __init__(self, host, port):
        self.host = host
        self.port = port
        socketClient.current_conns_id = socketClient.current_conns_id + 1
        self.conns_id = socketClient.current_conns_id
        self.__start_connections()


    def __start_connections(self):
        server_addr = (self.host, self.port)
        print("starting connection", self.conns_id, "to", server_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        self.sock = sock

    def send_data(self, binary_message, is_close=False):
        list = [binary_message]
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(
            connid=self.conns_id,
            msg_total=len(binary_message),
            recv_total=0,
            messages=list,
            outb=b"",
        )
        print(self.sock)
        sel.register(self.sock, events, data=data)

        try:
            while True:
                events = sel.select(timeout=1)
                if events:
                    for key, mask in events:
                        self.__service_connection(key, mask, is_close)
                if socketClient.break_flag == 1:
                    socketClient.break_flag = 0
                    break
        except Exception as e:
            print("Error occur in socket, exiting ", e)
        finally:
            sel.close()

    def __service_connection(self, key, mask, is_close):
        print("__service_connection in")
        #sock = self.sock
        data = key.data
        print(key)
        print(mask)
        if mask & selectors.EVENT_READ:
            recv_data = self.sock.recv(1024)  # Should be ready to read
            if recv_data:
                print("received", repr(recv_data), "from connection", data.connid)
                data.recv_total += len(recv_data)
                socketClient.break_flag = 1
            if is_close:
                print("unregister socket!")
                sel.unregister(self.sock)
                self.sock.close()
        if mask & selectors.EVENT_WRITE:
            if not data.outb and data.messages:
                data.outb = data.messages.pop(0)
            if data.outb:
                print("sending", repr(data.outb), "to connection", data.connid)
                sent = self.sock.send(data.outb)
                data.outb = data.outb[sent:]

if __name__ =='__main__':
    host = "127.0.0.1"
    port = 8888
    client = socketClient(host, port)
    client.send_data(b"222222SMMMs1")
    client.send_data(b"222222SMMMs2")
    client.send_data(b"222222SMMMs3", True)