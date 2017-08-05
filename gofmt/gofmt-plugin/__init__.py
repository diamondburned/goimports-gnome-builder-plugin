#!/usr/bin/env python3

from gi.repository import GObject
from gi.repository import Ide
from gi.repository import Gio


class MyAppaddin(GObject.Object, Ide.WorkbenchAddin):



    def do_load(self, workbench):
        context = workbench.get_context()
        bufmgr = context.get_buffer_manager()
        self.handler = bufmgr.connect('save-buffer', self.on_save_buffer)

    def do_unload(self, workbench):
        context = workbench.get_context()
        bufmgr = context.get_buffer_manager()
        bufmgr.disconnect(self.handler)

    def on_save_buffer(self, bufmgr, buffer):
        # If not go code return and exit
        lang = buffer.get_language()
        if lang is None or lang.get_id() not in ('go','golang'):
            return
        launcher = Ide.SubprocessLauncher.new(0)
        launcher.set_flags(Gio.SubprocessFlags.STDIN_PIPE | Gio.SubprocessFlags.STDOUT_PIPE)
         

        #setup our cmdline arguments
        launcher.push_argv('gofmt')
        launcher.set_run_on_host(True)


        #launch the process
        subprocess = launcher.spawn()

        begin, end = buffer.get_bounds()
        text = buffer.get_text(begin, end, True)

        #Write the buffer to the gofmt process
        if text == '':
            return
        ret, stdout, stderr = subprocess.communicate_utf8(text, None)

        # Write the new contents to the buffer
        buffer.set_text(stdout, len(stdout))
        print("Gofmt complete")


