snake_package\api\io

body.js
```js
let id = 0;

export default function Point(config = {}) {
    this.id = id++;
    this.width = config.width || 10;
    this.x = config.x || 0;
    this.y = config.y || 0;
    this.direction = config.direction || 3; // 0上 1右 2下 3左
    this.color = config.color || 'orange';
    this.speed = 5;
}

Point.prototype.go = function () {
    if (this.direction === 0) this.goUp();
    if (this.direction === 1) this.goRight();
    if (this.direction === 2) this.goDown();
    if (this.direction === 3) this.goLeft();
};

Point.prototype.goUp = function () {
    this.y = this.y - this.speed;
};

Point.prototype.goRight = function () {
    this.x = this.x + this.speed;
};

Point.prototype.goDown = function () {
    this.y = this.y + this.speed;
};

Point.prototype.goLeft = function () {
    this.x = this.x - this.speed;
};

```



ioConnect.js
```js
/**
 * Created by jiang on 2017/3/6.
 */
import socketioJwt from 'socketio-jwt';
import config from '../config';
import stage from './stage';
import Snake from './snake';

let timer;
let addPointTimer;

const dieCheck = (snakes) => {
    for (const key in snakes) {
        const snake = snakes[key];






        for (const _key in snakes) {
            const _snake = snakes[_key];







            if (key !== _key) {
                const _bodys = _snake.bodys;
                const head = snake.bodys[0];
                const user = snake.user;

                _bodys.forEach(_body => {
                    if (
                        !(
                            head.x > _body.x + _body.width ||
                            head.x + head.width < _body.x ||
                            head.y + head.width < _body.y ||
                            head.y > _body.y + _body.width
                        )
                    ) {
                        snakes[user._id] = new Snake();
                        snakes[user._id].user = user;

                        snake.bodys.forEach(i => {
                            for (let j = 0; j < 3; j++) {
                                stage.addCustomPoints(i.x, i.y);
                            }
                        });

                        stage.addMsg({
                            from: '系统',
                            content: snakes[_key].user.name + ' 击杀了 ' + user.name
                        });
                    }
                });
            }
        }
    }
};

const crashCheck = (snakes) => {
    for (const key in snakes) {
        const snake = snakes[key];

        stage.points.forEach((food, index) => {
            if (
                food &&
                !(snake.x > food.x + food.width ||
                    snake.x + snake.bodys[0].width < food.x ||
                    snake.y + snake.bodys[0].width < food.y ||
                    snake.y > food.y + food.width)
            ) {
                stage.points[index] = null;
                snake.eatFood();
            }
        });
    }

    stage.points = stage.points.filter(i => i);
};

const check = (snakes, io) => {
    for (const key in snakes) {
        snakes[key].move();
    }

    crashCheck(snakes, io);
};

export default function ioConnect(io, runnable) {
    const onlineUsers = {};
    const snakes = {};
    stage.initPoints();

    io.path('/ws');
    io
        .on('connection', socketioJwt.authorize({
            secret: config.tokenSecret,
            timeout: 15000
        }))
        .on('authenticated', (socket) => {

            socket.shouldSend = true;
            socket.timer = null;

            socket.on('login', data => {
                socket.user = data;

                if (!snakes[data._id]) {
                    snakes[data._id] = new Snake();
                    snakes[data._id].user = data;
                }

                onlineUsers[data._id] = data;
                onlineUsers[data._id].socketId = socket.id;
                console.log(`在线人数: ${Object.keys(onlineUsers).length}    ${data.name}上线`);

                stage.addMsg({
                    from: '系统',
                    content: data.name + '上线'
                });

                clearInterval(socket.timer);
                socket.timer = setInterval(() => {
                    if (socket.shouldSend) {
                        socket.shouldSend = false;
                        socket.emit('loop', { snakes, stage });
                    }
                }, 42);
            });

            socket.on('ok', code => {
                socket.shouldSend = true;

                if (!socket.user || !code) return;

                const _id = socket.user._id;
                const self = snakes[_id];

                switch (code) {
                    case 38:
                        if (self.direction === 2) return;

                        self.direction = 0;
                        break;
                    case 39:
                        if (self.direction === 3) return;

                        self.direction = 1;
                        break;
                    case 40:
                        if (self.direction === 0) return;

                        self.direction = 2;
                        break;
                    case 37:
                        if (self.direction === 1) return;

                        self.direction = 3;
                        break;
                    default:
                        break;
                }

                self.boundaryCheck();
            });

            socket.on('disconnect', () => {
                if (!socket.user) return;

                delete onlineUsers[socket.user._id];

                console.log(`在线人数: ${Object.keys(onlineUsers).length}    ${socket.user.name}下线`);

                stage.addMsg({
                    from: '系统',
                    content: socket.user.name + '下线'
                });
            });

            socket.on('message', msg => {
                if (!socket.user) return;

                stage.addMsg({
                    from: socket.user.name,
                    content: msg
                });
            });

            socket.on('reset', () => {
                if (!socket.user) return;

                // snakes[socket.user._id] = new Snake();
                // snakes[socket.user._id].user = socket.user;

                snakes[socket.user._id].resetColor();
            });
        });

    io.listen(runnable);

    clearInterval(timer);
    timer = setInterval(() => {
        check(snakes, io);
        dieCheck(snakes);
    }, 42);

    clearInterval(addPointTimer);
    addPointTimer = setInterval(() => {
        for (let i = 0; i < 10; i++) {
            stage.addPoints();
        }
    }, 3000);
}


```


