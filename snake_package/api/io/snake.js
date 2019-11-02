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
