# German Invoice (Rechnung) Generator
<img width="1671" height="972" alt="image" src="https://github.com/user-attachments/assets/f14de0f9-57d0-471c-891b-9d1a2273ab24" />


A web application built with **Python** and **Streamlit** that automates German VAT (*Mehrwertsteuer*) calculations, formats Euro currency according to German standards (`1.250,00 €`), and generates clean, printable HTML/PDF-ready invoices (*Rechnungen*).

## Features

- **German VAT Support:** Automatically calculates **19%** standard VAT (*Regelsteuersatz*), **7%** reduced VAT (*Ermäßigter Steuersatz*), or **0%** under *Kleinunternehmerregelung (§ 19 UStG)* with the required legal notice.
- **Dynamic Line-Item Management:** Add or remove billable services in real time using `st.session_state`.
- **German Currency & Date Formatting:** Formats monetary values (`1.234,50 €`) and dates (`DD.MM.YYYY`) to match German business conventions.
- **Live Preview & Printable Export:** Renders an instant live preview and exports a standalone, print-styled `.html` invoice (ready to save as PDF via browser print) with HTML escaping (`html.escape`) for safe input handling.

## Tech Stack

- **Language:** Python 3 (Standard Library: `html`, `datetime`)
- **Frontend / UI:** Streamlit

## Project Structure

```text
german_invoice_generator/
├── app.py              # Streamlit UI, session state management, and live preview
├── invoice_logic.py    # Pure Python currency formatting, VAT math, and HTML template builder
├── requirements.txt    # Python dependencies
├── .gitignore          # Excludes virtual environment and cache files
└── README.md           # Project documentation (EN / DE)
```

## Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/its-yassine/german_invoice_generator.git
   cd german_invoice_generator
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv .venv
   # Windows: .venv\Scripts\activate
   # macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Start the app:**
   ```bash
   streamlit run app.py
   ```

---

## Projektübersicht (Deutsch)

Ein Rechnungsgenerator auf Basis von **Python** und **Streamlit**, der deutsche Mehrwertsteuersätze (**19 %**, **7 %** sowie **0 % gemäß § 19 UStG**) berechnet, Beträge im deutschen Währungsformat (`1.250,00 €`) darstellt und eine druckfertige HTML-Rechnung inklusive Live-Vorschau erzeugt.
