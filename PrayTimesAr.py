#!/usr/bin/env python3

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

# استيراد المكتبات الرئيسية

import gi

gi.require_version("Gtk", "3.0")

gi.require_version("Notify", "0.7")

from gi.repository import Gtk, GObject, Notify

from umalqurra.hijri_date import HijriDate

import time, PrayTimesLib, datetime, pyglet

# استيراد ملف الواجهة الرسومية

builder = Gtk.Builder()

builder.add_from_file("PrayTimesAr.glade")


# الفئة الرئيسية

class SalatTimes():

    # التهيئة

    def __init__(self):

        # تعريف الكائنات الرئيسية

        self.builder = builder

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

        self.lb = builder.get_object("lb_cities")

        self.qa = builder.get_object("qa_cities")

        self.om = builder.get_object("om_cities")

        self.eg = builder.get_object("eg_cities")

        self.bh = builder.get_object("bh_cities")

        self.countries = {
            "مصر": [self.eg, "Egypt"],
            "المملكة العربية السعودية": [self.sa, "Makkah"],
            "الإمارات العربية المتحدة": [self.ae, "Makkah"],
            "عمان": [self.om, "Makkah"],
            "اليمن": [self.ye, "Makkah"],
            "قطر": [self.qa, "Makkah"],
            "البحرين": [self.bh, "Makkah"],
            "الكويت": [self.kw, "Makkah"],
            "العراق": [self.iq, "MWL"],
            "الأردن": [self.jo, "Makkah"],
            "سوريا": [self.sy, "Makkah"],
            "لبنان": [self.lb, "MWL"],
            "فلسطين": [self.ps, "MWL"],
            "السودان": [self.sd, "Egypt"],
            "ليبيا": [self.ly, "Egypt"],
            "تونس": [self.tn, "MWL"],
            "الجزائر": [self.dz, "Egypt"],
            "المغرب": [self.ma, "MWL"]
        }

        self.cities = {
            # مصر
            "القاهرة": [30.0500, 31.2500, +2],
            "الإسكندرية": [31.1981, 29.9192, +2],
            "أسيوط": [27.1828, 31.1828, +2],
            "بور سعيد": [31.2667, 32.3000, +2],
            "السويس": [29.9667, 32.5500, +2],
            "طنطا": [30.7911, 30.9981, +2],
            # المملكة العربية السعودية
            "الرياض": [24.6700, 46.6900, +3],
            "عنيزة": [26.085478, 43.9768123, +3],
            "المدينة النبوية": [24.4527, 39.6667, +3],
            "جدة": [21.5169, 39.219, +3],
            "الدمام": [26.4400, 50.1000, +3],
            "مكة المكرمة": [21.4200, 39.8300, +3],
            "حائل": [27.5258717, 41.6748334, +3],
            "أبها": [18.2200, 42.5100, +3],
            "الجوف": [29.9029354, 40.1848983, +3],
            "القريات": [31.316667, 37.366667, +3],
            "نجران": [17.48333, 44.11667, +3],
            "الطائف": [21.2703, 40.4158, +3],
            "الباحة": [20, 41.45, +3],
            "بريدة": [26.3317, 43.9717, +3],
            "جازان": [16.883333, 42.55, +3],
            "تبوك": [28.3833, 36.5833, +3],
            "حفر الباطن": [28.4342, 45.9636, +3],
            "الخفجي": [28.4403, 48.4844, +3],
            # الإمارات العربية المتحدة
            "دبي": [25.2522, 55.2800, +4],
            "أبو ظبي": [24.4500, 54.3833, +4],
            "عجمان": [25.4061, 55.4428, +4],
            "رأس الخيمة": [24.4500, 54.3833, +4],
            "الشرقية": [25.0000, 55.7500, +4],
            # عمان
            "مسقط": [23.6133, 58.5933, +4],
            "صلالة": [17.0175, 54.0828, +4],
            # اليمن
            "عدن": [12.7667, 45.0167, +3],
            "ذمار": [14.5500, 44.4017, +3],
            "المكلا": [14.5300, 49.1314, +3],
            "صنعاء": [15.3547, 44.2067, +3],
            "تعز": [13.5000, 44.0000],
            # قطر
            "الدوحة": [25.2867, 51.5333, +3],
            # البحرين
            "المنامة": [26.2361, 50.5831, +3],
            # الكويت
            "الكويت": [29.5000, 47.7500, +3],
            "الجهرة": [29.3375, 47.6581, +3],
            # العراق
            "النجف": [31.9922, 44.3514, +3],
            "بغداد": [33.3386, 44.3939, +3],
            "البصرة": [30.5000, 47.8500, +3],
            "إربيل": [36.1900, 44.0089, +3],
            "الكوفة": [32.0347, 44.4033, +3],
            "الموصل": [36.3350, 43.1189, +3],
            # الأردن
            "عمان": [31.9500, 35.9333, +3],
            "أربد": [32.5556, 35.8500, +3],
            "مأدبا": [31.7167, 35.8000, +3],
            # سوريا
            "اللاذيقية": [35.5167, 35.7833, +3],
            "حلب": [36.2028, 37.1586, +3],
            "دمشق": [33.5000, 36.3000, +3],
            "حماة": [35.1333, 36.7500, +3],
            "حمص": [34.7333, 36.7167, +3],
            "ركا": [35.9500, 39.0167, +3],
            "طرطوس": [34.8833, 35.8833, +3],
            # لبنان
            "عكا": [34.4167, 36.2167, +3],
            "بعلبك": [34.0000, 36.2000, +3],
            "بيروت": [33.8719, 35.5097, +3],
            "صيدا": [33.5631, 35.3689, +3],
            "طرابلس": [33.2711, 35.1964, +3],
            # فلسطين
            "إيلات": [29.5611, 34.9517, +3],
            "غزة": [31.5000, 34.4667, +3],
            "حيفا": [32.8156, 34.9892, +3],
            "تل أبيب": [32.0667, 34.7667, +3],
            # السودان
            "عطيرة": [17.7167, 34.0667, +3],
            "الخرطوم": [15.5881, 32.5342, +3],
            "كسلا": [13.1667, 32.6667, +3],
            "بور سودان": [19.6158, 37.2164, +3],
            # ليبيا
            "بنغازي": [32.1167, 20.0667, +2],
            "مصراته": [32.3783, 15.0906, +2],
            "سبها": [27.0333, 14.4333, +2],
            "طرابلس": [32.8925, 13.1800, +2],
            "طبرق": [32.0836, 23.9764, +2],
            # تونس
            "أريانا": [36.8625, 10.1956, +1],
            "قابس": [33.8833, 10.1167, +1],
            "القيروان": [35.6744, 10.1017, +1],
            "صفاقس": [34.7406, 10.7603, +1],
            "سوسة": [35.8256, 10.6411, +1],
            "تونس": [36.8028, 10.1797, +1],
            # الجزائر
            "الجزائر": [36.7631, 3.0506, +1],
            "عنابة": [36.9000, 7.7667, +1],
            "قسطنطينة": [36.3650, 6.6147, +1],
            "حوران": [35.6911, -0.6417, +1],
            "تلمسان": [34.8783, -1.3150, +1],
            # المغرب
            "أجادير": [29.0167, -10.2500, +0],
            "الدار البيضاء": [33.5931, -7.6164, +0],
            "فيز": [34.0528, -4.9828, +0],
            "القنطرة": [34.2608, -6.5794, +0],
            "مراكش": [31.6333, -8.0000, +0],
            "الرباط": [34.0253, -6.8361, +0],
            "طنجة": [35.7847, -5.8128, +0],
        }

        self.main_win = builder.get_object("window1")

        self.about_dialog = builder.get_object("aboutdialog1")

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

        self.adan_label = builder.get_object("label20")

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

        self.ger_date = builder.get_object("label31")

        self.hej_date = builder.get_object("label30")


      # ضبط الإعدادات الافتراضية

        self.times = self.calc_times.getTimes((self.data), (26.085478,
                                                            43.9768123), +3)
        self.sunrise_time = self.times["sunrise"]

        self.salat_time = {"صلاة الفجر": self.times["fajr"],
                           "صلاة الظهر": self.times["dhuhr"],
                           "صلاة العصر": self.times["asr"],
                           "صلاة المغرب": self.times["maghrib"],
                           "صلاة العشاء": self.times["isha"]}

        self.play_adan = False

        self.adan_sound = "makkah.wav"

        self.adan_set = True

        self.adan()

        self.salat_times()

        self.next_salat()

        self.status_icon.set_title("مواقيت الصلاة")

        self.main_win.show_all()

        GObject.timeout_add_seconds(1, self.adan)

        GObject.timeout_add_seconds(1, self.salat_times)

        GObject.timeout_add_seconds(1, self.next_salat)


    # دالة تعطيل أو تفعيل الأذان

    def enable_adan(self, widget):

        if widget.get_active():

            self.adan_box.show()

            self.adan_label.show()

            self.adan_set = True

        else:

            self.adan_box.hide()

            self.adan_label.hide()

            self.adan_set = False

    # دالة الصلاة التالية

    def next_salat(self):

        f = time.strptime("2 " + self.salat_time["صلاة الفجر"], "%d %H:%M")

        f1 = time.strptime(self.salat_time["صلاة الفجر"], "%H:%M")

        d = time.strptime(self.salat_time["صلاة الظهر"], "%H:%M")

        a = time.strptime(self.salat_time["صلاة العصر"], "%H:%M")

        m = time.strptime(self.salat_time["صلاة المغرب"], "%H:%M")

        i = time.strptime(self.salat_time["صلاة العشاء"], "%H:%M")

        t = time.strptime(time.strftime("%H:%M"), "%H:%M")

        if (t < f) and (t > i):

            self.eta = "صلاة الفجر"

        elif (t > f1) and (t < d):

            self.eta = "صلاة الظهر"

        elif (t > d) and (t < a):

            self.eta = "صلاة العصر"

        elif (t > a) and (t < m):

            self.eta = "صلاة المغرب"

        elif (t > m) and (t < i):

            self.eta = "صلاة العشاء"

        else:

            self.eta = "مجهول"

        self.next_salat_label.set_text(self.eta)

        return True

    # دالة تغيير الأذان

    def changed_adan(self, widget):

        adansound = widget.get_active_iter()

        model = widget.get_model()

        name = model[adansound][0]

        if name == "المسجد الحرام":

            self.adan_sound = "makkah.wav"

        elif name == "المسجد النبوي":

            self.adan_sound = "madinah.wav"

        elif name == "الأزهر":

            self.adan_sound = "egypt.wav"

    # دالة الأذان

    def adan(self):

        if self.adan_set == True:

            now = time.strftime("%H:%M")

            if now in self.salat_time.values():

                if self.play_adan == False:
                	
                    Notify.init("برنامج مواقيت الصلاة")
                    
                    adan_notify = Notify.Notification.new("حان وقت الأذان", "بدأ الأذان", "dialog-information")
                    
                    adan_notify.show()

                    adan = pyglet.resource.media(self.adan_sound)

                    adan.play()

                    self.time_label.set_text("حان وقت الأذان")

                    self.play_adan = True

            else:

                if self.play_adan == True:

                    self.play_adan = False

                self.time_label.set_text("\nالوقت الآن: %s" %(time.strftime("%H:%M:%S")))

                um = HijriDate(int(time.strftime("%Y")), int(time.strftime("%m")), int(time.strftime("%d")), gr=True)

                self.hej_date.set_text("\nالتاريخ الهجري: %s/%s/%s" % (int(um.year), int(um.month), int(um.day)))

                self.ger_date.set_text("\nالتاريخ الميلادي: %s" %(time.strftime(("%Y/%m/%d"))))

        else:

            self.time_label.set_text("\nالوقت الآن: %s" % (time.strftime("%H:%M:%S")))

            um = HijriDate(int(time.strftime("%Y")), int(time.strftime("%m")), int(time.strftime("%d")), gr=True)

            self.hej_date.set_text("\nالتاريخ الهجري: %s/%s/%s" % (int(um.year), int(um.month), int(um.day)))

            self.ger_date.set_text("\nالتاريخ الميلادي: %s" % (time.strftime(("%Y/%m/%d"))))

        return True



    # خيار عرض الوقت الحالي

    def show_time_now(self, widget):

        if widget.get_active():

            self.time_label.show()

        else:

            self.time_label.hide()



    # خيار عرض قائمة أوقات الصلاة

    def show_salat_times(self, widget):

        if widget.get_active():

            self.salat_times_grid.show()

        else:

            self.salat_times_grid.hide()



    # ضبط المدن

    def country(self, widget):

        country = widget.get_active_iter()

        model = widget.get_model()

        name = model[country][0]

        self.city_box.set_model(self.countries[name][0])

        self.calc_times.setMethod(self.countries[name][1])



    # ضبط الأوقات لكل مدينة

    def city(self, widget):

        self.data = [int(time.strftime("%Y")),int(time.strftime("%m")),int(time.strftime("%d"
                                                                                         ))]
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

            self.salat_time = {"صلاة الفجر": self.times["fajr"], "صلاة الظهر": self.times["dhuhr"],

                               "صلاة العصر": self.times["asr"], "صلاة المغرب": self.times["maghrib"],

                               "صلاة العشاء": salat_isha}

        else:

            self.sunrise_time = self.times["sunrise"]

            self.salat_time = {"صلاة الفجر": self.times["fajr"], "صلاة الظهر": self.times["dhuhr"],

                               "صلاة العصر": self.times["asr"], "صلاة المغرب": self.times["maghrib"],

                               "صلاة العشاء": self.times["isha"]}



    # عرض نافذة ضبط الصلاة يدويا

    def show_set_time_manual(self, widget):

        self.pray_win.show_all()



    # ضبط أوقات الصلاة يدويا

    def save_set_time_manual(self, widget, data=None):

        e1d = self.fajr_entry.get_text()

        e2d = self.duhur_entry.get_text()

        e3d = self.asr_entry.get_text()

        e4d = self.maghrib_entry.get_text()

        e5d = self.isha_entry.get_text()

        e6d = self.sunrise_entry.get_text()

        if not e1d or not e2d or not e3d or not e4d or not e5d:

            self.error_label.set_text("يرجى إدخال كافة البيانات")

        else:

            self.sunrise_time = e6d

            self.salat_time = {"صلاة الفجر": e1d, "صلاة الظهر": e2d, "صلاة العصر": e3d,

                               "صلاة المغرب": e4d, "صلاة العشاء": e5d}

            self.pray_win.hide_on_delete()



    # عرض نافذة حول

    def run_about(self, widget):

        self.about_dialog.run()

        self.about_dialog.hide_on_delete()



    # عرض نافذة الإعدادات

    def run_settings(self, widget):

        self.set_win.show_all()



    # عرض النافذة الرئيسية

    def show_program(self, widget, data=None):

        self.main_win.show_all()



    # ضبط أيقونة شريط المهام

    def sbe(self, si, event_button, event_time, data=None):

        self.menu2 = Gtk.Menu()

        show_window = Gtk.MenuItem("اعرض النافذة الرئيسية")

        show_settings_window = Gtk.MenuItem("الإعدادات")

        about_program = Gtk.MenuItem("حول البرنامج")

        quit_program = Gtk.MenuItem("اخرج")

        show_window.connect_object("activate", self.show_program, "اعرض النافذة الرئيسية")

        show_settings_window.connect_object('activate', self.run_settings, "الإعدادات")

        about_program.connect_object('activate', self.run_about, "حول البرنامج")

        quit_program.connect_object("activate", Gtk.main_quit, "اخرج")

        self.menu2.append(show_window)

        self.menu2.append(show_settings_window)

        self.menu2.append(about_program)

        self.menu2.append(quit_program)

        self.menu2.show_all()

        self.menu2.popup(None, None, None, si, event_button, event_time)



    def right(self, data, event_button, event_time):

        self.sbe(self.status_icon, event_button, event_time)



    def view_statusicon(self, widget):

        if widget.get_active():

            self.status_icon.set_visible(True)

        else:

            self.status_icon.set_visible(False)

            self.main_win.show_all()



    # عرض أوقات الصلاة

    def salat_times(self):

        self.fajr_label.set_text(self.salat_time["صلاة الفجر"])

        self.sunrise_label.set_text(self.sunrise_time)

        self.duhur_label.set_text(self.salat_time["صلاة الظهر"])

        self.asr_label.set_text(self.salat_time["صلاة العصر"])

        self.maghrib_label.set_text(self.salat_time["صلاة المغرب"])

        self.isha_label.set_text(self.salat_time["صلاة العشاء"])

        return True



    # دالة الخروج

    def quit(self, widget):

        Gtk.main_quit()



    # إخفاء النوافذ

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



# توصيل الإشارات

builder.connect_signals(SalatTimes())

Gtk.main()
