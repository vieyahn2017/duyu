import socketioJwt from 'socketio-jwt';
import config from '../config';
import stage from './stage';
import Snake from './snake';

let timer;
let addPointTimer;

const dieCheck = (snakes) => {
    for (const key in snakes) {
        const snake = snakes[key];

        if (snake.is_offline == true) {
            continue;
        }

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

        if (snake.is_offline == true) {
            continue;
        }
        
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

            socket.on('offline', () => {
                if (!socket.user) return;
                snakes[socket.user._id].offline();
            });

            socket.on('online', () => {
                if (!socket.user) return;
                snakes[socket.user._id].online();
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
