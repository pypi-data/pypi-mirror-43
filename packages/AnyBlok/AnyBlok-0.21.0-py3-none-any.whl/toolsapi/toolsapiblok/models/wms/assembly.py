from anyblok import Declarations

from anyblok_wms_base.exceptions import OperationInputsError

Model = Declarations.Model
register = Declarations.register


@register(Model.Wms.Operation)
class Assembly:

    def outcome_location(self):
        return [inp.location for inp in self.inputs if inp.location.type.code == "TRAY"][0]

    @classmethod
    def check_inputs_locations(cls, inputs, **kwargs):
        loc = [inp.location for inp in inputs if inp.location.type.code == "TRAY"][0]
        locations_error = any(inp.location != loc for inp in inputs[1:])
        # TODO: once PR#36 of AWB is merged, we can delete `'name' in kwargs` check
        if 'name' in kwargs and kwargs['name'] == 'final':
            locations_error = any(
                (inp.location != loc
                 and inp.location.type.parent != loc.type) for inp in inputs[1:]
            )
        if locations_error:
            raise OperationInputsError(
                cls,
                "Inputs {inputs} are in different Locations: {locations!r}",
                inputs=inputs,
                # in the passing case, building a set would have been
                # useless overhead
                locations=set(inp.location for inp in inputs))
