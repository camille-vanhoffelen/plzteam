# :pray: plzteam

plz get re

* [**tag-pro**](tag-pro)  
Runs tagpro in ur most favorite browser. Sends data to bff snekpro. Listens to snekpro for advice on how to move balls.
* [**snekpro**](snekpro)  
snekpro plays tagpro very good. Listens to data from bff tagpro. Computes good moves with reptile brain. Then sends keypresses to tagpro.

tag-pro and snekpro are friends, they like to run together.

## tag-pro

### Getting Started

```bash
cd tag-pro
./start_tagpro.sh
```

then visit [http://localhost:8080/webpack-dev-server/](http://localhost:8080/webpack-dev-server/)

### Installation

**Required: nvm**

```bash
cd tag-pro
nvm install 10.22
nvm exec 10.22 npm install
```

### Development

##### Sending data

Ball data is sent from `send_data()` in [player.js](tag-pro/lib/player.js).

Keypress data is listened by `listenForEvents()` in [keyboard.js](tag-pro/lib/keyboard.js).

## snekpro

### Getting Started

```bash
cd snekpro
./start_snekpro.sh
```

This will operate a POST endpoint at [http://localhost:6969/sneklisten](http://localhost:6969/sneklisten), server sent events on [http://localhost:6969/snekspeak](http://localhost:6969/snekspeak). Plz don't visit these, they are for tagpro.

### Installation

**Required: python 3.8.X, pipenv**

```bash
cd snekpro
pipenv install
```

### Development

uses [fastapi](https://fastapi.tiangolo.com/). many tutorials there.


