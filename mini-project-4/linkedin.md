Just wanted to share a quick snippet from my backend class lab today! We dove into WebSockets, and honestly, it’s a pretty interesting shift from how I normally build APIs.
I’m used to the standard REST setup where the client has to keep asking the server for new data (or you just have to refresh the page). Today, we built a real-time polling app using FastAPI where the server actually pushes the vote updates to all connected users instantly.
The biggest mental shift for me was figuring out connection management. Instead of a simple "one-and-done" request, I had to write logic to keep track of active users in a dictionary and make sure the server drops them gracefully if they close their browser tab mid-vote so the app doesn't crash.
It’s just a small lab exercise, but seeing the numbers update across different windows at the exact same time without touching the refresh button was super satisfying.
Here’s a quick recording of the UI in action.

[Linkedin Post](https://www.linkedin.com/posts/ayyoub-asri-25a911257_fastapi-websockets-backenddevelopment-ugcPost-7457902699028594688-Ofq4?utm_source=social_share_send&utm_medium=member_desktop_web&rcm=ACoAAD9RNSYBsUtIlOB_R2FuAtoKmEI2PRcYVZU)
