from glob import glob
from os.path import expanduser
from sqlite3 import connect

from instaloader import ConnectionException, Instaloader

'''
To add user and account info, make sure you are currently logged into specified account on firefox.
'''


## firefox cookie database location
FIREFOXCOOKIEFILE = glob(expanduser("C:/Users/madel\AppData/Roaming/Mozilla/Firefox/Profiles/4zse1jac.default-release/cookies.sqlite"))[0]

## only allow one attempt for session connection
instaloader = Instaloader(max_connection_attempts=1)

## get cookie id for instagram
instaloader.context._session.cookies.update(connect(FIREFOXCOOKIEFILE)
                                            .execute("SELECT name, value FROM moz_cookies "
                                                     "WHERE host='.instagram.com'"))
## check connection
try:
    username = instaloader.test_login()
    if not username:
        raise ConnectionException()
except ConnectionException:
    raise SystemExit("Cookie import failed. Are you logged in successfully in Firefox?")

instaloader.context.username = username

## save session to instaloader file for later use
instaloader.save_session_to_file()
