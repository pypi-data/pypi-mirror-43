pylresolv - DNS querying through libc libresolv.so using ctypes
===============================================================

Provides access to ``res_query`` (``resolver(3)``) and friends for very
basic DNS querying (beyond ``gethostbyname``).

*Right now, it only supports MX record lookups.*

This is *not* a replacement for fully featured DNS libraries like
``dnspython`` or ``pycares``, but rather a small wrapper to provide a bare
minimal lookup capability. Additionally, it serves as an example of how
to use ``-lresolv`` routines.

.. warning:: BEWARE!

    This library uses (a) not-so-well documented C library calls which
    (b) may differ in their ABI across different libc versions and
    operating systems. Proceed with caution. The only thing this has
    going for it, is its small size.


Most common usage
-----------------

.. code-block:: python

    from pylresolv import ns_parse, ns_type, res_query

    answer = res_query('gmail.com', rr_type=ns_type.ns_t_mx)
    ret = ns_parse(answer, handler=ns_type.handle_mx)
    print(ret)

Will produce something like::

    [(10, 'alt1.gmail-smtp-in.l.google.com'),
     (5, 'gmail-smtp-in.l.google.com'),
     (40, 'alt4.gmail-smtp-in.l.google.com'),
     (30, 'alt3.gmail-smtp-in.l.google.com'),
     (20, 'alt2.gmail-smtp-in.l.google.com')]


2019-03-17: 0.1
~~~~~~~~~~~~~~~

-  Initial release.


Copyright
---------

Copyright 2019, Walter Doekes (OSSO B.V.)

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License for more details.

You should have received a copy of the GNU General Public License along
with this program. If not, see http://www.gnu.org/licenses/.
