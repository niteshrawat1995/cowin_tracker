from .twilio import Twilio
from .click_send import ClickSend
from .fast2sms import Fast2Sms
from .linux import Linux

TWILIO = "twilio"
CLICKSEND = "clicksend"
FAST2SMS = "fast2sms"
LINUX = "linux"

config = {
    TWILIO: Twilio,
    CLICKSEND: ClickSend,
    FAST2SMS: Fast2Sms,
    LINUX: Linux
}
