if __name__ == "__main__":
    import asyncio
    import threading

    from src.api import *

    feed = WebsocketFeed("credentials/coinbasepro.json")
    loop = asyncio.get_event_loop()
    def background(loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(feed.subscribe("status", "status"))
        loop.run_until_complete(feed.listen())
    thread = threading.Thread(target=background, args=(loop,))
    thread.start()