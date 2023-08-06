from sqlalchemy import orm
from anyblok import Declarations

register = Declarations.register
Model = Declarations.Model


@register(Model)
class Wms:
    """Namespace for WMS related models and transversal methods.

    Since this Model does not have any persistent data, making instances of
    it is mostly irrelevant, and therefore, the transversal methods are
    classmethods.
    """

    @classmethod
    def filter_on_phobj_types(cls, types):
        PhysObj = cls.registry.Wms.PhysObj
        phobj_types = orm.aliased(PhysObj.Type, name='phobj_types')

        def add_filter(query):
            return (query.join(phobj_types, PhysObj.type)
                         .filter(phobj_types.code.in_(set(types))))
        return add_filter
