snake_package\api


api.js
```js
import express from 'express';
import bodyParser from 'body-parser';
import cookieParser from 'cookie-parser';
import http from 'http';
import SocketIo from 'socket.io';
import mongoose from 'mongoose';
import upload from 'jquery-file-upload-middleware';
import path from 'path';

import config from '../src/config';
import * as actions from './actions/index';
import dbConfig from './config';
import ioConnect from './io/ioConnect';
import resClear from './utils/resClear';
import tokenVerify from './utils/tokenVerify';
// import log from './utils/log';

const app = express();
const server = new http.Server(app);
const io = new SocketIo(server);
const { db } = dbConfig;

mongoose.connect(db, {useNewUrlParser: true});

app.use(bodyParser.json({ limit: '5mb' }));
app.use(cookieParser());
app.use(tokenVerify);
app.use('/uploads', (req, res, next) => {
    upload.fileHandler({
        uploadDir: () => path.join(__dirname, '../uploads', (req.token ? '/' + req.token._id : '')),
        uploadUrl: () => '/uploads'
    })(req, res, next);
});
// app.use(log());
app.use(resClear(actions));

const runnable = app.listen(config.apiPort, (err) => {
    if (err) console.error(err);
    console.info('\n==> 💻  api ==> ', config.apiHost, ':', config.apiPort, '\n');
});

ioConnect(io, runnable);

```

config.js
```js
/**
 * Created by isaac on 15/10/28.
 */
import path from 'path';

const uploadFolder = path.join(__dirname, '../uploads');
module.exports = {
    db: 'mongodb://127.0.0.1/jzc',
    sessionDb: 'mongodb://127.0.0.1/jzc',
    sessionDbConf: {
        secret: 'jzc rule!!!!',
        resave: false,
        saveUninitialized: false,
        cookie: { maxAge: 1000 * 60 * 60 * 24 }
    },
    uploadFolder,
    tokenSecret: 'only-you-s-b',
    tokenMaxAge: 60 * 60 * 24,
    tokenHeader: 'x-access-token'
};

```
