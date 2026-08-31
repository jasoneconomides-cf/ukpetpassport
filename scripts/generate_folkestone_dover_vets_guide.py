from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "folkestone-dover-animal-health-certificate-guide.pdf"
PUBLIC = ROOT / "public" / "folkestone-dover-animal-health-certificate-guide.pdf"

NAVY = colors.HexColor("#111827")
VIOLET = colors.HexColor("#5B21B6")
PURPLE = colors.HexColor("#7C3AED")
AMBER = colors.HexColor("#F59E0B")
PALE = colors.HexColor("#F5F3FF")
SLATE = colors.HexColor("#475569")
LINE = colors.HexColor("#D8DEE9")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverBrand", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=PURPLE, spaceAfter=15, tracking=1.3))
styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=29, leading=32, textColor=NAVY, alignment=TA_LEFT, spaceAfter=14))
styles.add(ParagraphStyle(name="CoverSub", parent=styles["Normal"], fontSize=12, leading=18, textColor=SLATE, spaceAfter=20))
styles.add(ParagraphStyle(name="H1x", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=NAVY, spaceAfter=10))
styles.add(ParagraphStyle(name="H2x", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=13, leading=17, textColor=VIOLET, spaceBefore=8, spaceAfter=7))
styles.add(ParagraphStyle(name="Bodyx", parent=styles["BodyText"], fontSize=9.2, leading=13.5, textColor=SLATE, spaceAfter=7))
styles.add(ParagraphStyle(name="Smallx", parent=styles["BodyText"], fontSize=7.3, leading=10, textColor=SLATE))
styles.add(ParagraphStyle(name="TableHead", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=7.3, leading=10, textColor=colors.white))
styles.add(ParagraphStyle(name="Callout", parent=styles["BodyText"], fontSize=9.2, leading=13.5, textColor=NAVY, backColor=colors.HexColor("#FFF7ED"), borderColor=AMBER, borderWidth=1, borderPadding=10, spaceBefore=8, spaceAfter=10))
styles.add(ParagraphStyle(name="Footerx", parent=styles["Normal"], fontSize=7, leading=9, textColor=colors.HexColor("#64748B"), alignment=TA_CENTER))


def link(url, label):
    return f'<link href="{url}" color="#5B21B6"><u>{label}</u></link>'


def p(text, style="Bodyx"):
    return Paragraph(text, styles[style])


def table(data, widths, font_size=7.2, header=True):
    converted = []
    for row_index, row in enumerate(data):
        style = "TableHead" if header and row_index == 0 else "Smallx"
        converted.append([cell if hasattr(cell, "wrap") else p(str(cell), style) for cell in row])
    t = Table(converted, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.45, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), font_size),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]
    if header:
        commands += [("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold")]
    t.setStyle(TableStyle(commands))
    return t


