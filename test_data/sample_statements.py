"""
Sample bank statement text for testing.
Simulates a realistic monthly bank statement.
"""

SIMPLE_STATEMENT = """
PERSONAL BANK STATEMENT
Account: **** 1234
Period: January 1-31, 2024

DEPOSITS AND CREDITS
Date        Description                     Amount
01/05/24    Employer Direct Deposit        +4,500.00
01/15/24    Freelance Payment              +1,200.00
01/20/24    Tax Refund                       +500.00

WITHDRAWALS AND DEBITS
Date        Description                     Amount
01/02/24    Rent - Landlord Payment        -1,800.00
01/03/24    Whole Foods Market               -156.78
01/05/24    Shell Gas Station                 -52.00
01/06/24    Amazon.com                       -89.99
01/07/24    Starbucks                         -12.50
01/08/24    Target                          -145.32
01/10/24    Electric Company                 -98.50
01/10/24    Water Utility                    -45.00
01/12/24    Chase Credit Card Payment       -500.00
01/14/24    Kroger Grocery                  -123.45
01/16/24    Chevron Gas                      -55.00
01/18/24    Netflix Subscription             -15.99
01/18/24    Spotify Premium                  -10.99
01/20/24    Restaurant - Italian Bistro     -87.50
01/22/24    Planet Fitness Membership        -29.99
01/24/24    CVS Pharmacy                     -34.56
01/26/24    Uber Ride                        -18.75
01/28/24    Trader Joe's                     -92.34
01/30/24    Internet Service Provider        -79.99

SUMMARY
Total Deposits:    $6,200.00
Total Withdrawals: $3,548.65
Net Change:        +2,651.35
"""

COMPLEX_STATEMENT = """
PREMIUM CHECKING ACCOUNT STATEMENT
Account Number: **** 5678
Statement Period: February 1-29, 2024

═══════════════════════════════════════════════
INCOME & DEPOSITS
═══════════════════════════════════════════════
02/01/24    Salary - Tech Corp             +8,500.00
02/10/24    Side Business Revenue          +2,400.00
02/15/24    Investment Dividend              +350.00
02/20/24    Rental Property Income         +1,800.00
02/25/24    Consulting Fee                 +1,500.00

═══════════════════════════════════════════════
HOUSING & UTILITIES
═══════════════════════════════════════════════
02/01/24    Mortgage Payment              -2,850.00
02/05/24    Property Tax                    -425.00
02/05/24    Home Insurance                  -165.00
02/08/24    Electric Bill                   -178.50
02/08/24    Gas Bill                        -89.25
02/08/24    Water/Sewer                     -67.80
02/10/24    Internet & Cable                -159.99
02/12/24    HOA Fees                        -225.00
02/15/24    Home Repair - Plumbing          -340.00

═══════════════════════════════════════════════
TRANSPORTATION
═══════════════════════════════════════════════
02/03/24    Car Payment - Toyota           -485.00
02/05/24    Car Insurance                   -178.50
02/07/24    Shell - Gas                     -68.90
02/12/24    Chevron - Gas                   -72.45
02/18/24    ExxonMobil - Gas                -65.30
02/22/24    Car Wash & Detail               -45.00
02/25/24    Oil Change & Maintenance        -125.00

═══════════════════════════════════════════════
FOOD & DINING
═══════════════════════════════════════════════
02/02/24    Whole Foods                    -187.43
02/04/24    Trader Joe's                    -94.28
02/06/24    Starbucks                       -18.75
02/08/24    Lunch - Chipotle                -15.80
02/09/24    Safeway Grocery                -156.92
02/11/24    Restaurant - Sushi              -98.50
02/13/24    Costco Bulk Purchase           -234.67
02/15/24    Dinner - Steakhouse            -156.80
02/16/24    Whole Foods                    -123.45
02/19/24    Lunch - Panera                  -24.50
02/21/24    Kroger Grocery                 -178.90
02/23/24    Restaurant - Mexican            -67.40
02/25/24    Starbucks                       -22.15
02/27/24    Trader Joe's                    -89.35
02/29/24    Dinner - Italian               -124.75

═══════════════════════════════════════════════
DEBT PAYMENTS
═══════════════════════════════════════════════
02/10/24    Chase Credit Card #1234       -1,250.00
02/10/24    Amex Credit Card #5678          -875.00
02/15/24    Discover Card #9012             -450.00
02/20/24    Student Loan Payment            -380.00

═══════════════════════════════════════════════
SHOPPING & ENTERTAINMENT
═══════════════════════════════════════════════
02/02/24    Amazon Prime Membership         -14.99
02/04/24    Amazon - Electronics           -299.99
02/06/24    Best Buy                       -456.78
02/08/24    Target                         -134.56
02/10/24    Netflix                         -17.99
02/10/24    Spotify                         -10.99
02/10/24    HBO Max                         -15.99
02/12/24    Movie Tickets                   -42.00
02/14/24    Flowers - Valentine's           -89.99
02/16/24    Clothing Store                 -234.50
02/18/24    Apple App Store                 -34.99
02/22/24    Concert Tickets                -180.00
02/25/24    Amazon - Books                  -67.43

═══════════════════════════════════════════════
HEALTH & FITNESS
═══════════════════════════════════════════════
02/01/24    Health Insurance Premium       -450.00
02/05/24    Gym Membership - 24HR           -49.99
02/08/24    Pharmacy - CVS                  -78.45
02/12/24    Doctor Visit Copay              -35.00
02/15/24    Dental Cleaning                 -125.00
02/20/24    Prescription Refill             -45.80
02/25/24    Vitamins - GNC                  -89.99

═══════════════════════════════════════════════
MISCELLANEOUS
═══════════════════════════════════════════════
02/03/24    Dry Cleaning                    -34.50
02/07/24    Pet Supplies - Petco            -87.65
02/10/24    Charitable Donation            -100.00
02/14/24    Hair Salon                      -95.00
02/18/24    Birthday Gift                   -125.00
02/22/24    Professional License Renewal    -250.00
02/28/24    Tax Preparation Fee            -350.00

═══════════════════════════════════════════════
FINANCIAL SUMMARY
═══════════════════════════════════════════════
Total Income:        $14,550.00
Total Expenses:      $13,247.23
Net Savings:         $1,302.77
Savings Rate:        8.95%

Average Daily Balance:   $12,456.78
Minimum Balance:         $1,234.56
Maximum Balance:         $18,901.23
"""

