from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
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
OUTPUT = ROOT / "public" / "checklist.pdf"

BRAND_GREEN = colors.HexColor("#20594C")
BRAND_BLUE = colors.HexColor("#EAF3F5")
BRAND_INK = colors.HexColor("#1F2933")
BRAND_MUTED = colors.HexColor("#5C6B73")
BRAND_RULE = colors.HexColor("#C9D8D5")
BRAND_WARN = colors.HexColor("#FFF4D6")


def on_page(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(BRAND_GREEN)
    canvas.rect(0, height - 15 * mm, width, 15 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(18 * mm, height - 9.5 * mm, "UK Pet Passport")
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(width - 18 * mm, height - 9.5 * mm, "Pet Travel Checklist - Updated July 2026")
    canvas.setStrokeColor(BRAND_RULE)
    canvas.line(18 * mm, 17 * mm, width - 18 * mm, 17 * mm)
    canvas.setFillColor(BRAND_MUTED)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(18 * mm, 11 * mm, "General guidance only. Always check GOV.UK and your destination country's official rules before travel.")
    canvas.drawRightString(width - 18 * mm, 11 * mm, f"Page {doc.page}")
    canvas.restoreState()


def styles():
    base = getSampleStyleSheet()
    base.add(
        ParagraphStyle(
            "TitleMain",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            textColor=BRAND_GREEN,
            alignment=TA_CENTER,
            spaceAfter=8,
        )
    )
    base.add(
        ParagraphStyle(
            "Subtitle",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=15,
            textColor=BRAND_MUTED,
            alignment=TA_CENTER,
            spaceAfter=12,
        )
    )
    base.add(
        ParagraphStyle(
            "Section",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13.5,
            leading=16,
            textColor=BRAND_GREEN,
            spaceBefore=10,
            spaceAfter=6,
        )
    )
    base.add(
        ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.6,
            leading=13.2,
            textColor=BRAND_INK,
            spaceAfter=5,
        )
    )
    base.add(
        ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.1,
            leading=10.5,
            textColor=BRAND_MUTED,
            spaceAfter=4,
        )
    )
    base.add(
        ParagraphStyle(
            "ChecklistBullet",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.2,
            leading=12.4,
            textColor=BRAND_INK,
            leftIndent=10,
            firstLineIndent=-10,
            spaceAfter=4,
        )
    )
    base.add(
        ParagraphStyle(
            "Cell",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.4,
            leading=10.8,
            textColor=BRAND_INK,
        )
    )
    base.add(
        ParagraphStyle(
            "CellHead",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8.5,
            leading=10.8,
            textColor=colors.white,
        )
    )
    return base


def p(text, style_name="Body"):
    return Paragraph(text, STYLES[style_name])


def bullet(text):
    return p(f"- {text}", "ChecklistBullet")


def checklist_table(rows):
    table_rows = [[p("Check", "CellHead"), p("What to do", "CellHead"), p("Notes", "CellHead")]]
    for check, action, notes in rows:
        table_rows.append([p(check, "Cell"), p(action, "Cell"), p(notes, "Cell")])

    table = Table(table_rows, colWidths=[34 * mm, 76 * mm, 55 * mm], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), BRAND_GREEN),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.35, BRAND_RULE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFA")]),
            ]
        )
    )
    return table


def callout(text):
    table = Table([[p(text, "Body")]], colWidths=[165 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), BRAND_WARN),
                ("BOX", (0, 0), (-1, -1), 0.4, colors.HexColor("#E3C46A")),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return table


