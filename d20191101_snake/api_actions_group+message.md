snake_package\api\actions\group

add.js
```js
import mongoose from 'mongoose';
const Group = mongoose.model('Group');

export default function add(req) {

  return new Promise((resolve, reject) => {
    const { name, _id } = req.body;

    const groupObj = new Group({ name, creator: _id });

    groupObj.save((err) => {
      if (err) reject({ msg: '创建失败' });
      resolve({ msg: '创建群组成功' });
    });
  });

}

```

all.js
```js
import mongoose from 'mongoose';
const Group = mongoose.model('Group');

export default function all(req) {

  return new Promise((resolve, reject) => {
    const { groups = [] } = req.query;

    Group
      .find()
      .where({ _id: { $nin: groups } })
      .exec((err, doc) => {
        if (err) reject({ msg: '查找错误', err });
        resolve({
          groups: doc
        });
      });
  });

}

```


index.js

```js
import '../../models/Message';
import '../../models/Admin';

export add from './add';
export all from './all';
export join from './join';

```

join.js
```js
import mongoose from 'mongoose';
const Admin = mongoose.model('Admin');

export default function join(req) {

  return new Promise((resolve, reject) => {
    const groupId = req.body._id;
    if (groupId) {
      const { _id, groups = [] } = req.body.user;
      groups.push(groupId);
      req.body.user.groups = groups;

      Admin.findOneAndUpdate({ _id }, { groups }, (err) => {
        if (err) reject({ msg: '添加失败' });
        resolve({ msg: '添加成功' });
      });
    } else {
      reject({ msg: '缺少参数' });
    }
  });

}

```








snake_package\api\actions\message

all.js
```js
import mongoose from 'mongoose';
const Message = mongoose.model('Message');

export default function all(req) {

  return new Promise((resolve, reject) => {
    const { to, come } = req.query;
    Message
      .find()
      .where({ $or: [{ come, to }, { come: to, to: come }] })
      .populate('file')
      .sort({ 'create_time': 1 })
      .exec((error, doc) => {
        if (error) {
          reject({ msg: '查询错误!: ' + error });
        } else {
          if (doc) {
            resolve({ messageList: doc });
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
import '../../models/Message';

export all from './all';

```
