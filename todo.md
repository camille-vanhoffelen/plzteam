# TODO

## Usefull Links

- [Multi Agent RL](https://bair.berkeley.edu/blog/2018/12/12/rllib/)
- [Open AI 5](https://openai.com/blog/openai-five/)
- [reward](https://www.researchgate.net/post/What_is_the_best_Reward_function_in_Reinforcement_Learning)
- [optimization functions](https://en.wikipedia.org/wiki/Test_functions_for_optimization)

## Random Thoughts

- maybe we'll need to change the keypress dtos: instead of keyup and keydown, have keypress and associated duration. could be more precise, both when reading between processes (as currently it is io speed dependent), but also when sending over api.
- we need to setup a game with a juke friendly situation (maybe only one flag, and one player spawns on that flag?) can change all this in lib/mapblueprint.js, it's v clean code.
- I'm stepping in RL territory, but I wonder if it's better to have a game where when "tagger" catches "juker", it wins and game resets, vs the "tagger" racks up more points teh more times it catches juker
- I think a game with a square map, no flag, and a game of tag, one ball has to hit the other ball before time runs out. that is a very good game for RL.
- if the fixed size game states list becomes too slow, [here](https://docs.python.org/2/library/multiprocessing.html#examples) is how we can implement shared deque.

- reset button works now, but mapLevel is hardcoded. I will take that out of the event listener next, and put in as CLI argument for node. (CANT HAVE CLI ARGUMENT)
- instead of node CLI arguments, add mapLevel to reset event on snekspeak side, so CLI is in python
- need to make sure agent can guarantee that observations were taken _after_ the latest action was taken. Can do that with action ids, and GameState keeps "latest action taken" variable with id.
- two game modes - "RL training" and "player", where "RL training" has no menu and starts straight into game, and where "player" has menu and the already trained RL agent is used as AI. 
- bound observations based on map? (e.g x y can't be more or less than map boundaries




-- need to add server and client https://github.com/ray-project/ray/blob/master/rllib/examples/serving/cartpole_client.py