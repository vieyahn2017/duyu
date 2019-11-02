snake_package\src\helpers

ApiClient.js
```js
import superagent from 'superagent';
import config from '../config';

const methods = ['get', 'post', 'put', 'patch', 'del'];

function formatUrl(path) {
    const adjustedPath = path[0] !== '/' ? '/' + path : path;
    if (__SERVER__) {
        // Prepend host and port of the API server to the path.
        return 'http://' + config.apiHost + ':' + config.apiPort + adjustedPath;
    }
    // Prepend `/api` to relative URL, to proxy to API server.
    return '/api' + adjustedPath;
}

export default class ApiClient {
    constructor(req) {
        methods.forEach((method) =>
            this[method] = (path, { params, data } = {}) => new Promise((resolve, reject) => {
                const request = superagent[method](formatUrl(path));

                if (__SERVER__ && req.get('cookie')) {
                    request.set('cookie', req.get('cookie'));
                }

                if (params) {
                    request.query(params);
                }

                if (data) {
                    request.send(data);
                }

                request.end((err, { body } = {}) => err ? reject(body || err) : resolve(body));
            }));
    }

    empty() {
    }
}


```

Html.js
```js
import PropTypes from 'prop-types';
import React, { Component } from 'react';
import ReactDOM from 'react-dom/server';
import serialize from 'serialize-javascript';
import Helmet from 'react-helmet';

export default class Html extends Component {
    static propTypes = {
        assets: PropTypes.object,
        component: PropTypes.node,
        store: PropTypes.object
    };

    render() {
        const { assets, component, store } = this.props;
        const content = component ? ReactDOM.renderToString(component) : '';
        const head = Helmet.rewind();

        return (
            <html lang="en-us">
            <head>
                {head.base.toComponent()}
                {head.title.toComponent()}
                {head.meta.toComponent()}
                {head.link.toComponent()}
                {head.script.toComponent()}

                <link
                    rel="shortcut icon"
                    href="/favicon.ico"
                />

                <meta
                    name="viewport"
                    content="width=device-width, initial-scale=1"
                />

                {
                    Object.keys(assets.styles).map((style, key) =>
                        <link
                            href={assets.styles[style]}
                            key={key}
                            media="screen, projection"
                            rel="stylesheet"
                            type="text/css"
                            charSet="UTF-8"
                        />
                    )}

                {
                    Object.keys(assets.styles).length === 0 ?
                        <style
                            dangerouslySetInnerHTML={{ __html: require('../containers/App/App.scss')._style }}
                        /> : null
                }
            </head>

            <body>
            <div
                id="content"
                dangerouslySetInnerHTML={{ __html: content }}
            />
            <script
                dangerouslySetInnerHTML={{ __html: `window.__data=${serialize(store.getState())};` }}
                charSet="UTF-8"
            />
            <script
                src={assets.javascript.main}
                charSet="UTF-8"
            />
            </body>
            </html>
        );
    }
}


```

