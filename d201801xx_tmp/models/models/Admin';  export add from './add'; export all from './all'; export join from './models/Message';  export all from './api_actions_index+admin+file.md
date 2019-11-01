snake_package\api\actions

index.js
```js
export * as admin from './admin/index';
export * as message from './message/index';
export * as file from './file/index';
export * as group from './group/index';

```



snake_package\api\actions\admin

add.js
```js
import mongoose from 'mongoose';
const Admin = mongoose.model('Admin');

export default function one(req) {

  return new Promise((resolve, reject) => {
    const { _id, selfId } = req.body;

    if (!_id) {
      reject({ msg: '不能添加空好友' });
    } else {
      saveFriends(_id, selfId);
      saveFriends(selfId, _id);
    }

    function saveFriends(a, b) {
      Admin
        .findOne({ _id: a })
        .select('friends')
        .exec((err, doc) => {
          const { friends = [] } = doc;
          if (friends.indexOf(b) > -1) {
            reject({ msg: '已经是好友了' });
          } else {
            friends.push(b);
            Admin.findOneAndUpdate({ _id: a }, { friends }, (err) => {
              if (err) {
                reject({ msg: '更新错误:' + err });
              } else {
                resolve({ msg: '更新成功' });
              }
            });
          }
        });
    }

  });
}

```

all.js
```js
import mongoose from 'mongoose';
const Admin = mongoose.model('Admin');

export default function all(req) {

  return new Promise((resolve, reject) => {
    const { _id } = req.query;

    Admin
      .find()
      .where({ friends: { $nin: [_id] }, _id: { $nin: [_id] } })
      .select('name _id')
      .exec((error, doc) => {
        if (error) {
          reject({ msg: '查询错误!', error });
        } else {
          if (doc) {
            resolve({ allAdmin: doc });
          } else {
            reject({ msg: '无结果' });
          }
        }
      });
  });

}
```

index.js
```js
import '../../models/Admin';
import '../../models/File';
import '../../models/Message';
import '../../models/Group';

export all from './all';
export loadAuth from './loadAuth';
export login from './login';
export register from './register';
export one from './one';
export logout from './logout';
export add from './add';
export list from './list';

```

list.js
```js
import mongoose from 'mongoose';
const Admin = mongoose.model('Admin');

export default function all(req) {

  return new Promise((resolve, reject) => {
    const { _id } = req.query;

    Admin
      .findOne({ _id })
      .select('friends')
      .populate({
        path: 'friends',
        select: '_id name avatar',
        populate: ({
          path: 'avatar'
        })
      })
      .exec((error, doc) => {
        if (error) {
          reject({ msg: '查询错误!', error });
        } else {
          if (doc) {
            resolve({ friends: doc.friends });
          } else {
            reject({ msg: '无结果' });
          }
        }
      });
  });

}

```

loadAuth.js
```js
export default (req) => Promise.resolve({ user: req.token });
```

login.js
```js
import mongoose from 'mongoose';
const Admin = mongoose.model('Admin');
import jwt from 'jsonwebtoken';
import config from '../../config';

export default function login(req) {

    return new Promise((resolve, reject) => {

        const { name, password } = req.body;
        Admin
            .findOne({ name })
            .populate('avatar')
            .exec((error, doc) => {
                if (error) {
                    reject({ msg: '登陆失败!', error });
                } else {
                    if (doc) {
                        if (doc.validPassword(password)) {

                            const user = {
                                _id: doc._id,
                                password: doc.password,
                                name: doc.name,
                                groups: doc.groups,
                                friends: doc.friends,
                                role: doc.role,
                                create_time: doc.create_time
                            };

                            const token = jwt.sign(
                                user,
                                config.tokenSecret,
                                { expiresIn: config.tokenMaxAge }
                            );

                            resolve({ user, token });

                        } else {
                            reject({ msg: '密码错误' });
                        }
                    } else {
                        reject({ msg: '用户不存在' });
                    }
                }
            });
    });

}

```


logout.js
```js
export default (req) => new Promise((resolve) => {
    req.token = null;
    return resolve(null);
});

```

one.js
```js
import mongoose from 'mongoose';
const Admin = mongoose.model('Admin');

export default function one(req) {

  return new Promise((resolve, reject) => {
    const { _id } = req.query;
    Admin
      .findOne({ _id })
      .populate('avatar friends groups')
      .exec((error, doc) => {
        if (error) {
          reject({ msg: '查询错误!', error });
        } else {
          if (doc) {
            doc.password = null;
            if (doc.friends.length > 0) {
              doc.friends.forEach(item => item.password = null);
            }
            resolve({ user: doc });
          } else {
            reject({ msg: '无结果' });
          }
        }
      });
  });

}

```

register.js
```js
/**
 * Created by isaac on 2/21/16.
 */
import mongoose from 'mongoose';
import jwt from 'jsonwebtoken';
import config from '../../config';
const Admin = mongoose.model('Admin');

export default function register(req) {

  return new Promise((resolve, reject) => {

    const { name, password } = req.body;
    if (name && password) {

      Admin.findOne({ name }, (err, doc) => {
        if (doc) {
          reject({
            msg: '此昵称已经被占用了!'
          });
        } else {
          const user = new Admin({ name });
          user.password = user.generateHash(password);

          user.save(err => {
            if (err) reject({ msg: '用户注册失败!', err });

            user.password = null;

            const _user = {
              _id: user._id,
              password: user.password,
              name: user.name,
              groups: user.groups,
              friends: user.friends,
              role: user.role,
              create_time: user.create_time
            };
            // req.session.user = user;
            const token = jwt.sign(
                _user,
                config.tokenSecret,
                { expiresIn: config.tokenMaxAge }
            );
            resolve({ user, token });
          });
        }
      });
    } else {
      reject({ msg: '缺少用户名或密码!' });
    }
  });
}

```

snake_package\api\actions\file

index.js
```js
import '../../models/File';

export save from './save';

```


save.js
```js
import mongoose from 'mongoose';
const File = mongoose.model('File');

export default function save(req) {

  return new Promise((resolve, reject) => {

    const { file } = req.body;

    const fileObj = new File(file);
    fileObj.save((err) => {
      if (err) reject({ msg: '保存错误', error });
      resolve({ msg: '保存成功' });
    });
  });

}

```
