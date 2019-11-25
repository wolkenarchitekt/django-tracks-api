class MyDBRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'tracks':
            return 'tracks'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'tracks':
            return 'tracks'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'tracks':
            return db == 'tracks'
        elif db == 'tracks':
            return False
        return None
