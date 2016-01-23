import os
from project.config import DOC_DIR
from datetime import datetime as dt

def pp(obj):
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(obj)

def key_label(keys):
    '''
    Converts 'column_name' to 'Column Name'
    for better viewing
    :param keys:
    :return labels:
    '''
    labels = {}
    for k in keys:
        v = k.replace('_',' ')
        v = v.title()
        labels[k] = v
    return labels

def get_full_path(path):
    return os.path.join(DOC_DIR,path)

def get_choice_string(choices=None, value=None):
    return choices[value][1]

def days_between(d1, d2):
    return abs((d2 - d1).days)

def sort_tuple(choices):
    '''
    Input tuple list
    return flat sorted by index list
    '''
    choices_list = []
    for k,v in sorted(choices):
        choices_list.append(v)

    return choices_list


def month_diff(start_date, end_date):
    y_dif = abs(end_date.year - start_date.year)*12
    m_dif = (end_date.month - start_date.month)

    return y_dif + m_dif


def add_months(sourcedate, months):
    from datetime import datetime as dt
    import calendar
    month = sourcedate.month - 1 + months
    year = int(sourcedate.year + month/12)
    month = month % 12 + 1
    day = max(sourcedate.day,calendar.monthrange(year,month)[1])
    return dt(year, month, day)


def accrue_month(month=None, year=None):
    from datetime import datetime as dt
    from datetime import timedelta

    from project import db
    from project.models import Contract, Accrual

    if month is None or year is None:
        date_ref = dt.now()
    # Last Date of the given Month
    else:
        date_ref = dt(year,month,1) - timedelta(days=1)

    contracts = Contract.query.\
        filter(Contract.status==1).\
        filter(Contract.support_provided==1).\
        filter(Contract.expired_date>date_ref)

    for i in contracts:

        month_dif = i.support_end_date.month - i.support_start_date.month
        # make sure to avoid dividing to zero
        if month_dif > 0:
            accrue_amount = i.value_support/month_dif
            accrual = Accrual(
                contract_id = i.id,
                amount= accrue_amount,
                accrued_date= date_ref,
                accrued=False
            )
            db.session.add(accrual)
        db.session.commit()


def accrue_contract(contract_id=None):
    from project import db
    from project.models import Contract, Accrual

    contract = Contract.query.\
        filter(Contract.id==contract_id).first()

#    start_month = contract.support_start_date.month
#    end_month = contract.support_end_date.month

    month_dif = month_diff(contract.support_end_date,
                           contract.support_start_date
                           )

    # make sure to avoid dividing to zero
    month_dif = month_dif if month_dif > 0 else 1

    for i in range(1,month_dif+1):

        accrue_amount = contract.value_support/month_dif
        accrual = Accrual(
            contract_id = contract.id,
            amount = accrue_amount,
            accrued_date = add_months(contract.support_start_date,i),
            accrued = False
        )
        db.session.add(accrual)
    db.session.commit()

def date_dif_identification(start_date=None):
    dif = start_date - dt.now()
    dif = abs(dif.days)
    if dif >= 365:
        val =  'Greater Than 1 Year'
    elif dif >= 180:
        val = 'Greater Than Half Year'
    elif dif >= 30:
        val = 'Greater Than 1 Month'
    elif dif >= 7:
        val = 'Greater Than 1 week'
    else:
        val = 'More Than 1 day'
    return val

def update_budget_task(record_id=None): # Task ID
    from project import db
    from project.models import Task, Invoice
    from project.utils.analytic import query_to_df

    task =Task.query.filter_by(id=record_id).first_or_404()
    invoice = Invoice.query.filter(Invoice.task_id==record_id).all()

    df = query_to_df(invoice)
    try:
        total_amount = df['capex_amount'].sum()

    except KeyError:
        total_amount = 0

    task.expenditure_actual = total_amount
    db.session.add(task)
    db.session.commit()


def group_sort_to_list(gp, str_list=None):
    '''
    :param gp:  # grouped by dataframe
    :param to_str:  # string equivalent
    :return:    # list of (i, count)
    '''
    if str_list is None:
        def get_key(x):
           return x
    else:
        def get_key(x):
           return str_list[x-1]

    result=[]
    for i in gp.groups:
        count = len(gp.get_group(i))
        result.append(
            (get_key(i), count)  #tuple
            )
    return sorted(result)

def get_history_data(success, fail):
    try:
        return success[0]
    except IndexError:
        return 'No Update'