saveOffLineMsg.js
```js
import mongoose from 'mongoose';
const Admin = mongoose.model('Admin');

export default function saveOffLineMsg(data) {
  const {to} = data;
  Admin
    .findOne({_id: to})
    .select('_id message_off_line')
    .exec((error, doc) => {
      if (error) {
        console.log('查询用户出错:' + error);
      } else {
        const newMessageArr = (doc.message_off_line && doc.message_off_line.length > 0) ? doc.message_off_line : [];
        newMessageArr.push(data);
        Admin.findOneAndUpdate({_id: doc._id}, {message_off_line: newMessageArr}, (error) => {
          if (error) console.log('存储离线消息错误:' + error);
        });
      }
    });
}

```



saveOnLineMsg.js
```js
import mongoose from 'mongoose';
const Message = mongoose.model('Message');
const File = mongoose.model('File');

export default function saveOnLineMsg(data) {

  return new Promise((resolve, reject) => {

    const { file, ...message } = data;

    if (file) {
      const fileObj = new File(file);
      const messageObj = new Message(message);
      messageObj.file = fileObj._id;

      fileObj.save();
      messageObj.save((error) => {
        if (error) reject('存储message错误:' + error);
        messageObj.file = fileObj;
        resolve(messageObj);
      });
    } else {
      const messageObj = new Message(message);
      messageObj.save((error) => {
        if (error) reject('存储message错误:' + error);
        resolve(messageObj);
      });
    }

  });
}

```


sendOffLineMsg.js
```js
import mongoose from 'mongoose';
const Admin = mongoose.model('Admin');
const Message = mongoose.model('Message');

export default function sendOffLineMsg(_id) {

  return new Promise((resolve, reject) => {
    Admin
      .findOne({_id})
      .select('_id message_off_line')
      .exec((error, doc) => {
        if (error) {
          reject('查询用户失败:' + error);
        } else {
          if (doc && doc.message_off_line && doc.message_off_line.length > 0) {

            const {message_off_line} = doc;
            Admin.findOneAndUpdate({_id: doc._id}, {message_off_line: []}, (error) => {
              if (error) reject('更新用户离线消息出错:' + error);
            });
            message_off_line.forEach((item) => {
              const message = new Message();
              message.come = item._id;
              message.to = item.to;
              message.msg = item;
              message.save((error) => {
                if (error) console.log('存储message错误:' + error);
              });
            });
            resolve(message_off_line);

          } else {
            reject('');
          }
        }
      });
  });

}

```



