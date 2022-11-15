from celery import Celery

# Creating a Celery object


# A class to override the __call__ function which will be called
# at the time of executing async task

def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.update(app.config["CELERY_CONFIG"])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                print("--------------")
                print("Starting the task now")
                print("--------------")
                return self.run(*args, **kwargs)


    celery.Task = ContextTask
    return celery



