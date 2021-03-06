#
# Registry Decoder
# Copyright (c) 2011 Digital Forensics Solutions, LLC
#
# Contact email:  registrydecoder@digitalforensicssolutions.com
#
# Authors:
# Andrew Case       - andrew@digitalforensicssolutions.com
# Lodovico Marziale - vico@digitalforensicssolutions.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details. 
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA 
#
import cPickle, os, sys, traceback
import registryparser.regparser as regparse
from errorclasses import *

class tree_handling:

    def __init__(self):
        self.reg_parser = regparse.regparser()

    def add_file_to_tree(self, gui, existingfilepath, fileid, case_obj, filepath):

        # get the keys from the registry
        keylist = self.reg_parser.parse_file(existingfilepath)

        # had to try/expect whole function b/c
        # exception occurs in 'for' due to being generator
        try:
            self.add_elements(keylist, gui, fileid, case_obj)
     
        # regfi throws generic Exception
        except Exception, e:
            print "--error: %s" % str(e)
            traceback.print_exc(file=sys.stdout)
            cont = gui.yesNoDialog("Unable to process %s" % filepath, "Would you like to skip this file?")

            if cont:
                return False
            else:
                raise RegFiKeyError(filepath)

        return True

    def add_elements(self, keylist, gui, fileid, case_obj):

        ktree = case_obj.tree
        
        i = 0

        for element in keylist:

            isroot = not i

            ktree.add_path(fileid, element, isroot)
            
            i = i + 1

            if i % 5000 == 0:
                if not hasattr(gui,"progressLabel"):
                    return

                gui.progressLabel.setText("Processed %d registry keys" % i)
 
                gui.update()
                gui.app.processEvents()
                gui.update()
                gui.app.processEvents()
       
            if i % 10000 == 0:
 
                case_obj.stringtable.commit_db()
                case_obj.vtable.conn.commit()
            
        case_obj.vtable.conn.commit()
        case_obj.stringtable.commit_db()
                
