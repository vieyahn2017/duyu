const mongoose = require('mongoose');
const ObjectId = mongoose.Schema.Types.ObjectId;

const SnakeBodySchema = mongoose.Schema({

  x               : {type: Number, required: true},
  y               : {type: Number, required: true},
  width           : {type: Number, required: true},
  height          : {type: Number, required: true},
  color           : {type: String, required: true}
});


module.exports = mongoose.model('SnakeBody', SnakeBodySchema);
