import asyncio
import struct


# Default event handlers
async def _tlv_packetizer(reader):
    header = await reader.readexactly(3)
    pkt_type, pkt_len = struct.unpack(">BH", header)
    payload = await reader.readexactly(pkt_len)

    return header + payload


def _disconnect_callback(addr):
    print("Client %s disconnected" % str(addr))


def _connect_callback(addr):
    print("New connection from %s" % str(addr))


def _recv_callback(message):
    print("<- %s" % str(message))


def _send_callback(message):
    print("-> %s" % str(message))


# Server
class AsyncStreamServer:
    def __init__(self,
                 ip,
                 port,
                 connect_callback=None,
                 recv_callback=None,
                 send_callback=None,
                 disconnect_callback=None,
                 packetizer=_tlv_packetizer):
        self.server = None
        self.ip = ip
        self.port = port
        self.connect_callback = connect_callback or _connect_callback
        self.recv_callback = recv_callback or _recv_callback
        self.send_callback = send_callback or _send_callback
        self.disconnect_callback = disconnect_callback or _disconnect_callback
        self.packetizer = packetizer
        self.event_loop = asyncio.get_event_loop()
        self.streams = {}

    async def handle_new_stream(self, reader, writer):
        done = False
        client_addr = writer.get_extra_info('peername')
        self.streams[client_addr] = (reader, writer)  # TODO custom datastructure

        while not done:
            try:
                # Receive on socket
                pkt = await self.packetizer(reader)
                reply = await self.recv_callback(pkt)
                if reply is not None:
                    writer.write(reply)
                    self.send_callback(reply)
                    await writer.drain()
            except (asyncio.streams.IncompleteReadError, ConnectionResetError):
                self.disconnect_callback(client_addr)
                writer.close()
                del reader
                del writer
                del self.streams[client_addr]
                done = True

    def start(self):
        server_coroutine = asyncio.start_server(self.handle_new_stream, '127.0.0.1', 3884)
        self.server = self.event_loop.run_until_complete(server_coroutine)
        print('Serving on {}'.format(self.server.sockets[0].getsockname()))

    def stop(self):
        print('Closing server')
        self.server.close()
        self.event_loop.run_until_complete(self.server.wait_closed())
        self.event_loop.close()

