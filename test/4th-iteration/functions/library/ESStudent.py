from ESDocument import ESDocument
from datetime import datetime

class ESStudent(ESDocument):

    def __init__(self, commons, req):
        super(ESStudent, self).__init__(commons, req, 'student')