snake_package\src\lib
Ball.js
```js
/**
 * Created by jiang_mac on 2016/10/13.
 */
function Ball(config) {
    if (!config) config = {};
    var randomR = Math.floor(Math.random() * 30 + 1);
    var contentEl = config.content ? document.getElementById(config.content) : document.body;
    var el = document.createElement('div');

    this.contentEl = contentEl;
    this.el = el;
    this.r = config.r || randomR;
    this.backgroundColor = config.backgroundColor || 'rgba(' + Math.floor(Math.random() * 255 + 1) + ',' + Math.floor(Math.random() * 255 + 1) + ',' + Math.floor(Math.random() * 255 + 1) + ',' + Math.random() + ')';
    this.left = config.left || Math.floor(Math.random() * (contentEl.offsetWidth - (config.r || randomR) * 2) + 1);
    this.top = config.top || Math.floor(Math.random() * (contentEl.offsetHeight - (config.r || randomR) * 2) + 1);
    this.speed = config.speed || Math.floor(Math.random() * 15 + 1);
    this.move = typeof config.move === 'undefined' ? true : config.move;
    this.life = config.life || 1;
    this.type = config.type || 'free';
    this.crash = typeof config.crash == 'undefined' ? false : config.crash;
    this.keyboard = typeof config.keyboard === 'undefined' ? false : config.keyboard;
    this.pause = false;
    this.maxLife = config.life || 1;
    this.spring = typeof config.spring === 'undefined' ? false : config.spring;
    this.state = Math.floor(Math.random() * 4 + 1);
    this.moveSpeedIndex = 0;
    this.moveSpeed = 2;
    this.checkSpeedIndex = 0;
    this.checkSpeed = 100;
    this.time = null;

    this.init();
}

Ball.prototype.init = function () {
    var elStyle = this.el.style;
    elStyle.position = 'absolute';
    elStyle.width = 2 * this.r + 'px';
    elStyle.height = 2 * this.r + 'px';
    elStyle.backgroundColor = this.backgroundColor;
    elStyle.borderRadius = '100000px';
    elStyle.left = this.left + 'px';
    elStyle.top = this.top + 'px';
    this.el.style.textAlign = 'center';
    this.contentEl.appendChild(this.el);
    this.contentEl.style.position = 'relative';

    this.setLife(this.life);
    this.setPause();

    if (window.BallArray) {
        window.BallArray.push(this);
    } else {
        window.BallArray = [];
        window.BallArray.push(this);
    }

    if (this.crash) this.startCrash();
    if (this.spring) this.startSpring();
    if (this.keyboard) this.onKeyDown();
    if (this.move && this.type === 'free') this.moving();
    if (this.type === 'bullet') this.up();
};

Ball.prototype.onKeyDown = function () {
    var self = this;
    document.addEventListener('keydown', function (e) {
        var el = self.el;
        var speed = self.speed;
        if (e.keyCode === 37) {
            el.style.left = el.offsetLeft - speed + 'px';
            el.left = self.left = el.offsetLeft;
        } else if (e.keyCode === 38) {
            el.style.top = el.offsetTop - speed + 'px';
            el.top = self.top = el.offsetTop;
        } else if (e.keyCode === 39) {
            el.style.left = el.offsetLeft + speed + 'px';
            el.left = self.left = el.offsetLeft;
        } else if (e.keyCode === 40) {
            el.style.top = el.offsetTop + speed + 'px';
            el.top = self.top = el.offsetTop;
        }
    });
};

Ball.prototype.setPause = function () {
    var self = this;
    document.addEventListener('keydown', function (e) {
        if (e.keyCode === 13) {
            if (!self.pause) {
                cancelAnimationFrame(self.time);
                self.pause = true;
            } else {
                if (self.move && self.type === 'free') self.moving();
                if (self.type === 'bullet') self.up();
                self.pause = false;
            }
        }
    });
};

Ball.prototype.moving = function () {
    var self = this;
    var el = this.el;
    var speed = self.speed;
    var contentEl = this.contentEl;
    var width = contentEl.offsetWidth;
    var height = contentEl.offsetHeight;

    run();

    function run() {
        self.time = requestAnimationFrame(run);
        self.moveSpeedIndex += 1;
        if (self.moveSpeedIndex === self.moveSpeed) {
            self.moveSpeedIndex = 0;
            switch (self.state) {
                case 1:
                    upLeft();
                    break;
                case 2:
                    upRight();
                    break;
                case 3:
                    downLeft();
                    break;
                case 4:
                    downRight();
                    break;
            }
        }
    }

    function upLeft() {
        el.style.left = el.offsetLeft - speed + 'px';
        el.style.top = el.offsetTop - speed + 'px';
        var left = self.left = el.offsetLeft;
        var top = self.top = el.offsetTop;

        if (left < 0) {
            self.state = self.state = 2;
        } else if (top < 0) {
            self.state = self.state = 3;
        }
    }

    function upRight() {
        var elWidth = self.r * 2;

        el.style.left = el.offsetLeft + speed + 'px';
        el.style.top = el.offsetTop - speed + 'px';
        var left = self.left = el.offsetLeft;
        var top = self.top = el.offsetTop;

        if (left > width - elWidth) {
            self.state = self.state = 1;
        } else if (top < 0) {
            self.state = self.state = 4;
        }
    }

    function downLeft() {
        var elHeight = self.r * 2;

        el.style.left = el.offsetLeft - speed + 'px';
        el.style.top = el.offsetTop + speed + 'px';
        var left = self.left = el.offsetLeft;
        var top = self.top = el.offsetTop;

        if (left < 0) {
            self.state = self.state = 4;
        } else if (top > height - elHeight) {
            self.state = self.state = 1;
        }
    }

    function downRight() {
        var elWidth = self.r * 2;
        var elHeight = self.r * 2;

        el.style.left = el.offsetLeft + speed + 'px';
        el.style.top = el.offsetTop + speed + 'px';
        var left = self.left = el.offsetLeft;
        var top = self.top = el.offsetTop;

        if (left > width - elWidth) {
            self.state = self.state = 3;
        } else if (top > height - elHeight) {
            self.state = self.state = 2;
        }
    }
};

Ball.prototype.eat = function (eneR) {
    var r = this.r;
    var oneVolume = Math.PI * r * r;
    var twoVolume = Math.PI * eneR * eneR;
    var allVolume = oneVolume + twoVolume;
    r = this.r = parseInt(Math.sqrt(allVolume / Math.PI));
    this.el.style.width = r * 2 + 'px';
    this.el.style.height = r * 2 + 'px';
    this.setLife(this.life);
};

Ball.prototype.destroy = function () {
    var parentNode = this.el.parentNode;
    if (parentNode) {
        parentNode.removeChild(this.el);
        this.life = -1;
        clearInterval(this.time);
    }
};

Ball.prototype.hit = function () {
    this.star();
    var life = this.life -= 1;
    this.setLife(life);
    if (this.life < 1) this.destroy();
};

Ball.prototype.setLife = function (life) {
    if (this.el) this.el.innerHTML = '<span style="opacity: 0.2; font-size: 0.5em; color: #ffffff; line-height: ' + this.r * 2 + 'px">' + (life === 1 ? '' : life) + '</span>';
};

Ball.prototype.star = function () {

};

Ball.prototype.up = function () {
    var self = this;
    var speed = this.speed;
    var el = this.el;
    var left = this.left = this.left - this.r;
    el.style.left = left + 'px';
    this.time = setInterval(run, 40);
    function run() {
        el.style.top = el.offsetTop - speed + 'px';
        self.top = el.offsetTop;
        if (self.top < 0) {
            clearInterval(self.time);
            self.destroy();
        }
    }
};

Ball.prototype.startCrash = function () {
    if (!window.crashTime) {
        console.log('开始碰撞检测');
        window.crashTime = setInterval(checkCrash, 40);
    }

    function checkCrash() {
        for (var i = 0; i < BallArray.length; i++) {
            var oneBall = BallArray[i];
            if (!oneBall || !oneBall.crash) continue;
            var oneR = oneBall.r;
            var oneLeft = oneBall.left;
            var oneTop = oneBall.top;

            for (var j = i + 1; j < BallArray.length; j++) {
                var twoBall = BallArray[j];
                if (!twoBall || !twoBall.crash) continue;
                var twoR = twoBall.r;
                var twoLeft = twoBall.left;
                var twoTop = twoBall.top;

                if (distance(oneR, oneLeft, oneTop, twoR, twoLeft, twoTop)) {
                    if (oneR > twoR) {
                        twoBall.hit();
                        if (twoBall.life < 1) {
                            BallArray[j] = null;
                            oneBall.eat(twoR);
                        }
                    } else {
                        oneBall.hit();
                        if (oneBall.life < 1) {
                            BallArray[i] = null;
                            twoBall.eat(oneR);
                        }
                    }
                }
            }
        }

        BallArray = BallArray.filter(function (item) {
            return !!item === true;
        });

        if (BallArray.length === 1) {
            console.log('-------- 检测碰撞停止 -------');
            clearInterval(window.crashTime);
        }

        function distance(oneR, oneLeft, oneTop, twoR, twoLeft, twoTop) {
            var oneCenterX = oneLeft + oneR;
            var oneCenterY = oneTop + oneR;
            var twoCenterX = twoLeft + twoR;
            var twoCenterY = twoTop + twoR;
            var centerLength = Math.sqrt((oneCenterX - twoCenterX) * (oneCenterX - twoCenterX) + (oneCenterY - twoCenterY) * (oneCenterY - twoCenterY));
            if (oneR - twoR === 0) {
                if (oneLeft - twoLeft === 0 && oneTop - twoTop === 0) {
                    return true;
                }
            } else if (oneR - twoR > 0) {
                if (centerLength <= oneR - twoR) {
                    return true
                }
            } else if (oneR - twoR < 0) {
                if (centerLength <= twoR - oneR) {
                    return true
                }
            }
            return false;
        }
    }
};

Ball.prototype.startSpring = function () {
    if (!window.springTime) {
        console.log('开始对撞检测');
        window.springTime = setInterval(checkSpring, 40);
    }

    checkSpring();

    function checkSpring() {
        window.springTime = requestAnimationFrame(checkSpring);

        for (var i = 0; i < BallArray.length; i++) {
            var oneBall = BallArray[i];
            if (!oneBall || !oneBall.spring) continue;
            var oneR = oneBall.r;
            var oneLeft = oneBall.left;
            var oneTop = oneBall.top;

            for (var j = i + 1; j < BallArray.length; j++) {
                var twoBall = BallArray[j];
                if (!twoBall || !twoBall.spring) continue;
                var twoR = twoBall.r;
                var twoLeft = twoBall.left;
                var twoTop = twoBall.top;

                if (distance(oneR, oneLeft, oneTop, twoR, twoLeft, twoTop)) {
                    oneBall.state = reverseDirection(oneBall.state);
                    twoBall.state = reverseDirection(twoBall.state);
                }
            }
        }

        BallArray = BallArray.filter(function (item) {
            return !!item === true;
        });

        if (BallArray.length === 1) {
            console.log('-------- 检测碰撞停止 -------');
            cancelAnimationFrame(window.springTime);
        }

        function reverseDirection(state) {
            switch (state) {
                case 1:
                    return 4;
                case 2:
                    return 3;
                case 3:
                    return 2;
                case 4:
                    return 1;
            }
        }

        function distance(oneR, oneLeft, oneTop, twoR, twoLeft, twoTop) {
            var oneCenterX = oneLeft + oneR;
            var oneCenterY = oneTop + oneR;
            var twoCenterX = twoLeft + twoR;
            var twoCenterY = twoTop + twoR;
            var centerLength = Math.sqrt((oneCenterX - twoCenterX) * (oneCenterX - twoCenterX) + (oneCenterY - twoCenterY) * (oneCenterY - twoCenterY));
            if (oneR + twoR >= centerLength) return true;
            return false;
        }
    }
};

export default Ball;


```


