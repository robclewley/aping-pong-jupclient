# APIng pong

This is a ["serious game"](https://www.growthengineering.co.uk/what-are-serious-games/) of 1- or 2-player [Pong](https://en.wikipedia.org/wiki/Pong) intended to train intermediate-level students in data visualization and artificially intelligent control algorithms ("bots"). It  is designed to be played by (your) bots, not humans. The example client in this repo was created in Python using Jupyter notebooks and is deliberately basic so you can learn to develop a better one.

You play the game by interacting with a cloud-hosted server via a JSON REST API, which means the game is always available and is agnostic to client-side implementations of how you play. You can even try to play it from your OS shell using `curl`, e.g. by starting with `curl aping-pong.herokuapp.com/request_game/1` to begin a single-player game at Level 1.

The server will sleep when not used for extended periods, but it lives [here](https://aping-pong.herokuapp.com/) and you can wake it up by visiting the URL or using the `wakeupserver` API endpoint (see below).

Read more about the rationale for the game on [my blog](https://robclewley.github.io/2019/01/10/pong-via-api-=-aping-pong).

## An example Jupyter game client runnable in binder

Click here to try out the platform with a naive visual interface in a Jupyter notebook (it will take a minute to prepare itself): [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/robclewley/aping-pong-jupclient/master?filepath=play.ipynb)

## Features:
 * Single and two player (online)
 * Increasing levels of difficulty

Levels 1 and 2 are *single player* against a back wall (like the game of squash) and can be played immediately by accessing the API. Level 1 uses perfect frictionless physics for all bounces on walls and the paddle. Among other minor differences, level 2 approximates [paddle bounce mechanics](https://gamedev.stackexchange.com/questions/4253/in-pong-how-do-you-calculate-the-balls-direction-when-it-bounces-off-the-paddl) similar to [Pong and Breakout games](https://www.gamasutra.com/view/feature/130053/breaking_down_breakout_system_and_.php) of old. It works as if the paddle is rounded: the ball direction is reversed when it strikes the leading edge of the paddle and is reflected at a shallower angle from the trailing edge. You'll have to make some observations to infer the specifics!

Levels 3 and 4 are *two player* and you'll actually need someone else to join the lobby trying to play the same level for you to be paired. There's a timeout of around 20s so if no-one else joins you'll need to re-enter the lobby to start a new game. The paddle behavior of levels 3 and 4 match those of levels 1 and 2, respectively.

Once a game is pending, there is a timer of about 10 seconds until the ball is served. Status requests will show a negative time (countdown) while pending. Note that the paddle controls are live during this time. The serve of the ball will begin automatically from time 0 from one of the players in a 2-player game (randomly selected).

There's a limit of 3 API calls per second per player to prevent spamming and overloading the server. For bot controls, you shouldn't need many requests to infer the necessary information.

Each game consists only of a single "point" volley, and the specifications of the ball speed and court dimensions are slightly randomized. Players have 10 seconds after the game is over to request a status update about the outcome, after which the game closes. The API call counts after the game include up to 1 for any calls prior to game time 0 and none once the game has ended.

Only one game per ID is possible at a time, and previous games must finish unless the `cancel` endpoint is used (although the 10 second game reset timer will still be in effect). 2-player games cannot be canceled once begun.

There is a [public leaderboard on the landing page](https://aping-pong.herokuapp.com/dashboard) to incentivize improving volley lengths and reduce the number of API calls necessary to win. Game stats will be shown associated with the public IDs of players. If you wish to "claim" any positions on leaderboards, register a name to the `private_id` matching the `public_id`. You can also reuse your `private_id`, or have multiple of them, as you prefer.


## API endpoints:
 * `wakeupserver`
   - Use this to ensure the server is up and ready to accept new games. Repeat periodically until the server responds with a non-empty message before requesting a game.
 * `request_game/<level>`
   - Enter the game lobby to initiate a game at the specified level (see above). It returns a unique, secret `private_id` for the game session and useful contextual metadata about the game court, initial state, etc. (see Data Structures section below).
 * `status/<private_id>`
   - Valid once a game is pending. Return current state of the game.
 * `move/<private_id>/<delta_x>`
   - Valid once a game is pending. Move your paddle by the given amount, up to the allowed maximum shown in the status data. This call also returns the current state of the game.
 * `register_name/<private_id>/<public_id>/<name>`
   - Register a name to associate with a public ID, as shown on leaderboards. You have to specify the exact private ID that matches it, i.e. you must have stored the private ID after requesting a game.
   - Names must be 4 to 50 characters, unique, and spaces and mixed case are allowed.
 * `cancel/<private_id>`
   - Cancel a current game belonging to this ID. The reset timer will take effect before a new game can be started.

## Data structures

Courts are rectangular and their exact center is at (0,0). Orientation of the court is "vertical", with paddle motion along the horizontal x-axis direction.

The game request endpoint returns data like this:

```
{'context': 'Save private ID for later reference; use `status` endpoint to track further progress',
 'private_id': 'f2ee404d7eea4c2d',
 'status': 'Level 2 game countdown to your serve'}
 ```

Status and move endpoints return data like this:

```
{'ball': [0.8471329685000001, -26.9289018768],
 'court length': 53.8578037536,
 'court width': 16.9668896027,
 'max_paddle_move': 0.5,
 'status': 'Level 2 game countdown to your serve',
 't': -1.5620527267000002,
 'your public ID': 'd971b62457c65332',
 'your_paddle': [[-0.1832090784, -26.9289018768],
                 [1.8774750155, -26.9289018768]]}
```

Your paddle is described by its two endpoints along the bottom edge of the court.

You might like to store the returned data because the final JSON packet of the game will note the winner and the duration, and thereafter the game state will be inaccessible.

## Work in progress

Later levels will feature paddle velocity rather than direct control over its position, allowing the classic mechanic of applying "english" (spin) to the ball.

## Legal

By the way, no personal information is collected by the game server, including your IP address! Anonymized usage stats are logged for basic analytic purposes.
