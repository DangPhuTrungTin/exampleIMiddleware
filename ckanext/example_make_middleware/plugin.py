import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
class Example_Make_MiddlewarePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IPackageController,inherit=True)
    plugins.implements(plugins.IMiddleware,inherit=True)
    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'example_make_middleware')
    def after_update(self,context,pkg_dict):
        db=self.db
        class Myuser(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            username = db.Column(db.String, unique=True, nullable=False)
            email = db.Column(db.String, unique=True, nullable=False)

        db.create_all()
        db.session.commit()
        db.session.add(Myuser(username="Flask", email="example@example.com"))
        db.session.commit()
        users = Myuser.query.all()
        import logging
        level = logging.INFO
        logger = logging.getLogger(__name__)
        logger.log(level, users)
        return pkg_dict
    def make_middleware(self, app, config):
        from ckan.config.middleware.flask_app import CKANFlask
        #because CKAN will call make_middleware method for both flask app and pythons app,
        #but SQLAlchemy just used on only flask app.
        if isinstance(app,CKANFlask):
            from flask_sqlalchemy import SQLAlchemy
            app.config['SQLALCHEMY_DATABASE_URI']="postgresql://ckan_default:ckan@localhost/ckan_default"
            self.db = SQLAlchemy(app)
        return app

