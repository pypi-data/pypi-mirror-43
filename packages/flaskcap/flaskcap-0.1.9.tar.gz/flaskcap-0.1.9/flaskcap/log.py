# coding:utf-8

import os
import re
import sys
import time
import shutil
from logging import Handler


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY2:
    FileNotExistError = OSError
    BinaryType = str

    reload(sys)
    sys.setdefaultencoding('utf8')
if PY3:
    FileNotExistError = FileNotFoundError
    BinaryType = bytes


OS_POSIX = False
OS_NT = False
if os.name == 'posix':
    OS_POSIX = True
elif os.name == 'nt':
    OS_NT = True

if OS_POSIX:      # Unix
    import fcntl
    from fcntl import LOCK_EX, LOCK_UN

    def flock(fd, flags=LOCK_EX):
        fcntl.flock(fd, flags)

    def funlock(fd):
        fcntl.flock(fd, LOCK_UN)

elif OS_NT:       # Windows (pip install pywin32)
    import win32con
    import win32file
    import pywintypes

    LOCK_EX = win32con.LOCKFILE_EXCLUSIVE_LOCK
    LOCK_UN = win32con.LOCKFILE_FAIL_IMMEDIATELY
    __overlapped = pywintypes.OVERLAPPED()


    def flock(fd, flags=LOCK_EX):
        _file = win32file._get_osfhandle(fd)
        win32file.LockFileEx(_file, flags, 0, 0x7fff0000, __overlapped)

    def funlock(fd):
        try:
            _file = win32file._get_osfhandle(fd)
            win32file.UnlockFileEx(_file, 0, 0x7fff0000, __overlapped)
        except pywintypes.error as exc:
            if exc.winerror == 158:
                # Already Unlocked
                pass
            else:
                raise exc


ST_INO = 1
ST_DEV = 2
ST_MTIME = 8
_MIDNIGHT = 24 * 60 * 60  # number of seconds in a day


