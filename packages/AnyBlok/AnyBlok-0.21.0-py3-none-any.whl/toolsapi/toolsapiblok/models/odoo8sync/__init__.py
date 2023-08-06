# flake8: noqa
"""This Python package is to handle synchronizations with Odoo 8.

By synchronization, we mean that this is about data that is duplicated
between Odoo8 and Tooks / Kehl. Therefore, the facilities provided by this
package are to be thought of as scaffolding for the strangling pattern.

By contrast, normal delegation of functional fields don't fit into this
package. For example, if Odoo 8 or any subsequent system doesn't handle
Preparations anymore, and issues messages telling Tools / Kehl that a
Sales Order has been confirmed (so that it can issue
Preparations), the handling of that message is is not a synchronization
task.

Splitting synchronizations in the current separate package will help
getting rid of parts of the code once they're not needed anymore.
That's why the tests are provided inside the current package (a good practice
in many cases)

Example: while the manufacturing process is been done on the Odoo 8 side,
it's necessary to reflect the consumption of parts and the production of
the outcome on the Tools / Kehl side.
"""
def import_declarations(reload=None):
    from . import ns
    from . import fab_packing
    from . import reception
    from . import physobj_type
    from . import location
    from . import internal_move
    if reload is not None:
        reload(ns)
        reload(fab_packing)
        reload(reception)
        reload(physobj_type)
        reload(internal_move)
