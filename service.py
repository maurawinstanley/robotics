import models
class ColorsService:
    def __init__(self):
        self.model = models.ColorsModel()
        
    def create(self, params):
    	params = params.json
    	self.model.create(params["Color"])
    	return 'OK'

       