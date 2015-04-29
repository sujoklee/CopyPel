from pymongo import MongoClient

db = MongoClient().forecast

def get_forecast(id):
	return db.find_one({'_id':id})

def get_forecasts():
	return list(db.find())

def get_latest_prediction(usr_id,forecast_id):
	cursor = db.predictions.find({'usr_id':usr_id,'forecast_id':forecast_id}).sort({'date':-1}).limit(1)
	if cursor.count():
		return cursor.next()
	else:
		return None

def get_predictions_for_user(usr_id):
	return list(db.predictions.find({'usr_id':str(usr_id)}))

def get_prediction(usr_id,forecast_id):
	return db.predictions.find_one({'usr_id':usr_id,'forecast_id':forecast_id})

def get_org_prediction(organization,forecast_id):
	return db.org_predictions.find_one({'organization':organization,'forecast_id':forecast_id})

def get_overall_prediction(forecast_id):
	return db.overall_predictions.find_one({'forecast_id':forecast_id})

def get_overall_predictions():
	return list(db.overall_predictions.find())

def get_org_predictions(organization):
	return list(db.org_predictions.find({'organization':organization}))

def get_average_org_prediction(organization,forecast_id):
	result = db.predictions.aggregate([{"$match":{'organization':organization,'forecast_id':forecast_id}},{"$group":{'_id':None,'average':{"$avg":"$current_prediction"}}}])
	if len(result['result']):
		return result['result'][0]['average']
	else:
		return None

def get_average_prediction(forecast_id):
	result = db.predictions.aggregate([{"$match":{'forecast_id':forecast_id}},{"$group":{'_id':None,'average':{"$avg":"$current_prediction"}}}])
	if len(result['result']):
		return result['result'][0]['average']
	else:
		return None

def get_counter(counter_type):
	counter = db.counters.find_one({'type':counter_type})
	if counter:
		counter['counter'] += 1
	else:
		counter = {'type':counter_type,'counter':1}
	db.counters.save(counter)
	return counter['counter']

def save_org_prediction(prediction):
	db.org_predictions.save(prediction)

def save_overall_prediction(prediction):
	db.overall_predictions.save(prediction)

def save_prediction(prediction):
	db.predictions.save(prediction)

def get_forecast(forecast_id):
	return db.forecasts.find_one({'forecast_id':forecast_id})

def save_forecast(forecast):
	db.forecasts.save(forecast)