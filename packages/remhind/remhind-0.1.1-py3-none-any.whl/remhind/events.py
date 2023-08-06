import asyncio
import calendar
import datetime
import logging
import pathlib
import sqlite3
from dataclasses import dataclass, InitVar

import gi
import icalendar
import pytz
from dateutil.rrule import rruleset, rrulestr
from tzlocal import get_localzone

gi.require_version('Notify', '0.7')
from gi.repository import Notify  # noqa

LOCAL_TZ = get_localzone()
MIN_SEQ = -999
MIN_DT = datetime.datetime(1900, 1, 1, tzinfo=LOCAL_TZ)


def _date2datetime(date):
    if (isinstance(date, datetime.date)
            and not isinstance(date, datetime.datetime)):
        # It should be 00:00 UTC per the RFC
        date = LOCAL_TZ.localize(
            datetime.datetime.combine(date, datetime.time(12, 0)))
    return date


def _to_utc_timestamp(dt):
    if dt.tzinfo is not None:
        dt = dt.astimezone(pytz.UTC)
    return calendar.timegm(dt.timetuple())


def _from_utc_timestamp(timestamp, tz=None):
    if tz is None:
        tz = LOCAL_TZ
    return datetime.datetime.fromtimestamp(
        timestamp, tz=pytz.UTC).astimezone(tz)


def parse_rule(component):
    if 'dtstart' in component:
        dtstart = _date2datetime(component['dtstart'].dt)
    elif 'due' in component:
        dtstart = _date2datetime(component['due'].dt)

    rule_set = rruleset()

    rrules = component.get('rrule', [])
    if not isinstance(rrules, list):
        rrules = [rrules]
    for rrule in rrules:
        rule_set.rrule(rrulestr(
                'RRULE:%s' % rrule.to_ical().decode(),
                dtstart=dtstart))

    rdates = component.get('rdate', [])
    if not isinstance(rdates, list):
        rdates = [rdates]
    for rdate in rdates:
        for rd in rdate.dts:
            rule_set.rdate(rd.dt)

    exrules = component.get('exrule', [])
    if not isinstance(exrules, list):
        exrules = [exrules]
    for exrule in exrules:
        rule_set.exrule(rrulestr(
                'EXRULE:%s' % exrule.to_ical().decode(),
                dtstart=dtstart))

    exdates = component.get('exdate', [])
    if not isinstance(exdates, list):
        exdates = [exdates]
    for exdate in exdates:
        for exd in exdate.dts:
            rule_set.exdate(exd.dt)

    return rule_set


def get_component_from_ics(uid, ics):
    cal = icalendar.Calendar.from_ical(ics)
    for component in cal.walk():
        if component.get('uid') == uid:
            return component
    return None


@dataclass
class Alarm:
    id: int
    event: str
    message: str
    displayed: bool
    date_timestamp: InitVar
    due_timestamp: InitVar
    date: datetime.datetime = None
    due_date: datetime.datetime = None

    def __post_init__(self, date_timestamp, due_timestamp):
        self.date = _from_utc_timestamp(date_timestamp)
        self.due_date = _from_utc_timestamp(due_timestamp)


