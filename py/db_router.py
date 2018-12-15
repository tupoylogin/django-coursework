

def decide_on_model(model):
    """Small helper function to pipe all DB operations of py model to the kursach_data DB"""
    return 'kursach_data' if model._meta.app_label == 'py' else None


class MyDbRouter:
    """
    Implements a database router so that:

    * Django related data - DB alias `default` - MySQL DB `world_django`
    * Legacy "kursach" database data (everything "non-Django") - DB alias `kursach_data` - MySQL DB `kursach`
    """
    def db_for_read(self, model, **hints):
        return decide_on_model(model)

    def db_for_write(self, model, **hints):
        return decide_on_model(model)

    def allow_relation(self, obj1, obj2, **hints):
        # Allow any relation if both models are part of the worlddata app
        if obj1._meta.app_label == 'py' and obj2._meta.app_label == 'py':
            return True
        # Allow if neither is part of worlddata app
        elif 'py' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        # by default return None - "undecided"

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # allow migrations on the "default" (django related data) DB
        if db == 'default' and app_label != 'py':
            return True

        # allow migrations on the legacy database too:
        # this will enable to actually alter the database schema of the legacy DB!
        if db == 'kursach_data' and app_label == "py":
           return True
        return False