var AWS = require('aws-sdk');
var glue = new AWS.Glue();
var sqs = new AWS.SQS();
	exports.handler = function(event, context,callback) {
		console.log(JSON.stringify(event, null, 3));
		if(event.Records.length > 0 && event.Records[0].eventSource == 'aws:sqs'){
			startCrawler('UdacityCrawler', function(err2,data2){
				if(err2) callback(err2)
				else callback(null,data2)
			})
		}else{
		var dbName = 'udacityDB';
		var params = {
			DatabaseInput: {
				Name: dbName,
				Description: 'Blog Post database',
			}
		};
		glue.createDatabase(params, function(err, data) {
				var params1 = {
					DatabaseName: dbName,
					Name: 'UdacityCrawler',
					Role: 'service-role/UdacityDataLake-GlueLabRole-1D6QKPRO1DJOM',
					Targets: {
						S3Targets: [{ Path: 's3://udacitydatalake-raws3bucket-1bzpc5li2rs64' }]
					},
					Description: 'crawler test'
				};
				glue.createCrawler(params1, function(err1, data1) {
					startCrawler('UdacityCrawler', function(err2,data2){
						if(err2) callback(err2)
						else callback(null,data2)
					})
				});
		});
	};
};
function startCrawler(name,callback){
	var params = {
		Name: name,
	};
	glue.startCrawler(params, function(err, data) {
		if (err){
			console.log(JSON.stringify(err,null,3 ))
			var params1 = {
				MessageBody: 'retry',
				QueueUrl: 'https://sqs.us-east-1.amazonaws.com/437131580668/UdacityDataLake-SQSqueue-1NHRVQ6ZDCEE8'
			};
			sqs.sendMessage(params1, function(err1, data1) {
				if (err1) callback(err1);
				else     callback(null, data1)
			});
		}
		else{
			callback(null, data)
		}
	});
	}