class SQLiteDB:

    def __init__(self, db_path=None):
        self.db_path = ':memory:' if db_path is None else db_path
        init_db = db_path is None or not self.db_path.exists()
        self._conn = sqlite3.connect(self.db_path)
        if init_db:
            self._init_db()

    def _init_db(self):
        logging.debug(f'Initializing database {self.db_path}')
        self._conn.execute("""
            CREATE TABLE alarms (
                id INTEGER PRIMARY KEY,
                event TEXT NOT NULL,
                date INTEGER NOT NULL,
                due_date INTEGER NOT NULL,
                message TEXT NOT NULL,
                displayed INTEGER)""")
        self._conn.execute("""
            CREATE TABLE occurences (
                event TEXT PRIMARY KEY,
                date INTEGER NOT NULL)""")
        self._conn.execute("""
            CREATE TABLE events (
                event TEXT PRIMARY KEY,
                sequence INTEGER,
                path TEXT)""")
        self._conn.commit()

    def remove_event(self, uid):
        self._conn.execute("DELETE FROM alarms WHERE event = ?", (uid,))
        self._conn.execute("DELETE FROM occurences WHERE event = ?", (uid,))
        self._conn.execute("DELETE FROM events WHERE event = ?", (uid,))
        self._conn.commit()

    def add_alarm(self, event_uid, date, due_date, message):
        date = _to_utc_timestamp(date)
        due_date = _to_utc_timestamp(due_date)
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT 1 FROM alarms"
            " WHERE event=? AND date=?  AND due_date=? AND message=?",
            (event_uid, date, due_date, message))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO alarms
                    (event, date, due_date, message, displayed)
                VALUES (?, ?, ?, ?, 0)""",
                (event_uid, date, due_date, message))
            self._conn.commit()

    def get_alarms(self, start_date, end_date):
        start_date = _to_utc_timestamp(start_date)
        end_date = _to_utc_timestamp(end_date)
        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT id, event, message, displayed, date, due_date
            FROM alarms
            WHERE (date >= ?) AND (date < ?)
            """, (start_date, end_date))
        alarms = [Alarm(*r) for r in cursor.fetchall()]
        if alarms:
            cursor.execute(
                "UPDATE alarms SET displayed=1 WHERE id in (%s)"
                % ','.join('?' * len(alarms)),
                [a.id for a in alarms])
            self._conn.commit()
        return alarms

    def add_last_occurence(self, event_uid, date):
        self._conn.execute("""
            INSERT OR REPLACE INTO occurences(event, date)
            VALUES (?, ?)
            """, (event_uid, _to_utc_timestamp(date)))
        self._conn.commit()

    def get_last_occurences(self):
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT event, MAX(date) FROM occurences GROUP BY event")
        return {e: _from_utc_timestamp(d) for e, d in cursor.fetchall()}

    def get_ics_files(self, events):
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT event, path FROM events WHERE event in (%s)"
            % ','.join('?' * len(events)),
            list(events))
        return dict(cursor.fetchall())

    def get_uids(self, path):
        cursor = self._conn.cursor()
        cursor.execute("SELECT event FROM events WHERE path=?", (str(path),))
        return {r[0] for r in cursor}

    def get_events_sequence(self):
        cursor = self._conn.cursor()
        cursor.execute("SELECT event, sequence FROM events")
        return dict(cursor.fetchall())

    def add_event(self, uid, sequence, path):
        self._conn.execute("""
            INSERT OR REPLACE INTO events (event, sequence, path)
            VALUES (?, ?, ?)""",
            (uid, int(sequence), str(path)))
        self._conn.commit()