stats.module.js
```js
/**
 * @author mrdoob / http://mrdoob.com/
 */

var Stats = function () {

    var mode = 0;

    var container = document.createElement( 'div' );
    container.style.cssText = 'position:fixed;top:0;left:0;cursor:pointer;opacity:0.9;z-index:10000';
    container.addEventListener( 'click', function ( event ) {

        event.preventDefault();
        showPanel( ++ mode % container.children.length );

    }, false );

    //

    function addPanel( panel ) {

        container.appendChild( panel.dom );
        return panel;

    }

    function showPanel( id ) {

        for ( var i = 0; i < container.children.length; i ++ ) {

            container.children[ i ].style.display = i === id ? 'block' : 'none';

        }

        mode = id;

    }

    //

    var beginTime = ( performance || Date ).now(), prevTime = beginTime, frames = 0;

    var fpsPanel = addPanel( new Stats.Panel( 'FPS', '#0ff', '#002' ) );
    var msPanel = addPanel( new Stats.Panel( 'MS', '#0f0', '#020' ) );

    if ( self.performance && self.performance.memory ) {

        var memPanel = addPanel( new Stats.Panel( 'MB', '#f08', '#201' ) );

    }

    showPanel( 0 );

    return {

        REVISION: 16,

        dom: container,

        addPanel: addPanel,
        showPanel: showPanel,

        begin: function () {

            beginTime = ( performance || Date ).now();

        },

        end: function () {

            frames ++;

            var time = ( performance || Date ).now();

            msPanel.update( time - beginTime, 200 );

            if ( time >= prevTime + 1000 ) {

                fpsPanel.update( ( frames * 1000 ) / ( time - prevTime ), 100 );

                prevTime = time;
                frames = 0;

                if ( memPanel ) {

                    var memory = performance.memory;
                    memPanel.update( memory.usedJSHeapSize / 1048576, memory.jsHeapSizeLimit / 1048576 );

                }

            }

            return time;

        },

        update: function () {

            beginTime = this.end();

        },

        // Backwards Compatibility

        domElement: container,
        setMode: showPanel

    };

};

Stats.Panel = function ( name, fg, bg ) {

    var min = Infinity, max = 0, round = Math.round;
    var PR = round( window.devicePixelRatio || 1 );

    var WIDTH = 80 * PR, HEIGHT = 48 * PR,
            TEXT_X = 3 * PR, TEXT_Y = 2 * PR,
            GRAPH_X = 3 * PR, GRAPH_Y = 15 * PR,
            GRAPH_WIDTH = 74 * PR, GRAPH_HEIGHT = 30 * PR;

    var canvas = document.createElement( 'canvas' );
    canvas.width = WIDTH;
    canvas.height = HEIGHT;
    canvas.style.cssText = 'width:80px;height:48px';

    var context = canvas.getContext( '2d' );
    context.font = 'bold ' + ( 9 * PR ) + 'px Helvetica,Arial,sans-serif';
    context.textBaseline = 'top';

    context.fillStyle = bg;
    context.fillRect( 0, 0, WIDTH, HEIGHT );

    context.fillStyle = fg;
    context.fillText( name, TEXT_X, TEXT_Y );
    context.fillRect( GRAPH_X, GRAPH_Y, GRAPH_WIDTH, GRAPH_HEIGHT );

    context.fillStyle = bg;
    context.globalAlpha = 0.9;
    context.fillRect( GRAPH_X, GRAPH_Y, GRAPH_WIDTH, GRAPH_HEIGHT );

    return {

        dom: canvas,

        update: function ( value, maxValue ) {

            min = Math.min( min, value );
            max = Math.max( max, value );

            context.fillStyle = bg;
            context.globalAlpha = 1;
            context.fillRect( 0, 0, WIDTH, GRAPH_Y );
            context.fillStyle = fg;
            context.fillText( round( value ) + ' ' + name + ' (' + round( min ) + '-' + round( max ) + ')', TEXT_X, TEXT_Y );

            context.drawImage( canvas, GRAPH_X + PR, GRAPH_Y, GRAPH_WIDTH - PR, GRAPH_HEIGHT, GRAPH_X, GRAPH_Y, GRAPH_WIDTH - PR, GRAPH_HEIGHT );

            context.fillRect( GRAPH_X + GRAPH_WIDTH - PR, GRAPH_Y, PR, GRAPH_HEIGHT );

            context.fillStyle = bg;
            context.globalAlpha = 0.9;
            context.fillRect( GRAPH_X + GRAPH_WIDTH - PR, GRAPH_Y, PR, round( ( 1 - ( value / maxValue ) ) * GRAPH_HEIGHT ) );

        }

    };

};

export default Stats;


```

