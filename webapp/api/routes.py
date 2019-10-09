from webapp.api import bp


# GET
@bp.route('/request/open_account/<id>', methods=['GET'])
def get_request_open_account(id):
    pass


@bp.route('/request/open_account/<state_id>', methods=['GET'])
def get_request_open_account_by_state(state_id):
    pass


@bp.route('/request/open_account', methods=['GET'])
def get_request_open_account_all():
    pass


# POST
@bp.route('/request/open_account', methods=['POST'])
def create_request_open_account():
    pass
