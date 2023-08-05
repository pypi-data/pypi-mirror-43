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

""" Some trivial tests for the trivial repr handler. """

import trivrepr


class Base(trivrepr.TrivialRepr):
    """ A test class. """

    def __init__(self, num):
        # type: (Base, int) -> None
        """ Store a number into an object. """
        super(Base, self).__init__()
        self.num = num

    def increment(self):
        # type: (Base) -> None
        """ Increment the stored number. """
        self.num = self.num + 1

    def query(self):
        # type: (Base) -> int
        """ Return the stored number. """
        return self.num


class Derived(Base):
    """ Another test class. """

    def __init__(self, num, stri):
        # type: (Derived, int, str) -> None
        """ Store a number and a string into an object. """
        super(Derived, self).__init__(num)
        self.stri = stri

    def trim(self):
        # type: (Derived) -> None
        """ Remove whitespace from the start and end of the string. """
        self.stri = self.stri.strip()

    def announce(self):
        # type: (Derived) -> str
        """ Return the string and the number. """
        return '{stri}: {num}'.format(stri=self.stri, num=self.num)


def test_base():
    # type: () -> None
    """ Test the handling of the base class. """
    base = Base(17)
    assert base.query() == 17

    rep = repr(base)
    assert rep.startswith('Base(')
    assert 'num=17' in rep
    assert ',' not in rep

    base.increment()
    assert base.query() == 18

    rep = repr(base)
    assert rep.startswith('Base(')
    assert 'num=18' in rep
    assert ',' not in rep


def test_derived():
    # type: () -> None
    """ Test the handling of the derived class. """
    untrimmed = ' hi \t'
    trimmed = untrimmed.strip()

    derived = Derived(17, untrimmed)
    assert derived.query() == 17
    assert derived.announce() == untrimmed + ': 17'

    rep = repr(derived)
    assert rep.startswith('Derived(')
    assert 'num=17' in rep
    assert 'stri={stri}'.format(stri=repr(untrimmed)) in rep
    assert len(rep.split(', ')) == 2

    derived.increment()
    derived.trim()
    assert derived.query() == 18
    assert derived.announce() == trimmed + ': 18'

    rep = repr(derived)
    assert rep.startswith('Derived(')
    assert 'num=18' in rep
    assert 'stri={stri}'.format(stri=repr(trimmed)) in rep
    assert len(rep.split(', ')) == 2
