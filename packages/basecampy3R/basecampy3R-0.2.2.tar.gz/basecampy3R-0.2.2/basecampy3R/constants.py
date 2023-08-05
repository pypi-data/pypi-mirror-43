from .__version__ import __version__

API_URL = "https://3.basecampapi.com/"

DOCK_NAME_CAMPFIRE = 'chat'
DOCK_NAME_MESSAGE_BOARD = 'message_board'
DOCK_NAME_TODOS = 'todoset'
DOCK_NAME_SCHEDULE = 'schedule'
DOCK_NAME_CHECKIN = 'questionnaire'
DOCK_NAME_VAULT = 'vault'
DOCK_NAME_FORWARDS = 'inbox'

RATE_LIMIT_REQUESTS = 50
RATE_LIMIT_PER_SECONDS = 10

VERSION = __version__

USER_AGENT = "BasecamPY3 {version} (https://github.com/phistrom/basecampy3)".format(version=VERSION)
