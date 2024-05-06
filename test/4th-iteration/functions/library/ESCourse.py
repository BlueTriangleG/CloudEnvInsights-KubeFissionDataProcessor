from ESDocument import ESDocument

class ESCourse(ESDocument):

    def __init__(self, commons, req):
        super(ESCourse, self).__init__(commons, req, 'course')

