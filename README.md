# APIng pong Jupyter client in binder

This is an API-based ping pong game. It is intended as a mode of training data visualization and artificially intelligent control algorithms ("bots"). The game is also meant to be played by (your) bots, not humans. This example client is deliberately basic and you are supposed to develop a better one to play effectively. Later, there will be a public leaderboard on a landing page. No personal information is collected, including your IP address!

Click below to play:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/robclewley/aping-pong-jupclient/master?filepath=play.ipynb)

## Features:
 * Single and two player (online)
 * Increasing levels of difficulty

Levels 1 and 2 are *single player* (squash) and can be played instantly.

Levels 3 and 4 are *two player* (you'll actually need someone else to join the lobby trying to play the same level for you to be paired). There's a timeout if no-one else joins.

Once a game has been initiated, there is a timeout of about 10 seconds before the game will start. Status requests will show negative time (countdown) to reflect this. The serve of the ball will begin automatically from time 0 from one of the players (randomly selected).

Each game consists only of a single "point" volley, and the specifications of the ball speed and court dimensions are slightly randomized.

## Endpoints:
 * `request_game/<level>`
   - returns a unique `private_id` for the game session and useful contextual metadata about the game court, initial state, etc.
 * `status/<private_id>`
   - return current state of game.
 * `move/<private_id>/<dx>`
   - can only move paddle up to a maximum given in the status data.
