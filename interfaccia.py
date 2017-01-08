#!/usr/bin/env python2
# example checkbutton.py

import pygtk
pygtk.require('2.0')
import gtk
import sys

class AVRFuseGUI:
        
    def __init__(self, setUp=[0x00,0x00,0x00]):
        self.HighFuse = self.HighFuse_start = setUp[0]
        if (len (setUp) == 1):
            self.LowFuse = self.LowFuse_start = 0x00
        elif (len (setUp) == 2):
            self.LowFuse = self.LowFuse_start = setUp[1]
            self.ExtFuse = self.ExtFuse_start = 0x00
        else:
            self.LowFuse = self.LowFuse_start = setUp[1]
            self.ExtFuse = self.ExtFuse_start = setUp[2]
        
        self.initGUI()
        
    # Create the window and populates with elemets
    def initGUI(self):
        
        HighFuseNames         = ["CKSEL0", "CKSEL1", "CKSEL2", "CKSEL3", "SUT0", "SUT1", "CKOUT", "CKDIV8"]
        self.HighFuseCheckButtons  = map(lambda i:gtk.CheckButton(HighFuseNames[i]), range(len(HighFuseNames)))        
        self.signal_HighFuseCheckButtons = [None]*len(HighFuseNames)
        
        LowFuseNames         = ["BOOTRST", "BOOTSZ0", "BOOTSZ1", "EESAVE", "WDTON", "SPIEN", "RSTDISBL", "DWEN"]
        self.LowFuseCheckButtons  = map(lambda i:gtk.CheckButton(LowFuseNames[i]), range(len(LowFuseNames)))
        self.signal_LowFuseCheckButtons = [None]*len(LowFuseNames)
        
        ExtFuseNames         = ["BODLEVEL0", "BODLEVEL1", "BODLEVEL2"]
        self.ExtFuseCheckButtons = map(lambda i:gtk.CheckButton(ExtFuseNames[i]), range(len(ExtFuseNames)))
        self.signal_ExtFuseCheckButtons = [None]*len(ExtFuseNames)
        
        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    
        # Set the window title
        self.window.set_title("AVR Fuses Calculator")
        try:
            self.window.set_icon_from_file('icon.png')
        except:
            print "vabbuo"
        # Set a handler for delete_event that immediately
        # exits GTK.
        self.window.connect("delete_event", self.delete_event)

        # Sets the border width of the window.
        #~ self.window.set_border_width(20)
        
        self.create_interior()
        
        self.window.show_all()
    
    def create_interior(self):
        # Main container
        self.MainContainer = gtk.VBox()
        self.window.add(self.MainContainer)
        
        self.MenuBar = self.CreateMenu()
        self.MainContainer.pack_start(self.MenuBar, False, False)
        
        self.ContentContainer = gtk.VBox()
        self.MainContainer.pack_start(self.ContentContainer, False, False)
        
        self.ContentContainer.set_border_width(20)
        
        
        self.FuseContainer = gtk.Table(1,3)
        self.ContentContainer.add(self.FuseContainer)
        self.LeftFuseContainer = gtk.VBox()
        
        self.FuseContainer.add(self.LeftFuseContainer)
        
        self.HighFuseLabel = gtk.Label("High Fuse")
        self.LeftFuseContainer.pack_start(self.HighFuseLabel, False, False)
        
        # high fuses
        for i in range (0,len(self.HighFuseCheckButtons)):
            self.HighFuseCheckButtons[i].set_active(not (self.HighFuse_start & (1<<i)))
            self.signal_HighFuseCheckButtons[i] = self.HighFuseCheckButtons[i].connect("toggled", self.callback_HighFuseCheckButton, i)
            self.LeftFuseContainer.pack_start(self.HighFuseCheckButtons[i], True, True)
        
        
        self.MiddleFuseContainer = gtk.VBox()
        
        self.FuseContainer.attach(self.MiddleFuseContainer, 1,2,0,1)
        self.LowFuseLabel = gtk.Label("Low Fuse")
        self.MiddleFuseContainer.pack_start(self.LowFuseLabel, False, False)
        
        # low fuses
        for i in range (0,len(self.LowFuseCheckButtons)):
            self.LowFuseCheckButtons[i].set_active(not(self.LowFuse_start & (1<<i)))
            self.signal_LowFuseCheckButtons[i] = self.LowFuseCheckButtons[i].connect("toggled", self.callback_LowFuseCheckButton, i)
            self.MiddleFuseContainer.pack_start(self.LowFuseCheckButtons[i], True, True)
        
        
        self.RightFuseContainer = gtk.VBox()
        
        self.FuseContainer.attach(self.RightFuseContainer, 2,3,0,1)
        self.ExtFuseLabel = gtk.Label("Ext Fuse")
        self.RightFuseContainer.pack_start(self.ExtFuseLabel, False, False)
        
        # low fuses
        for i in range (0,len(self.ExtFuseCheckButtons)):
            self.ExtFuseCheckButtons[i].set_active(not(self.ExtFuse_start & (1<<i)))
            self.signal_ExtFuseCheckButtons[i] = self.ExtFuseCheckButtons[i].connect("toggled", self.callback_ExtFuseCheckButton, i)
            self.RightFuseContainer.pack_start(self.ExtFuseCheckButtons[i], True, True)
        
        self.HighFuseString = gtk.Entry()
        self.HighFuseString.set_text(hex(self.HighFuse))
        self.HighFuseString.set_editable(True)
        self.ContentContainer.pack_start(self.HighFuseString, True, True)
        self.signal_HighFuseString = self.HighFuseString.connect("changed", self.callback_HighFuseString)
        
        self.LowFuseString = gtk.Entry()
        self.LowFuseString.set_text(hex(self.LowFuse))
        self.LowFuseString.set_editable(True)
        self.ContentContainer.pack_start(self.LowFuseString, True, True)
        self.signal_LowFuseString = self.LowFuseString.connect("changed", self.callback_LowFuseString)
        
        self.ExtFuseString = gtk.Entry()
        self.ExtFuseString.set_text(hex(self.ExtFuse))
        self.ExtFuseString.set_editable(True)
        self.ContentContainer.pack_start(self.ExtFuseString, True, True)
        self.signal_ExtFuseString = self.ExtFuseString.connect("changed", self.callback_ExtFuseString)

        # Create "Quit" button
        button = gtk.Button("Quit")

        # When the button is clicked, we call the mainquit function
        # and the program exits
        button.connect("clicked", self.delete_event, self)
        #~ button.connect("clicked", lambda wid: gtk.main_quit())

        # Insert the quit button
        self.ContentContainer.pack_start(button, True, True)
    
    def CreateMenu(self):
        menu_bar = gtk.MenuBar()
        
        
        file_menu = gtk.Menu()
        open_item = gtk.ImageMenuItem( stock_id=gtk.STOCK_OPEN) 
        #~ open_item.connect( "activate", self.open_file)
        self.save_item = gtk.ImageMenuItem( stock_id=gtk.STOCK_SAVE) 
        #~ self.save_item.connect( "activate", self.save_file)
        quit_item = gtk.ImageMenuItem( stock_id=gtk.STOCK_QUIT) 
        #~ quit_item.connect( "activate", self.quit)
        for i in [open_item, self.save_item, gtk.SeparatorMenuItem(), quit_item]:
            i.show()
            file_menu.append( i)
        # menu bar
        
        file_menu_item = gtk.MenuItem( "File")
        file_menu_item.set_submenu(file_menu)
        menu_bar.append(file_menu_item)
        
        help_menu = gtk.Menu()
        about_item = gtk.ImageMenuItem(stock_id=gtk.STOCK_ABOUT) 
        help_menu.append(about_item)
        about_item.connect( "activate", self.callback_about)
        help_menu_item = gtk.MenuItem( "Help")
        help_menu_item.set_submenu( help_menu)
        
        
        menu_bar.append(help_menu_item)
        return menu_bar
        
        
        
    # Our callback.
    # The data passed to this method is printed to stdout
    def callback_HighFuseCheckButton(self, widget, data=None):
        self.HighFuse ^= (1<<data)
        self.HighFuseString.handler_block(self.signal_HighFuseString)
        self.HighFuseString.set_text(hex(self.HighFuse))
        self.HighFuseString.handler_unblock(self.signal_HighFuseString)
        self.HighFuseString.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FFFFFF"))    
        print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
        print hex(self.HighFuse)
        
    def callback_LowFuseCheckButton(self, widget, data=None):
        self.LowFuse ^= (1<<data)
        self.LowFuseString.handler_block(self.signal_LowFuseString)
        self.LowFuseString.set_text(hex(self.LowFuse))
        self.LowFuseString.handler_unblock(self.signal_LowFuseString)
        self.LowFuseString.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FFFFFF"))    
        print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
        print hex(self.LowFuse)
        
    def callback_ExtFuseCheckButton(self, widget, data=None):
        self.ExtFuse ^= (1<<data)
        self.ExtFuseString.handler_block(self.signal_ExtFuseString)
        self.ExtFuseString.set_text(hex(self.ExtFuse))
        self.ExtFuseString.handler_unblock(self.signal_ExtFuseString)
        self.ExtFuseString.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FFFFFF"))    
        print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
        print hex(self.ExtFuse)
        
    def callback_HighFuseString(self, widget):
        written = widget.get_text()
        if (written.find("0x") != 0):
            widget.set_text("0x")
            widget.set_position(-1)
        else:
            print written
            try:
                written = int(written,16)
                if (written > 0xFF):
                    raise("TooBig")
            except:
                widget.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FF0000"))
                return
                
            widget.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FFFFFF"))    
            
            print bin(written)
            print bin(self.HighFuse)
            print bin(written^self.HighFuse)
            
            for i in range(0,len(self.HighFuseCheckButtons)):
                if ((written^self.HighFuse) & 1<<i):
                    self.HighFuseCheckButtons[i].handler_block(self.signal_HighFuseCheckButtons[i])
                    self.HighFuseCheckButtons[i].set_active(not(written & 1<<i));
                    self.HighFuseCheckButtons[i].handler_unblock(self.signal_HighFuseCheckButtons[i])
                
            self.HighFuse = written
        
    def callback_LowFuseString(self, widget):
        written = widget.get_text()
        if (written.find("0x") != 0):
            widget.set_text("0x")
            widget.set_position(-1)
        else:
            print written
            try:
                written = int(written,16)
                if (written > 0xFF):
                    raise("TooBig")
            except:
                widget.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FF0000"))
                return
                
            widget.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FFFFFF"))    
            
            print bin(written)
            print bin(self.LowFuse)
            print bin(written^self.LowFuse)
            
            for i in range(0,len(self.LowFuseCheckButtons)):
                if ((written^self.LowFuse) & 1<<i):
                    self.LowFuseCheckButtons[i].handler_block(self.signal_LowFuseCheckButtons[i])
                    self.LowFuseCheckButtons[i].set_active(not(written & 1<<i));
                    self.LowFuseCheckButtons[i].handler_unblock(self.signal_LowFuseCheckButtons[i])
                
            self.LowFuse = written
        
        
    def callback_ExtFuseString(self, widget):
        written = widget.get_text()
        if (written.find("0x") != 0):
            widget.set_text("0x")
            widget.set_position(-1)
        else:
            print written
            try:
                written = int(written,16)
                if (written > 0xFF or written < 0xF8):
                    raise("TooBig")
            except:
                widget.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FF0000"))
                return
                
            widget.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FFFFFF"))    
            
            print bin(written)
            print bin(self.ExtFuse)
            print bin(written^self.ExtFuse)
            
            for i in range(0,len(self.ExtFuseCheckButtons)):
                if ((written^self.ExtFuse) & 1<<i):
                    self.ExtFuseCheckButtons[i].handler_block(self.signal_ExtFuseCheckButtons[i])
                    self.ExtFuseCheckButtons[i].set_active(not(written & 1<<i));
                    self.ExtFuseCheckButtons[i].handler_unblock(self.signal_ExtFuseCheckButtons[i])
                
            self.ExtFuse = written
        
    def callback_about(self, widget):
        # The AboutDialog has good helper methods which
        # setup the dialog and add the content ensuring all
        # about dialog are consistant.  Below is a small example

        # Create AboutDialog object
        dialog = gtk.AboutDialog()

        # Add the application name to the dialog
        dialog.set_name('AVR fuses about')

        # Set the application version
        dialog.set_version('0.1')

        # Pass a list of authors.  This is then connected to the 'Credits'
        # button.  When clicked the buttons opens a new window showing
        # each author on their own line.
        dialog.set_authors(['GF', 'Example'])

        # Add a short comment about the application, this appears below the application
        # name in the dialog
        dialog.set_comments('Stupidissimo programmino per micro AVR.')

        # Add license information, this is connected to the 'License' button
        # and is displayed in a new window.
        dialog.set_license('Distributed under the GPL license version go to fish it.')

        # Show the dialog
        dialog.run()

        # The destroy method must be called otherwise the 'Close' button will
        # not work.
        dialog.destroy()
        
    # This callback quits the program
    def delete_event(self, widget, event, data=None):
        dialog = gtk.MessageDialog(self.window, gtk.DIALOG_MODAL,
                                   gtk.MESSAGE_INFO, gtk.BUTTONS_YES_NO,
                                   "Uscire padavero?")
        dialog.set_title("Sihuro?")

        response = dialog.run()
        dialog.destroy()
        if response == gtk.RESPONSE_YES:
            gtk.main_quit()
            return False # returning False makes "destroy-event" be signalled
                         # for the window.
        else:
            return True # returning True avoids it to signal "destroy-event"


def main():
    gtk.main()
    return 0       

def howTo():
    print "Use: ./"+sys.argv[0]+" [HIGH FUSE] [LOW FUSE]"
    print "A GUI for calculating the AVR Fuse bits"

if __name__ == "__main__":
    if len(sys.argv) == 1:
        AVRFuseGUI()
    elif len(sys.argv) > 3:
        howTo()
        sys.exit(1)
    else:
        if (sys.argv[1].find("--help") == 0):
            howTo()
            sys.exit(0)
        
        tmp = sys.argv[1:]
        
        for i in range(0,len(tmp)):
            try:
                tmp[i] = int(tmp[i], 16)
                if (tmp[i] > 0xFF):
                    raise("TooBig")
            except:
                print "Not correct parameters"
                sys.exit(1)
            
        AVRFuseGUI(tmp)
    
    main()
