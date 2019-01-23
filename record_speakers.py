import subprocess
import sys
import os
import gi
import re
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Record:
    def __init__(self):
        self.gladefile = "record_speakers.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("Record_Speakers")
        self.textbox = self.builder.get_object("entry1")
        self.menu = self.builder.get_object("menu1")
        self.infobar = self.builder.get_object("infobar1")
        self.label1 = self.builder.get_object("label1")
        self.label2 = self.builder.get_object("label2")
        self.status_count = 0
        self.window.show()

    def on_Record_Speakers_destroy(self, object, data=None):
        print "Quit with Cancel"
        Gtk.main_quit()

    def on_switch1_notify(self, switch, gparam):
        music_path = os.environ["HOME"]
        music_path = music_path + "/Music"
        print music_path
        if switch.get_active():
            self.label1.set_text("Recording Started")

            if len(self.textbox.get_text()) != 0:
                mp3file = self.textbox.get_text() + ".mp3"
            else:
                mp3file = "audio.mp3"

            mp3file = music_path + "/" + mp3file
            # Update the file save path
            self.label2.set_text("File saved at: %s" % mp3file)
            print "Saving file to " + mp3file
            # Form the command to record from the speakers
            # Find Pulse Audio's monitor stream
            cmd_find_dev = "pacmd list-sources | grep -e 'stereo.monitor' | awk '{print $2}' | sed 's/[<>]//g'"
            p = subprocess.Popen(cmd_find_dev, stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            alsa_stream = output.strip('\n')
            print "Alsa Monitor stream found at %s" % alsa_stream
            # Escape any special characters
            mp3file = re.escape(mp3file)
            print "Escaping special characters %s" % mp3file
            cmd_rec = "parec -d "
            cmd_lame = " | lame -r -V0 - " + mp3file + " &"
            cmd_rec = cmd_rec + alsa_stream + cmd_lame
            print "Recording...\n %s" % cmd_rec
            # Start recording
            os.system(cmd_rec)

        else:
            print "Stop"
            self.label1.set_text("Recording Stopped")
            subprocess.call(["pkill", "parec"])

if __name__ == "__main__":
  main = Record()
  Gtk.main()
