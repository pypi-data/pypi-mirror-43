# Copyright (c) 2019  Peter Pentchev <roam@ringlet.net>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

""" Helper module for constructing repr() strings.

The trivrepr module contains the TrivialRepr class that may be
derived from to provide an implementation of __repr__() for
simple classes that have all their attributes passed directly to
the constructor.

    import trivrepr

    class KeyValue(trivrepr.TrivialRepr):
        def __init__(self, key, value, more='hi'):
            super(KeyValue, self).__init__()
            self.key = key
            self.value = value
            self.more = more

    kv = KeyValue(key='key', value='val')
    print(repr(kv))

This program will output:

    KeyValue(key='key', value='val', more='hi')

The trivrepr module is fully typed. """


import inspect


try:
    from typing import List

    _TYPING_USED = (List,)
except ImportError:
    pass


VERSION = '0.1.1'

_GET_SPEC = getattr(inspect, 'getfullargspec', getattr(inspect, 'getargspec'))


class TrivialRepr(object):
    # pylint: disable=too-few-public-methods
    """ Helper class that generates a repr() string.

    Derived classes should take care that all arguments to the __init__()
    method correspond to object attributes with exactly the same names. """

    def __repr__(self):
        # type: (TrivialRepr) -> str
        """ Provide a Python-esque representation of the object. """
        attrlist = _GET_SPEC(self.__init__).args[1:]  # type: ignore
        return '{tname}({attrs})'.format(
            tname=type(self).__name__,
            attrs=', '.join([
                '{name}={value}'.format(name=name,
                                        value=repr(getattr(self, name)))
                for name in attrlist
            ]))
