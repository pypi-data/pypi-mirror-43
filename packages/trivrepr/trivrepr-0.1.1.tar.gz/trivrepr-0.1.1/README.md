# trivrepr - a helper for generating repr() strings

## Description

The trivrepr module contains the TrivialRepr class that may be
derived from to provide an implementation of `__repr__()` for
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

The trivrepr module is fully typed.

## Version history

- 0.1.1 (2019-03-07)
  - Add the news.py tool for preparing the distribution changelog.
  - Correct the project's homepage URL.
  - Use setuptools-git to include more files in the sdist tarball.

- 0.1.0 (2019-03-06)
  - Initial public release.

## Author

Peter Pentchev <roam@ringlet.net>

## Copyright and license

    Copyright (c) 2019  Peter Pentchev <roam@ringlet.net>
    All rights reserved.
    
    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions
    are met:
    1. Redistributions of source code must retain the above copyright
       notice, this list of conditions and the following disclaimer.
    2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.
    
    THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
    ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
    FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
    OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
    HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
    LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
    OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
    SUCH DAMAGE.
