const mongoose = require('mongoose');
const ObjectId = mongoose.Schema.Types.ObjectId;

const SnakeSchema = mongoose.Schema({

  id              : {type: Number, required: true},
  length          : {type: Number, required: true},
  direction       : {type: Number, required: true},
  x               : {type: Number, required: true},
  y               : {type: Number, required: true},
  speed           : {type: Number, required: true},
  life            : {type: Number, required: true},
  space           : {type: Number, required: true},
  pointLength     : {type: Number, required: true},
  bigFood         : {type: Number, required: true},
  currentFood     : {type: Number, required: true},
  moveLen         : {type: Number, required: true},
  lv              : {type: Number, required: true},
  weight          : {type: Number, required: true},

  bodys           : [{type: ObjectId, ref: 'SnakeBody'}],
  color           : {type: String, required: true},
  rgb             : [{type: Number, required: true}],
  
  offline_time    : {type: Date, default: Date.now},
  is_offline      : {type: Boolean, default: true}
});


module.exports = mongoose.model('Snake', SnakeSchema);
