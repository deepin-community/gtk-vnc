#!/usr/bin/gjs

imports.gi.versions.Gtk = "3.0";
imports.gi.versions.GtkVnc = "2.0";

const Vnc = imports.gi.GtkVnc;
const GVnc = imports.gi.GVnc;
const Gtk = imports.gi.Gtk;

Gtk.init(null);

GVnc.util_set_debug(true);

var win = new Gtk.Window({title: "GTK-VNC with JavaScript"});
var disp = new Vnc.Display();

win.add(disp);
disp.open_host("localhost", "5900");
win.show_all();
Gtk.main();
