#!/usr/bin/env python3
# -*- coding:utf-8 -*
#
# Copyright (C) 2017 Free Electrons SAS
# Author: Florent Jacquet <florent.jacquet@free-electrons.com>
#
# This module is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import os
import sys
import configparser

"""
To test the script, just export those variables and play with their values

export LAB=lab-free-electrons
export TREE=mainline
"""

config = configparser.ConfigParser()
config.read('labs.ini')

lab_name = os.environ['LAB']
tree_name = os.environ['TREE']
branch = os.environ['BRANCH']

# Is the lab existing?
if lab_name not in config.sections():
    print("Unknown lab '{}'. refusing boot of tree '{}' as config is needed.".format(
        lab_name, tree_name))
    sys.exit(1)

lab = config[lab_name]

# Is the tree whitelisted for this lab
lab_tree_whitelist = lab.get('tree_whitelist')
if lab_tree_whitelist:
    whitelisted_trees = lab_tree_whitelist.split()
    for whitelisted_tree in whitelisted_trees:
        if '#' in whitelisted_tree:
            w_tree = whitelisted_tree.split('#')[0]
            w_branch = whitelisted_tree.split('#')[1]
            if tree_name == w_tree and branch == w_branch:
                print("Tree {} and branch {} is whitelisted for lab {}". format(tree_name, branch, lab_name))
                sys.exit(0)
        else:
            if tree_name == whitelisted_tree:
                print("Tree {} is whitelisted for lab {}". format(tree_name, lab_name))
                sys.exit(0)
    print("Tree {} is not whitelisted for lab {}".format(tree_name, lab_name))
    sys.exit(1)

# Is the tree blacklisted for this lab?
lab_tree_blacklist = lab.get('tree_blacklist')
if lab_tree_blacklist and tree_name in lab_tree_blacklist.split():
    print("Tree '{}' is blacklisted for lab '{}'".format(
        tree_name, lab_name))
    sys.exit(1)

print("Booting tree '{}' is allowed for lab '{}'".format(
    tree_name, lab_name))
sys.exit(0)
