#!/usr/bin/python

# GTK VNC Widget
#
# Copyright (C) 2006  Anthony Liguori <anthony@codemonkey.ws>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.0 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA

from __future__ import print_function

import sys

usage = """
usage: gvncviewer.py <host>[:<display>] [password]
       gvncviewer.py unix:<path> [password]

Connect to the given <host> and <display>. If the <display> is omitted,
it defaults to 0.

Alternatively, a unix domain socket can be specified using unix:<path>.
"""

if "-h" in sys.argv or "--help" in sys.argv:
    print(usage)
    sys.exit(0)

if len(sys.argv) != 2 and len(sys.argv) != 3:
    print(usage)
    sys.exit(1)


# a fancy 'print_nothing' lambda function
info = lambda *args, **kwargs : None

if "-v" in sys.argv:
	info = print
	sys.argv.remove("-v")

if "--verbose" in sys.argv:
	info = print
	sys.argv.remove("--verbose")


import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkVnc', '2.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GtkVnc

def set_title(vnc, window, grabbed):
    name = vnc.get_name()
    keys = vnc.get_grab_keys()
    keystr = None
    for i in range(keys.nkeysyms):
        k = keys.get_nth(i)
        if keystr is None:
            keystr = Gdk.keyval_name(k)
        else:
            keystr = keystr + "+" + Gdk.keyval_name(k)
    if grabbed:
        subtitle = "(Press %s to release pointer) " % keystr
    else:
        subtitle = ""

    window.set_title("%s%s - GVncViewer" % (subtitle, name))

def vnc_screenshot(src, ev, vnc):
    if ev.keyval == Gdk.KEY_F11:
        pix = vnc.get_pixbuf()
        pix.savev("gvncviewer.png", "png", ["tEXt::Generator App"], ["gvncviewer.py"])
        info("Screenshot saved to gvncviewer.png")

    return False

def vnc_close(src, window, data = None):
    info("Window closed by user")
    Gtk.main_quit()

def vnc_grab(src, window):
    set_title(src, window, True)

def vnc_ungrab(src, window):
    set_title(src, window, False)

def vnc_connected(src):
    info("Connected to server")

def vnc_initialized(src, window):
    info("Connection initialized")
    set_title(src, window, False)
    window.show_all()

def vnc_disconnected(src):
    info("Disconnected from server")
    Gtk.main_quit()

def send_caf1(src, vnc):
    info("Send Ctrl+Alt+F1")
    vnc.send_keys([Gdk.KEY_Control_L, Gdk.KEY_Alt_L, Gdk.KEY_F1])

def send_caf2(src, vnc):
    info("Send Ctrl+Alt+F2")
    vnc.send_keys([Gdk.KEY_Control_L, Gdk.KEY_Alt_L, Gdk.KEY_F2])

def send_caf3(src, vnc):
    info("Send Ctrl+Alt+F3")
    vnc.send_keys([Gdk.KEY_Control_L, Gdk.KEY_Alt_L, Gdk.KEY_F3])

def send_caf7(src, vnc):
    info("Send Ctrl+Alt+F7")
    vnc.send_keys([Gdk.KEY_Control_L, Gdk.KEY_Alt_L, Gdk.KEY_F7])

def send_cad(src, vnc):
    info("Send Ctrl+Alt+Del")
    vnc.send_keys([Gdk.KEY_Control_L, Gdk.KEY_Alt_L, Gdk.KEY_Delete])

def send_cab(src, vnc):
    info("Send Ctrl+Alt+BackSpace")
    vnc.send_keys([Gdk.KEY_Control_L, Gdk.KEY_Alt_L, Gdk.KEY_BackSpace])

