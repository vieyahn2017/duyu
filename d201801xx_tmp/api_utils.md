snake_package\api\utils


log.js
```js
import log4js from 'log4js';

export default () => {

};
```


resClear.js
```js
/**
 * Created by jiang on 2017/3/21.
 */

import mapUrl from './url.js';
import PrettyError from 'pretty-error';
const pretty = new PrettyError();

export default function resClear(actions) {

  return (req, res) => {

    const splittedUrlPath = req.url.split('?')[0].split('/').slice(1);
    const {action, params} = mapUrl(actions, splittedUrlPath);

    if (action) {
      action(req, params)
        .then((result) => {
          if (result instanceof Function) {
            result(res);
          } else {
            res.json(result);
          }
        }, (reason) => {
          if (reason && reason.redirect) {
            res.redirect(reason.redirect);
          } else {
            console.error('API ERROR:', pretty.render(reason));
            res.status(reason.status || 500).json(reason);
          }
        });
    } else {
      res.status(404).end('NOT FOUND');
    }
  }
}
```


tokenVerify.js
```js
/**
 * Created by jiang on 2017/10/11.
 */
import jwt from 'jsonwebtoken';
import dbConfig from '../config';

const noVerify = ['/admin/login', '/admin/logout', '/admin/register'];

export default (req, res, next) => {
    if (noVerify.indexOf(req.path) > -1) {
        next();
    } else {
        const token = req.body.token || req.query.token || req.headers[dbConfig.tokenHeader] || req.cookies.token;
        if (token) {
            jwt.verify(token, dbConfig.tokenSecret, (err, decoded) => {
                if (err) {
                    if (req.path === '/admin/loadAuth') {
                        next();
                    } else {
                        res.status(401).json({ msg: '登录过期，请退出重新登录' });
                    }
                } else {
                    req.token = decoded;
                    next();
                }
            });
        } else {
            if (req.path === '/admin/loadAuth') {
                next();
            } else {
                res.status(500).json({ msg: '无权限或未登录' });
            }
        }
    }
};

```


url.js
```js
export default function mapUrl(availableActions = {}, url = []) {

  const notFound = {action: null, params: []};

  if (url.length === 0 || Object.keys(availableActions).length === 0) {
    return notFound;
  }

  const reducer = (prev, current) => {
    if (prev.action && prev.action[current]) {
      return {action: prev.action[current], params: []};
    } else {
      if (typeof prev.action === 'function') {
        return {action: prev.action, params: prev.params.concat(current)};
      } else {
        return notFound;
      }
    }
  };

  const actionAndParams = url.reduce(reducer, {action: availableActions, params: []});
  return (typeof actionAndParams.action === 'function') ? actionAndParams : notFound;
}

```


util.js
```js
/**
 * Created by jiang on 2017/3/14.
 */
export function decodeBase64Image(dataString) {
  const matches = dataString.match(/^data:([A-Za-z-+\/]+);base64,(.+)$/);
  const response = {};

  if (matches.length !== 3) {
    return new Error('Invalid input string');
  }

  response.type = matches[1];
  response.data = new Buffer(matches[2], 'base64');

  return response;
}

export function randomString() {
  let time = new Date().getTime();
  let suffix = Math.random().toString(36).substring(5);
  return `${time}-${suffix}`;
}

```


