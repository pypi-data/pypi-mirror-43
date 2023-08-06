from notification import Notification, NotificationEvent
from reason import Reason, ReasonCode
import json

if __name__ == "__main__":
    r = Reason(ReasonCode.GENERAL_ERROR, 'seila')
    n = Notification(event=NotificationEvent.Failed, reason=r)
    print(n.ToJson())
    # print(json.dumps(n.ToJson(), indent=4))
