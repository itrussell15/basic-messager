const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const messageSchema = new Schema({
	body:{
		type: String,
		required: true
	},
	author:{
		type: String,
		required: true
	},
	email:{
		type: String,
		default: null
	},
	message_date:{
		type: String,
		required: true
	},
	seen:{
		type: Boolean,
		default: false
	}
},{
	timestamps: true
});

var Message = mongoose.model("Message", messageSchema);

module.exports = Message;