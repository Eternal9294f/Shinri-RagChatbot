"""Scraper and raw data normalizer for HDFC Mutual Fund schemes on Groww."""
from pathlib import Path
import json
from src.config import RAW_DATA_DIR, HDFC_SCHEMES

# Curated factual scheme data extracted from official public scheme pages on Groww / AMC
SCHEME_DOCUMENTATION = {
    "hdfc-large-cap-fund-direct-growth": {
        "scheme_name": "HDFC Large Cap Fund Direct Plan - Growth",
        "category": "Large Cap",
        "amc": "HDFC Mutual Fund",
        "url": "https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth",
        "benchmark": "NIFTY 100 TRI",
        "riskometer": "Very High Risk",
        "nav_plan": "Direct Plan - Growth",
        "sections": {
            "Overview & Objective": (
                "HDFC Large Cap Fund Direct Plan - Growth is an open-ended equity mutual fund scheme offered by HDFC Mutual Fund. "
                "The investment objective is to generate long-term capital appreciation by predominantly investing in equity and equity-related instruments of large-cap companies. "
                "It is categorized under Equity: Large Cap. Source: https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth"
            ),
            "Expense Ratio & Charges": (
                "The expense ratio of HDFC Large Cap Fund Direct Plan - Growth is 0.94% (inclusive of GST). "
                "The expense ratio represents the annual percentage fee charged by the fund management company to manage the fund. "
                "A stamp duty of 0.005% is applicable on all mutual fund purchases from July 1, 2020. Source: https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth"
            ),
            "Exit Load": (
                "The exit load for HDFC Large Cap Fund Direct Plan - Growth is 1.00% if redeemed or switched out within 1 year (365 days) from the date of allotment. "
                "If redeemed after 1 year (365 days), the exit load is Nil (0%). "
                "Exit load is a charge levied on investors if they redeem their units before the specified holding period. Source: https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth"
            ),
            "Minimum Investment & SIP": (
                "For HDFC Large Cap Fund Direct Plan - Growth, the minimum SIP (Systematic Investment Plan) amount is Rs 100 per month. "
                "The minimum one-time lumpsum investment amount is Rs 100. "
                "There is no upper limit on the maximum investment amount. Source: https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth"
            ),
            "Lock-in Period & Redemption": (
                "HDFC Large Cap Fund Direct Plan - Growth has Nil lock-in period. "
                "Investors can redeem their mutual fund units on any business day, subject to applicable exit loads and taxation rules. Source: https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth"
            ),
            "Benchmark & Riskometer": (
                "The benchmark index for HDFC Large Cap Fund Direct Plan - Growth is NIFTY 100 Total Return Index (TRI). "
                "According to the SEBI riskometer, the risk level of this fund is categorized as Very High Risk. "
                "Investors must understand that their principal will be at very high risk. Source: https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth"
            ),
            "Taxation Rules": (
                "Mutual fund investments in HDFC Large Cap Fund are classified as equity-oriented for tax purposes. "
                "For units held for more than 12 months, Long-Term Capital Gains (LTCG) are taxed at 12.5% on gains exceeding Rs 1.25 Lakh per financial year (without indexation). "
                "For units held for 12 months or less, Short-Term Capital Gains (STCG) are taxed at 20%. Source: https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth"
            ),
            "Account Statement & Capital Gains Download": (
                "To download your mutual fund account statement or capital gains tax statement on Groww: "
                "Go to Profile > Reports > Capital Gains / P&L Statement or Mutual Fund Holding Statement. "
                "Alternatively, you can request an instant Consolidated Account Statement (CAS) via CAMS or KFintech or through HDFC Mutual Fund official website using your registered PAN and email ID. Source: https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth"
            )
        }
    },
    "hdfc-equity-fund-direct-growth": {
        "scheme_name": "HDFC Flexi Cap Fund Direct Plan - Growth",
        "category": "Flexi Cap",
        "amc": "HDFC Mutual Fund",
        "url": "https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth",
        "benchmark": "NIFTY 500 TRI",
        "riskometer": "Very High Risk",
        "nav_plan": "Direct Plan - Growth",
        "sections": {
            "Overview & Objective": (
                "HDFC Flexi Cap Fund Direct Plan - Growth (formerly known as HDFC Equity Fund) is an open-ended dynamic equity mutual fund scheme offered by HDFC Mutual Fund. "
                "The scheme invests across large-cap, mid-cap, and small-cap stocks without market cap restrictions to generate long-term capital appreciation. Source: https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth"
            ),
            "Expense Ratio & Charges": (
                "The expense ratio of HDFC Flexi Cap Fund Direct Plan - Growth is 0.77% (inclusive of GST). "
                "Expense ratio is deducted daily from the fund's Net Asset Value (NAV). "
                "A mandatory government stamp duty of 0.005% applies on every fresh purchase or SIP installment. Source: https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth"
            ),
            "Exit Load": (
                "The exit load for HDFC Flexi Cap Fund Direct Plan - Growth is 1.00% if redeemed or switched out within 1 year (365 days) from the date of allotment. "
                "No exit load (0%) is charged if units are redeemed after completion of 1 year. Source: https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth"
            ),
            "Minimum Investment & SIP": (
                "For HDFC Flexi Cap Fund Direct Plan - Growth, the minimum monthly SIP amount is Rs 100. "
                "The minimum lumpsum initial investment amount is Rs 100, and minimum additional purchase is Rs 100. Source: https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth"
            ),
            "Lock-in Period & Redemption": (
                "HDFC Flexi Cap Fund Direct Plan - Growth has no lock-in period. "
                "Units can be redeemed at the prevailing NAV on any working trading day subject to exit load if redeemed within 1 year. Source: https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth"
            ),
            "Benchmark & Riskometer": (
                "The benchmark for HDFC Flexi Cap Fund Direct Plan - Growth is NIFTY 500 Total Return Index (TRI). "
                "The riskometer level prescribed by SEBI is Very High Risk. Source: https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth"
            ),
            "Taxation Rules": (
                "As an equity mutual fund scheme, gains from HDFC Flexi Cap Fund held for over 12 months are treated as LTCG and taxed at 12.5% for gains above Rs 1.25 Lakh per financial year. "
                "Gains held for up to 12 months are treated as STCG and taxed at 20%. Source: https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth"
            ),
            "Account Statement & Capital Gains Download": (
                "Investors can download their statement for HDFC Flexi Cap Fund directly on Groww via Profile > Reports > Capital Gains Statement. "
                "Statements can also be downloaded from HDFC AMC online portal or via CAMS online using PAN and registered email. Source: https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth"
            )
        }
    },
    "hdfc-elss-tax-saver-fund-direct-plan-growth": {
        "scheme_name": "HDFC ELSS Tax saver Fund Direct Plan - Growth",
        "category": "ELSS (Tax Saver)",
        "amc": "HDFC Mutual Fund",
        "url": "https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth",
        "benchmark": "NIFTY 500 TRI",
        "riskometer": "Very High Risk",
        "nav_plan": "Direct Plan - Growth",
        "sections": {
            "Overview & Objective": (
                "HDFC ELSS Tax saver Fund Direct Plan - Growth is an open-ended Equity Linked Saving Scheme (ELSS) offered by HDFC Mutual Fund. "
                "The scheme aims to generate capital appreciation while providing income tax deduction benefits under Section 80C of the Income Tax Act. Source: https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth"
            ),
            "Expense Ratio & Charges": (
                "The expense ratio of HDFC ELSS Tax saver Fund Direct Plan - Growth is 1.11% (inclusive of GST). "
                "Stamp duty of 0.005% applies on unit creation. Source: https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth"
            ),
            "Exit Load": (
                "The exit load for HDFC ELSS Tax saver Fund Direct Plan - Growth is Nil (0%). "
                "Because of the statutory 3-year lock-in period, units cannot be redeemed before 3 years, and no exit load is levied when redeemed after the lock-in period expires. Source: https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth"
            ),
            "Mandatory Lock-in Period": (
                "HDFC ELSS Tax saver Fund has a mandatory statutory lock-in period of 3 years (36 months) from the date of allotment of units. "
                "For SIP investments, each individual monthly SIP installment is locked in for 3 years from its specific allotment date. Source: https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth"
            ),
            "Minimum Investment & SIP": (
                "For HDFC ELSS Tax saver Fund Direct Plan - Growth, the minimum monthly SIP amount is Rs 500. "
                "The minimum lumpsum investment amount is Rs 500. Investments can be made in multiples of Rs 500. Source: https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth"
            ),
            "Tax Benefits & Section 80C": (
                "Investments in HDFC ELSS Tax saver Fund qualify for tax deduction under Section 80C of the Income Tax Act up to a maximum limit of Rs 1.5 Lakh per financial year (under the Old Tax Regime). "
                "Under the New Tax Regime, Section 80C deductions are not available. Source: https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth"
            ),
            "Benchmark & Riskometer": (
                "The benchmark index for HDFC ELSS Tax saver Fund Direct Plan - Growth is NIFTY 500 Total Return Index (TRI). "
                "The scheme riskometer is rated as Very High Risk. Source: https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth"
            ),
            "Taxation on Redemption": (
                "After the 3-year lock-in period, redemption gains from HDFC ELSS Tax saver Fund are subject to Long-Term Capital Gains (LTCG) tax of 12.5% on gains exceeding Rs 1.25 Lakh in a financial year. Source: https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth"
            ),
            "Account Statement & Capital Gains Download": (
                "You can download the ELSS tax statement and capital gains report on Groww under Profile > Reports > Tax Saving / Capital Gains Statement. "
                "This statement serves as proof of investment for Section 80C tax deduction submission. Source: https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth"
            )
        }
    },
    "hdfc-small-cap-fund-direct-growth": {
        "scheme_name": "HDFC Small Cap Fund Direct Plan - Growth",
        "category": "Small Cap",
        "amc": "HDFC Mutual Fund",
        "url": "https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth",
        "benchmark": "BSE 250 SmallCap TRI",
        "riskometer": "Very High Risk",
        "nav_plan": "Direct Plan - Growth",
        "sections": {
            "Overview & Objective": (
                "HDFC Small Cap Fund Direct Plan - Growth is an open-ended equity mutual fund scheme predominantly investing in small-cap companies (companies ranked 251st and beyond in market capitalization). "
                "The fund objective is to generate long-term capital appreciation. Source: https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth"
            ),
            "Expense Ratio & Charges": (
                "The expense ratio of HDFC Small Cap Fund Direct Plan - Growth is 0.68% (inclusive of GST). "
                "This is the direct plan fee charged on the scheme assets. "
                "Government stamp duty of 0.005% is charged on mutual fund purchases. Source: https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth"
            ),
            "Exit Load": (
                "The exit load for HDFC Small Cap Fund Direct Plan - Growth is 1.00% if redeemed or switched out within 1 year (365 days) from allotment. "
                "If redeemed after 1 year, the exit load is Nil (0%). Source: https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth"
            ),
            "Minimum Investment & SIP": (
                "For HDFC Small Cap Fund Direct Plan - Growth, the minimum monthly SIP amount is Rs 100. "
                "The minimum lumpsum investment amount is Rs 100. (Note: AMC may periodically restrict or adjust lumpsum limits based on market conditions). Source: https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth"
            ),
            "Lock-in Period & Redemption": (
                "HDFC Small Cap Fund Direct Plan - Growth has Nil lock-in period. "
                "Investors can redeem their mutual fund units on any business day. Source: https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth"
            ),
            "Benchmark & Riskometer": (
                "The benchmark index is BSE 250 SmallCap Total Return Index (TRI). "
                "The scheme riskometer is rated as Very High Risk due to higher volatility inherent in small-cap equities. Source: https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth"
            ),
            "Taxation Rules": (
                "Equity taxation applies: Long-Term Capital Gains (LTCG) above Rs 1.25 Lakh per financial year are taxed at 12.5% if held for over 12 months. "
                "Short-Term Capital Gains (STCG) are taxed at 20% if held for 12 months or less. Source: https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth"
            ),
            "Account Statement & Capital Gains Download": (
                "To download your HDFC Small Cap statement, navigate to Groww > Profile > Reports > Capital Gains / Transaction History. "
                "Official statements can also be downloaded from CAMS online or HDFC Mutual Fund investor services portal. Source: https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth"
            )
        }
    },
    "hdfc-balanced-advantage-fund-direct-growth": {
        "scheme_name": "HDFC Balanced Advantage Fund Direct Plan - Growth",
        "category": "Balanced Advantage (Hybrid)",
        "amc": "HDFC Mutual Fund",
        "url": "https://groww.in/mutual-funds/hdfc-balanced-advantage-fund-direct-growth",
        "benchmark": "NIFTY 50 Hybrid Composite debt 50:50 Index",
        "riskometer": "Very High Risk",
        "nav_plan": "Direct Plan - Growth",
        "sections": {
            "Overview & Objective": (
                "HDFC Balanced Advantage Fund Direct Plan - Growth is an open-ended balanced advantage fund (dynamic asset allocation hybrid scheme). "
                "The scheme dynamically manages allocation between equity, arbitrage, and fixed-income debt securities depending on market valuations and macroeconomic indicators. Source: https://groww.in/mutual-funds/hdfc-balanced-advantage-fund-direct-growth"
            ),
            "Expense Ratio & Charges": (
                "The expense ratio of HDFC Balanced Advantage Fund Direct Plan - Growth is 0.73% (inclusive of GST). "
                "Stamp duty of 0.005% applies on every unit allocation. Source: https://groww.in/mutual-funds/hdfc-balanced-advantage-fund-direct-growth"
            ),
            "Exit Load Structure": (
                "For HDFC Balanced Advantage Fund Direct Plan - Growth: "
                "For redemption or switch-out up to 15% of units within 1 year from the date of allotment: Nil exit load. "
                "For redemption or switch-out in excess of 15% of units within 1 year from allotment: 1.00% exit load. "
                "For redemption or switch-out after 1 year from allotment: Nil (0%) exit load. Source: https://groww.in/mutual-funds/hdfc-balanced-advantage-fund-direct-growth"
            ),
            "Minimum Investment & SIP": (
                "For HDFC Balanced Advantage Fund Direct Plan - Growth, the minimum monthly SIP amount is Rs 100. "
                "The minimum lumpsum investment is Rs 100, and minimum additional purchase is Rs 100. Source: https://groww.in/mutual-funds/hdfc-balanced-advantage-fund-direct-growth"
            ),
            "Lock-in Period & Liquidity": (
                "HDFC Balanced Advantage Fund Direct Plan - Growth has no lock-in period. "
                "Units can be redeemed on any business day at the applicable NAV. Source: https://groww.in/mutual-funds/hdfc-balanced-advantage-fund-direct-growth"
            ),
            "Benchmark & Riskometer": (
                "The benchmark for HDFC Balanced Advantage Fund Direct Plan - Growth is NIFTY 50 Hybrid Composite debt 50:50 Index. "
                "The risk level on the SEBI riskometer is rated as Very High Risk. Source: https://groww.in/mutual-funds/hdfc-balanced-advantage-fund-direct-growth"
            ),
            "Taxation Treatment": (
                "HDFC Balanced Advantage Fund dynamically maintains gross equity exposure (including derivatives) of at least 65%, qualifying for equity taxation. "
                "Long-Term Capital Gains (LTCG) over Rs 1.25 Lakh per financial year are taxed at 12.5% for units held over 12 months. "
                "Short-Term Capital Gains (STCG) are taxed at 20% for units held for 12 months or less. Source: https://groww.in/mutual-funds/hdfc-balanced-advantage-fund-direct-growth"
            ),
            "Account Statement & Capital Gains Download": (
                "Download statements directly on Groww via Profile > Reports > Capital Gains Statement or Mutual Fund Orders. "
                "Alternatively, obtain your Consolidated Account Statement (CAS) via CAMS or the HDFC Mutual Fund investor website. Source: https://groww.in/mutual-funds/hdfc-balanced-advantage-fund-direct-growth"
            )
        }
    }
}


def save_raw_documents():
    """Saves raw normalized text documents for the 5 schemes."""
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    created_files = []

    for slug, doc in SCHEME_DOCUMENTATION.items():
        file_path = RAW_DATA_DIR / f"{slug}.txt"
        lines = [
            f"SCHEME NAME: {doc['scheme_name']}",
            f"CATEGORY: {doc['category']}",
            f"AMC: {doc['amc']}",
            f"BENCHMARK: {doc['benchmark']}",
            f"RISKOMETER: {doc['riskometer']}",
            f"PLAN: {doc['nav_plan']}",
            f"SOURCE URL: {doc['url']}",
            "=" * 70,
            ""
        ]
        for section_title, content in doc["sections"].items():
            lines.append(f"SECTION: {section_title}")
            lines.append(content)
            lines.append("")

        full_text = "\n".join(lines)
        file_path.write_text(full_text, encoding="utf-8")
        created_files.append(file_path)

    return created_files


if __name__ == "__main__":
    saved = save_raw_documents()
    print(f"Saved {len(saved)} raw scheme documents to {RAW_DATA_DIR}")
