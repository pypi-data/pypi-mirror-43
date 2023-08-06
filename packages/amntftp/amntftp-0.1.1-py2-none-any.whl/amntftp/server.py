import consts
import kthread
import lair3.sockets
import os
import select
import struct
import time

def get_string(data):
    """Returns a null-trimmed string from the provided value"""
    try:
        idx = str(data).index("\x00")
    except Exception:
        return None
    return data[0:idx]

class TFTPServer(object):
    """TFTP server class"""
    def __init__(self, port = 69, listen_host = '0.0.0.0', context = {}):
        self.listen_host = listen_host
        self.listen_port = port
        self.context = context
        self.sock = None
        self.shutting_down = False
        self.output_dir = None
        self.tftproot = None
        
        self.files = []
        self.uploaded = []
        self.transfers = []
        self.thread = None
        self.incoming_file_hook = None

    def __repr__(self):
        repstr = str(super(TFTPServer, self).__repr__()[:-1])
        return str(repstr + " {}:{}>".format(self.listen_host, self.listen_port))

    def start(self):
        """Starts the TFTP server"""
        self.sock = lair3.sockets.UdpSock.create(LocalHost = self.listen_host, LocalPort = self.listen_port, Context = {})

        self.thread = kthread.KThread(name = "TFTPServerMonitor", target = self.monitor_socket)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        """Stops the TFTP server"""
        self.shutting_down = True
        start = time.time()
        while len(self.transfers) > 0:
            # give it some time to complete any remaining transfers
            time.sleep(0.5)
            dur = time.time() - start
            if (dur > 30):
                break

        del self.files[:]
        if self.thread is not None:
            self.thread.terminate()
        try:
            self.sock.close()
        except Exception as e:
            pass

    def __del__(self):
        self.stop()

    def register_file(self, fn, content, once = False):
        """Register a file for a TFTP client to request"""
        self.files.append({'name':fn,'data':content,'once':once})

    def set_tftproot(self, rootdir):
        """Register a directory to serve files from"""
        if os.path.isdir(rootdir):
            self.tftproot = rootdir

    def set_output_dir(self, outdir):
        """Register a directory to store uploaded files"""
        if os.path.isdir(outdir):
            self.output_dir = outdir

    def send_error(self, fromaddr, num):
        """Send error packet with code and message"""
        if (num < 1 or num >= len(consts.ERRCODES)):
            # out of array bounds...
            return

        pkt = struct.pack('>HH', consts.OpError, num)
        pkt += consts.ERRCODES[num]
        pkt += '\x00'
        self.send_packet(fromaddr, pkt)

    def send_packet(self, fromaddr, pkt):
        """Sends a single packet to the specified client"""
        self.sock.sendto(pkt, fromaddr[0], fromaddr[1])

    def find_file(self, fname):
        """Retrieve the dict that references a file name"""

        # check the files list first
        for f in self.files:
            if fname == f['name']:
                return f

        # if tftproot is specified and the file was not found, search the directory for a match
        if self.tftproot is not None:
            return self.find_file_in_root(fname)

        # I didn't find shit
        return None

    def find_file_in_root(self, fname):
        """Finds a file in the tftproot directory and adds a one-time entry to the files list"""
        fn = os.path.expanduser(os.path.join(self.tftproot, fname))

        if self.tftproot in fn and fn.index(self.tftproot) != 0:
            return None

        if os.path.isfile(fn) == False:
            return None

        # read the file and register it with once = True
        data = None
        with open(fn, "rb") as fd:
            data = fd.read()

        self.register_file(fname, data, True)

        # return last dict in the list
        return self.files[-1]

    def find_transfer(self, typ, fromaddr, block):
        for tr in self.transfers:
            if (tr['type'] == typ and tr['from'] == fromaddr and tr['block'] == block):
                return tr

        return None

    def save_output(self, tr):
        self.uploaded.append(tr['file'])
        
        if self.incoming_file_hook is not None:
            return self.incoming_file_hook(tr)

        if self.output_dir is not None:
            try:
                fn = os.path.split(tr['file']['name'])[-1]

                if fn is not None:
                    fn = os.path.join(os.path.abspath(self.output_dir), fn)
                    with open(fn, "wb") as fd:
                        fd.write(tr['file']['data'])
            except Exception as e:
                pass

    def check_retransmission(self, tr):
        elapsed = time.time() - tr['last_sent']
        if (elapsed >= tr['timeout']):
            if (tr['retries'] < 3):
                tr['last_sent'] = None
                tr['retries'] = tr['retries'] + 1
            else:
                self.transfers.remove(tr)

    def monitor_socket(self):
        """Polls the socket for pending read/write activity"""
        while True:
            rds = [self.sock]
            wds = []
            # check if socket is ready to write if there are pending transactions
            for tr in self.transfers:
                if 'last_sent' not in tr or not tr['last_sent']:
                    wds.append(self.sock)
                    break

            eds = [self.sock]

            r,w,e = select.select(rds, wds, eds, 1)

            if r is not None and len(r) > 0 and self.sock in r:
                buf, host, port = self.sock.recvfrom(65535)
                fromaddr = (host, port)
                self.dispatch_request(fromaddr, buf)

            # handle transfers
            for tr in self.transfers:
                if tr['type'] == consts.OpRead:
                    if 'last_sent' in tr and tr['last_sent'] is not None:
                        self.check_retransmission(tr)
                    elif w is not None and len(w) > 0 and self.sock in w:
                        # no ACK needs to be sent, send data
                        chunk = tr['file']['data'][tr['offset']:(tr['offset'] + tr['blksize'])]
                        if chunk is not None and len(chunk) >= 0:
                            pkt = struct.pack('>HH', consts.OpData, tr['block'])
                            pkt += chunk

                            self.send_packet(tr['from'], pkt)
                            tr['last_sent'] = time.time()

                            # handle single-use files
                            if 'once' in tr['file'] and tr['file']['once'] == True:
                                tr['file']['started'] = True
                    else:
                        # might need to send one last ACK before we disconnect...
                        pass

                else:
                    if 'last_sent' in tr and tr['last_sent'] is not None:
                        self.check_retransmission(tr)
                    elif w is not None and len(w) > 0 and self.sock in w:
                        # send ACK
                        pkt = struct.pack('>HH', consts.OpAck, tr['block'])
                        self.send_packet(tr['from'], pkt)
                        tr['last_sent'] = time.time()

                        if 'last_size' in tr and tr['last_size'] is not None and tr['last_size'] < tr['blksize']:
                            self.save_output(tr)
                            self.transfers.remove(tr)


    def next_block(self, tr):
        tr['block'] = tr['block'] + 1
        tr['last_sent'] = None
        tr['retries'] = 0

    def dispatch_request(self, fromaddr, buf):
        """Packet handler function"""
        if len(buf) < 2:
            return

        op = struct.unpack('>H', buf[0:2])[0]
        buf = buf[2:]

        if op == consts.OpRead:
            fn = get_string(buf)
            if fn is not None:
                buf = buf[len(fn) + 1:]

            mode = get_string(buf)
            if mode is not None:
                buf = buf[len(mode) + 1:]

            file = self.find_file(fn)
            if self.shutting_down == False and file is not None:
                if file['once'] == True and 'started' in file and file['started'] == True:
                    self.send_error(fromaddr, consts.ErrFileNotFound)
                else:
                    transfer = {
                        'type':consts.OpRead,
                        'from':fromaddr,
                        'file':file,
                        'block':1,
                        'blksize':512,
                        'offset':0,
                        'timeout':3,
                        'last_sent':None,
                        'retries':0
                        }

                    self.process_options(fromaddr, buf, transfer)
                    self.transfers.append(transfer)
            else:
                self.send_error(fromaddr, consts.ErrFileNotFound)
        elif op == consts.OpWrite:
            fn = get_string(buf)
            if fn is not None:
                buf = buf[len(fn) + 1:]

            mode = get_string(buf)
            if mode is not None:
                buf = buf[len(mode) + 1:]

            if self.shutting_down == False:
                transfer = {
                    'type':consts.OpWrite,
                    'from':fromaddr,
                    'file':{'name':fn,'data':''},
                    'block':0,
                    'blksize':512,
                    'timeout':3,
                    'last_sent':None,
                    'retries':0
                }

                self.process_options(fromaddr, buf, transfer)
                self.transfers.append(transfer)
            else:
                self.send_error(fromaddr, consts.ErrIllegalOperation)
        elif op == consts.OpAck:
            block = struct.unpack('>H', buf[0:2])[0]
            tr = self.find_transfer(consts.OpRead, fromaddr, block)

            if tr is None:
                if block == 0:
                    return
                self.send_error(fromaddr, consts.ErrUnknownTransferId)
            else:
                tr['offset'] = tr['offset'] + tr['blksize']
                self.next_block(tr)

                if (tr['offset'] > len(tr['file']['data'])):
                    self.transfers.remove(tr)

                    if tr['file']['once'] == True:
                        self.files.remove(tr['file'])
        elif op == consts.OpData:
            block = struct.unpack('>H', buf[0:2])[0]
            data = buf[2:]

            tr = self.find_transfer(consts.OpWrite, fromaddr, (block - 1))
            if tr is None:
                self.send_error(fromaddr, consts.ErrUnknownTransferId)
            else:
                tr['file']['data'] = tr['file']['data'] + data
                tr['last_size'] = len(data)
                self.next_block(tr)
        else:
            self.send_error(fromaddr, consts.ErrAccessViolation)

    def process_options(self, fromaddr, buf, tr):
        found = 0
        to_ack = []

        while len(buf) >= 4:
            opt = get_string(buf)
            if opt is not None:
                buf = buf[len(opt) + 1:]
            else:
                break

            val = get_string(buf)
            if val is not None:
                buf = buf[len(val) + 1:]
            else:
                break

            found += 1

            opt = opt.lower()

            if opt == 'blksize':
                val = int(val)
                if val > 0:
                    tr['blksize'] = val
                    to_ack.append([opt, str(val)])

            elif opt == 'timeout':
                val = int(val)
                if val >= 1 and val <= 255:
                    tr['timeout'] = val
                    to_ack.append([opt, str(val)])

            elif opt == 'tsize':
                if tr['type'] == consts.OpRead:
                    length = len(tr['file']['data'])
                else:
                    val = int(val)
                    length = val
                to_ack.append([opt, str(length)])

        if len(to_ack) < 1:
            return

        data = struct.pack('>H', consts.OpOptAck)
        for el in to_ack:
            data += el[0] + "\x00" + el[1] + "\x00"
   
        self.send_packet(fromaddr, data)