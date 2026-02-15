"""
End-to-end test with a REAL PDF bank statement.
Tests the complete pipeline: PDF → OCR → Categorize → Metrics → AI Analysis
"""
import asyncio
import json
import os
import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load env vars
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")


async def test_real_pdf(pdf_path: str):
    """Run the full pipeline on a real PDF."""

    print("\n" + "=" * 60)
    print("🧪 REAL PDF END-TO-END TEST")
    print("=" * 60)
    print(f"📄 File: {pdf_path}")
    print(f"📅 Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # ── Step 1: Verify the PDF exists ──
    if not os.path.exists(pdf_path):
        print(f"❌ File not found: {pdf_path}")
        sys.exit(1)
    file_size = os.path.getsize(pdf_path) / 1024
    print(f"✅ File found ({file_size:.1f} KB)")

    # ── Step 2: OCR ──
    print("\n" + "-" * 40)
    print("📸 Step 2: Running OCR...")
    t0 = time.time()

    from tools.ocr_engine import OCREngine
    ocr = OCREngine()
    ocr_result = ocr.extract_from_pdf(pdf_path)

    extracted_text = ocr_result.get("text", "")
    tables = ocr_result.get("tables", [])
    method = ocr_result.get("method", "unknown")

    ocr_time = time.time() - t0
    print(f"   ⏱️  OCR completed in {ocr_time:.2f}s  (method: {method})")
    print(f"   📝 Extracted {len(extracted_text)} characters")
    print(f"   📊 Found {len(tables)} table(s)")
    print(f"\n   --- Text Preview (first 500 chars) ---")
    print(f"   {extracted_text[:500]}")
    print(f"   --- end preview ---\n")

    if tables:
        print(f"   --- Table Preview (first table, first 5 rows) ---")
        for row in tables[0][:5]:
            print(f"   {row}")
        print(f"   --- end table preview ---\n")

    if not extracted_text.strip() and not tables:
        print("⚠️  OCR returned empty text and no tables – cannot continue.")
        return

    # ── Step 3: Build transactions from OCR data ──
    print("-" * 40)
    print("🏷️  Step 3: Building & categorizing transactions...")
    t1 = time.time()

    raw_transactions = []

    # Try to parse from tables first (more structured)
    if tables:
        for table in tables:
            if not table or len(table) < 2:
                continue
            header = table[0]  # first row as header
            print(f"   📋 Table header: {header}")
            for row in table[1:]:
                if not row or not any(row):
                    continue
                # Each row: [Month, Housing, Bills, Food, Personal, ...]
                month = row[0] if row[0] else ""
                for col_idx in range(1, len(row)):
                    if col_idx < len(header) and row[col_idx]:
                        category_name = header[col_idx] if col_idx < len(header) else f"Col{col_idx}"
                        amount_str = str(row[col_idx]).replace("$", "").replace(",", "").strip()
                        try:
                            amount = float(amount_str)
                            raw_transactions.append({
                                "description": f"{category_name} - {month}",
                                "amount": -abs(amount),  # expenses are negative
                                "date": month,
                                "category": category_name,  # pre-assigned from table header
                            })
                        except (ValueError, TypeError):
                            pass

    # If no table data, try regex parsing from text
    if not raw_transactions:
        import re
        for line in extracted_text.splitlines():
            m = re.search(
                r'(\d{1,2}[/-]\d{1,2}[/-]?\d{0,4})?\s*'
                r'(.+?)'
                r'\s+[₹$]?\s*([+-]?\d[\d,]*\.?\d*)\s*$',
                line.strip()
            )
            if m:
                desc = m.group(2).strip()
                amount_str = m.group(3).replace(',', '')
                try:
                    amount = float(amount_str)
                    if desc and len(desc) > 2:
                        raw_transactions.append({
                            "description": desc,
                            "amount": amount,
                            "date": m.group(1) or "",
                        })
                except ValueError:
                    pass

    print(f"   📊 Built {len(raw_transactions)} transactions")

    # Categorize transactions
    from tools.transaction_categorizer import TransactionCategorizer
    categorizer = TransactionCategorizer()
    categorized = categorizer.categorize_transactions(raw_transactions)
    cat_time = time.time() - t1
    print(f"   ⏱️  Categorization completed in {cat_time:.2f}s")

    # Show category distribution
    from collections import Counter
    cats = Counter(t.get("category", "Unknown") for t in categorized)
    print("\n   Category Distribution:")
    for cat, count in cats.most_common():
        print(f"      {cat}: {count}")

    # ── Step 4: Metrics Calculation ──
    print("\n" + "-" * 40)
    print("🧮 Step 4: Calculating financial metrics...")
    t2 = time.time()

    from tools.financial_metrics_engine import FinancialMetricsEngine
    metrics_engine = FinancialMetricsEngine()

    if categorized:
        metrics = metrics_engine.calculate_all_metrics(categorized)
    else:
        metrics = {
            "total_income": 0,
            "total_expenses": 0,
            "net_cash_flow": 0,
            "savings_rate": 0,
        }

    metrics_time = time.time() - t2
    print(f"   ⏱️  Metrics completed in {metrics_time:.2f}s")
    print(f"   💰 Total Income:   ${metrics.get('total_income', 0):,.2f}")
    print(f"   💸 Total Expenses: ${metrics.get('total_expenses', 0):,.2f}")
    print(f"   📈 Net Cash Flow:  ${metrics.get('net_cash_flow', 0):,.2f}")
    print(f"   🏦 Savings Rate:   {metrics.get('savings_rate', 0):.1f}%")

    if 'expenses_by_category' in metrics:
        print("\n   Expenses by Category:")
        for cat, amt in metrics['expenses_by_category'].items():
            print(f"      {cat}: ${amt:,.2f}")

    # ── Step 5: AI Agent Analysis via AnalysisService ──
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("\n⚠️  OPENROUTER_API_KEY not set – skipping AI agent analysis.")
        print("   Set it in .env or export OPENROUTER_API_KEY=...")
    else:
        print("\n" + "-" * 40)
        print("🤖 Step 5: Running AI Agent Analysis via AnalysisService...")
        print("   (Calling 4 LLM agents via OpenRouter – may take 20-30s)")
        t3 = time.time()

        try:
            from backend.services.analysis_service import AnalysisService
            service = AnalysisService(api_key)

            # Read the actual PDF bytes and run the full pipeline
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()

            ai_result = await service.analyze_bank_statement(pdf_bytes)

            ai_time = time.time() - t3
            print(f"   ⏱️  AI Analysis completed in {ai_time:.2f}s")

            # Log results from each agent
            for agent_key in ["debt_analysis", "savings_strategy", "budget_recommendations", "risk_score"]:
                data = ai_result.get(agent_key)
                if data:
                    print(f"   ✅ {agent_key}: responded")
                else:
                    print(f"   ❌ {agent_key}: no response")

            # Check for errors
            if ai_result.get("errors"):
                print(f"\n   ⚠️  Errors: {ai_result['errors']}")

            # Save full result
            out_path = Path(__file__).parent.parent / "test_data" / "real_pdf_result.json"
            out_path.parent.mkdir(exist_ok=True)
            with open(out_path, "w") as f:
                json.dump(ai_result, f, indent=2, default=str)
            print(f"\n   💾 Full result saved to: {out_path}")

        except Exception as e:
            print(f"   ❌ AI Analysis failed: {e}")
            import traceback
            traceback.print_exc()

    # ── Summary ──
    total_time = time.time() - t0
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"   📄 PDF:               {Path(pdf_path).name}")
    print(f"   📝 OCR Method:        {method}")
    print(f"   📝 OCR Text:          {len(extracted_text)} chars  ({ocr_time:.1f}s)")
    print(f"   📊 Tables Found:      {len(tables)}")
    print(f"   📊 Transactions:      {len(raw_transactions)} parsed")
    if categorized:
        print(f"   🏷️  Categories:       {len(set(t.get('category', '?') for t in categorized))} unique")
    print(f"   💰 Income:            ${metrics.get('total_income', 0):,.2f}")
    print(f"   💸 Expenses:          ${metrics.get('total_expenses', 0):,.2f}")
    print(f"   ⏱️  Total Time:       {total_time:.1f}s")
    print("=" * 60)


if __name__ == "__main__":
    pdf = sys.argv[1] if len(sys.argv) > 1 else str(
        Path(__file__).parent.parent / "Personal_Monthly_Expenditure_2021.pdf"
    )
    asyncio.run(test_real_pdf(pdf))
