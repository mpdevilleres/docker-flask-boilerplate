from project.utils import sort_tuple
##############
#  Resource  #
##############
class ChoicesContractor(object):
    '''
    this method ensure a dynamic choice_list for selectField
    '''
    def __iter__(self):
        from project.models import Contractor
        for i in Contractor.query.order_by(Contractor.name.asc()).all():
            yield (i.id, i.name)

class ChoicesContract(object):
    '''
    this method ensure a dynamic choice_list for selectField
    '''
    def __iter__(self):
        from project.models import Contract
        change_type = sort_tuple(choices_change_type())
        change_number = sort_tuple(choices_change_number())
        for i in Contract.query.order_by(Contract.contract_number.asc()).all():
            yield (i.id, '{} {}-{}'.format(i.contract_number,
                                   change_type[i.change_type-1],
                                   change_number[i.change_number-1]
                                           )
                   )
class ChoicesProject(object):
    '''
    this method ensure a dynamic choice_list for selectField
    '''
    def __iter__(self):
        from project.models import Project
        #yield (0,'')
        for i in Project.query.order_by(Project.project_no.asc()).all():
            yield (i.id, i.project_no)

class ChoicesDocument(object):
    '''
    this method ensure a dynamic choice_list for selectField
    '''
    def __iter__(self):
        from project.models import Document
        #yield (0,'')
        for i in Document.query.order_by(Document.reference_no.asc()).all():
            yield (i.id, i.reference_no)

class ChoicesUser(object):
    '''
    this method ensure a dynamic choice_list for selectField
    '''
    def __iter__(self):
        from project.models import User
        #yield (0,'')
        for i in User.query.filter(User.section==False).order_by(User.full_name.asc()).all():
            yield (i.id, i.full_name)

class ChoicesSection(object):
    '''
    this method ensure a dynamic choice_list for selectField
    '''
    def __iter__(self):
        from project.models import User
        #yield (0,'')
        query = User.query.\
                filter(User.first_name=='').\
                order_by(User.full_name.asc()).all()

        for i in query:
            yield (i.id, i.full_name)

class ChoicesTeamUser(object):
    '''
    this method ensure a dynamic choice_list for selectField
    '''
    def __iter__(self):
        from project.models import User
        #yield (0,'')
        for i in User.query.\
                filter(User.group_id<=2).\
                order_by(User.full_name.asc()).all():
            yield (i.id, i.full_name)

class ChoicesTask(object):
    '''
    this method ensure a dynamic choice_list for selectField
    '''
    def __iter__(self):
        from project.models import Task
        for i in Task.query.order_by(Task.task_no.asc()).all():
            yield (i.id, i.task_no)

class ChoicesVoucher(object):
    '''
    this method ensure a dynamic choice_list for selectField
    '''
    def __iter__(self):
        from project.models import Voucher
        for i in Voucher.query.order_by(Voucher.reference_no.asc()).all():
            #string_val = "%s [%s AED]" % (i.reference_no, i.amount)
            string_val = r'{}; {}'.format(i.reference_no, i.amount)
            yield (i.id, string_val)

# Start Vendor Management Choices
def choices_memo_destination():
    return [
        (1, 'OUTGOING'),
        (2, 'INCOMING')
    ]

def choices_csr_types():
    return [
    (1, 'Hardware'),
    (2, 'Software'),
    (3, 'Snag')
]

def choices_csr_status():
    return [
    (1, 'Open'),
    (2, 'Close')
]

def choices_signed_by():
    return [
        (1, 'SVP/MN'),
        (2, 'D/VR&SS'),
        (3, 'A.D/VR&SS'),
        (4, 'A.SVP/MN'),
        (5, 'Vendor'),
        (6, 'D/T&VM'),
        (7, 'CTO'),
    ]

# End Vendor Management Choices

# Start Task Team Management Choices

def choices_team_task_category():
    return [
        (1, 'Dispute'),
        (2, 'Delay Penalty'),
        (3, 'Invoice'),
        (4, 'Support Warranty'),
        (5, 'Others'),
    ]

