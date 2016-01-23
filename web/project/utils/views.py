# project/utils/views.py


#################
#### imports ####
#################

from flask import render_template, request, flash, redirect, url_for
from flask.ext.login import login_required
from flask.views import View


################
#### routes ####
################
from project import db
from project.user_mgt.utils import access_level_required


class AddEditView(View):
    '''
    Classify the basic function view same as below logic

    @contract_mgt_blueprint.route('/contractor', methods=['GET','POST'])
    @contract_mgt_blueprint.route('/contractor/<record_id>', methods=['GET','POST'])
    @login_required
    def add_contractor(record_id=None):

        _model = Contractor
        _form = ContractorForm
        _form_title = 'Contractor'
        _template = 'default/add-form.html'
        _func_name = 'contract_mgt.add_contractor'
        _form_seq = [
            ['name', 'short_hand'],
            ['profile', 'remarks']
        ]

        try:
            record_id = int(record_id)
        except ValueError:
            return render_template('errors/404.html'), 404

        if record_id is None:
            record = _model()
            form = _form()
        else:
            record = _model.query.filter_by(id=record_id).first_or_404()
            form = _form(obj=record)

        if request.method == 'POST' and form.validate():
            form.populate_obj(record)
            db.session.add(record)
            db.session.commit()
            flash('<strong>Success!</strong> Database Updated.')
            return redirect(url_for('{}'.format(_func_name)))

        return render_template(_template,
                               form=form,
                               form_title = _form_title,
                               form_seq = _form_seq)
    '''
    methods = ['GET', 'POST']
    # Access Levels
    # 3 Must be End-User above
    # 2 Must be Part of Budget Team
    # 1 Must be Admin
    decorators = [access_level_required(2),
                  login_required]

    _model = None
    _form = None
    _form_title = None
    _template = None
    _func_name = None
    _form_seq = None
    db=db

    def dispatch_request(self, record_id=None):
        if record_id is None:
            self.record = self._model()
            form = self._form()
        else:

            # Ensure/Check that record_id is a int Type
            # Else Return 404
            try:
                record_id = int(record_id)
            except (ValueError):
                return render_template('errors/404.html'), 404


            self.record = self._model.query.filter_by(id=record_id).first_or_404()
            form = self._form(obj=self.record)

        if request.method == 'POST' and form.validate():
            form.populate_obj(self.record)
            self.save()
            flash('<strong>Success!</strong> Database Updated.')
            return form.redirect(url_for('{}'.format(self._func_name)))

        return render_template(self._template,
                               form=form,
                               form_title = self._form_title,
                               form_seq = self._form_seq)

    def save(self):
        self.db.session.add(self.record)
        self.db.session.commit()

def register_api(view, endpoint, url, blueprint, pk='record_id', pk_type='int'):
    '''
    :param view: Eg. AddEditContractView
    :param endpoint: Eg. 'contract' will be use for
                        url_for('contract_mgt.contract')
    :param url: Eg. /contract/
    :param pk:  Eg. 'record_id'
    :param blueprint:
    :return:
    '''
    view_func = view.as_view(endpoint)

    blueprint.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET', 'POST'])
    blueprint.add_url_rule('%s/<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                     methods=['GET', 'POST'])