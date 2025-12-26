"""
CSI Division Standards

Construction Specifications Institute (CSI) MasterFormat divisions
for organizing construction costs
"""

CSI_DIVISIONS = {
    '00': {
        'name': 'Procurement and Contracting Requirements',
        'description': 'Bidding, contracting, and project closeout'
    },
    '01': {
        'name': 'General Requirements',
        'description': 'Administrative, procedural, and temporary facility requirements'
    },
    '02': {
        'name': 'Existing Conditions',
        'description': 'Assessment, remediation, demolition, and site preparation'
    },
    '03': {
        'name': 'Concrete',
        'description': 'Concrete forming, reinforcing, and finishing'
    },
    '04': {
        'name': 'Masonry',
        'description': 'Brick, block, stone masonry'
    },
    '05': {
        'name': 'Metals',
        'description': 'Structural steel, metal fabrications, metal decking'
    },
    '06': {
        'name': 'Wood, Plastics, and Composites',
        'description': 'Rough carpentry, finish carpentry, architectural woodwork'
    },
    '07': {
        'name': 'Thermal and Moisture Protection',
        'description': 'Waterproofing, insulation, roofing, siding'
    },
    '08': {
        'name': 'Openings',
        'description': 'Doors, windows, glazing, hardware'
    },
    '09': {
        'name': 'Finishes',
        'description': 'Drywall, plaster, flooring, ceiling, painting'
    },
    '10': {
        'name': 'Specialties',
        'description': 'Toilet accessories, signage, partitions'
    },
    '11': {
        'name': 'Equipment',
        'description': 'Commercial, institutional equipment'
    },
    '12': {
        'name': 'Furnishings',
        'description': 'Furniture, window treatments, casework'
    },
    '13': {
        'name': 'Special Construction',
        'description': 'Pre-engineered structures, special facilities'
    },
    '14': {
        'name': 'Conveying Equipment',
        'description': 'Elevators, escalators, lifts'
    },
    '21': {
        'name': 'Fire Suppression',
        'description': 'Fire sprinkler systems, standpipes'
    },
    '22': {
        'name': 'Plumbing',
        'description': 'Plumbing fixtures, piping, equipment'
    },
    '23': {
        'name': 'HVAC',
        'description': 'Heating, ventilating, air conditioning'
    },
    '25': {
        'name': 'Integrated Automation',
        'description': 'Building automation systems'
    },
    '26': {
        'name': 'Electrical',
        'description': 'Electrical systems, lighting, power distribution'
    },
    '27': {
        'name': 'Communications',
        'description': 'Data, telephone, audio-visual systems'
    },
    '28': {
        'name': 'Electronic Safety and Security',
        'description': 'Security systems, fire alarms'
    },
    '31': {
        'name': 'Earthwork',
        'description': 'Excavation, grading, soil treatment'
    },
    '32': {
        'name': 'Exterior Improvements',
        'description': 'Paving, landscaping, site improvements'
    },
    '33': {
        'name': 'Utilities',
        'description': 'Water, sewer, electrical utilities'
    }
}


def get_division_name(division_code: str) -> str:
    """Get division name from code"""
    return CSI_DIVISIONS.get(division_code, {}).get('name', 'Unknown Division')


def get_all_divisions() -> dict:
    """Get all CSI divisions"""
    return CSI_DIVISIONS
