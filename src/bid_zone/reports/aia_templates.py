"""
AIA Agreement Templates Generator
Generates standard AIA subcontractor agreement templates
"""

from typing import Dict, Optional
from datetime import datetime


class AIATemplateGenerator:
    """
    Generates AIA standard form subcontractor agreements.
    """
    
    def __init__(self, project_name: str = "Untitled Project"):
        self.project_name = project_name
        self.date = datetime.now()
    
    def generate_a401_template(
        self,
        division: str,
        scope_of_work: str,
        subcontractor_name: str = "[SUBCONTRACTOR NAME]",
        contract_amount: float = 0.0
    ) -> str:
        """
        Generate AIA A401 Standard Form of Agreement Between Contractor and Subcontractor.
        
        Args:
            division: CSI Division (e.g., "03 - Concrete")
            scope_of_work: Detailed scope description
            subcontractor_name: Name of subcontractor
            contract_amount: Contract amount
            
        Returns:
            AIA A401 template text
        """
        template = f"""
================================================================================
                    AIA DOCUMENT A401 – 2017
        STANDARD FORM OF AGREEMENT BETWEEN CONTRACTOR AND SUBCONTRACTOR
================================================================================

This Agreement is made as of {self.date.strftime('%B %d, %Y')}

BETWEEN the Contractor:
    [CONTRACTOR NAME]
    [ADDRESS]
    [CITY, STATE ZIP]

and the Subcontractor:
    {subcontractor_name}
    [ADDRESS]
    [CITY, STATE ZIP]

Project:
    Name: {self.project_name}
    Location: [PROJECT ADDRESS]
    Owner: [OWNER NAME]

The Contractor and Subcontractor agree as follows:

ARTICLE 1   THE SUBCONTRACT DOCUMENTS
The Subcontract Documents consist of this Agreement, the Conditions of the
Subcontract, and the other documents listed in this Agreement.

ARTICLE 2   SCOPE OF WORK

Division: {division}

The Subcontractor shall execute the following portion of the Work:

{scope_of_work}

The Subcontractor shall furnish all labor, materials, equipment, tools,
construction equipment and machinery, water, heat, utilities, transportation,
and other facilities and services necessary for proper execution and completion
of the Subcontract Work, whether temporary or permanent and whether or not
incorporated or to be incorporated in the Work.

ARTICLE 3   THE CONTRACT SUM

§ 3.1 The Contractor shall pay the Subcontractor the Contract Sum in current
funds for the Subcontractor's performance of the Subcontract. The Contract Sum
shall be:

    ${contract_amount:,.2f} ({"AMOUNT IN WORDS" if contract_amount == 0 else ""})

§ 3.2 The Contract Sum is based upon the following:
    • Unit prices as specified in attached schedule
    • Quantities as shown on plans and specifications
    • Includes all labor, materials, equipment, and overhead/profit

ARTICLE 4   PROGRESS PAYMENTS

§ 4.1 Based upon Applications for Payment submitted to the Contractor by the
Subcontractor and Certificates for Payment issued by the Architect, the
Contractor shall make progress payments on account of the Contract Sum to the
Subcontractor as provided below and elsewhere in the Subcontract Documents.

§ 4.2 Applications for Payment shall be submitted monthly, on or before the
25th day of each month.

§ 4.3 Provided an Application for Payment is received by the Contractor not
later than the date established in the Subcontract Documents, the Contractor
shall make payment to the Subcontractor not later than seven (7) days after
the Contractor receives payment from the Owner.

§ 4.4 Each progress payment shall be in an amount equal to the percentage of
the Work completed, less retainage as follows:
    • Retainage: 10% until 50% completion
    • Retainage: 5% from 50% to Substantial Completion
    • Final payment upon completion and acceptance

ARTICLE 5   FINAL PAYMENT

§ 5.1 Final payment, constituting the entire unpaid balance of the Contract
Sum, shall be made by the Contractor to the Subcontractor when:
    1. The Subcontractor's Work is fully completed
    2. All submittals have been approved
    3. Final cleanup has been completed
    4. All punchlist items have been completed
    5. Final release and waiver of liens has been provided

ARTICLE 6   INSURANCE AND BONDS

§ 6.1 The Subcontractor shall purchase and maintain insurance as required by
the Contract Documents, including:
    • Commercial General Liability
    • Automobile Liability
    • Workers' Compensation
    • Employer's Liability

Certificate of Insurance shall be provided prior to commencing work.

ARTICLE 7   SUBMITTALS AND SHOP DRAWINGS

§ 7.1 The Subcontractor shall submit all shop drawings, product data, samples,
and other submittals required by the Contract Documents in accordance with
the approved submittal schedule.

§ 7.2 All submittals shall be reviewed and stamped by the Subcontractor prior
to submission to the Contractor.

ARTICLE 8   WARRANTY

§ 8.1 The Subcontractor warrants to the Owner, Architect, and Contractor that
materials and equipment furnished under the Contract will be of good quality
and new unless the Contract Documents require or permit otherwise.

§ 8.2 The Subcontractor further warrants that the Work will conform to the
requirements of the Contract Documents and will be free from defects, except
for those inherent in the quality of the Work the Contract Documents require
or permit.

§ 8.3 Warranty Period: One (1) year from date of Substantial Completion unless
otherwise specified.

ARTICLE 9   INDEMNIFICATION

§ 9.1 To the fullest extent permitted by law, the Subcontractor shall indemnify
and hold harmless the Owner, Contractor, Architect, and their agents and
employees from and against claims, damages, losses, and expenses arising out
of or resulting from performance of the Subcontractor's Work.

ARTICLE 10   DISPUTE RESOLUTION

§ 10.1 Claims, disputes, and other matters in question arising out of or
relating to this Subcontract shall be subject to mediation as a condition
precedent to binding dispute resolution.

ARTICLE 11   TERMINATION OR SUSPENSION

§ 11.1 The Contractor may terminate or suspend the Subcontract for cause or
convenience in accordance with the provisions of the General Conditions of
the Contract for Construction.

================================================================================

This Agreement executed as of the day and year first written above.

CONTRACTOR:                           SUBCONTRACTOR:

_____________________________        _____________________________
Signature                            Signature

_____________________________        _____________________________
Print Name                           Print Name

_____________________________        _____________________________
Title                                Title

_____________________________        _____________________________
Date                                 Date

================================================================================
                                END OF DOCUMENT
================================================================================
"""
        return template
    
    def generate_g702_template(
        self,
        division: str,
        period_ending: Optional[datetime] = None
    ) -> str:
        """
        Generate AIA G702 Application and Certificate for Payment template.
        
        Args:
            division: CSI Division
            period_ending: Period ending date
            
        Returns:
            AIA G702 template text
        """
        period = period_ending or self.date
        
        template = f"""
================================================================================
                    AIA DOCUMENT G702 – 1992
            APPLICATION AND CERTIFICATE FOR PAYMENT
================================================================================

TO OWNER: [OWNER NAME]
        [OWNER ADDRESS]

FROM CONTRACTOR: [CONTRACTOR NAME]

PROJECT: {self.project_name}
        [PROJECT ADDRESS]
        [PROJECT NUMBER]

DIVISION: {division}

PERIOD TO: {period.strftime('%B %d, %Y')}

APPLICATION NO: ______    PERIOD ENDING: {period.strftime('%m/%d/%Y')}

VIA ARCHITECT: [ARCHITECT NAME]
              [ARCHITECT ADDRESS]

CONTRACT FOR: {division} Work

CONTRACT DATE: {self.date.strftime('%B %d, %Y')}


CONTRACTOR'S APPLICATION FOR PAYMENT

Application is made for payment, as shown below, in connection with the
Contract. Continuation Sheet(s), AIA Document G703, are attached.

1. ORIGINAL CONTRACT SUM                                    $______________

2. Net change by Change Orders                              $______________

3. CONTRACT SUM TO DATE (Line 1 ± 2)                       $______________

4. TOTAL COMPLETED & STORED TO DATE                         $______________
   (Column G on G703)

5. RETAINAGE:
   a. ____% of Completed Work                              $______________
      (Column D + E on G703)
   
   b. ____% of Stored Material                             $______________
      (Column F on G703)
   
   Total Retainage (Lines 5a + 5b)                         $______________

6. TOTAL EARNED LESS RETAINAGE                              $______________
   (Line 4 Less Line 5 Total)

7. LESS PREVIOUS CERTIFICATES FOR PAYMENT                   $______________
   (Line 6 from prior Certificate)

8. CURRENT PAYMENT DUE                                      $______________

9. BALANCE TO FINISH, INCLUDING RETAINAGE                   $______________
   (Line 3 less Line 6)


CHANGE ORDER SUMMARY                              ADDITIONS     DEDUCTIONS
Total changes approved in previous months         $________     $________
Total approved this month                         $________     $________
TOTALS                                           $________     $________
NET CHANGES by Change Order                       $______________


CONTRACTOR CERTIFICATION

The undersigned Contractor certifies that to the best of the Contractor's
knowledge, information and belief, the Work covered by this Application for
Payment has been completed in accordance with the Contract Documents, that
all amounts have been paid by the Contractor for Work for which previous
Certificates for Payment were issued and payments received from the Owner,
and that current payment shown herein is now due.


CONTRACTOR: _____________________________

By: _____________________________    Date: _______________
    (Signature)

    _____________________________
    (Print Name and Title)


ARCHITECT'S CERTIFICATE FOR PAYMENT

In accordance with the Contract Documents, based on on-site observations and
the data comprising this application, the Architect certifies to the Owner
that to the best of the Architect's knowledge, information and belief, the
Work has progressed as indicated, the quality of the Work is in accordance
with the Contract Documents, and the Contractor is entitled to payment of
the AMOUNT CERTIFIED.


AMOUNT CERTIFIED: $________________

(Attach explanation if amount certified differs from the amount applied.
Initial all figures on this Application and on the Continuation Sheet that
are changed to conform to the amount certified.)


ARCHITECT: _____________________________

By: _____________________________    Date: _______________
    (Signature)

    _____________________________
    (Print Name and Title)


This Certificate is not negotiable. The AMOUNT CERTIFIED is payable only to
the Contractor named herein. Issuance, payment and acceptance of payment are
without prejudice to any rights of the Owner or Contractor under this Contract.

================================================================================
                                END OF DOCUMENT
================================================================================
"""
        return template
    
    def generate_g703_template(self, division: str, line_items: list) -> str:
        """
        Generate AIA G703 Continuation Sheet template.
        
        Args:
            division: CSI Division
            line_items: List of line items with quantities and costs
            
        Returns:
            AIA G703 template text
        """
        template = f"""
================================================================================
                    AIA DOCUMENT G703 – 1992
                    CONTINUATION SHEET
================================================================================

APPLICATION NO: ______

PROJECT: {self.project_name}
DIVISION: {division}
PERIOD TO: {self.date.strftime('%B %d, %Y')}

"""
        
        # Table header
        template += f"""
{'':4} {'Description':35} {'Scheduled':>12} {'Work Comp':>12} {'%':>6} {'Balance':>12}
{'No.':4} {'of Work':35} {'Value':>12} {'This Period':>12} {'Comp':>6} {'To Finish':>12}
{'':4} {'':35} {'(C)':>12} {'(D)':>12} {'(E)':>6} {'(F)':>12}
{'-'*4} {'-'*35} {'-'*12} {'-'*12} {'-'*6} {'-'*12}
"""
        
        # Sample line items
        if not line_items:
            line_items = [
                {"no": "1", "desc": "Mobilization", "scheduled": 5000, "completed": 5000, "pct": 100},
                {"no": "2", "desc": "Materials", "scheduled": 25000, "completed": 15000, "pct": 60},
                {"no": "3", "desc": "Labor", "scheduled": 30000, "completed": 18000, "pct": 60},
            ]
        
        total_scheduled = 0
        total_completed = 0
        
        for item in line_items:
            no = item.get("no", "")
            desc = item.get("desc", "")[:33]
            scheduled = item.get("scheduled", 0)
            completed = item.get("completed", 0)
            pct = item.get("pct", 0)
            balance = scheduled - completed
            
            template += f"{no:4} {desc:35} ${scheduled:11,.2f} ${completed:11,.2f} {pct:5.1f}% ${balance:11,.2f}\n"
            
            total_scheduled += scheduled
            total_completed += completed
        
        total_balance = total_scheduled - total_completed
        total_pct = (total_completed / total_scheduled * 100) if total_scheduled > 0 else 0
        
        template += f"{'-'*4} {'-'*35} {'-'*12} {'-'*12} {'-'*6} {'-'*12}\n"
        template += f"{'':4} {'TOTALS':35} ${total_scheduled:11,.2f} ${total_completed:11,.2f} {total_pct:5.1f}% ${total_balance:11,.2f}\n"
        
        template += """
================================================================================
                                END OF DOCUMENT
================================================================================
"""
        return template
    
    def generate_subcontractor_package(
        self,
        division: str,
        scope_of_work: str,
        contract_amount: float,
        output_dir: str = "outputs"
    ) -> Dict[str, str]:
        """
        Generate complete subcontractor package with all AIA forms.
        
        Args:
            division: CSI Division
            scope_of_work: Scope of work description
            contract_amount: Contract amount
            output_dir: Output directory
            
        Returns:
            Dict with paths to generated files
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        files = {}
        
        # Generate A401
        a401_content = self.generate_a401_template(division, scope_of_work, contract_amount=contract_amount)
        a401_path = os.path.join(output_dir, f"AIA_A401_{division.replace(' ', '_')}.txt")
        with open(a401_path, 'w') as f:
            f.write(a401_content)
        files['a401'] = a401_path
        
        # Generate G702
        g702_content = self.generate_g702_template(division)
        g702_path = os.path.join(output_dir, f"AIA_G702_{division.replace(' ', '_')}.txt")
        with open(g702_path, 'w') as f:
            f.write(g702_content)
        files['g702'] = g702_path
        
        # Generate G703
        g703_content = self.generate_g703_template(division, [])
        g703_path = os.path.join(output_dir, f"AIA_G703_{division.replace(' ', '_')}.txt")
        with open(g703_path, 'w') as f:
            f.write(g703_content)
        files['g703'] = g703_path
        
        return files
