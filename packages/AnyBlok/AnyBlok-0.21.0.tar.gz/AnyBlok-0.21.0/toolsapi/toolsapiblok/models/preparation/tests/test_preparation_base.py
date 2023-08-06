from datetime import datetime
from anyblok.tests.testcase import BlokTestCase


class TestPreparationBase(BlokTestCase):

    @staticmethod
    def get_preparation_data():
        return {
            'preparation_type': '',
            'properties': {
                'preparation_data': {
                    'quantity': '',
                    'reason': '',
                    'sale_channel_code': '',
                },
                'bom': {
                    'inputs': {}
                }
            }
        }

    def get_preparation_inputs(self):
        data = self.get_preparation_data()
        return data['properties']['bom']['inputs']

    def plan_obj_arrival(self, gt, dt=datetime.now()):
        op = self.Operation.Arrival.create(
            physobj_type=gt,
            location=gt.get_default_storage_location(),
            dt_execution=dt,
            state='planned'
        )
        return op.outcomes[0]

    def reserve_preparation(self):
        for req in self.preparation.requests:
            req.reserve()
