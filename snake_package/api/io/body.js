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