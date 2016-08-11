
# -*- coding: utf-8 -*-

'''
--------------------- Copyright Block ----------------------

Prayer Times Program (ver 5.0)
Copyright (C) 2016 Abdullah Radwan

License: GNU GPL v3.0

TERMS OF USE:
	Permission is granted to use this code, with or
	without modification, in any website or application
	provided that credit is given to the original work
	with a link back to Abdullah Radwan.

This program is distributed in the hope that it will
be useful, but WITHOUT ANY WARRANTY.

PLEASE DO NOT REMOVE THIS COPYRIGHT BLOCK.'''

# Import main libs

import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, GObject

from umalqurra.hijri_date import HijriDate

import time, PrayTimesLib, datetime, pyglet

# Import Glade File

builder = Gtk.Builder()

builder.add_from_file("PrayTimesEn.glade")


# Main class

class SalatTimes:

    # Initialization

    def __init__(self):

        # Set main objects

        self.builder = builder

        self.lb = builder.get_object("lb_cities")

        self.sa = builder.get_object("sa_cities")

        self.ae = builder.get_object("ae_cities")

        self.ma = builder.get_object("ma_cities")

        self.ps = builder.get_object("ps_cities")

        self.iq = builder.get_object("iq_cities")

        self.ye = builder.get_object("ye_cities")

        self.sy = builder.get_object("sy_cities")

        self.dz = builder.get_object("dz_cities")

        self.ly = builder.get_object("ly_cities")

        self.kw = builder.get_object("kw_cities")

        self.jo = builder.get_object("jo_cities")

        self.sd = builder.get_object("sd_cities")

        self.tn = builder.get_object("tn_cities")

        self.bh = builder.get_object("bh_cities")

        self.qa = builder.get_object("qa_cities")

        self.om = builder.get_object("om_cities")

        self.eg = builder.get_object("eg_cities")

        self.countries = {
            "Egypt": [self.eg, "Egypt"],
            "Saudi Arabia": [self.sa, "Makkah"],
            "United Arabic Emirates": [self.ae, "Makkah"],
            "Oman": [self.om, "Makkah"],
            "Yemen": [self.ye, "Makkah"],
            "Qatar": [self.qa, "Makkah"],
            "Bahrain": [self.bh, "Makkah"],
            "Kuwait": [self.kw, "Makkah"],
            "Iraq": [self.iq, "MWL"],
            "Jordan": [self.jo, "Makkah"],
            "Syria": [self.sy, "Makkah"],
            "Lebanon": [self.lb, "MWL"],
            "Palestine": [self.ps, "MWL"],
            "Sudan": [self.sd, "Egypt"],
            "Libya": [self.ly, "Egypt"],
            "Tunisia": [self.tn, "MWL"],
            "Algeria": [self.dz, "Egypt"],
            "Morocco": [self.ma, "MWL"]
        }

        self.cities = {
            # Egypt
            "Cairo": [30.0500, 31.2500, +2],
            "Alexandria": [31.1981, 29.9192, +2],
            "Asyut": [27.1828, 31.1828, +2],
            "Port Said": [31.2667, 32.3000, +2],
            "Suez": [29.9667, 32.5500, +2],
            "Tanta": [30.7911, 30.9981, +2],
            # Saudi Arabia
            "Riyadh": [24.6700, 46.6900, +3],
            "Onaizah": [26.085478, 43.9768123, +3],
            "Madinah": [24.4527, 39.6667, +3],
            "Jeddah": [21.5169, 39.219, +3],
            "Dammam": [26.4400, 50.1000, +3],
            "Makkah": [21.4200, 39.8300, +3],
            "Hail": [27.5258717, 41.6748334, +3],
            "Abha": [18.2200, 42.5100, +3],
            "Al Jouf": [29.9029354, 40.1848983, +3],
            "Al Qurayyat": [31.316667, 37.366667, +3],
            "Najran": [17.48333, 44.11667, +3],
            "Taif": [21.2703, 40.4158, +3],
            "Al Baha": [20, 41.45, +3],
            "Buraidah": [26.3317, 43.9717, +3],
            "Jazan": [16.883333, 42.55, +3],
            "Tabuk": [28.3833, 36.5833, +3],
            "Hafr Al Batin": [28.4342, 45.9636, +3],
            "Al Khafji": [28.4403, 48.4844, +3],
            # United Arabic Emirates
            "Dubai": [25.2522, 55.2800, +4],
            "Abu Dhabi": [24.4500, 54.3833, +4],
            "Ajman": [25.4061, 55.4428, +4],
            "Ras al Khaima": [24.4500, 54.3833, +4],
            "Sharjah": [25.0000, 55.7500, +4],
            # Oman
            "Muscat": [23.6133, 58.5933, +4],
            "Salala": [17.0175, 54.0828, +4],
            # Yemen
            "Aden": [12.7667, 45.0167, +3],
            "Dhamar": [14.5500, 44.4017, +3],
            "Mukalla": [14.5300, 49.1314, +3],
            "Sanaa": [15.3547, 44.2067, +3],
            "Taiz": [13.5000, 44.0000],
            # Qatar
            "Doha": [25.2867, 51.5333, +3],
            # Bahrain
            "Manama": [26.2361, 50.5831, +3],
            # Kuwait
            "Kuwait": [29.5000, 47.7500, +3],
            "Al Jahara": [29.3375, 47.6581, +3],
            # Iraq
            "An Najaf": [31.9922, 44.3514, +3],
            "Baghdad": [33.3386, 44.3939, +3],
            "Basra": [30.5000, 47.8500, +3],
            "Erbil": [36.1900, 44.0089, +3],
            "Kufa": [32.0347, 44.4033, +3],
            "Mosul": [36.3350, 43.1189, +3],
            # Jordan
            "Amman": [31.9500, 35.9333, +3],
            "Irbid": [32.5556, 35.8500, +3],
            "Madaba": [31.7167, 35.8000, +3],
            # Syria
            "Al Ladhiqiyah": [35.5167, 35.7833, +3],
            "Aleppo": [36.2028, 37.1586, +3],
            "Damascus": [33.5000, 36.3000, +3],
            "Hama": [35.1333, 36.7500, +3],
            "Hasakeh": [36.5000, 41.0000, +3],
            "Homs": [34.7333, 36.7167, +3],
            "Rakka": [35.9500, 39.0167, +3],
            "Tartous": [34.8833, 35.8833, +3],
            # Lebanon
            "Akka": [34.4167, 36.2167, +3],
            "Baalbek": [34.0000, 36.2000, +3],
            "Beirut": [33.8719, 35.5097, +3],
            "Sidon": [33.5631, 35.3689, +3],
            "Tyre": [33.2711, 35.1964, +3],
            # Palestine
            "Elat": [29.5611, 34.9517, +3],
            "Gaza": [31.5000, 34.4667, +3],
            "Haifa": [32.8156, 34.9892, +3],
            "Tel Aviv": [32.0667, 34.7667, +3],
            # Sudan
            "Atbara": [17.7167, 34.0667, +3],
            "Kassala": [16.0000, 36.0000, +3],
            "Khartoum": [15.5881, 32.5342, +3],
            "Kosti": [13.1667, 32.6667, +3],
            "Port Sudan": [19.6158, 37.2164, +3],
            # Libya
            "Agedabia": [30.7592, 20.2231, +2],
            "Benghazi": [32.1167, 20.0667, +2],
            "Misurata": [32.3783, 15.0906, +2],
            "Sebha": [27.0333, 14.4333, +2],
            "Tripoli": [32.8925, 13.1800, +2],
            "Tubruq": [32.0836, 23.9764, +2],
            # Tunisia
            "Ariana": [36.8625, 10.1956, +1],
            "Djerba": [33.8747, 10.8592, +1],
            "Gabes": [33.8833, 10.1167, +1],
            "Kairouan": [35.6744, 10.1017, +1],
            "Sfax": [34.7406, 10.7603, +1],
            "Sousse": [35.8256, 10.6411, +1],
            "Tunis": [36.8028, 10.1797, +1],
            # Algeria
            "Algiers": [36.7631, 3.0506, +1],
            "Annaba": [36.9000, 7.7667, +1],
            "Bejaia": [36.7500, 5.0833, +1],
            "Blida": [36.4686, 2.8289, +1],
            "Constantine": [36.3650, 6.6147, +1],
            "Oran": [35.6911, -0.6417, +1],
            "Setif": [36.1914, 5.4094, +1],
            "Skikda": [36.8792, 6.9067, +1],
            "Tlemcen": [34.8783, -1.3150, +1],
            # Morocco
            "Agadir": [29.0167, -10.2500, +0],
            "Casablanca": [33.5931, -7.6164, +0],
            "Fez": [34.0528, -4.9828, +0],
            "Kenitra": [34.2608, -6.5794, +0],
            "Marrakech": [31.6333, -8.0000, +0],
            "Meknes": [33.9000, -5.5500, +0],
            "Oujda": [34.6867, -1.9114, +0],
            "Rabat": [34.0253, -6.8361, +0],
            "Safi": [32.3000, -9.2386, +0],
            "Tangier": [35.7847, -5.8128, +0],
        }

        self.main_win = builder.get_object("window1")

        self.about_dialog = builder.get_object("aboutdia"
                                               "log1")

        self.set_win = builder.get_object("window2")

        self.pray_win = builder.get_object("window3")

        self.time_label = builder.get_object("label11")

        self.error_label = builder.get_object("label24")

        self.fajr_entry = builder.get_object("entry1")

        self.duhur_entry = builder.get_object("entry2")

        self.asr_entry = builder.get_object("entry3")

        self.maghrib_entry = builder.get_object("entry4")

        self.isha_entry = builder.get_object("entry5")

        self.status_icon = builder.get_object("statusicon1")

        self.adan_box = builder.get_object("combobox3")

        self.calc_times = PrayTimesLib.PrayTimes()

        self.salat_times_grid = builder.get_object("grid1")

        self.fajr_label = builder.get_object("label2")

        self.duhur_label = builder.get_object("label4")

        self.asr_label = builder.get_object("label6")

        self.maghrib_label = builder.get_object("label8")

        self.isha_label = builder.get_object("label10")

        self.next_salat_label = builder.get_object("label26")

        self.country_box = builder.get_object("combobox2")

        self.city_box = builder.get_object("combobox1")

        self.data = datetime.date.today()

        self.sunrise_entry = builder.get_object("entry6")

        self.sunrise_label = builder.get_object("label28")

        self.hj_date = builder.get_object("label30")

        self.gr_date = builder.get_object("label31")

        # Set default parameters

        self.times = self.calc_times.getTimes((self.data), (26.085478, 43.9768123), +3)

        self.sunrise_time = self.times["sunrise"]

        self.salat_time = {"Salat Al Fajr": self.times["fajr"], "Salat Al Duhur": self.times["dhuhr"],

                           "Salat Al Asr": self.times["asr"], "Salat Al Maghrib": self.times["maghrib"],

                           "Salat Al Isha": self.times["isha"]}

        self.play_adan = False

        self.adan_sound = "makkah.wav"

        self.adan_set = True

        self.adan()

        self.salat_times()

        self.next_salat()

        self.main_win.show_all()

        GObject.timeout_add_seconds(1, self.adan)

        GObject.timeout_add_seconds(1, self.next_salat)



    # Enable or disable adan function

    def enable_adan(self, widget):

        if widget.get_active():

            self.adan_box.show()

            self.adan_label.show()

            self.adan_set = True

        else:

            self.adan_box.hide()

            self.adan_label.hide()

            self.adan_set = False



    # Next prayer function

    def next_salat(self):

        d = time.strptime(self.salat_time["Salat Al Duhur"], "%H:%M")

        a = time.strptime(self.salat_time["Salat Al Asr"], "%H:%M")

        m = time.strptime(self.salat_time["Salat Al Maghrib"], "%H:%M")

        i = time.strptime(self.salat_time["Salat Al Isha"], "%H:%M")

        t = time.strptime(time.strftime("%H:%M"), "%H:%M")

        h = time.strptime('23:59', "%H:%M")

        f = time.strptime("2 " + self.salat_time["Salat Al Fajr"], "%d %H:%M")

        f1 = time.strptime(self.salat_time["Salat Al Fajr"], "%H:%M")

        if (t < f) and (t > i):

            self.eta = "Salat Al Fajr"

        elif (t > f1) and (t < d):

            self.eta = "Salat Al Duhur"

        elif (t > d) and (t < a):

            self.eta = "Salat Al Asr"

        elif (t > a) and (t < m):

            self.eta = "Salat Al Maghrib"

        elif (t > m) and (t < i):

            self.eta = "Salat Al Isha"

        else:

            self.eta = "Unknows"

        self.next_salat_label.set_text(self.eta)

        return True



    # Change adan function

    def changed_adan(self, widget):

        adansound = widget.get_active_iter()

        model = widget.get_model()

        name = model[adansound][0]

        if name == "Makkah":

            self.adan_sound = "makkah.wav"

        elif name == "Madinah":

            self.adan_sound = "madinah.wav"

        elif name == "Egypt":

            self.adan_sound = "egypt.wav"



    # Adan function

    def adan(self):
        if self.adan_set == True:

            now = time.strftime("%H:%M")

            if now in self.salat_time.values():

                if self.play_adan == False:

                    adan = pyglet.resource.media(self.adan_sound)

                    adan.play()

                    self.time_label.set_text("Adan Now")

                    self.play_adan = True

            else:

                if self.play_adan == True:

                    self.play_adan = False

                self.time_label.set_text("\nTime Now: %s" % (time.strftime("%H:%M:%S")))

                um = HijriDate(int(time.strftime("%Y")), int(time.strftime("%m")), int(time.strftime("%d")), gr=True)

                self.hj_date.set_text("\nHijri Date: %s/%s/%s" % (int(um.year), int(um.month), int(um.day)))

                self.gr_date.set_text("\nGregorian Date: %s" % (time.strftime(("%Y/%m/%d"))))

        else:

            self.time_label.set_text("\nTime Now: %s\n\nDate Today: %s" % (time.strftime("%H:%M:%S"), (time.strftime("%Y/%m/%d"))))

        return True



    # Show time now option

    def show_time_now(self, widget):

        if widget.get_active():

            self.time_label.show()

        else:

            self.time_label.hide()



    # Show salat times option

    def show_salat_times(self, widget):

        if widget.get_active():

            self.salat_times_grid.show()

        else:

            self.salat_times_grid.hide()

    # Set cities

    def country(self, widget):

        country = widget.get_active_iter()

        model = widget.get_model()

        name = model[country][0]

        self.city_box.set_model(self.countries[name][0])

        self.calc_times.setMethod(self.countries[name][1])



    # Set times to each city

    def city(self, widget):

        self.data = [int(time.strftime("%Y")), int(time.strftime("%m")), int(time.strftime("%d"))]

        city = widget.get_active_iter()

        model = widget.get_model()

        name = model[city][0]

        self.times = self.calc_times.getTimes((self.data), (self.cities[name][0], self.cities[name][1]),
                                              self.cities[name][2])

        if self.calc_times.getMethod() == "Makkah":

            um = HijriDate(int(time.strftime("%Y")), int(time.strftime("%m")), int(time.strftime("%d")), gr=True)

            if um.month == 9.0:

                hours = 2

                minutes = 0

            else:

                hours = 1

                minutes = 30

            m = datetime.datetime.strptime(self.times["maghrib"], "%H:%M")

            add_min = m + datetime.timedelta(hours=hours, minutes=minutes)

            salat_isha = str(add_min.strftime("%H:%M"))

            self.sunrise_time = self.times["sunrise"]

            self.salat_time = {"Salat Al Fajr": self.times["fajr"], "Salat Al Duhur": self.times["dhuhr"],
                               "Salat Al Asr": self.times["asr"], "Salat Al Maghrib": self.times["maghrib"],
                               "Salat Al Isha": salat_isha}

        else:

            self.sunrise_time = self.times["sunrise"]

            self.salat_time = {"Salat Al Fajr": self.times["fajr"], "Salat Al Duhur": self.times["dhuhr"],
                               "Salat Al Asr": self.times["asr"], "Salat Al Maghrib": self.times["maghrib"],
                               "Salat Al Isha": self.times["isha"]}


    # Show set salat times manual window

    def show_set_time_manual(self, widget):

        self.pray_win.show_all()


    # Set salat manual function

    def save_set_time_manual(self, widget, data=None):

        e1d = self.fajr_entry.get_text()

        e2d = self.duhur_entry.get_text()

        e3d = self.asr_entry.get_text()

        e4d = self.maghrib_entry.get_text()

        e5d = self.isha_entry.get_text()

        e6d = self.sunrise_entry.get_text()

        if not e1d or not e2d or not e3d or not e4d or not e5d:

            self.error_label.set_text("Please Enter All Data")

        else:

            self.sunrise_time = e6d

            self.salat_time = {"Salat Al Fajr": e1d, "Salat Al Duhur": e2d, "Salat Al Asr": e3d,
                               "Salat Al Maghrib": e4d, "Salat Al Isha": e5d}

            self.salat_times()

            self.pray_win.hide_on_delete()


    # Start about dialog

    def run_about(self, widget):

        self.about_dialog.run()

        self.about_dialog.hide_on_delete()


    # Show settings window

    def run_settings(self, widget):

        self.set_win.show_all()


    # Show main window

    def show_program(self, widget, data=None):

        self.main_win.show_all()


    # Set right click menu on statue bar icon

    def sbe(self, si, event_button, event_time, data=None):

        self.menu2 = Gtk.Menu()

        show_window = Gtk.MenuItem("Show Main Window")

        show_settings_window = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_PREFERENCES)

        show_settings_window.set_always_show_image(True)

        about_program = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_ABOUT)

        about_program.set_always_show_image(True)

        quit_program = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_CLOSE)

        quit_program.set_always_show_image(True)

        show_window.connect_object("activate", self.show_program, "Show Main Window")

        show_settings_window.connect_object('activate', self.run_settings, "Preferences")

        about_program.connect_object('activate', self.run_about, "About")

        quit_program.connect_object("activate", Gtk.main_quit, "Quit")

        self.menu2.append(show_window)

        self.menu2.append(show_settings_window)

        self.menu2.append(about_program)

        self.menu2.append(quit_program)

        self.menu2.show_all()

        self.menu2.popup(None, None, None, si, event_button, event_time)



    def right(self, data, event_button, event_time):

        self.sbe(self.status_icon, event_button, event_time)



    def view_statusicon(self, widget=None):

        if widget.get_active():

            self.status_icon.set_visible(True)

        else:

            self.status_icon.set_visible(False)

            self.main_win.show_all()



    # Set salat times on main window

    def salat_times(self,widget=None):

        self.fajr_label.set_text(self.salat_time["Salat Al Fajr"])

        self.sunrise_label.set_text(self.sunrise_time)

        self.duhur_label.set_text(self.salat_time["Salat Al Duhur"])

        self.asr_label.set_text(self.salat_time["Salat Al Asr"])

        self.maghrib_label.set_text(self.salat_time["Salat Al Maghrib"])

        self.isha_label.set_text(self.salat_time["Salat Al Isha"])

        return True



    # Quit function

    def quit(self, widget):

        Gtk.main_quit()



    # Hide windows

    def delete_event(self, widget, data=None):

        if self.status_icon.get_visible() == True:

            self.main_win.hide_on_delete()

        else:

             Gtk.main_quit()

        return True



    def delete_event1(self, widget, data=None):

        self.set_win.hide_on_delete()

        return True


    def delete_event2(self, widget, data=None):

        self.pray_win.hide_on_delete()

        return True


# Connect signals

builder.connect_signals(SalatTimes())

Gtk.main()
