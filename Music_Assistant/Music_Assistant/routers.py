
class MultiDBRouter:
    def db_for_read(self, model, **hints):
        """Направляет операции чтения на соответствующую БД."""
        if model._meta.model_name == "users":
            return 'default'
        elif model._meta.model_name == "musicbase":
            return 'music_mongodb'
        elif model._meta.model_name == "musiclinks":
            return 'links_mongodb'
        return None

    def db_for_write(self, model, **hints):
        """Направляет операции записи на соответствующую БД."""
        return self.db_for_read(model, **hints)

    def allow_relation(self, obj1, obj2, **hints):
        """Определяет, могут ли две модели иметь отношение."""
        # Так как связи между разными базами данных в Django запрещены,
        # здесь требуется условие, запрещающее связи.
        if obj1._state.db in ['default', 'music_mongodb', 'links_mongodb'] and \
           obj2._state.db in ['default', 'music_mongodb', 'links_mongodb']:
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Управляет миграциями моделей."""
        if db == 'default':
            # Указывается, что миграции для default БД разрешены только для определенных моделей
            return model_name in ['users']
        if db == 'music_mongodb':
            return model_name in ['musicbase']
        if db == 'links_mongodb':
            return model_name in ['musiclinks']
        return None