snake_package\src\utils
validation.js
```js
const isEmpty = value => value === undefined || value === null || value === '';
const join = (rules) => (value, data) => rules.map(rule => rule(value, data)).filter(error => !!error)[0 /* first error */];

export function email(value) {
    // Let's not start a debate on email regex. This is just for an example app!
    if (!isEmpty(value) && !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(value)) {
        return 'Invalid email address';
    }
}

export function required(value) {
    if (isEmpty(value)) {
        return 'Required';
    }
}

export function minLength(min) {
    return value => {
        if (!isEmpty(value) && value.length < min) {
            return `Must be at least ${min} characters`;
        }
    };
}

export function maxLength(max) {
    return value => {
        if (!isEmpty(value) && value.length > max) {
            return `Must be no more than ${max} characters`;
        }
    };
}

export function integer(value) {
    if (!Number.isInteger(Number(value))) {
        return 'Must be an integer';
    }
}

export function oneOf(enumeration) {
    return value => {
        if (!~enumeration.indexOf(value)) {
            return `Must be one of: ${enumeration.join(', ')}`;
        }
    };
}

export function match(field) {
    return (value, data) => {
        if (data) {
            if (value !== data[field]) {
                return 'Do not match';
            }
        }
    };
}

export function createValidator(rules) {
    return (data = {}) => {
        const errors = {};
        Object.keys(rules).forEach((key) => {
            const rule = join([].concat(rules[key])); // concat enables both functions and arrays of functions
            const error = rule(data[key], data);
            if (error) {
                errors[key] = error;
            }
        });
        return errors;
    };
}


```


