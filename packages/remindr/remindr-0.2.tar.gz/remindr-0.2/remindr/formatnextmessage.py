# vim:ts=4:sw=4:ft=python:fileencoding=utf-8
# Copyright © 2017-2019 Carl Chenet <carl.chenet@ohmytux.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

'''Manage entries to remind to users'''

# standard libraires imports
import os
import os.path
import sys

def formatnextmessage(options, content):
    '''Format the next message'''
    foundprefix = False
    nextmessage = ''
    language = content[0:2]
    for parameter in options['prefix']:
        if parameter.endswith('_prefix'):
            if parameter.startswith(language):
                foundprefix = True
                nextmessage = ' '.join([options['prefix'][parameter], content[3:]])
    if not foundprefix:
        nextmessage = ' '.join([options['prefix']['prefix'], content[0:]])
    # replace escaped line sep by real line sep
    nextmessage = nextmessage.replace('\\n', '\n')
    return nextmessage, language
