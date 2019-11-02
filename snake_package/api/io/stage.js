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