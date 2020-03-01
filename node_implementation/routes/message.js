const express = require("express");
const bodyParser = require("body-parser");
const mongoose = require('mongoose');

const Message = require("../models/messageModel");

const messageRouter = express.Router();

messageRouter.use(bodyParser.json())

messageRouter.route("/")

.get((req, res, next) => { //req and res will could be modified from the app.all part
	Message.find({})
	.then((mess) => {
		res.statusCode = 200;
		res.setHeader("Content-Type", "application/json");
		res.json(mess)
	})
	
})

.post((req, res, next) => {
	Message.create(req.body)
	.then((mess) => {
		console.log("Message posted!");
		res.statusCode = 200;
		res.setHeader("Content-Type", "application/json");
		res.json(mess);
	}, (err) => next(err))
	.catch((err) => next(err));
})	

.put((req, res, next) =>{
	res.statusCode = 403;
	res.end("PUT operation not supported on /message" + req.params.dishId)
})

.delete((req, res, next) =>{
	Message.remove({})
	.then((resp) => {
		res.statusCode = 200;
		res.setHeader("Content-Type", "application/json");
		res.json(resp);
	}, (err) => next(err))
	.catch((err) => next(err));
});

messageRouter.route("/:messageID")

.get((req, res, next) => {
	res.statusCode = 403;
	res.end("GET operation not supported on /message/" + req.params.messageID)
})

.put((req, res, next) => {
	Message.findByIdAndUpdate(req.params.messageID, {
		$set: req.body
	}, {new: true})
	.then((resp) => {
		res.statusCode = 200;
		res.setHeader("Content-Type", "application/json");
		res.json(resp)
	}, (err) => next(err))
	.catch((err) => next(err));
})

.post((req, res, next) =>{
	res.statusCode = 403;
	res.end("PUT operation not supported on /message/" + req.params.messageID)
})

.delete((req, res, next) =>{
	Message.findByIdAndRemove(req.params.messageID)
	.then((mess) => {
		res.statusCode = 200;
		res.setHeader("Content-Type", "application/json");
		res.json(mess);
	}, (err) => next(err))
	.catch((err) => next(err));
});

 
module.exports = messageRouter;
