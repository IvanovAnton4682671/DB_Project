
class MultiDBRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'users_core':
            # return ['default', 'music_mongodb']
            # return 'default'
            return 'music_mongodb'
        elif model._meta.app_label == 'music_core':
            return 'music_mongodb'
        elif model._meta.app_label == 'music_links_core':
            return 'links_mongodb'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'users_core':
            return 'default'
        elif model._meta.app_label == 'music_links_core':
            return 'links_mongodb'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'default':
            return app_label in ['users_core', 'music_links_core']
        elif db == 'music_mongodb':
            return app_label == 'music_core'
        elif db == 'links_mongodb':
            return app_label == 'music_links_core'
        return None
