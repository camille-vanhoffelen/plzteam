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
- reset button works now, but mapLevel is hardcoded. I will take that out of the event listener next, and put in as CLI argument for node.

- the externalMultAgentEnv interface makes it so that that both agent take actions and observe at the same time, maybe seperate it into two single agent env running in parrallel?