def vnc_auth_cred(src, credList):
    prompt = 0
    data = []

    info(type(credList))
    for i in range(credList.n_values):
        data.append(None)
        if credList.get_nth(i) in (GtkVnc.DisplayCredential.USERNAME, GtkVnc.DisplayCredential.PASSWORD):
            prompt = prompt + 1
        elif credList.get_nth(i) == GtkVnc.DisplayCredential.CLIENTNAME:
            data[i] = "gvncviewer"

    if prompt:
        dialog = Gtk.Dialog("Authentication required", None, 0, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
        dialog.set_default_response(Gtk.ResponseType.OK)
        label = []
        entry = []

        box = Gtk.Table(2, prompt)

        row = 0
        for i in range(credList.n_values):
            entry.append(Gtk.Entry())
            if credList.get_nth(i) == GtkVnc.DisplayCredential.USERNAME:
                label.append(Gtk.Label("Username:"))
            elif credList.get_nth(i) == GtkVnc.DisplayCredential.PASSWORD:
                label.append(Gtk.Label("Password:"))
                entry[-1].set_visibility(False)
                entry[-1].set_activates_default(True)
            else:
                entry[-1].destroy()
                continue

            box.attach(label[row], 0, 1, row, row+1, 0, 0, 3, 3)
            box.attach(entry[row], 1, 2, row, row+1, 0, 0, 3, 3)
            row = row + 1

        vbox = dialog.get_child()
        vbox.add(box)

        dialog.show_all()
        res = dialog.run()
        dialog.hide()

        if res == Gtk.ResponseType.OK:
            row = 0
            for i in range(credList.n_values):
                if credList.get_nth(i) in (GtkVnc.DisplayCredential.USERNAME, GtkVnc.DisplayCredential.PASSWORD):
                    data[i] = entry[row].get_text()
                    row = row + 1

        dialog.destroy()

    for i in range(credList.n_values):
        if i < len(data) and data[i] != None:
            if src.set_credential(credList.get_nth(i), data[i]):
                info("Cannot set credential type %d" % (credList.get_nth(i)))
                src.close()
        else:
            info("Unsupported credential type %d" % (credList.get_nth(i)))
            src.close()

window = Gtk.Window()
vnc = GtkVnc.Display()

layout = Gtk.VBox()
window.add(layout)

menubar = Gtk.MenuBar()
sendkeys = Gtk.MenuItem.new_with_mnemonic("_Send keys")
menubar.append(sendkeys)

buttons = Gtk.HBox()
caf1 = Gtk.MenuItem.new_with_mnemonic("Ctrl+Alt+F_1")
caf2 = Gtk.MenuItem.new_with_mnemonic("Ctrl+Alt+F_2")
caf3 = Gtk.MenuItem.new_with_mnemonic("Ctrl+Alt+F_3")
caf7 = Gtk.MenuItem.new_with_mnemonic("Ctrl+Alt+F_7")
cad = Gtk.MenuItem.new_with_mnemonic("Ctrl+Alt+_Del")
cab = Gtk.MenuItem.new_with_mnemonic("Ctrl+Alt+_Backspace")

submenu = Gtk.Menu()
submenu.append(caf1)
submenu.append(caf2)
submenu.append(caf3)
submenu.append(caf7)
submenu.append(cad)
submenu.append(cab)
sendkeys.set_submenu(submenu)

caf1.connect("activate", send_caf1, vnc)
caf2.connect("activate", send_caf2, vnc)
caf3.connect("activate", send_caf3, vnc)
caf7.connect("activate", send_caf7, vnc)
cad.connect("activate", send_cad, vnc)
cab.connect("activate", send_cab, vnc)


layout.add(menubar)
layout.add(vnc)

vnc.realize()
vnc.set_pointer_grab(True)
vnc.set_keyboard_grab(True)

# Example to change grab key combination to Ctrl+Alt+g
grab_keys = GtkVnc.GrabSequence.new([ Gdk.KEY_Control_L, Gdk.KEY_Alt_L, Gdk.KEY_g ])
vnc.set_grab_keys(grab_keys)

#v.set_pointer_local(True)

if len(sys.argv) == 3:
    vnc.set_credential(GtkVnc.DisplayCredential.PASSWORD, sys.argv[2])

target = sys.argv[1]

if ":" in target:
    host, target = target.split(":", 1)

    if host == 'unix':
        path = target  # path of the domain socket
    else:
        port = str(5900 + int(target)) # port number of the display
else:
    host = target
    port = "5900"

if host == "unix":
    import socket
    domain_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM, 0)
    info("Connecting to domain socket", path)
    domain_socket.connect(path)
    vnc.open_fd(domain_socket.fileno())
else:
    info("Connecting to %s:%s" % (host, port))
    vnc.open_host(host, port)

vnc.connect("vnc-pointer-grab", vnc_grab, window)
vnc.connect("vnc-pointer-ungrab", vnc_ungrab, window)

vnc.connect("vnc-connected", vnc_connected)
vnc.connect("vnc-initialized", vnc_initialized, window)
vnc.connect("vnc-disconnected", vnc_disconnected)
vnc.connect("vnc-auth-credential", vnc_auth_cred)

window.connect("key-press-event", vnc_screenshot, vnc)
window.connect("destroy", vnc_close, window)

Gtk.main()
