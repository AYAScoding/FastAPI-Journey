1- I use a dictionary called active_connections. It acts like a guest list where the "Key" is the Poll ID and the "Value" is a list of everyone's WebSocket connection.If a user closes their tab, the code catches a WebSocketDisconnect error.The app is graceful. It just removes that one person from the list so the server doesn't try to send them data anymore. It doesn't crash the whole app.

2- I used a Python dictionary because it’s the fastest way to build a prototype. It doesn't require setting up a separate database.Since the data is only in the computer's RAM, everything is deleted if I restart the server.But To make this real, I would need a database so the votes stay saved even if the power goes out.

3- a Race condition could be triggered,wich could result losing some votes , specially in big projects that have a lot of users.

4- the key difference is that Rest requires you to refresh the page in order to get fresh data, but for websocket it's live and you can see the changes happening without refresh, each of them has it's usecases, web socket where real time updates are crusial and rest for generally most of the other cases.