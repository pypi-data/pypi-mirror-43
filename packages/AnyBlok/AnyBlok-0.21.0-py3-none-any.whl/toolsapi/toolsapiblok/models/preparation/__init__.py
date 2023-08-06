def import_declarations(reload=None):
    from . import preparation
    from . import np_eyewear
    from . import unifocal_glasses
    from . import progressive_glasses
    from . import frame_only
    from . import lens_only
    from . import home_trial
    from . import simple
    if reload is not None:
        reload(preparation)
        reload(np_eyewear)
        reload(unifocal_glasses)
        reload(progressive_glasses)
        reload(frame_only)
        reload(lens_only)
        reload(home_trial)
        reload(simple)