client.js
```js
/**
 * THIS IS THE ENTRY POINT FOR THE CLIENT, JUST LIKE server.js IS THE ENTRY POINT FOR THE SERVER.
 */
import 'babel-polyfill';
import React from 'react';
import ReactDOM from 'react-dom';
import createStore from './redux/create';
import ApiClient from './helpers/ApiClient';
import { Provider } from 'react-redux';
import { Router, browserHistory } from 'react-router';
import { syncHistoryWithStore } from 'react-router-redux';
import { ReduxAsyncConnect } from 'redux-async-connect';
import getRoutes from './routes';

const client = new ApiClient();
const dest = document.getElementById('content');
const store = createStore(browserHistory, client, window.__data);
const history = syncHistoryWithStore(browserHistory, store);

const component = (
    <Router
        render={(props) =>
            <ReduxAsyncConnect
                {...props}
                helpers={{ client }}
                filter={item => !item.deferred}
            />}
        history={history}
    >
        {getRoutes(store)}
    </Router>
);

ReactDOM.render(
    <Provider
        store={store}
        key="provider"
    >
        {component}
    </Provider>,
    dest
);

if (process.env.NODE_ENV !== 'production') {
    window.React = React;

    if (!dest || !dest.firstChild || !dest.firstChild.attributes || !dest.firstChild.attributes['data-react-checksum']) {
        console.error('Server-side React render was discarded. Make sure that your initial render does not contain any client-side code.');
    }
}

if (__DEVTOOLS__ && !window.devToolsExtension) {
    const DevTools = require('./containers/DevTools/DevTools');
    ReactDOM.render(
        <Provider
            store={store}
            key="provider"
        >
            <div style={{ height: '100%' }}>
                {component}
                <DevTools />
            </div>
        </Provider>,
        dest
    );
}


```