class TimedRotatingLogging(Handler):
    def __init__(self, filename, when='d', interval=1, backupCount=0, encoding='utf-8', utc=False,
                 atTime=None):
        super(TimedRotatingLogging, self).__init__()
        self.baseFilename = os.path.abspath(filename)
        self.fd = self._open()
        self.when = when.upper()
        self.backupCount = backupCount
        self.encoding = encoding
        self.utc = utc
        self.atTime = atTime
        # super(NaturalTimedRotating, self).__init__(filename, 'a', encoding, delay)
        # Calculate the real rollover interval, which is just the number of
        # seconds between rollovers.  Also set the filename suffix used when
        # a rollover occurs.  Current 'when' events supported:
        # S - Seconds
        # M - Minutes
        # H - Hours
        # D - Days
        # midnight - roll over at midnight
        # W{0-6} - roll over on a certain day; 0 - Monday
        #
        # Case of the 'when' specifier is not important; lower or upper case
        # will work.
        if self.when == 'S':
            self.interval = 1 # one second
            self.suffix = "%Y-%m-%d_%H-%M-%S"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$"
        elif self.when == 'M':
            self.interval = 60 # one minute
            self.suffix = "%Y-%m-%d_%H-%M"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}$"
        elif self.when == 'H':
            self.interval = 60 * 60 # one hour
            self.suffix = "%Y-%m-%d_%H"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}_\d{2}$"
        elif self.when == 'D' or self.when == 'MIDNIGHT':
            self.interval = 60 * 60 * 24 # one day
            self.suffix = "%Y-%m-%d"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}$"
        elif self.when.startswith('W'):
            self.interval = 60 * 60 * 24 * 7 # one week
            if len(self.when) != 2:
                raise ValueError("You must specify a day for weekly rollover from 0 to 6 (0 is Monday): %s" % self.when)
            if self.when[1] < '0' or self.when[1] > '6':
                raise ValueError("Invalid day specified for weekly rollover: %s" % self.when)
            self.dayOfWeek = int(self.when[1])
            self.suffix = "%Y-%m-%d"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}$"
        else:
            raise ValueError("Invalid rollover interval specified: %s" % self.when)

        self.extMatch = re.compile(self.extMatch)
        self.interval = self.interval * interval

        # customer
        self.dev, self.ino = -1, -1
        self._statfd()

        if os.path.exists(filename):
            t = os.stat(filename)[ST_MTIME]
        else:
            t = int(time.time())
        self.rolloverAt = self.computeRollover(t)

    def _open(self):
        """
        Open the current base file with the (original) mode and encoding.
        Return the resulting stream.
        """
        return os.open(self.baseFilename, os.O_WRONLY | os.O_CREAT | os.O_APPEND)

    def close(self):
        self.acquire()
        try:
            if self.fd:
                os.fsync(self.fd)
                os.close(self.fd)
            self.fd = 0
        finally:
            self.release()

    def _statfd(self):
        if self.fd:
            sres = os.fstat(self.fd)
            self.dev, self.ino = sres[ST_DEV], sres[ST_INO]

    def reopenIfNeeded(self):
        """
        Reopen log file if needed.

        Checks if the underlying file has changed, and if it
        has, close the old stream and reopen the file to get the
        current stream.
        """
        try:
            sres = os.stat(self.baseFilename)
        except FileNotExistError:
            sres = None

        if not sres or sres[ST_DEV] != self.dev or sres[ST_INO] != self.ino:
            if self.fd:
                os.fsync(self.fd)
                os.close(self.fd)
                self.fd = 0
                fd = self._open()
                if fd:
                    self.fd = fd
                self.rolloverAt = self.computeRollover(int(time.time()))
                self._statfd()

    def shouldRollover(self):
        """
        Determine if rollover should occur.

        record is not used, as we are just comparing times, but it is needed so
        the method signatures are the same
        """
        t = int(time.time())
        if t >= self.rolloverAt:
            return 1
        return 0

    def getFilesToDelete(self):
        """
        Determine the files to delete when rolling over.

        More specific than the earlier method, which just used glob.glob().
        """
        dirName, baseName = os.path.split(self.baseFilename)
        fileNames = os.listdir(dirName)
        result = []
        prefix = baseName + "."
        plen = len(prefix)
        for fileName in fileNames:
            if fileName[:plen] == prefix:
                suffix = fileName[plen:]
                if self.extMatch.match(suffix):
                    result.append(os.path.join(dirName, fileName))
        result.sort()
        if len(result) < self.backupCount:
            result = []
        else:
            result = result[:len(result) - self.backupCount]
        return result

    def emit(self, record):
        """
        Emit a record.

        Output the record to the file, catering for rollover as described
        in doRollover().
        """
        self.reopenIfNeeded()
        if self.shouldRollover():
            flock(self.fd)
            if self.shouldRollover():
                self.doRollover()
            funlock(self.fd)
        try:
            msg = self.format(record) + '\n'
            if type(msg) is BinaryType:
                msg = msg.decode('utf-8', 'ignore')
            if OS_NT:
                flock(self.fd)
            os.write(self.fd, msg.encode(self.encoding))
        except Exception:
            self.handleError(record)
        finally:
            if OS_NT:
                funlock(self.fd)

    def computeRollover(self, currentTime):
        """
        Work out the rollover time based on the specified time.
        """
        result = currentTime + self.interval
        if self.utc:
            t = time.gmtime(currentTime)
        else:
            t = time.localtime(currentTime)

        # rotate according natural Minute
        if self.when == 'M':
            result = currentTime + 60 - t[5]
        # rotate according natural Hour
        elif self.when == 'H':
            result = currentTime + 3600 - (t[4] * 60) - t[5]
        # rotate according natural Day
        elif self.when == 'D':
            result = currentTime + (24 - t[3]) * 3600 - t[4] * 60 - t[5]
        # If we are rolling over at midnight or weekly, then the interval is already known.
        # What we need to figure out is WHEN the next interval is.  In other words,
        # if you are rolling over at midnight, then your base interval is 1 day,
        # but you want to start that one day clock at midnight, not now.  So, we
        # have to fudge the rolloverAt value in order to trigger the first rollover
        # at the right time.  After that, the regular interval will take care of
        # the rest.  Note that this code doesn't care about leap seconds. :)
        elif self.when == 'MIDNIGHT' or self.when.startswith('W'):
            # This could be done with less code, but I wanted it to be clear
            if self.utc:
                t = time.gmtime(currentTime)
            else:
                t = time.localtime(currentTime)
            currentHour = t[3]
            currentMinute = t[4]
            currentSecond = t[5]
            currentDay = t[6]
            # r is the number of seconds left between now and the next rotation
            if self.atTime is None:
                rotate_ts = _MIDNIGHT
            else:
                rotate_ts = ((self.atTime.hour * 60 + self.atTime.minute)*60 +
                    self.atTime.second)

            r = rotate_ts - ((currentHour * 60 + currentMinute) * 60 +
                currentSecond)
            if r < 0:
                # Rotate time is before the current time (for example when
                # self.rotateAt is 13:45 and it now 14:15), rotation is
                # tomorrow.
                r += _MIDNIGHT
                currentDay = (currentDay + 1) % 7
            result = currentTime + r
            # If we are rolling over on a certain day, add in the number of days until
            # the next rollover, but offset by 1 since we just calculated the time
            # until the next day starts.  There are three cases:
            # Case 1) The day to rollover is today; in this case, do nothing
            # Case 2) The day to rollover is further in the interval (i.e., today is
            #         day 2 (Wednesday) and rollover is on day 6 (Sunday).  Days to
            #         next rollover is simply 6 - 2 - 1, or 3.
            # Case 3) The day to rollover is behind us in the interval (i.e., today
            #         is day 5 (Saturday) and rollover is on day 3 (Thursday).
            #         Days to rollover is 6 - 5 + 3, or 4.  In this case, it's the
            #         number of days left in the current week (1) plus the number
            #         of days in the next week until the rollover day (3).
            # The calculations described in 2) and 3) above need to have a day added.
            # This is because the above time calculation takes us to midnight on this
            # day, i.e. the start of the next day.
            if self.when.startswith('W'):
                day = currentDay # 0 is Monday
                if day != self.dayOfWeek:
                    if day < self.dayOfWeek:
                        daysToWait = self.dayOfWeek - day
                    else:
                        daysToWait = 6 - day + self.dayOfWeek + 1
                    newRolloverAt = result + (daysToWait * (60 * 60 * 24))
                    if not self.utc:
                        dstNow = t[-1]
                        dstAtRollover = time.localtime(newRolloverAt)[-1]
                        if dstNow != dstAtRollover:
                            if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                                addend = -3600
                            else:           # DST bows out before next rollover, so we need to add an hour
                                addend = 3600
                            newRolloverAt += addend
                    result = newRolloverAt
        return result

    def doRollover(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.
        """
        # get the time that this sequence started at and make it a TimeTuple
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        dfn = self.baseFilename + "." + time.strftime(self.suffix, timeTuple)
        if not os.path.exists(dfn) and os.path.exists(self.baseFilename):
            try:
                shutil.copy2(self.baseFilename, dfn)
                os.ftruncate(self.fd, 0)
            except Exception:
                pass

        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval

        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        #If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:           # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt
