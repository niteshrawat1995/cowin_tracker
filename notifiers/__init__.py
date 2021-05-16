from .twilio import Twilio
from .click_send import ClickSend
from .fast2sms import Fast2Sms
from .linux import Linux
from .gmail import Gmail

TWILIO = "twilio"
CLICKSEND = "clicksend"
FAST2SMS = "fast2sms"
LINUX = "linux"
GMAIL = "gmail"

config = {
    TWILIO: Twilio,
    CLICKSEND: ClickSend,
    FAST2SMS: Fast2Sms,
    LINUX: Linux,
    GMAIL: Gmail
}
