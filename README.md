This pipeline is used with my Twitch Chat Highlights, which saves only the most interests moments to video files, with metadata in the filename. That project stores all Twitch messages in this format: "streamName$twitch username:message|seconds since epoch" . I remove special characters from "message", so this is the lowest cost way for me store it. There's also some mathematical quality filters which prevent certain messages from ever being saved to the database.

Usage: chatget.py [streamname] [timeAt] [duration]. All variables are derived from the video file.

After some quality filters, similar messages within the same time of each other are merged together using levenshtein distance.

The output of chatget.py is sent to a file. After cutting out the rough edges, and censoring unhelpful sentiment, chatvid.py generates a fluid, mobile-friendly,readable replay of chat, emotes included. 

Under each message, the total amount of people who expressed that sentiment is totaled. The first few users' names appear. for example: "DiceSA, Keepo7, +35"

With this pipeline, I embed the video of chat in sync with the origin livestream, to display their interesting reaction to the stream. https://www.youtube.com/watch?v=ZmgLTj7tLKE