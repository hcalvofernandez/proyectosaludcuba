from trytond.pool import Pool
from health_ophthalmology_13.models.health_ophthalmology import *

def register():
    Pool.register(
        OphthalmologyEvaluation,
        OphthalmologyFindings,    
        module='health_ophthalmology', type_='model')
