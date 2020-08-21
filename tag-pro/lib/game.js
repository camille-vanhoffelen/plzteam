import $ from "jquery";
import Player from './player'
import Flag from './flag'
import Spike from './spike'
import CollisionDectector from './collision-detector'

export default class Game {
  constructor(gameID, context, canvas, keyboard, map, blueprint) {
    this.gameID = gameID
    this.canvas = canvas
    this.context = context
    this.keyboard = keyboard
    this.map = map
    this.players = []
    this.flags = []
    this.blueprint = blueprint
    this.spikes = []
    this.collisionDetector = {}     
    this.running = false
    this.initial = true
  }

  init() {
    let self = this

    self.players.push(new Player(self.map, self.blueprint.redPlayerOptions))
    self.players.push(new Player(self.map, self.blueprint.bluePlayerOptions))

    self.flags.push(new Flag(self.blueprint.blueFlagOptions))
    self.flags.push(new Flag(self.blueprint.redFlagOptions))

    if (self.blueprint.spikes) {
      self.blueprint.spikes.forEach(spikeOptions => {
        self.spikes.push(new Spike(spikeOptions))
      })
    }
    self.collisionDetector = new CollisionDectector(self.players, self.flags, self.spikes)
  }

  start() {
    let self = this
    self.running = true
  }

  update(game_counter) {
    this.updateScoreboard()
    this.players.forEach(player => player.move(this.keyboard.keys))
    this.send_data()
    this.spikes.forEach(spike => spike.move(game_counter))
    this.collisionDetector.checkAllCollisions()
  }

  player_data(player) {
    return {
      'player_id': player.player_id,
      'x': player.x,
      'dx': player.dx,
      'y': player.y,
      'dy': player.dy
    }
  }

  send_data() {
    let players_data = this.players.map(this.player_data)
    let data = { 
       'game_id' : this.gameID,
       'initial' : this.initial,
       'players': players_data
    }
    $.post( "http://localhost:6969/sneklisten/", JSON.stringify(data));
  }

  updateScoreboard() {
    document.querySelector("#red-score").innerHTML = this.collisionDetector.redScore
    document.querySelector("#blue-score").innerHTML = this.collisionDetector.blueScore
  }

  draw() {
    this.context.clearRect(0, 0, this.canvas.width, this.canvas.height)
    this.map.render(this.context)
    this.flags.forEach(flag => flag.draw(this.context))
    this.spikes.forEach(spike => spike.draw(this.context))
    this.players.forEach(player => player.draw(this.context))
  }
}
