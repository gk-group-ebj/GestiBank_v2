from webapp import create_app, db
import webapp.bdd.models.account

if __name__ == '__main__':
    app = create_app()

    @app.shell_context_processor
    def inject_conf_var():
        return {'db': db, "Account": webapp.Account, "PaidAccount": webapp.PaidAccount, "DebitAccount": webapp.DebitAccount}
