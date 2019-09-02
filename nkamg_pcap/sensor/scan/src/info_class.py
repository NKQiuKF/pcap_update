#!/usr/bin/env python
# coding=utf-8


class Port(object):
    __slots__ = ()

    def __init__(self):
        self.protocol = self.portid = self.state = self.name = ''

    # return a csv format string
    # See csv pattern in file 'csv.conf'
    def to_csv(self):
        port_info = (self.portid, self.protocol, self.state, self.name)
        return port_info

    @property
    def portid(self):
        return self._portid
    @portid.setter
    def portid(self, integer):
        try:
            self._portid = int(integer)
        except:
            self._portid = ''

    @property
    def protocol(self):
        return self._protocol
    @protocol.setter
    def protocol(self, string):
        self._protocol = str(string)

    @property
    def state(self):
        return self._state
    @state.setter
    def state(self, string):
        self._state = str(string)

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, string):
        self._name = str(string)


class Host():
    __slots__ = ()

    def __init__(self):
        self.ip = self.os = ''
        port = Port()
        self.ports = [port]

    def to_csv(self):
        host_info = []
        for port in self.ports:
            line = [self.ip, self.os]
            line.extend(port.to_csv())
            line = tuple(line)
            host_info.append(line)
        return host_info

    @property
    def ip(self):
        return self._ip
    @ip.setter
    def ip(self, string):
        self._ip = str(string)

    @property
    def os(self):
        return self._os
    @os.setter
    def os(self, string):
        self._os = str(string)

    @property
    def ports(self):
        return self._ports
    @ports.setter
    def ports(self, ports):
        self._ports = ports
