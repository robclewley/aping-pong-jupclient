# APIng pong Jupyter client in binder

This is a JSON REST API-based ping pong game that connects to a cloud-hosted server, which means the game is always available and is agnostic to client-side implementations for play. You can even try to play it from your OS shell using `curl`, e.g. by starting with `curl aping-pong.herokuapp.com/request_game/1` to begin a single-player game at Level 1.

The game is intended as a setting to train intermediate-level students in data visualization and artificially intelligent control algorithms ("bots"). The game is designed to be best played by (your) bots, not humans. This example client was created in Python using Jupyter notebooks and is deliberately basic and you can learn to develop a better one to play it effectively.

Click here to play manually to try out the platform: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/robclewley/aping-pong-jupclient/master?filepath=play.ipynb)

## Features:
 * Single and two player (online)
 * Increasing levels of difficulty

Levels 1 and 2 are *single player* against a back wall (like the game of squash) and can be played immediately by accessing the API. Level 1 uses perfect frictionless physics for all bounces on walls and the paddle. Among other minor differences, level 2 approximates [paddle bounce mechanics](https://gamedev.stackexchange.com/questions/4253/in-pong-how-do-you-calculate-the-balls-direction-when-it-bounces-off-the-paddl) similar to [Pong and Breakout games](https://www.gamasutra.com/view/feature/130053/breaking_down_breakout_system_and_.php) of old. It works as if the paddle is rounded: the ball direction is reversed when it strikes the leading edge of the paddle and is reflected at a shallower angle from the trailing edge. You'll have to make some observations to infer the specifics!

Levels 3 and 4 are *two player* and you'll actually need someone else to join the lobby trying to play the same level for you to be paired. There's a timeout of around 20s so if no-one else joins you'll need to re-enter the lobby to start a new game. The paddle behavior of levels 3 and 4 match those of levels 1 and 2, respectively.

Once a game is pending, there is a timeout of about 10 seconds before the ball is served. Status requests will show a negative time (countdown) to reflect this. Note that the game controls are live during the time that the game is pending. The serve of the ball will begin automatically from time 0 from one of the players (randomly selected).

There's a limit of 3 API calls per second per player to prevent spamming and overloading the server. For bot controls, you shouldn't need many requests to determine the information needed for correctly moving the paddle.

Each game consists only of a single "point" volley, and the specifications of the ball speed and court dimensions are slightly randomized. Players have 1 minute after the game is over to request a status update about the outcome, after which the game closes. The API call counts after the game include up to 1 for any calls prior to game time 0 and none once the game has ended.

## API endpoints:
 * `wakeupserver`
   - Use this to ensure the server is up and ready to accept new games. Repeat periodically until the server responds with a non-empty message before requesting a game.
 * `request_game/<level>`
   - Enter the game lobby to initiate a game at the specified level (see above). It returns a unique `private_id` for the game session and useful contextual metadata about the game court, initial state, etc. (see Data Structures section below).
 * `status/<private_id>`
   - Valid once a game is pending. Return current state of the game.
 * `move/<private_id>/<delta_x>`
   - Valid once a game is pending. Move your paddle by the given amount, up to the allowed maximum shown in the status data. This call also returns the current state of the game.

## Data structures

Courts are rectangular and their exact center is at (0,0). Orientation is vertical, and paddles along in the horizontal x-axis.

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

There will be a public leaderboard on a landing page with incentives to improve volley lengths and reduce the number of API calls necessary to win. Game stats will be shown associated with the public IDs of players. If you wish to "claim" any positions on leaderboards, you'll be able to submit the `private_id` matching the `public_id` to add your name or tag. You can also reuse your `private_id`, or have multiple of them, as you prefer.

## Legal

By the way, no personal information is collected by the game server, including your IP address! Anonymized usage stats are logged for basic analytic purposes.