snake.js
```js
import stage from './stage';
import Body from './body';

let id = 0;

function getRandomColor() {
    const rand = Math.floor(Math.random() * 0xFFFFFF).toString(16);
    if (rand.length === 6) {
        return rand;
    } else {
        return getRandomColor();
    }
}

function getRGB(_color) {
    let color = _color.toLowerCase();

    if (color.length === 4) {
        let colorNew = '#';
        for (let i = 1; i < 4; i += 1) {
            colorNew += color.slice(i, i + 1).concat(color.slice(i, i + 1));
        }
        color = colorNew;
    }

    const colorChange = [];

    for (let i = 1; i < 7; i += 2) {
        colorChange.push(parseInt('0x' + color.slice(i, i + 2)));
    }

    return colorChange;
}

export default function Snake(config = {}) {
    const color = '#' + getRandomColor();

    this.id = id++;
    this.length = config.length || 10;
    this.direction = config.direction || 3; // 0上 1右 2下 3左
    this.x = config.x || parseInt(Math.random() * stage.width);
    this.y = config.y || parseInt(Math.random() * stage.height);
    this.speed = config.speed || 95;
    this.life = config.life || 1;
    this.bodys = [];
    this.space = 0;
    this.pointLength = 5;
    this.bigFood = 0;
    this.currentFood = 0;
    this.color = color;
    this.rgb = getRGB(color);
    this.moveLen = 0;
    this.lv = 1;
    this.speed = 10;
    this.weight = 0;

    this.init();
}

Snake.prototype.resetColor = function() {
    this.color = '#' + getRandomColor();
    this.rgb = getRGB(this.color);
};

Snake.prototype.init = function () {
    this.createBody();
};

Snake.prototype.eatFood = function () {
    this.bigFood++;
    this.currentFood++;
    this.weight++;

    if (this.currentFood >= this.pointLength - 4) {
        this.currentFood = 0;

        const lastBody = this.bodys[this.bodys.length - 1];

        const body = new Body({
            x: this.lastState ? this.lastState.x : lastBody.x + (this.pointLength + this.space),
            y: this.lastState ? this.lastState.y : lastBody.y,
            width: this.pointLength,
            height: this.pointLength,
            color: this.color
        });

        this.bodys.push(body);
        this.length++;
    }

    if (this.bigFood >= ((this.pointLength - 4) * 10)) {
        this.bigFood = 0;

        this.pointLength++;
        this.lv++;

        this.bodys.forEach(i => {
            i.width = this.pointLength;
            i.height = this.pointLength;
        });
    }
};

Snake.prototype.boundaryCheck = function () {
    if (this.direction === 3 && this.x <= this.pointLength * 2) this.direction = 2;
    if (this.direction === 1 && this.x >= stage.width - (this.pointLength + this.space) * 2) this.direction = 0;
    if (this.direction === 0 && this.y <= this.pointLength * 2 + this.space) this.direction = 3;
    if (this.direction === 2 && this.y >= stage.height - (this.pointLength * 2 + this.space)) this.direction = 1;
};

Snake.prototype.createBody = function () {
    for (let i = 0; i < this.length; i++) {
        const body = new Body({
            x: this.x + i * (this.pointLength + this.space),
            y: this.y,
            width: this.pointLength,
            height: this.pointLength,
            color: this.color
        });

        this.bodys.push(body);
    }
};

Snake.prototype.move = function () {
    this.boundaryCheck();

    const head = this.bodys[0];

    const speed = head.speed;
    const _speed = 5 - ((this.lv + 9) / 10 - 1);

    if (speed !== _speed && speed > 1) {
        this.speed = _speed;
        this.bodys.forEach(i => i.speed = _speed);
    }

    head.go();
    this.moveLen += head.speed;

    if (this.moveLen + head.speed < this.pointLength + this.space) return;

    this.moveLen = 0;

    const states = this.bodys.map(function (i) {
        return Object.assign({}, i);
    });

    this.lastState = states[states.length - 1];

    head.direction = this.direction;
    this.x = head.x;
    this.y = head.y;
    this.direction = head.direction;

    this.bodys.forEach(function (i, index) {
        if (index !== 0) {
            i.direction = states[index - 1].direction;
            i.x = states[index - 1].x;
            i.y = states[index - 1].y;
        }
    });
};


```


stage.js
```js
let id = 0;
let messageId = 0;

export default {
    width: 1920,
    height: 900,
    points: [],
    message: [],
    addPoints() {
        const r = Math.floor(Math.random() * 256);
        const g = Math.floor(Math.random() * 256);
        const b = Math.floor(Math.random() * 256);
        const color = '#' + r.toString(16) + g.toString(16) + b.toString(16);

        this.points.push({
            id: id,
            x: parseInt(Math.random() * this.width),
            y: parseInt(Math.random() * this.height),
            width: parseInt(Math.random() * 2 + 2),
            color
        });

        id++;

        if (this.points.length > 3000) this.points.splice(0, this.points.length - 3000);
    },
    addCustomPoints(x, y) {
        const r = Math.floor(Math.random() * 256);
        const g = Math.floor(Math.random() * 256);
        const b = Math.floor(Math.random() * 256);
        const color = '#' + r.toString(16) + g.toString(16) + b.toString(16);

        this.points.push({
            id: id,
            x: parseInt(Math.random() * 11 + x),
            y: parseInt(Math.random() * 11 + y),
            width: parseInt(Math.random() * 2 + 2),
            color
        });

        id++;

        if (this.points.length > 3000) this.points.splice(0, this.points.length - 3000);
    },
    initPoints() {
        for (let i = 0; i < 500; i++) {
            this.addPoints();
        }
    },
    addMsg(obj) {
        if (this.message.length > 100) {
            this.message.shift();
        } else {
            this.message.push({ ...obj, id: messageId++ });
        }
    }
};

```
