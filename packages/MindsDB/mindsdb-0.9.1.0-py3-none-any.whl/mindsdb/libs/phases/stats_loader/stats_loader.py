from mindsdb.libs.constants.mindsdb import *
from mindsdb.libs.phases.base_module import BaseModule


class StatsLoader(BaseModule):

    phase_name = PHASE_STATS_GENERATOR

    def run(self):

        self.transaction.persistent_model_metadata = self.transaction.persistent_model_metadata.find_one(self.transaction.persistent_model_metadata.getPkey())

        # laod the most accurate model

        info = self.transaction.persistent_ml_model_info.find({'model_name':self.transaction.metadata.model_name}, order_by=[('r_squared',-1)])

        if info is not None and len(info)>0:
            self.transaction.persistent_ml_model_info = info[0]

        else:

            self.log.error('No model found for this statement, please check if model_name {model_name} was trained'.format(model_name=self.transaction.metadata.model_name))

def test():

    from mindsdb.libs.test.test_controller import TestController

    module = TestController('CREATE MODEL FROM (SELECT * FROM Uploads.views.tweets2 LIMIT 100) AS tweets4 PREDICT likes', PHASE_DATA_EXTRACTOR)

    return

# only run the test if this file is called from debugger
if __name__ == "__main__":
    test()
