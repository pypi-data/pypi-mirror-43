from anyblok.declarations import Declarations, hybrid_method
from anyblok.column import Selection, String

Model = Declarations.Model
register = Declarations.register


@register(Model.Wms)
class Operation:
    reason = String(nullable=True)
    operation_type = Selection(selections='get_operation_types', nullable=True)

    @classmethod
    def get_operation_types(cls):
        return dict(
            picking='Picking',
            assembly='Assembly',
            quality_control='Quality control',
            packing='Packing',
            shipping='Shipping',
        )

    @hybrid_method
    def query_join_output_physobj(self, query):
        """
        join on the output of an operation using PhysObj.Avatar.outcome_of
        :param op_type: the operation type to filter on
        :param query: the base query
        :return:
        """
        WmsOperation = self.registry.Wms.Operation
        PhysObj = self.registry.Wms.PhysObj
        OutputObj = PhysObj.aliased(name="output_obj")
        OutputAvatar = PhysObj.Avatar.aliased(name="output_av")
        OutputType = PhysObj.Type.aliased(name="output_type")
        if "output_obj" not in str(query):
            query = (query
                     .join(OutputAvatar, OutputAvatar.outcome_of_id == WmsOperation.id)
                     .join(OutputObj, OutputAvatar.obj_id == OutputObj.id)
                     .join(OutputType, OutputObj.type_id == OutputType.id))
        return {
            'query': query,
            'obj_alias': OutputObj,
            'av_alias': OutputAvatar,
            'type_alias': OutputType,
        }

    @hybrid_method
    def query_join_input_physobj(self, query):
        """
        join on the input of an operation using Operation.HistoryInput.operation
        :param op_type: the operation type to filter on
        :param query: the base query
        :return:
        """
        WmsOperation = self.registry.Wms.Operation
        PhysObj = self.registry.Wms.PhysObj
        HI = WmsOperation.HistoryInput
        InputObj = PhysObj.aliased(name="input_obj")
        InputAvatar = PhysObj.Avatar.aliased(name="input_av")
        InputType = PhysObj.Type.aliased(name="input_type")
        if "input_obj" not in str(query):
            query = (query
                     .join(HI, WmsOperation.id == HI.operation_id)
                     .join(InputAvatar, HI.avatar_id == InputAvatar.id)
                     .join(InputObj, InputAvatar.obj_id == InputObj.id)
                     .join(InputType, InputObj.type_id == InputType.id))

        return {
            'query': query,
            'obj_alias': InputObj,
            'av_alias': InputAvatar,
            'type_alias': InputType,
        }

    @hybrid_method
    def query_filter_avatar_is_present(self):
        """
        add filter on Avatar.state 'present'
        :return:
        """
        return self.registry.Wms.PhysObj.Avatar.state == 'present'
