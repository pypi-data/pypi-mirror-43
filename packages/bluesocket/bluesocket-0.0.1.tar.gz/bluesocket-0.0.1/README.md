# bluesocket
Logger for Django Channels

Push your logging through socket connection.

```
from bluesocket import Logger, logging`

logger = Logger(consumer, "name", level=logging.DEBUG)
logger.debug('message')
```

# Supported Consumers

`from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer`

# Install

`pip install bluesocket`