def build_story():
    story = []
    story.append(p("UK to Europe Pet Travel Checklist", "TitleMain"))
    story.append(
        p(
            "For dogs, cats and ferrets travelling from Great Britain to the EU. "
            "Fully refreshed against GOV.UK guidance and April 2026 EU rule updates.",
            "Subtitle",
        )
    )
    story.append(
        callout(
            "<b>Core rule:</b> GB residents should get an Animal Health Certificate "
            "(AHC) for each trip from Great Britain to the EU. One AHC can include "
            "up to five pets, so costs are not automatically charged per pet."
        )
    )
    story.append(Spacer(1, 8))

    story.append(p("Key Facts", "Section"))
    for item in [
        "An AHC can include up to five pets.",
        "A new AHC is needed for each trip from Great Britain to an EU country.",
        "The AHC must be signed by an Official Veterinarian (OV). Your usual vet can issue one if they are an OV.",
        "The AHC is valid for entry into the EU for 10 days after issue, then for 6 months for onward EU travel and re-entry to Great Britain.",
        "Pets must be microchipped before, or at the same time as, their rabies vaccination.",
        "A pet must be at least 12 weeks old before rabies vaccination. After a first rabies vaccination, you must wait at least 21 full days before travel.",
        "Dogs usually need tapeworm treatment before entering Great Britain, unless travelling directly from Finland, Ireland, Northern Ireland, Malta or Norway.",
        "GB residents should not use EU pet passports to enter the EU. GOV.UK says GB residents should get an AHC when travelling from GB to the EU.",
    ]:
        story.append(bullet(item))

    story.append(p("Before You Book", "Section"))
    story.append(
        checklist_table(
            [
                (
                    "Destination rules",
                    "Check the official entry rules for the country you are visiting.",
                    "Individual EU member states may have additional requirements.",
                ),
                (
                    "Number of pets",
                    "Confirm whether your journey is non-commercial and within the five-pet limit.",
                    "April 2026 GOV.UK guidance notes a five-pet limit per private vehicle for EU entry.",
                ),
                (
                    "Route",
                    "Check your ferry, tunnel, airline or carrier pet rules before booking.",
                    "Some carriers have limited pet spaces or route-specific paperwork checks.",
                ),
                (
                    "Timing",
                    "Plan backwards from your EU entry date and return-to-GB date.",
                    "Rabies timing, AHC timing and dog tapeworm timing are separate checks.",
                ),
            ]
        )
    )

    story.append(PageBreak())
    story.append(p("Vet and Document Checks", "Section"))
    story.append(
        checklist_table(
            [
                (
                    "Microchip",
                    "Confirm your pet's microchip number and implantation date.",
                    "Microchip must be before, or at the same time as, rabies vaccination.",
                ),
                (
                    "Rabies",
                    "Check your pet has a valid rabies vaccination or booster.",
                    "For a first rabies vaccination, wait at least 21 full days before travel.",
                ),
                (
                    "OV appointment",
                    "Book an Official Veterinarian for the AHC.",
                    "Tell the practice you need an AHC, not just a normal health check.",
                ),
                (
                    "Records to bring",
                    "Bring proof of microchipping and vaccination history.",
                    "Ask your vet what records they need before the appointment.",
                ),
                (
                    "AHC issue date",
                    "Get the AHC issued within the 10-day EU entry window.",
                    "Day 1 is the date the AHC is issued.",
                ),
                (
                    "Multiple pets",
                    "Ask the OV to include all eligible pets travelling together on one AHC where appropriate.",
                    "GOV.UK allows up to five pets on one AHC.",
                ),
            ]
        )
    )

    story.append(p("Before Travel", "Section"))
    for item in [
        "Check every microchip number, date, name, species and destination detail on the AHC.",
        "Keep the original AHC with you. Digital copies are useful backups, but border checks may require the original.",
        "Confirm the carrier's pet check in process and arrive early enough for document checks.",
        "If travelling with a dog, plan any required tapeworm treatment around your return-to-GB timing.",
    ]:
        story.append(bullet(item))

    story.append(p("Returning to Great Britain", "Section"))
    story.append(
        checklist_table(
            [
                (
                    "AHC return validity",
                    "Use the AHC for re-entry to Great Britain within 6 months of issue, if the rabies vaccination remains valid.",
                    "If you stay abroad longer than 6 months, check GOV.UK for the document needed to return.",
                ),
                (
                    "Dogs",
                    "Arrange tapeworm treatment with a vet 24 to 120 hours before entering Great Britain.",
                    "Not required if coming directly from Finland, Ireland, Northern Ireland, Malta or Norway.",
                ),
                (
                    "Cats and ferrets",
                    "Tapeworm treatment is not required for cats or ferrets under GOV.UK dog tapeworm rules.",
                    "Still check destination and carrier rules.",
                ),
                (
                    "Next trip",
                    "Get a new AHC for the next trip from Great Britain to the EU.",
                    "AHCs are single-use for GB-to-EU entry.",
                ),
            ]
        )
    )

    story.append(PageBreak())
    story.append(p("What Changed From Older Advice", "Section"))
    for item in [
        "Do not treat AHC cost as automatically per pet. One AHC can cover up to five pets.",
        "Do not describe an AHC as simply valid for 10 days. The 10 days are for EU entry; later validity can cover onward EU travel and re-entry to Great Britain for up to 6 months.",
        "Do not say every normal vet is unable to issue an AHC. A normal vet can issue one if they are an Official Veterinarian.",
        "Do not say every typo automatically means quarantine. Paperwork errors can cause delays, refusal or other problems, so details should be checked carefully.",
        "Do not use old GB-resident EU pet passport assumptions. GOV.UK says GB residents should get an AHC for travel from GB to the EU.",
    ]:
        story.append(bullet(item))

    story.append(p("Cost Notes", "Section"))
    story.append(
        p(
            "AHC prices vary by veterinary practice and may include extra charges for additional pets, "
            "vaccinations or treatments. Ask the OV practice for a written quote. Avoid assuming that "
            "two pets means double the certificate cost, because GOV.UK allows up to five pets on one AHC.",
            "Body",
        )
    )

    story.append(p("Official Sources Checked", "Section"))
    refs = [
        (
            "GOV.UK - Taking your pet dog, cat or ferret abroad",
            "https://www.gov.uk/taking-your-pet-abroad",
        ),
        (
            "GOV.UK - Getting an animal health certificate",
            "https://www.gov.uk/taking-your-pet-abroad/getting-an-animal-health-certificate",
        ),
        (
            "GOV.UK - New EU rules for pet travel for GB residents",
            "https://www.gov.uk/government/news/new-eu-rules-for-pet-travel-for-gb-residents",
        ),
        (
            "GOV.UK - Bringing your pet dog, cat or ferret to Great Britain",
            "https://www.gov.uk/bring-pet-to-great-britain",
        ),
        (
            "GOV.UK - Tapeworm treatment for dogs entering Great Britain",
            "https://www.gov.uk/bring-pet-to-great-britain/tapeworm-treatment-dogs",
        ),
        (
            "RCVS Find a Vet",
            "https://findavet.rcvs.org.uk/",
        ),
    ]
    for name, url in refs:
        story.append(bullet(f"<b>{name}</b><br/>{url}"))

    story.append(p("Disclaimer", "Section"))
    story.append(
        p(
            "This checklist provides general information for UK pet owners and is not veterinary, legal or border-control advice. "
            "Rules can change, and destination countries and carriers may apply extra requirements. Always check official guidance "
            "and speak to an Official Veterinarian before travel.",
            "Small",
        )
    )
    return story


def build_pdf():
    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=22 * mm,
        bottomMargin=22 * mm,
        title="UK to Europe Pet Travel Checklist",
        author="UK Pet Passport",
        subject="Checklist for UK pet owners travelling to the EU with dogs, cats and ferrets",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    doc.addPageTemplates([PageTemplate(id="checklist", frames=[frame], onPage=on_page)])
    doc.build(build_story())


if __name__ == "__main__":
    STYLES = styles()
    build_pdf()
