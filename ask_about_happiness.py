#!/usr/bin/env python3
import notify2
import random
import sys
import csv
import datetime
import numpy as np

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


def rating_callback(notification, action):
    rating = int(action)
    print('Rated {}'.format(action))
    new_entry = [datetime.datetime.now().isoformat(), rating]
    with open('happiness_history.csv', 'a') as hist_csv:
        writer = csv.writer(hist_csv)
        writer.writerow(new_entry)
    Gtk.main_quit()
    notification.close()


def closed_callback(notification):
    print('Closed notification.')
    new_entry = [datetime.datetime.now().isoformat(), np.NaN]
    with open('happiness_history.csv', 'a') as hist_csv:
        writer = csv.writer(hist_csv)
        writer.writerow(new_entry)
    Gtk.main_quit()


def decide_to_ask(freq_to_ask, freq_run):
    return random.random() < freq_to_ask / freq_run


def ask_about_happiness():
    happiness_check_notification = notify2.Notification(
        'Happiness Check', 'How happy are you right now?')
    happiness_check_notification.set_timeout(notify2.EXPIRES_NEVER)

    for rating in range(1, 6):
        happiness_check_notification.add_action(
            str(rating), str(rating), rating_callback)

    happiness_check_notification.connect('closed', closed_callback)

    if not happiness_check_notification.show():
        print('Failed to show notification.')
        sys.exit(1)

    Gtk.main()


if __name__ == "__main__":
    if not notify2.init('Wellness Checker', mainloop='glib'):
        sys.exit(1)

    if 'actions' not in notify2.get_server_caps():
        sys.exit(1)

    if decide_to_ask(1 / 60, 1 / 10):
        print('Asking about happiness.')
        ask_about_happiness()
    else:
        print('Not asking about happiness.')
    sys.exit(0)
