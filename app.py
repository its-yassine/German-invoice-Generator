from datetime import date, timedelta
import streamlit as st
import streamlit.components.v1 as components
import invoice_logic as inv

st.set_page_config(page_title="German Invoice Generator", layout="wide")

st.title("German Invoice (Rechnung) Generator")
st.caption("Automated German VAT (MwSt.) Calculation & Printable Invoice Builder — Python & Streamlit")

# Initialize sample line items in session state so the preview works immediately
if "items" not in st.session_state:
    st.session_state.items = [
        {"description": "Python Backend & SQLite Integration (8 Std.)", "quantity": 8, "unit_price": 45.00},
        {"description": "Streamlit Dashboard Deployment & Testing", "quantity": 1, "unit_price": 180.00},
    ]

TAX_OPTIONS = {
    "19% — Regelsteuersatz (Standard German VAT)": 19,
    "7% — Ermäßigter Steuersatz (Reduced VAT)": 7,
    "0% — Kleinunternehmerregelung (§ 19 UStG)": 0,
}

left_col, right_col = st.columns([1, 1.25], gap="large")

# --- LEFT COLUMN: INPUTS & LINE ITEMS ---
with left_col:
    st.subheader("1. Invoice & Party Details")

    with st.expander("Sender & Recipient Information", expanded=True):
        sender_name = st.text_input("Your Name / Business (Absender)", value="Yassine IT Solutions")
        sender_address = st.text_area(
            "Sender Address",
            value="Musterstraße 12\n10115 Berlin, Deutschland",
            height=68,
        )
        client_name = st.text_input("Client Company (Empfänger)", value="NordCloud Systems GmbH")
        client_address = st.text_area(
            "Client Address",
            value="Hafenstraße 44\n20457 Hamburg, Deutschland",
            height=68,
        )

    with st.expander("Invoice Metadata & Tax Rate", expanded=True):
        m1, m2 = st.columns(2)
        with m1:
            invoice_number = st.text_input("Invoice Number (Rechnungsnr.)", value="RE-2026-001")
            invoice_date = st.date_input("Invoice Date", value=date.today())
        with m2:
            tax_id = st.text_input("Tax ID (Steuernummer / USt-IdNr.)", value="DE123456789")
            due_date = st.date_input("Due Date (Zahlungsziel)", value=date.today() + timedelta(days=14))

        tax_label = st.selectbox("German VAT Rate (MwSt.)", list(TAX_OPTIONS.keys()))
        tax_rate = TAX_OPTIONS[tax_label]

        bank_details = st.text_input(
            "Bank / IBAN Details",
            value="DE89 3704 0044 0532 0130 00 | BIC: COBADEFFXXX",
        )

    st.subheader("2. Line Items (Leistungen)")
    with st.form("add_item_form", clear_on_submit=True):
        desc = st.text_input("Service / Item Description *")
        q_col, p_col = st.columns(2)
        with q_col:
            qty = st.number_input("Quantity (Menge)", min_value=1, value=1, step=1)
        with p_col:
            price = st.number_input("Unit Price in € (Einzelpreis)", min_value=0.0, value=50.0, step=5.0)

        if st.form_submit_button("Add Line Item"):
            if desc.strip():
                st.session_state.items.append(
                    {"description": desc.strip(), "quantity": int(qty), "unit_price": float(price)}
                )
                st.rerun()
            else:
                st.error("Please enter a service or item description.")

    if st.session_state.items:
        for idx, item in enumerate(st.session_state.items):
            r1, r2 = st.columns([5, 1])
            with r1:
                st.write(
                    f"**{idx + 1}. {item['description']}** — "
                    f"{item['quantity']} × {inv.format_eur(item['unit_price'])}"
                )
            with r2:
                if st.button("Remove", key=f"del_{idx}"):
                    st.session_state.items.pop(idx)
                    st.rerun()

        if st.button("Clear All Items", type="secondary"):
            st.session_state.items = []
            st.rerun()

# --- RIGHT COLUMN: LIVE CALCULATIONS & PRINTABLE PREVIEW ---
with right_col:
    st.subheader("3. Summary & Live Invoice Preview")

    totals = inv.calculate_totals(st.session_state.items, tax_rate)
    k1, k2, k3 = st.columns(3)
    k1.metric("Nettobetrag (Net)", totals["net_formatted"])
    k2.metric(f"MwSt. ({tax_rate}%)", totals["tax_formatted"])
    k3.metric("Bruttobetrag (Total)", totals["gross_formatted"])

    invoice_payload = {
        "sender_name": sender_name,
        "sender_address": sender_address,
        "client_name": client_name,
        "client_address": client_address,
        "invoice_number": invoice_number,
        "invoice_date": invoice_date.strftime("%d.%m.%Y"),
        "due_date": due_date.strftime("%d.%m.%Y"),
        "tax_id": tax_id,
        "tax_rate": tax_rate,
        "bank_details": bank_details,
        "items": st.session_state.items,
    }

    html_invoice = inv.generate_invoice_html(invoice_payload)

    st.download_button(
        label="Download Printable Invoice (.html)",
        data=html_invoice,
        file_name=f"Rechnung_{invoice_number}.html",
        mime="text/html",
        type="primary",
    )
    st.caption("Tip: Open the downloaded HTML file in any browser and press Ctrl+P (or Cmd+P) to save as PDF.")

    components.html(html_invoice, height=740, scrolling=True)