class EventCollection:

    def __init__(self, db_path=None):
        self.db = SQLiteDB(db_path)
        self._last_occurences = self.db.get_last_occurences()

    def add(self, cal_obj, ics, occurence=None):
        logging.debug(f"Adding event '{cal_obj['uid']}'"
            f" from {ics} starting at {occurence}")
        if (occurence is not None
                and occurence < self._last_occurences[cal_obj['uid']]):
            return
        obj_sequence = cal_obj.get('sequence', 0)
        self.db.add_event(cal_obj['uid'], obj_sequence, ics)

        summary = cal_obj.get('summary', '')
        if 'dtstart' in cal_obj:
            start_dt = _date2datetime(cal_obj['dtstart'].dt)
        elif 'due' in cal_obj:
            start_dt = _date2datetime(cal_obj['due'].dt)
        else:
            start_dt = None
        if 'dtend' in cal_obj:
            end_dt = _date2datetime(cal_obj['dtend'].dt)
            duration = end_dt - start_dt
        elif 'duration' in cal_obj:
            duration = cal_obj['duration'].dt
        else:
            duration = datetime.timedelta()
        latest_occurence = self._last_occurences.get(cal_obj['uid'], start_dt)
        if occurence is None:
            occurence = latest_occurence

        def _add_occurence(dt):
            for component in cal_obj.subcomponents:
                if not isinstance(component, icalendar.Alarm):
                    continue
                if component['action'] != 'DISPLAY':
                    continue
                trigger = component['trigger']
                if trigger.params.get('value') == 'DATE-TIME':
                    alarm_dt = trigger.dt
                else:
                    if trigger.params.get('related') == 'END':
                        alarm_dt = dt + duration + trigger.dt
                    else:
                        alarm_dt = dt + trigger.dt

                message = component.get('description', summary)
                if message:
                    self.db.add_alarm(cal_obj['uid'], alarm_dt, dt, message)

            if summary:
                self.db.add_alarm(cal_obj['uid'], dt, dt, summary)

        has_rules = ('rrule' in cal_obj or 'exrule' in cal_obj
            or 'rdate' in cal_obj or 'exdate' in cal_obj)
        if not has_rules:
            if start_dt:
                _add_occurence(start_dt)
                self.db.add_last_occurence(cal_obj['uid'], start_dt)
        else:
            rules = parse_rule(cal_obj)
            for occurence in rules.xafter(latest_occurence, 10, inc=True):
                _add_occurence(occurence)
            self.db.add_last_occurence(cal_obj['uid'], occurence)
            latest_occurence = occurence
        self._last_occurences[cal_obj['uid']] = latest_occurence

    def remove(self, path):
        for uid in self.db.get_uids(path):
            self.db.remove_event(uid)

    def get_due_alarms(self, date):
        end_date = date + datetime.timedelta(minutes=1)
        alarms = self.db.get_alarms(date, end_date)

        max_alarms = {}
        for alarm in alarms:
            if alarm.event in max_alarms:
                max_alarms[alarm.event] = max(
                    max_alarms[alarm.event], alarm.due_date)
            else:
                max_alarms[alarm.event] = alarm.due_date
        to_renew = {event for event, date in max_alarms.items()
            if date >= self._last_occurences.get(event, MIN_DT)}
        ics_files = self.db.get_ics_files(to_renew)
        for event_uid, ics in ics_files.items():
            event = get_component_from_ics(
                event_uid, pathlib.Path(ics).read_text())
            self.add(event, ics, max_alarms[event_uid])

        return alarms


class CalendarStore:

    def __init__(self, sources, db_path):
        self.sources = sources
        self.events = EventCollection(db_path)
        for source in sources:
            self.add_source_events(source)

    def add_source_events(self, source):
        for cal_file, component in self.get_interesting_components(source):
            self.events.add(component, cal_file)

    def get_interesting_components(self, source):
        cal_path = pathlib.Path(source['path'])
        for ics in cal_path.expanduser().glob('*.ics'):
            yield from self._get_components_from_ics(ics)

    def _get_components_from_ics(self, ics):
        cal = icalendar.Calendar.from_ical(ics.read_text())
        for component in cal.subcomponents:
            if isinstance(component, icalendar.Event):
                yield (ics, component)
            elif isinstance(component, icalendar.Todo) and (
                    component.get('status', 'NEEDS-ACTION') == 'NEEDS-ACTION'):
                yield (ics, component)

    def add_file(self, ics):
        logging.info(f'Adding events from {ics}')
        for cal_file, component in self._get_components_from_ics(ics):
            self.events.add(component, cal_file)

    def remove_file(self, ics):
        logging.info(f'Removing events from {ics}')
        self.events.remove(ics)

    def modify_file(self, ics):
        logging.info(f'Updating events from {ics}')
        for cal_file, component in self._get_components_from_ics(ics):
            self.events.add(component, cal_file)


async def check_events(calendar_store):
    while True:
        now = datetime.datetime.now(LOCAL_TZ).replace(second=0, microsecond=0)
        due_alarms = calendar_store.events.get_due_alarms(now)
        for alarm in due_alarms:
            if alarm.displayed:
                continue
            logging.debug(f'Notifying of alarm {alarm.id} "{alarm.message}"')
            n = Notify.Notification.new(
                "{a.due_date:%H:%M} {a.message}".format(a=alarm), "Alarm")
            n.show()
        # Take some security to ensure we don't miss any minute
        await asyncio.sleep(45)
