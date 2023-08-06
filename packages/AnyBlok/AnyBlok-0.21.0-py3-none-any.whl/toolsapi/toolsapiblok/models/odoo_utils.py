from anyblok import Declarations
from logging import getLogger

logger = getLogger(__name__)


@Declarations.register(Declarations.Model)
class OdooUtils:
    """Helpers for the communication and data interchange with Odoo

    This carries general translation methods to help with the correspondence
    of data between Odoo8 or later and Tools / Kehl.

    These shouldn't be tied to any specific communication means so that they
    can be used from bus message consumers, various scripts etc.

    We're using an Anyblok Model instead of stuffing the methods in a
    stateless module, because it might become necessary for some future
    methods to make use of the database.

    The implementations of these methods are by no means fixed ; instead,
    this API is meant to encapsulate the various changes that will be needed
    to maintain the communitcation between the systems, so that other parts
    of Tools / Kehl can avoid bothering with that.

    In other words, if the result of one of this methods doesn't fit a corner
    case, it's likely that the right move is to change its implementation,
    rather than introducing conditions on the caller side.
    """

    @classmethod
    def odoo8_product_to_tools_wms(cls, product_code, production_lot_name):
        """Convert an Odoo8 product code into PhysObj code and Type code

        Depending on the family, the information that's on the Odoo8 side
        in the product code and the production lot name corresponds to
        PhysObj.Type.code and PhysObj.code on the Tools side.

        :param production_lot_name: can be `None`
        :returns: (PhysObj.Type.code, PhysObj.code)
                  The PhysObj code can be None
        :raises: ValueError(code) on unrecognized Odoo product code
        """
        return product_code, production_lot_name

    @classmethod
    def odoo8_product_schema_to_tools_wms(cls, data, pop=False):
        """Same as :meth:`odoo8_product_to_tools_wms`, from a :class:`dict`

        This is called `_schema` because the information is taken from data
        with expected keys being those defined by :class:`OdooProductSchema`,
        whose validation is supposed to have happened beforehand.

        :param bool pop: if True, used values are removed from ``data``
        """
        read = data.pop if pop else data.get
        return cls.odoo8_product_to_tools_wms(
            cls.translate_odoo_code(read('odoo_product_code')),
            read('odoo_production_lot_name', None))

    @staticmethod
    def translate_odoo_code(code):
        if code == "SUN-ORGA-150-005-PLAN":
            return "SUN-ORGA-150-005+000+000"

        return code

    @classmethod
    def tools_wms_to_odoo8_product(cls, type_code, physobj_code):
        """Convert a PhysObj code and Type code to Odoo8 product code

        Depending on the family, the information that's on the Odoo8 side
        in the product code and the production lot name corresponds to
        PhysObj.Type.code and PhysObj.code on the Tools side.

        :param physobj_code: can be `None`
        :returns: (PhysObj.Type.code, PhysObj.code)
                  The PhysObj code can be None
        :raises: ValueError('type'|'physobj', type_code, physobj_code)
                 if conversion fails.
        """
        return type_code, physobj_code
