from fpdf import FPDF

class DesignDoc(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Google Ads API Integration Design Documentation', 0, 1, 'C')
        self.ln(10)

    def chapter_title(self, label):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, label, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, text):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 7, text)
        self.ln()

pdf = DesignDoc()
pdf.add_page()

pdf.chapter_title('1. Tool Purpose')
pdf.chapter_body(
    "The 'Pesona Property Manager' tool is an automated management system designed to streamline real estate marketing for the Pesona Kahuripan 12 housing project. "
    "The tool integrates a custom Landing Page with the Google Ads API to automate lead generation tracking and campaign optimization."
)

pdf.chapter_title('2. Features and Functionality')
pdf.chapter_body(
    "- Automatic Search Campaign creation based on property project data.\n"
    "- Real-time conversion tracking for WhatsApp inquiry button clicks.\n"
    "- Automated budget management and bid adjustments for Jabodetabek target area.\n"
    "- Performance reporting integration with local project logs."
)

pdf.chapter_title('3. API Usage Details')
pdf.chapter_body(
    "The tool uses the Google Ads API to:\n"
    "- Manage Campaign Budgets (CampaignBudgetService).\n"
    "- Create and update Search Campaigns (CampaignService).\n"
    "- Track customer conversions via Webpage/Contact actions (ConversionActionService).\n"
    "- Retrieve performance metrics for reporting (GoogleAdsService)."
)

pdf.chapter_title('4. Architecture and Security')
pdf.chapter_body(
    "The tool is built using Python and the official Google Ads Python Client Library. "
    "Authentication is handled via OAuth2 (Client ID, Client Secret, and Refresh Token) ensuring secure access. "
    "User data is stored in a private environment and follows Google Ads API best practices for data privacy."
)

pdf.output("Pesona_Property_Manager_Design_Doc.pdf")