EDGE_CASE_HIGH_DEBT = """
CHECKING ACCOUNT STATEMENT
Period: March 2024

INCOME
03/01/24    Salary                        +3,200.00
03/15/24    Part-time Job                    +800.00

DEBT PAYMENTS (High Debt Scenario)
03/05/24    Credit Card 1 - Min Payment     -125.00 (Balance: $8,500)
03/05/24    Credit Card 2 - Min Payment     -95.00 (Balance: $6,200)
03/05/24    Credit Card 3 - Min Payment     -75.00 (Balance: $4,800)
03/10/24    Personal Loan                   -450.00 (Balance: $15,000)
03/10/24    Student Loan                    -280.00 (Balance: $32,000)
03/15/24    Car Loan                        -385.00 (Balance: $18,500)
03/20/24    Medical Bill Payment            -150.00 (Balance: $5,200)

ESSENTIAL EXPENSES
03/01/24    Rent                          -1,400.00
03/05/24    Utilities                       -195.00
03/07/24    Groceries                       -280.00
03/10/24    Gas                              -85.00
03/15/24    Phone Bill                       -75.00
03/20/24    Car Insurance                   -145.00

Total Income:     $4,000.00
Total Expenses:   $3,940.00
Total Debt:       $90,200.00
Debt-to-Income:   22.55 (Very High!)
"""

EDGE_CASE_NO_INCOME = """
STUDENT CHECKING ACCOUNT
Period: April 2024

EXPENSES ONLY (Student with no income)
04/01/24    Tuition Payment (Parents)     -2,500.00
04/03/24    Textbooks                       -450.00
04/05/24    Groceries                       -120.00
04/08/24    Fast Food                        -45.00
04/10/24    Coffee Shop                      -32.00
04/12/24    Gas                              -50.00
04/15/24    Groceries                       -115.00
04/18/24    Entertainment                    -60.00
04/20/24    Clothing                         -95.00
04/22/24    Groceries                       -108.00
04/25/24    Restaurant                       -75.00
04/28/24    Phone Bill                       -65.00

Total Income:     $0.00
Total Expenses:   $3,715.00
Net Change:       -$3,715.00
"""
