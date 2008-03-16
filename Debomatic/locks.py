# Deb-o-Matic
#
# Copyright (C) 2007-2008 Luca Falavigna
#
# Author: Luca Falavigna <dktrkranz@ubuntu.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; only version 2 of the License
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA.

from threading import Semaphore
from Debomatic import globals

def buildlock_acquire():
    try:
        return globals.sema.build.acquire(False)
    except:
        globals.sema.build = Semaphore(globals.Options.getint('default', 'maxbuilds'))
        return buildlock_acquire()

def buildlock_release():
    try:
        globals.sema.build.release()
    except:
        pass

def pbuilderlock_acquire(distribution):
    try:
        return globals.sema.pbuilder[distribution].acquire(False)
    except AttributeError:
        globals.sema.pbuilder = dict()
        return pbuilderlock_acquire(distribution)
    except KeyError:
        globals.sema.pbuilder[distribution] = Semaphore()
        return pbuilderlock_acquire(distribution)

def pbuilderlock_release(distribution):
    try:
        globals.sema.pbuilder[distribution].release()
    except:
        pass
