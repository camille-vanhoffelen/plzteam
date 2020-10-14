import $ from "jquery";
import Player from './player'
import Flag from './flag'
import Spike from './spike'
import CollisionDectector from './collision-detector'

/*
 * Game of "Catch me if you can"
 */
export default class Game {
    constructor(gameID, context, canvas, keyboard, map, blueprint, timeLimit) {
        this.gameID = gameID
        this.canvas = canvas
        this.context = context
        this.keyboard = keyboard
        this.map = map
        this.flags = []
        this.blueprint = blueprint
        this.spikes = []
        this.collisionDetector = {}
        this.timeLimit = timeLimit
        this.timer = timeLimit
        this.running = false
        this.isInitial = true
        this.isFinal = false
        this.winner = null
        this.init()
    }

    init() {
        let self = this

        self.attacker = new Player(self.map, self.blueprint.redPlayerOptions)
        self.defender = new Player(self.map, self.blueprint.bluePlayerOptions)

        self.flags.push(new Flag(self.blueprint.blueFlagOptions))
        self.flags.push(new Flag(self.blueprint.redFlagOptions))

        if (self.blueprint.spikes) {
            self.blueprint.spikes.forEach(spikeOptions => {
                self.spikes.push(new Spike(spikeOptions))
            })
        }
        self.collisionDetector = new CollisionDectector([self.attacker, self.defender], self.flags, self.spikes)
    }

    start() {
        let self = this
        self.running = true
    }

    update(gameCounter) {
        this.timer = this.timeLimit - gameCounter
        if (this.timer === 0) {
            this.timeOut()
        } else {
            this.updateScoreboard()
            this.attacker.move(this.keyboard.keys)
            this.defender.move(this.keyboard.keys)
            this.spikes.forEach(spike => spike.move(gameCounter))
            this.collisionDetector.checkAllCollisions()
            if (this.collisionDetector.ballCollisions.collided) {
                this.collision()
            }
        }
    }

    timeOut() {
        this.isFinal = true
        this.winner = this.defender.player_id
        this.timer = 0
    }

    collision() {
        this.isFinal = true
        this.winner = this.attacker.player_id
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

    sendData() {
        console.log(typeof this.player_data(this.attacker))
        let data = {
            'game_id': this.gameID,
            'initial': this.isInitial,
            'final': this.isFinal,
            'attacker': this.player_data(this.attacker),
            'defender': this.player_data(this.defender),
            'winner': this.winner,
            'timer' : this.timer
        }
        console.log(data)
        $.post("http://localhost:6969/sneklisten/", JSON.stringify(data));
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
        this.attacker.draw(this.context)
        this.defender.draw(this.context)
    }
}
