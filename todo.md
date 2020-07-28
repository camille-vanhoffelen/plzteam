# TODO

## Usefull Links

- [Multi Agent RL](https://bair.berkeley.edu/blog/2018/12/12/rllib/)
- [Open AI 5](https://openai.com/blog/openai-five/)

## Random Thoughts

- maybe we'll need to change the keypress dtos: instead of keyup and keydown, have keypress and associated duration. could be more precise, both when reading between processes (as currently it is io speed dependent), but also when sending over api.
- we need to setup a game with a juke friendly situation (maybe only one flag, and one player spawns on that flag?) can change all this in lib/mapblueprint.js, it's v clean code.
- I'm stepping in RL territory, but I wonder if it's better to have a game where when "tagger" catches "juker", it wins and game resets, vs the "tagger" racks up more points teh more times it catches juker
- I think a game with a square map, no flag, and a game of tag, one ball has to hit the other ball before time runs out. that is a very good game for RL.