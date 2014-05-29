# -*- coding: UTF-8 -*-
##############################################################################
#
#    OdooRPC
#    Copyright (C) 2014 Sébastien Alix.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
"""This module contains some helper functions used to save and load sessions
in `OdooRPC`.
"""
import os
import stat
from ConfigParser import SafeConfigParser

from odoorpc import error


def get_all(rc_file='~/.odoorpcrc'):
    """Return all session configurations from the `rc_file` file.
    
    >>> import odoorpc
    >>> odoorpc.tools.session.get_all()
    {'foo': {'protocol': 'jsonrpc', 'user': 'admin', 'timeout': 120, 'database': 'db_name', 'passwd': 'admin', 'type': 'ODOO', 'port': 8069, 'server': 'localhost'}}
    """
    conf = SafeConfigParser()
    conf.read([os.path.expanduser(rc_file)])
    sessions = {}
    for name in conf.sections():
        sessions[name] = {
            'type': conf.get(name, 'type'),
            'server': conf.get(name, 'server'),
            'protocol': conf.get(name, 'protocol'),
            'port': conf.getint(name, 'port'),
            'timeout': conf.getint(name, 'timeout'),
            'user': conf.get(name, 'user'),
            'passwd': conf.get(name, 'passwd'),
            'database': conf.get(name, 'database'),
        }
    return sessions


def get(name, rc_file='~/.odoorpcrc'):
    """Return the session configuration identified by `name`
    from the `rc_file` file.

    >>> import odoorpc
    >>> odoorpc.tools.session.get('foo')
    {'protocol': 'jsonrpc', 'user': 'admin', 'timeout': 120, 'database': 'db_name', 'passwd': 'admin', 'type': 'ODOO', 'port': 8069, 'server': 'localhost'}

    :raise: :class:`odoorpc.error.Error`
    """
    conf = SafeConfigParser()
    conf.read([os.path.expanduser(rc_file)])
    if not conf.has_section(name):
        raise error.Error(
            "'{0}' session does not exist".format(name))
    return {
        'type': conf.get(name, 'type'),
        'server': conf.get(name, 'server'),
        'protocol': conf.get(name, 'protocol'),
        'port': conf.getint(name, 'port'),
        'timeout': conf.getint(name, 'timeout'),
        'user': conf.get(name, 'user'),
        'passwd': conf.get(name, 'passwd'),
        'database': conf.get(name, 'database'),
    }


#def list(rc_file='~/.odoorpcrc'):
#    """Return a list of all sessions available in the
#    `rc_file` file.
#    """
#    conf = SafeConfigParser()
#    conf.read([os.path.expanduser(rc_file)])
#    # TODO
#    return conf.sections()


def save(name, data, rc_file='~/.odoorpcrc'):
    """Save the `data` session configuration under the name `name`
    in the `rc_file` file.

    >>> import odoorpc
    >>> odoorpc.tools.session.save(
    ...     'foo',
    ...     {'type': 'ODOO', 'server': 'localhost', 'protocol': 'jsonrpc',
    ...      'port': 8069, 'timeout': 120, 'user': 'admin', 'passwd': 'admin',
    ...      'database': 'db_name'})
    """
    conf = SafeConfigParser()
    conf.read([os.path.expanduser(rc_file)])
    if not conf.has_section(name):
        conf.add_section(name)
    for k, v in data.iteritems():
        conf.set(name, k, str(v))
    with open(os.path.expanduser(rc_file), 'wb') as file_:
        os.chmod(os.path.expanduser(rc_file), stat.S_IREAD | stat.S_IWRITE)
        conf.write(file_)


def remove(name, rc_file='~/.odoorpcrc'):
    """Remove the session configuration identified by `name`
    from the `rc_file` file.

    >>> import odoorpc
    >>> odoorpc.tools.session.remove('foo')

    :raise: :class:`odoorpc.error.Error`
    """
    conf = SafeConfigParser()
    conf.read([os.path.expanduser(rc_file)])
    if not conf.has_section(name):
        raise error.Error(
            "'{0}' session does not exist".format(name))
    conf.remove_section(name)
    with open(os.path.expanduser(rc_file), 'wb') as file_:
        conf.write(file_)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: