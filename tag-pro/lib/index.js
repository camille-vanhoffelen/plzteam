import Game from './game'
import Keyboard from './keyboard'
import Map from './map'
import MapBlueprint from './map-blueprint'
import Dom from './dom'

var canvas = document.getElementById('game')
var context = canvas.getContext('2d')

var mapLevel = "level_one"
const dom = new Dom()
var game = null
var keyboard = new Keyboard().listenForEvents()
var gameCounter = 0
var timeLimit = 500


requestAnimationFrame(function gameLoop() {

    // initial state
    if (keyboard.keys.reset) {
        console.log("Reset game")
        keyboard.keys.reset = false
        let gameID = keyboard.metadata.gameID
        setStage(mapLevel)
        initTotalScores()
        game = prepareGame(gameID, mapLevel)
        gameCounter = 0
        game.start()
        renderTimeBar()
        game.sendData()
        game.draw()
        game.isInitial = false
    }

    // main loop
    if (game && !game.isFinal) {
        gameCounter++
        renderTimeBar()
        game.update(gameCounter)
        game.draw()
        game.sendData()

    // final state
    } else if (game) {
        game.sendData()
    }

    requestAnimationFrame(gameLoop)
})

function renderTimeBar() {
    var timeCanvas = document.getElementById('time-bar')
    var timeContext = timeCanvas.getContext('2d')

    timeContext.clearRect(0, 0, timeCanvas.width, timeCanvas.height)
    timeContext.beginPath()

    timeContext.fillStyle = "#d3d3d3"
    timeContext.fillRect(0, 0, timeCanvas.width, timeCanvas.height)
    timeContext.fillStyle = "green"

    timeContext.fillRect(0, 0, timeCanvas.width * (1 - gameCounter / timeLimit), timeCanvas.height)
}

function setStage(level) {
    console.log("Setting stage, level: " + level)
    dom.hideMenu()
    dom.showGame(level)
    // TODO remove this? don't need if always reset to start
    // prepareGame(level, dom.canvas)
}

function displayTotalScores() {
    document.querySelector("#red-total").innerHTML = localStorage.getItem('redTotal')
    document.querySelector("#blue-total").innerHTML = localStorage.getItem('blueTotal')
}

function initTotalScores() {
    localStorage.getItem('redTotal') || localStorage.setItem('redTotal', 0)
    localStorage.getItem('blueTotal') || localStorage.setItem('blueTotal', 0)
}

function writeTotalScores(game) {

    if (game && game.collisionDetector.redScore > game.collisionDetector.blueScore) {
        alert("Red Won!")
        localStorage.setItem('redTotal', parseInt(localStorage.getItem('redTotal')) + 1)
    } else if (game && game.collisionDetector.redScore < game.collisionDetector.blueScore) {
        alert("Blue Won!")
        localStorage.setItem('blueTotal', parseInt(localStorage.getItem('blueTotal')) + 1)
    } else {
        alert("Tie Game!")
    }
}

function prepareGame(gameID, mapLevel) {
    var blueprint = new MapBlueprint()[mapLevel]
    var map = new Map(blueprint)

    canvas.setAttribute("width", `${map.cols * map.tsize}px`)
    canvas.setAttribute("height", `${map.rows * map.tsize}px`)

    var game = new Game(gameID, context, canvas, keyboard, map, blueprint, timeLimit)
    game.init()
    return game
}