config.js
```js
require('babel-polyfill');

const environment = {
    development: {
        isProduction: false
    },
    production: {
        isProduction: true
    }
}[process.env.NODE_ENV || 'development'];

module.exports = Object.assign({
    host: process.env.HOST || 'localhost',
    port: process.env.PORT,
    apiHost: process.env.APIHOST || 'localhost',
    apiPort: process.env.APIPORT,
    app: {
        title: 'dog-chat',
        description: 'dog-chat',
        head: {
            titleTemplate: 'dog-chat: %s',
            meta: [
                { name: 'description', content: 'dog-chat' },
                { charset: 'utf-8' },
                { property: 'og:site_name', content: 'dog-chat' },
                { property: 'og:image', content: 'dog.png' },
                { property: 'og:locale', content: 'en_US' },
                { property: 'og:title', content: 'dog-chat' },
                { property: 'og:description', content: 'dog-chat' },
                { property: 'og:card', content: 'dog-chat' },
                { property: 'og:site', content: 'dog-chat' },
                { property: 'og:creator', content: 'jzc' },
                { property: 'og:image:width', content: '200' },
                { property: 'og:image:height', content: '200' }
            ]
        }
    },
}, environment);


```

routes.js
```js
import React from 'react';
import { IndexRoute, Route } from 'react-router';
import { isLoaded as isAuthLoaded, load as loadAuth } from 'redux/modules/auth';
import {
    NotFound,
    App,
    Login,
    Container,
    WebGlStage
} from 'containers';

export default (store) => {
    const requireLogin = (nextState, replace, cb) => {
        function checkAuth() {
            const { auth: { user } } = store.getState();
            if (!user) replace('/');
            cb();
        }

        if (!isAuthLoaded(store.getState())) {
            store.dispatch(loadAuth()).then(checkAuth);
        } else {
            checkAuth();
        }
    };

    return (
        <Route path="/" component={App}>
            <IndexRoute component={Login} />

            <Route onEnter={requireLogin}>
                <Route path="/home" component={Container} />
                <Route path="/webgl" component={WebGlStage} />
            </Route>

            <Route path="*" component={NotFound} status={404} />
        </Route>
    );
};


```


