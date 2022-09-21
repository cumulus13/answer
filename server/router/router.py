# class Router(object):                                                                                            
                                                                                                                  
#     appname = ''                                                                                                 
                                                                                                                  
#     def db_for_read(self, model, **hints):                                                                       
#         """                                                                                                      
#         Attempts to read self.appname models go to model.db.                                                     
#          """                                                                                                      
#         if model._meta.app_label == self.appname:                                                                
#             return model.db                                                                                      
#         return None                                                                                              
                                                                                                                  
#     def db_for_write(self, model, **hints):                                                                      
#         """                                                                                                      
#         Attempts to write self.appname models go to model.db.                                                    
#         """                                                                                                      
#         if model._meta.app_label == self.appname: 
#             return model.db                                                                                      
#         return None                                                                                              
                                                                                                                  
#     def allow_relation(self, obj1, obj2, **hints):                                                               
#         """                                                                                                      
#         Allow relations if a model in the self.appname app is involved.                                          
#         """                                                                                                      
#         if obj1._meta.app_label == self.appname or obj2._meta.app_label == self.appname:                          
#             return True                                                                                           
#         return None                                                                                              
                                                                                                                  
#     # This is possibly the new way, for beyond 1.8.                                                              
#     '''                                                                                                          
#     def allow_migrate(self, db, app_label, model_name=None, **hints):                                            
#         """                                                                                                      
#         Make sure the self.appname app only appears in the self.appname                                          
#         database.                                                                                                
#          "                                                                                                      
#         if app_label == self.appname:                                                                            
#             return db == self.appname                                                                            
#         return None                                                                                              
#     '''                                                                                                          
                                                                                                                  
#     # Contrary to Djano docs this one works with 1.8, not the one above.                                         
#     def allow_migrate(self, db, model, model_name=None):
#             """                                                                                                  
#             Make sure the self.appname app only appears in the self.appname                                      
#             database.                                                                                            
#             """                                                                                                  
#             if db == self.appname:                                                                               
#                 return model._meta.app_label == self.appname                                                     
#             elif model._meta.app_label == self.appname:                                                          
#                 return False                                                                                     
#             return None

class Router(object):

    appname = ''
    
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    # route_app_labels = {'auth', 'contenttypes'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to auth_db.
        """
        if model._meta.app_label == self.appname:
            return model.db
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to auth_db.
        """
        if model._meta.app_label == self.appname:
            return model.db
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        # if (
        #     obj1._meta.app_label in self.route_app_labels or
        #     obj2._meta.app_label in self.route_app_labels
        # ):
        #    return True
        # return None

        if obj1._meta.app_label == self.appname or obj2._meta.app_label == self.appname:                          
            return True                                                                                           
        return None                                                                                              

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        
        # if app_label == self.appname:
        #     return db == self.appname
        # return None
        if db == self.appname:                                                                               
            return model._meta.app_label == self.appname                                                     
        elif model._meta.app_label == self.appname:                                                          
            return False                                                                                     
        return None

import random

class PrimaryReplicaRouter:
    def db_for_read(self, model, **hints):
        """
        Reads go to a randomly-chosen replica.
        """
        return random.choice(['replica1', 'replica2'])

    def db_for_write(self, model, **hints):
        """
        Writes always go to primary.
        """
        return 'primary'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in the primary/replica pool.
        """
        db_set = {'primary', 'replica1', 'replica2'}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        All non-auth models end up in this pool.
        """
        return True