def page_chrome(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(NAVY)
    canvas.rect(0, height - 13 * mm, width, 13 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(18 * mm, height - 8.5 * mm, "UK PET PASSPORT")
    canvas.setFillColor(colors.HexColor("#CBD5E1"))
    canvas.setFont("Helvetica", 7)
    canvas.drawRightString(width - 18 * mm, height - 8.5 * mm, "Folkestone & Dover AHC comparison")
    canvas.setStrokeColor(LINE)
    canvas.line(18 * mm, 15 * mm, width - 18 * mm, 15 * mm)
    canvas.setFillColor(colors.HexColor("#64748B"))
    canvas.setFont("Helvetica", 7)
    canvas.drawString(18 * mm, 10 * mm, "Latest version: ukpetpassport.com/folkestonedovervets")
    canvas.drawRightString(width - 18 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(str(OUTPUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=22 * mm, bottomMargin=20 * mm, title="Folkestone and Dover Animal Health Certificate Price Comparison Guide", author="UK Pet Passport")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    doc.addPageTemplates(PageTemplate(id="guide", frames=frame, onPage=page_chrome))
    story = []

    story += [Spacer(1, 13 * mm), p("UK PET PASSPORT", "CoverBrand"), p("Folkestone & Dover<br/><font color='#7C3AED'>Animal Health Certificate<br/>Price Comparison Guide</font>", "CoverTitle"), p("A practical comparison of providers near Dover and LeShuttle, including standard, multi-pet, repeat-trip, urgent and collection arrangements.", "CoverSub")]
    story += [Table([[p("PRICES CHECKED", "Smallx"), p("30 AUGUST 2026", "Smallx")], [p("ALWAYS GET THE LATEST VERSION", "Smallx"), p(link("https://ukpetpassport.com/folkestonedovervets", "ukpetpassport.com/folkestonedovervets"), "Smallx")]], colWidths=[55 * mm, 98 * mm], style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), PALE), ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#DDD6FE")), ("INNERGRID", (0, 0), (-1, -1), .5, colors.HexColor("#DDD6FE")), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 9), ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))]
    story += [Spacer(1, 16 * mm), p("Independent guide", "H2x"), p("UK Pet Passport is not affiliated with LeShuttle, Eurotunnel, GOV.UK or any veterinary provider. This guide is not a recommendation, quotation or booking service. Prices and terms can change. Confirm the current total and availability directly with the provider before booking.", "Callout"), p("General information only. Check current pet-travel requirements with GOV.UK, your destination authority, carrier and an Official Veterinarian.", "Smallx"), PageBreak()]

    story += [p("How to use this guide", "H1x"), p("The lowest headline price is not automatically the lowest total for your trip. The best fit can change according to the number of pets, how soon you travel, when you need to collect, and whether the provider issued your previous AHC."), p("A repeat or reprint price still means a new Animal Health Certificate for the new trip. Provider conditions determine whether an existing customer qualifies for a discount."), p("What we compared", "H2x")]
    story += [table([["Comparison", "Why it matters"], ["Standard price", "The advertised starting price for a new AHC."], ["Additional pets", "One AHC can cover up to five pets in eligible non-commercial travel, but provider charges differ."], ["Repeat trip", "Some providers discount a new certificate when details are unchanged."], ["Urgent service", "Short notice may increase the fee and remains subject to capacity."], ["Collection", "Opening hours, precise appointments and out-of-hours options vary."], ["Pet attendance", "The provider normally needs to scan the pet's microchip before issue."]], [42 * mm, 112 * mm])]
    story += [p("Before booking, ask for one written total covering your exact pets, travel date, destination, notice period, consultation and collection time.", "Callout"), PageBreak()]

    story += [p("Standard and multi-pet published pricing", "H1x"), p("These figures were checked against provider websites on 30 August 2026. Blank or unknown figures should be confirmed directly.")]
    standard = [
        ["Provider", "1 pet", "2 pets", "3 pets", "4 pets", "5 pets"],
        ["Euro Pets Folkestone*", "£95", "£120", "£145", "£170", "£195"],
        ["Easy Pet Travel", "£99", "£124", "£149", "£174", "£199"],
        ["Abbeywell / AHC Online", "£95", "£130", "£165", "£200", "£235"],
        ["White Cliffs Vets", "£153", "Not published", "Not published", "Not published", "Not published"],
        ["Manor Vets", "£251", "Not published", "Not published", "Not published", "Not published"],
        ["Hawkinge Veterinary Surgery", "Quote", "Quote", "Quote", "Quote", "Quote"],
        ["Hythe Vet Centre", "Quote", "Quote", "Quote", "Quote", "Quote"],
    ]
    story += [table(standard, [44 * mm, 22 * mm, 22 * mm, 22 * mm, 22 * mm, 22 * mm]), p("* Euro Pets was added as a nearby specialist provider; it was not listed on the LeShuttle leaflet used for the original shortlist.", "Smallx"), p("Published additional-pet basis", "H2x"), table([["Provider", "Published basis"], ["Euro Pets Folkestone", "£25 for each additional pet"], ["Easy Pet Travel", "£25 for each additional pet"], ["Abbeywell / AHC Online", "£35 for each additional pet"], ["Other providers", "Not published or requires confirmation"]], [58 * mm, 96 * mm]), PageBreak()]

    story += [p("Repeat-trip comparison", "H1x"), p("Eligibility is provider-specific. A changed address, owner, pet, rabies record, language or EU entry country can remove a discount.")]
    repeat = [
        ["Provider", "Published eligibility summary", "1 pet", "2 pets", "5 pets"],
        ["Abbeywell / AHC Online", "Previous Abbeywell AHC; details identical; at least 10 days' notice", "£65", "£95", "£185"],
        ["Easy Pet Travel", "Previous EPT AHC; listed owner, pet, address, vaccination and entry details unchanged; at least 7 days", "£69", "£94", "£169"],
        ["Euro Pets Folkestone", "Previous Euro Pets AHC; same details; more than 3 days' notice", "£70", "£95", "£170"],
        ["Other providers", "No repeat discount published", "Ask", "Ask", "Ask"],
    ]
    story += [table(repeat, [38 * mm, 67 * mm, 16 * mm, 16 * mm, 16 * mm]), p("Why repeat pricing deserves attention", "H2x"), p("The provider that appears cheapest for a first journey may not be cheapest for a later journey. Compare the trip you are booking now, then keep your records accurate so you can establish whether a repeat rate applies next time."), p("Do not assume a prior certificate can simply be reused. Each journey still needs the travel document required by the rules in force at that time.", "Callout"), PageBreak()]

    story += [p("Urgent and collection arrangements", "H1x"), p("Availability is never guaranteed. Contact the provider before making travel plans around an urgent service.")]
    urgent = [
        ["Provider / service", "Notice or timing", "1 pet", "2 pets"],
        ["Abbeywell standard", "At least 10 days", "£95", "£130"],
        ["Abbeywell express", "5 to 9 days", "£145", "£180"],
        ["Abbeywell urgent", "Same day to 4 days", "£195", "£230"],
        ["Easy Pet Travel standard", "Documents at least 3 days before travel", "£99", "£124"],
        ["Easy Pet Travel night", "Night collection; documents at least 3 days", "£144", "£169"],
        ["Easy Pet Travel short notice", "Within 72 hours", "£150", "£175"],
        ["Easy Pet Travel urgent", "Within 24 hours", "£199", "£224"],
        ["Euro Pets standard", "More than 3 days", "£95", "£120"],
        ["Euro Pets urgent", "Less than 3 days", "£170", "£195"],
        ["Euro Pets out of hours", "06:00-08:00 or 20:00-22:30", "+£30", "+£30"],
    ]
    story += [table(urgent, [48 * mm, 67 * mm, 20 * mm, 20 * mm]), p("Published collection picture", "H2x"), p("Easy Pet Travel advertised the broadest collection availability. Euro Pets advertised seven-day collection plus specified out-of-hours periods. Abbeywell published weekday and Saturday collection hours and was closed Sundays and bank holidays. Conventional practices generally used normal surgery hours. Confirm all times when booking."), PageBreak()]

    story += [p("Provider contacts and source links", "H1x"), p("Use the provider's own site for the current price, conditions and availability. Phone or email where the website does not answer your exact question.")]
    contacts = [
        ["Provider", "Website or contact"],
        ["Abbeywell / AHC Online", link("https://animalhealthcertificate.online/pricing/", "Current pricing") + " | " + link("https://animalhealthcertificate.online/services/", "Service conditions")],
        ["Easy Pet Travel", link("https://www.animalhealthcertificates.com/ourprices", "Prices and service information")],
        ["Euro Pets Folkestone", link("https://europets.co.uk/", "Provider website")],
        ["White Cliffs Vets", link("https://ivc.co.uk/find-a-vet/white-cliffs-vets-whitfield/services-and-prices", "Official practice prices") + " | 01304 414141"],
        ["Manor Vets", link("https://ivc.co.uk/find-a-vet/manor-vets-folkestone/services-and-prices", "Official practice prices") + " | 01303 273203"],
        ["Hawkinge Veterinary Surgery", "01303 764190 | hawkingevetsurgery@gmail.com"],
        ["Hythe Vet Centre", "01303 260003 | hello@hythevetcentre.co.uk"],
    ]
    story += [table(contacts, [52 * mm, 102 * mm]), p("Six questions worth asking", "H2x"), p("1. What is the complete price for my number of pets travelling together?<br/>2. Is the fee per certificate, owner or pet?<br/>3. Is a consultation or examination charged separately?<br/>4. Do you accept pets that are not registered patients?<br/>5. What qualifies for a repeat-customer discount?<br/>6. What notice is required, and are urgent or out-of-hours charges added?")]
    story += [p("Official rules", "H2x"), p(link("https://www.gov.uk/taking-your-pet-abroad", "GOV.UK: Taking your pet abroad") + "<br/>" + link("https://www.gov.uk/taking-your-pet-abroad/getting-an-animal-health-certificate", "GOV.UK: Getting an Animal Health Certificate")), p("This guide provides general information only and cannot account for your pet, route or circumstances. UK Pet Passport is an independent publisher and is not an official service.", "Callout")]

    doc.build(story)
    PUBLIC.write_bytes(OUTPUT.read_bytes())
    print(OUTPUT)
    print(PUBLIC)


if __name__ == "__main__":
    build()
