import html


def format_eur(amount: float) -> str:
    """Formats a float into German Euro currency style (e.g., 1250.5 -> '1.250,50 €')."""
    formatted = f"{amount:,.2f}"
    german_style = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{german_style} €"


def calculate_totals(items: list[dict], tax_rate: int) -> dict:
    """Calculates net subtotal, VAT (MwSt.), and gross total from line items."""
    net_total = round(sum(item["quantity"] * item["unit_price"] for item in items), 2)
    tax_amount = round(net_total * (tax_rate / 100.0), 2)
    gross_total = round(net_total + tax_amount, 2)
    return {
        "net_total": net_total,
        "tax_amount": tax_amount,
        "gross_total": gross_total,
        "net_formatted": format_eur(net_total),
        "tax_formatted": format_eur(tax_amount),
        "gross_formatted": format_eur(gross_total),
    }


def generate_invoice_html(data: dict) -> str:
    """Generates a clean, print-ready German invoice (Rechnung) in HTML/CSS."""
    esc = html.escape
    totals = calculate_totals(data["items"], data["tax_rate"])

    rows_html = ""
    for idx, item in enumerate(data["items"], start=1):
        line_total = round(item["quantity"] * item["unit_price"], 2)
        rows_html += f"""
        <tr>
            <td class="center">{idx}</td>
            <td>{esc(item["description"])}</td>
            <td class="right">{item["quantity"]}</td>
            <td class="right">{format_eur(item["unit_price"])}</td>
            <td class="right">{format_eur(line_total)}</td>
        </tr>
        """

    if not rows_html:
        rows_html = """
        <tr>
            <td colspan="5" class="center empty">Keine Positionen vorhanden / No line items added</td>
        </tr>
        """

    if data["tax_rate"] == 0:
        tax_note_html = (
            "<p class='tax-note'>Gemäß § 19 UStG wird keine Umsatzsteuer berechnet "
            "(Kleinunternehmerregelung).</p>"
        )
    else:
        tax_note_html = ""

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<title>Rechnung {esc(data["invoice_number"])}</title>
<style>
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
        color: #1f2937;
        margin: 0;
        padding: 32px;
        background: #ffffff;
        line-height: 1.5;
    }}
    .invoice-box {{
        max-width: 800px;
        margin: auto;
        border: 1px solid #e5e7eb;
        padding: 40px;
        border-radius: 8px;
    }}
    .header {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        border-bottom: 2px solid #111827;
        padding-bottom: 20px;
        margin-bottom: 28px;
    }}
    .sender-name {{
        font-size: 20px;
        font-weight: 700;
        color: #111827;
        margin: 0 0 4px 0;
    }}
    .muted {{
        color: #6b7280;
        font-size: 13px;
        margin: 0;
        white-space: pre-line;
    }}
    .doc-title {{
        text-align: right;
    }}
    .doc-title h1 {{
        margin: 0;
        font-size: 28px;
        letter-spacing: 1px;
        color: #111827;
    }}
    .meta-grid {{
        display: flex;
        justify-content: space-between;
        margin-bottom: 32px;
        gap: 24px;
    }}
    .client-box, .meta-box {{
        font-size: 14px;
    }}
    .section-label {{
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #6b7280;
        margin-bottom: 6px;
        font-weight: 600;
    }}
    .meta-table td {{
        padding: 3px 0;
    }}
    .meta-table td:first-child {{
        color: #6b7280;
        padding-right: 16px;
    }}
    table.items {{
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 24px;
        font-size: 14px;
    }}
    table.items th {{
        background: #f3f4f6;
        color: #111827;
        font-weight: 600;
        padding: 10px 12px;
        border-bottom: 2px solid #d1d5db;
        text-align: left;
    }}
    table.items td {{
        padding: 10px 12px;
        border-bottom: 1px solid #e5e7eb;
    }}
    .center {{ text-align: center !important; }}
    .right {{ text-align: right !important; }}
    .empty {{ color: #9ca3af; font-style: italic; padding: 20px; }}
    .totals-wrapper {{
        display: flex;
        justify-content: flex-end;
    }}
    table.totals {{
        width: 320px;
        border-collapse: collapse;
        font-size: 14px;
    }}
    table.totals td {{
        padding: 6px 8px;
    }}
    table.totals tr.grand-total td {{
        border-top: 2px solid #111827;
        font-weight: 700;
        font-size: 16px;
        padding-top: 10px;
        color: #111827;
    }}
    .tax-note {{
        font-size: 13px;
        color: #4b5563;
        margin-top: 16px;
    }}
    .footer {{
        margin-top: 40px;
        padding-top: 16px;
        border-top: 1px solid #e5e7eb;
        font-size: 12px;
        color: #6b7280;
        display: flex;
        justify-content: space-between;
    }}
    @media print {{
        body {{ padding: 0; }}
        .invoice-box {{ border: none; padding: 0; }}
    }}
</style>
</head>
<body>
<div class="invoice-box">
    <div class="header">
        <div>
            <p class="sender-name">{esc(data["sender_name"])}</p>
            <p class="muted">{esc(data["sender_address"])}</p>
        </div>
        <div class="doc-title">
            <h1>RECHNUNG</h1>
            <p class="muted">Nr. {esc(data["invoice_number"])}</p>
        </div>
    </div>

    <div class="meta-grid">
        <div class="client-box">
            <div class="section-label">Rechnungsempfänger / Bill To</div>
            <strong>{esc(data["client_name"])}</strong><br>
            <span class="muted">{esc(data["client_address"])}</span>
        </div>
        <div class="meta-box">
            <div class="section-label">Rechnungsdetails</div>
            <table class="meta-table">
                <tr><td>Rechnungsnummer:</td><td><strong>{esc(data["invoice_number"])}</strong></td></tr>
                <tr><td>Rechnungsdatum:</td><td>{esc(data["invoice_date"])}</td></tr>
                <tr><td>Zahlungsziel:</td><td>{esc(data["due_date"])}</td></tr>
                <tr><td>Steuernummer:</td><td>{esc(data["tax_id"])}</td></tr>
            </table>
        </div>
    </div>

    <table class="items">
        <thead>
            <tr>
                <th class="center" style="width: 50px;">Pos.</th>
                <th>Beschreibung / Leistung</th>
                <th class="right" style="width: 80px;">Menge</th>
                <th class="right" style="width: 120px;">Einzelpreis</th>
                <th class="right" style="width: 120px;">Gesamt</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>

    <div class="totals-wrapper">
        <table class="totals">
            <tr>
                <td>Nettobetrag:</td>
                <td class="right">{totals["net_formatted"]}</td>
            </tr>
            <tr>
                <td>MwSt. ({data["tax_rate"]}%):</td>
                <td class="right">{totals["tax_formatted"]}</td>
            </tr>
            <tr class="grand-total">
                <td>Rechnungsbetrag:</td>
                <td class="right">{totals["gross_formatted"]}</td>
            </tr>
        </table>
    </div>

    {tax_note_html}

    <div class="footer">
        <div>
            <strong>Bankverbindung:</strong><br>
            {esc(data["bank_details"])}
        </div>
        <div class="right">
            Vielen Dank für Ihren Auftrag!<br>
            Bitte geben Sie bei der Überweisung die Rechnungsnummer an.
        </div>
    </div>
</div>
</body>
</html>
"""