def choices_team_task_severity():
    return [
        (1, 'Priority'),
        (2, 'Average'),
        (3, 'Low'),
    ]

def choices_team_task_class():
    return [
        (1, 'Internal'),
        (2, 'Vendor Relationship'),
    ]

def choices_team_task_status():
    return [
        (1, 'Open'),
        (2, 'Close'),
        (3, 'On-Hold'),
    ]

def choices_document_destination():
    return [
        (1, 'OUTGOING'),
        (2, 'INCOMING')
    ]

def choices_document_type():
    return [
        (1, 'Internal-CEO'),
        (2,'Internal-CTO'),
        (3,'Internal-Section Head'),
        (4,'Internal-Contract Department'),
        (5,'Internal-Human Resources'),
        (6,'Internal-Procurement'),
        (17,'Internal-Delay'),
        (7,'External-Vendor'),
        (8,'External-CSR HW'),
        (9,'External-CSR SNAG'),
        (10,'External-CSR SW'),
        (11,'External-Incident'),
        (12,'External-Performance'),
        (13,'External-Notification'),
        (14,'External-Implementation'),
        (15,'External-Progress'),
        (16,'External-Delay'),
        ]

def choices_document_status():
    return [
        (1, 'Under Preparation'),
        (2, 'For Signature'),
        (3, 'Waiting for Response'),
        (4, 'Vendor Replied'),
        (5, 'Done'),
        (6, 'Cancelled'),
        (7, 'No Action'),
    ]

def choices_document_signed_by():
    return [
        (1, 'SVP/MN'),
        (2, 'D/VR&SS'),
        (3, 'A.D/VR&SS'),
        (4, 'A.SVP/MN'),
        (5, 'Vendor'),
        (6, 'D/T&VM'),
        (7, 'CTO'),
    ]

# End Task Team Management Choices

# Start Contract Management Choices
def choices_applicable_question():
    return [
        (False, 'No'),
        (True, 'Yes'),
    ]


def choices_req_cert_issued():
    return [
        (1, 'RFQ'),
        (2, 'RFP'),
        (3, 'RFS'),
        (4, 'PAC'),
        (5, 'FAC'),
        (6, 'Committee')
        ]

def choices_type_opex():
    return [
        (1, 'Ongoing'),
        (2, 'Renewal'),
        (3, 'Planned'),
        ]

def choices_change_type():
    return [
        (3, 'AMD'),
        (2, 'ADD'),
        (1, 'PRINCIPAL'),
        ]

def choices_change_number():
    return [
            (1, 'I'),
            (2, 'II'),
            (3, 'III'),
            (4, 'IV'),
            (5, 'V'),
            (6, 'VI'),
            (7, 'VII'),
            (8, 'VIII'),
            (9, 'IX'),
            (10, 'X'),
            (11, 'XI'),
            (12, 'XII'),
            (13, 'XIII'),
            (14, 'XIV'),
            (15, 'XV'),
            (16, 'XVI'),
            (17, 'XVII'),
            (18, 'XVIII'),
            (19, 'XIX'),
            (20, 'XX'),
            ]

def choices_support_provided():
    return [
        (1, 'Yes'),
        (2, 'No')
        ]

def choices_status():
    return [
        (1, 'Active'),
        (2, 'Expired'),
        (3, 'Cancelled'),
        (3, 'On Hold'),
    ]

def choices_class_budget():
    return [
        (1, 'OPEX'),
        (2, 'CAPEX'),
        (3, 'BOTH'),
    ]

def choices_class_contract():
    return [
        (1, 'Project'),
        (2, 'Delivery'),
        (3, 'Support'),
    ]

def choices_certificate_type():
    return [
        (1, 'Ready For Service'),
        (2, 'Provisional Acceptance Certificate'),
        (3, 'Final Acceptance Certificate'),
    ]

def choices_task_status():
    return [
        (2, 'Closed'),
        (1, 'Open'),
        ]
