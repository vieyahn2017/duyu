snake_package\api\models

Admin.js
```js
const mongoose = require('mongoose');
const bcrypt = require('bcrypt-nodejs');
const ObjectId = mongoose.Schema.Types.ObjectId;

const AdminSchema = mongoose.Schema({

  name            : {type: String, required: true},
  nick_name       : String,
  password        : {type: String, required: true},
  avatar          : {type: ObjectId, ref: 'File'},
  create_time     : {type: Date, default: Date.now},
  update_time     : Date,
  role            : {type: String, default: 'admin'},
  birthday        : Date,
  id_card         : String,
  qq              : String,
  wechat          : String,
  phone           : String,
  is_married      : {type: Boolean, default: false},
  friends         : [{type: ObjectId, ref: 'Admin'}],
  groups          : [{type:ObjectId, ref: 'Group'}]
});

AdminSchema.methods.generateHash = function (password) {
  return bcrypt.hashSync(password, bcrypt.genSaltSync(8), null);
};

AdminSchema.methods.validPassword = function (password) {
  return bcrypt.compareSync(password, this.password);
};

module.exports = mongoose.model('Admin', AdminSchema);

```


File.js
```js
const mongoose = require('mongoose');
const ObjectId = mongoose.Schema.Types.ObjectId;

const FileSchema = mongoose.Schema({

  name       : String,
  path       : String,
  size       : Number,
  type       : String,
  creator    : {type: ObjectId, ref: 'Admin'},
  create_time: {type: Date, default: Date.now}
});

module.exports = mongoose.model('File', FileSchema);

```


Group.js
```js
const mongoose = require('mongoose');
const ObjectId = mongoose.Schema.Types.ObjectId;

const GroupSchema = mongoose.Schema({

  name       : String,
  creator    : {type: ObjectId, ref: 'Admin'},
  create_time: {type: Date, default: Date.now}
});

module.exports = mongoose.model('Group', GroupSchema);

```


Message.js
```js
const mongoose = require('mongoose');
const ObjectId = mongoose.Schema.Types.ObjectId;

const MessageSchema = mongoose.Schema({
  come       : {type: ObjectId, ref: 'Admin'},
  to         : {type: ObjectId, ref: 'Admin'},
  is_cancel  : {type: Boolean, default: false},
  content    : String,
  file       : {type: ObjectId, ref: 'File'},
  create_time: {type: Date, default: Date.now},
  is_offline : {type: Boolean, default: false},
  group      : {type: ObjectId, ref: 'Group'}
});

module.exports = mongoose.model('Message', MessageSchema);

```

