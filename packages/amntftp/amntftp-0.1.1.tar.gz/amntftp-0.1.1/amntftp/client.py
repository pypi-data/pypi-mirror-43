# RFC 1350 - THE TFTP PROTOCOL
import consts
import kthread
import lair3.sockets
import os
import random
import re
import struct
import tempfile
import time

def get_string(data):
    """Returns a null-trimmed string from the provided value"""
    try:
        idx = str(data).index("\x00")
    except Exception:
        return None
    return data[0:idx]

def parse_tftp_response(string):
    if len(string) < 4:
        return None

    ret = struct.unpack(">HH", string[0:4])

    if len(string) == 4:
        # no data
        return (ret[0], ret[1], '')
    elif ret[0] == consts.OpData:
        # entire packet
        return (ret[0], ret[1], string[4:])
    else:
        # trim any nulls
        nulterm = get_string(string[4:])
        if nulterm is None:
            return (ret[0], ret[1], '')
        else:
            return (ret[0], ret[1], nulterm)

class TFTPClient(object):
    def __init__(self, **kwargs):
        self.threads = []
        self.server_sock = None
        self.client_sock = None
        self.complete = None
        self.recv_tempfile = None
        self.status = None
        if 'LocalHost' in kwargs and kwargs['LocalHost'] is not None:
            self.local_host = kwargs['LocalHost']
        else:
            self.local_host = "0.0.0.0"
        if 'LocalPort' in kwargs and kwargs['LocalPort'] is not None:
            self.local_port = kwargs['LocalPort']
        else:
            self.local_port = (1025 + random.randrange(0xffff - 1025))
        if 'PeerHost' in kwargs and kwargs['PeerHost'] is not None:
            self.peer_host = kwargs['PeerHost']
        else:
            raise ValueError("PeerHost is a required argument")
        if 'PeerPort' in kwargs and kwargs['PeerPort'] is not None:
            self.peer_port = kwargs['PeerPort']
        else:
            self.peer_port = 69
        if 'Context' in kwargs:
            self.context = kwargs['Context']
        else:
            self.context = None
        if 'LocalFile' in kwargs:
            self.local_file = str(kwargs['LocalFile'])
        else:
            self.local_file = None
        if 'RemoteFile' in kwargs and kwargs['RemoteFile'] is not None:
            self.remote_file = str(kwargs['RemoteFile'])
        else:
            if self.local_file is not None:
                self.remote_file = os.path.split(self.local_file)[-1]
            else:
                self.remote_file = None
        if 'Mode' in kwargs and kwargs['Mode'] is not None:
            self.mode = kwargs['Mode']
        else:
            self.mode = "octet"
        if 'Action' in kwargs and kwargs['Action'] is not None:
            self.action = kwargs['Action']
        else:
            raise ValueError("Action is a required argument")
        if 'BlockSize' in kwargs and kwargs['BlockSize'] is not None:
            self.block_size = kwargs['BlockSize']
        else:
            self.block_size = 512

    def start_server_socket(self, log_func = None):
        self.server_sock = lair3.sockets.UdpSock.create(LocalHost = self.local_host, LocalPort = self.local_port, Context = self.context, ReuseAddress = True)
        if self.server_sock is not None and log_func is not None:
            log_func("Started TFTP client listener on {}:{}".format(self.local_host, self.local_port))
        if log_func is not None:
            thr = kthread.KThread(name = "TFTPServerMonitor", target = self.monitor_server_sock, args = (lambda msg: log_func(msg),))
        else:
            thr = kthread.KThread(name = "TFTPServerMonitor", target = self.monitor_server_sock)
        thr.daemon = True
        thr.start()
        self.threads.append(thr)

    def monitor_server_sock(self, log_func = None):
        if log_func is not None:
            log_func("Listening for incoming ACKs")

        res = self.server_sock.recvfrom()
        if res is not None and len(res[0]) > 0 and None not in res:
            code, typ, data = parse_tftp_response(res[0])
            if code == consts.OpAck and self.action == 'upload':
                if log_func is not None:
                    if typ == 0:
                        log_func("WRQ accepted, sending file.")
                    self.send_data(res[1], res[2], lambda msg: log_func(msg))
                else:
                    self.send_data(res[1], res[2])
        
            elif code == consts.OpData and self.action == 'download':
                if log_func is not None:
                    self.recv_data(res[1], res[2], data, lambda msg: log_func(msg))
                else:
                    self.recv_data(res[1], res[2], data)
            elif code == consts.OpError:
                if log_func is not None:
                    log_func("TFTP Error (type: {}, message: '{}')".format(typ, data))
                self.status = {'error':[code,typ,data]}
            else:
                if log_func is not None:
                    log_func("Unknown TFTP response (code: {}, type: {}, message: '{}')".format(code, typ, data))
                self.status = {'error':[code,typ,data]}

        self.stop()

    def monitor_client_sock(self, log_func = None):
        res = self.client_sock.recvfrom()
        if res is not None and res[1] is not None:
            code, typ, data = parse_tftp_response(res[0])
            if log_func:
                log_func("Unexpected TFTP response (code: {}, type: {}, message: '{}')".format(code, typ, data))
            self.status = {'error':[code,typ,data]}
            self.stop()

    def stop(self):
        self.complete = True
        try:
            self.server_sock.close()
            self.client_sock.close()
            self.server_sock = None
            self.client_sock = None
            for t in self.threads:
                t.kill()
        except Exception:
            return None

    def __del__(self):
        self.stop()

    def rrq_packet(self):
        return struct.pack(">H", consts.OpRead) + self.remote_file + "\x00" + self.mode + "\x00"

    def ack_packet(self, blockn = 0):
        return struct.pack(">HH", consts.OpAck, blockn)

    def send_read_request(self, log_func = None):
        self.status = None
        self.complete = False
        if log_func:
            self.start_server_socket(lambda msg: log_func(msg))
        else:
            self.start_server_socket()
        self.client_sock = lair3.sockets.UdpSock.create(PeerHost = self.peer_host, PeerPort = self.peer_port, LocalHost = self.local_host, LocalPort = self.local_port, Context = self.context, ReuseAddress = True)
        self.client_sock.sendto(self.rrq_packet(), self.peer_host, self.peer_port)
        if log_func:
            thr = kthread.KThread(name = "TFTPClientMonitor", target = self.monitor_client_sock, args = (lambda msg: log_func(msg),))
        else:
            thr = kthread.KThread(name = "TFTPClientMonitor", target = self.monitor_client_sock)
        thr.daemon = True
        thr.start()
        self.threads.append(thr)
        while self.complete != True:
            time.sleep(0.50)
            continue
        return self.status

    def recv_data(self, host, port, first_block, log_func = None):
        # see if we can open a writable file, otherwise use a temp
        try:
            self.recv_tempfile = open(self.local_file, "wb")
        except Exception:
            tmpfd, self.local_file = tempfile.mkstemp(prefix = "amntftp")
            self.recv_tempfile = os.fdopen(tmpfd, "wb")

        recvd_blocks = 1
        if log_func:
            log_func("Source file: {}, destination file: {}".format(self.remote_file, self.local_file))
            log_func("Received and ACKed {} bytes in block {}".format(len(first_block), recvd_blocks))
            self.write_and_ack_data(first_block, 1, host, port, lambda msg: log_func(msg))
        else:
            self.write_and_ack_data(first_block, 1, host, port)
        curr_block = first_block
        while len(curr_block) == 512:
            res = self.server_sock.recvfrom()
            if res is not None and len(res[0]) > 0:
                code, blockn, curr_block = parse_tftp_response(res[0])
                if code == 3:
                    if log_func:
                        self.write_and_ack_data(curr_block, blockn, host, port, lambda msg: log_func(msg))
                    else:
                        self.write_and_ack_data(curr_block, blockn, host, port)
                    recvd_blocks += 1
                else:
                    if log_func:
                        log_func("Unexpected TFTP response (code: {}, type: {}, message: '{}')".format(code, blockn, curr_block))
                    self.stop()
        if log_func:
            log_func("Transferred {} bytes in {} blocks, download complete.".format(self.recv_tempfile.tell(), recvd_blocks))
        self.status = {'success':[self.local_file, self.remote_file, self.recv_tempfile.tell(), recvd_blocks]}
        self.recv_tempfile.close()
        self.stop()  

    def write_and_ack_data(self, data, blockn, host, port, log_func = None):
        self.recv_tempfile.write(data)
        self.recv_tempfile.flush()
        req = self.ack_packet(blockn)
        self.server_sock.sendto(req, host, port)
        if log_func:
            log_func("Received and ACKed {} bytes in block {}".format(len(data), blockn))

    def wrq_packet(self):
        return struct.pack(">H", consts.OpWrite) + self.remote_file + "\x00" + self.mode + "\x00"

    def blockify_data(self):
        if self.local_file is None:
            return []

        mach = re.search(r'^DATA:(.*)', self.local_file, re.MULTILINE)
        if mach is not None:
            data = mach.group(1)
        elif os.path.isfile(self.local_file) == True:
            try:
                with open(self.local_file, "rb") as f:
                    data = f.read()
            except Exception:
                return []
        else:
            return []

        data_blox = re.findall(r'.{1,' + ('%d' % (self.block_size)) + r'}', data, re.MULTILINE | re.DOTALL)
        if len(data_blox) > 1 and len(data_blox[-1]) == 0:
            data_blox.pop()

        return data_blox

    def send_write_request(self, log_func = None):
        self.status = None
        self.complete = False
        if log_func:
            self.start_server_socket(lambda msg: log_func(msg))
        else:
            self.start_server_socket()
        self.client_sock = lair3.sockets.UdpSock.create(PeerHost = self.peer_host, PeerPort = self.peer_port, LocalHost = self.local_host, LocalPort = self.local_port, Context = self.context, ReuseAddress = True)
        self.client_sock.sendto(self.wrq_packet(), self.peer_host, self.peer_port)

        if log_func:
            thr = kthread.KThread(name = "TFTPClientMonitor", target = self.monitor_client_sock, args = (lambda msg: log_func(msg),))
        else:
            thr = kthread.KThread(name = "TFTPClientMonitor", target = self.monitor_client_sock)
        thr.daemon = True
        thr.start()
        self.threads.append(thr)

        while self.complete != True:
            time.sleep(0.50)
            continue

        return self.status

    def send_data(self, host, port, log_func = None):
        self.status = {'write_allowed':True}
        data_blox = self.blockify_data()
        if data_blox is None or len(data_blox) == 0:
            if log_func:
                log_func("No data to send.")
            self.status = {'success':[self.local_file, self.local_file, 0, 0]}
            return None

        sent_data = 0
        sent_blox = 0
        send_retries = 0
        xpectd_blox = len(data_blox)
        xpectd_len = len("".join(data_blox))
        if log_func:
            if re.search(r'^DATA:', self.local_file) is not None:
                log_func("Source file: {}, destination file: {}".format("(DATA)", self.remote_file))
            else:
                log_func("Source file: {}, destination file: {}".format(self.local_file, self.remote_file))
            log_func("Sending {} bytes ({} blocks)".format(xpectd_len, xpectd_blox))

        for idx, data_block in enumerate(data_blox):
            while True:
                req = struct.pack(">HH", consts.OpData, idx + 1) + data_block
                if self.server_sock.sendto(req, host, port) <= 0:
                    send_retries += 1
                    if send_retries > 100:
                        break
                    else:
                        continue
                send_retries = 0
                res = self.server_sock.recvfrom()
                if res is not None and len(res[0]) > 0:
                    code, typ, msg = parse_tftp_response(res[0])
                    if code == 4:
                        if typ == idx + 1:
                            sent_blox += 1
                            sent_data += len(data_block)
                            if log_func:
                                log_func("Sent {} bytes in block {}".format(len(data_block), idx + 1))
                            break
                        else:
                            continue
                    else:
                        if log_func:
                            log_func("Unexpected TFTP response (code: {}, type: {}, message: '{}')".format(code, typ, msg))
                        break

        if send_retries > 100:
            if log_func:
                log_func("Exceeded retry limit")

        if log_func:
            if sent_data == xpectd_len:
                log_func("Transferred {} bytes in {} blocks; upload complete.".format(sent_data, sent_blox))
            else:
                log_func("Incomplete upload; sent {} / {} bytes ({} / {} blocks)".format(sent_data, xpectd_len, sent_blox, xpectd_blox))

        if sent_data == xpectd_len:
            self.status = {'success': [self.local_file, self.remote_file, sent_data, sent_blox]}