server.js
```js
import Express from 'express';
import React from 'react';
import ReactDOM from 'react-dom/server';
import config from './config';
import favicon from 'serve-favicon';
import compression from 'compression';
import httpProxy from 'http-proxy';
import path from 'path';
import createStore from './redux/create';
import ApiClient from './helpers/ApiClient';
import Html from './helpers/Html';
import PrettyError from 'pretty-error';
import http from 'http';

import { match } from 'react-router';
import { syncHistoryWithStore } from 'react-router-redux';
import { ReduxAsyncConnect, loadOnServer } from 'redux-async-connect';
import createHistory from 'react-router/lib/createMemoryHistory';
import { Provider } from 'react-redux';
import getRoutes from './routes';

const targetUrl = 'http://' + config.apiHost + ':' + config.apiPort;
const pretty = new PrettyError();
const app = new Express();
const server = new http.Server(app);
const proxy = httpProxy.createProxyServer({ target: targetUrl, ws: true });

app.use(compression());
app.use(favicon(path.join(__dirname, '..', 'static', 'favicon.ico')));

app.use(Express.static(path.join(__dirname, '..', 'static')));
app.use(Express.static(path.join(__dirname, '..', 'uploads')));

app.use('/api', (req, res) => {
    proxy.web(req, res, { target: targetUrl });
});

app.use('/ws', (req, res) => {
    proxy.web(req, res, { target: targetUrl + '/ws' });
});

server.on('upgrade', (req, socket, head) => {
    proxy.ws(req, socket, head);
});

proxy.on('error', (error, req, res) => {
    if (error.code !== 'ECONNRESET') console.error('proxy error', error);
    if (!res.headersSent) res.writeHead(500, { 'content-type': 'application/json' });

    res.end(JSON.stringify({ error: 'proxy_error', reason: error.message }));
});

app.use((req, res) => {
    if (__DEVELOPMENT__) webpackIsomorphicTools.refresh();

    const client = new ApiClient(req);
    const memoryHistory = createHistory(req.originalUrl);
    const store = createStore(memoryHistory, client);
    const history = syncHistoryWithStore(memoryHistory, store);

    function hydrateOnClient() {
        res.send('<!doctype html>' +
            ReactDOM.renderToString(
                <Html
                    assets={webpackIsomorphicTools.assets()}
                    store={store}
                />
            ));
    }

    if (__DISABLE_SSR__) {
        hydrateOnClient();
        return;
    }

    match({ history, routes: getRoutes(store), location: req.originalUrl }, (error, redirectLocation, renderProps) => {
        if (redirectLocation) {
            res.redirect(redirectLocation.pathname + redirectLocation.search);
        } else if (error) {
            console.error('ROUTER ERROR:', pretty.render(error));
            res.status(500);
            hydrateOnClient();
        } else if (renderProps) {
            loadOnServer({ ...renderProps, store, helpers: { client } }).then(() => {
                const component = (
                    <Provider
                        store={store}
                        key="provider"
                    >
                        <ReduxAsyncConnect {...renderProps} />
                    </Provider>
                );

                res.status(200);

                global.navigator = { userAgent: req.headers['user-agent'] };

                res.send('<!doctype html>\n' +
                    ReactDOM.renderToString(
                        <Html
                            assets={webpackIsomorphicTools.assets()}
                            component={component}
                            store={store}
                        />
                    ));
            });
        } else {
            res.status(404).send('Not found');
        }
    });
});

server.listen(config.port, (err) => {
    console.info('----\n==> ✅  %s is running, talking to API server on %s.', config.app.title, config.apiPort);
    console.info('==> 💻  Open http://%s:%s in a browser to view the app.', config.host, config.port);
});


```
