"""
Hindustan Unilever Limited (HUL) - Executive Decision Intelligence Engine
Real-Time Counterfactual Scenario Simulation Engine
Project - 12: Executive Decision Intelligence

Simulates board-level 'What-If' trade-offs across operational levers and computes
recalibrated financial projections: Net Revenue, EBITDA Margin, Gross Margin, and FCF.
"""

import numpy as np

class ScenarioSimulator:
    def __init__(self):
        # Baseline annual enterprise benchmarks for HUL (approx ₹58,000 Cr revenue base)
        self.baseline = {
            "net_revenue_cr": 14650.0,      # Quarterly base revenue in ₹ Cr (~₹58,600 Cr annual)
            "ebitda_margin_pct": 23.40,     # Quarterly EBITDA Margin %
            "gross_margin_pct": 51.20,      # Quarterly Gross Margin %
            "free_cash_flow_cr": 2420.0,    # Quarterly Free Cash Flow in ₹ Cr
            # Baseline operational lever settings
            "focus_sku_stockout_rate": 6.5,
            "otif_secondary_pct": 89.2,
            "commodity_hedging_coverage_pct": 62.0,
            "distributor_wc_days": 21.8,
            "shikhar_app_order_share_pct": 34.0,
            "trade_scheme_discount_depth_pct": 7.8,
            "batch_changeover_latency_min": 68.0
        }

    def simulate(self, levers):
        """
        Calculates counterfactual financial outcomes given adjusted operational inputs.
        levers: dict of modified operational KPI values.
        """
        # Read user levers with fallbacks to baseline
        stockout = float(levers.get("focus_sku_stockout_rate", self.baseline["focus_sku_stockout_rate"]))
        otif = float(levers.get("otif_secondary_pct", self.baseline["otif_secondary_pct"]))
        hedging = float(levers.get("commodity_hedging_coverage_pct", self.baseline["commodity_hedging_coverage_pct"]))
        dist_wc = float(levers.get("distributor_wc_days", self.baseline["distributor_wc_days"]))
        shikhar = float(levers.get("shikhar_app_order_share_pct", self.baseline["shikhar_app_order_share_pct"]))
        discount = float(levers.get("trade_scheme_discount_depth_pct", self.baseline["trade_scheme_discount_depth_pct"]))
        changeover = float(levers.get("batch_changeover_latency_min", self.baseline["batch_changeover_latency_min"]))

        # 1. Delta computations
        delta_stockout = stockout - self.baseline["focus_sku_stockout_rate"]
        delta_otif = otif - self.baseline["otif_secondary_pct"]
        delta_hedging = hedging - self.baseline["commodity_hedging_coverage_pct"]
        delta_wc = dist_wc - self.baseline["distributor_wc_days"]
        delta_shikhar = shikhar - self.baseline["shikhar_app_order_share_pct"]
        delta_discount = discount - self.baseline["trade_scheme_discount_depth_pct"]
        delta_changeover = changeover - self.baseline["batch_changeover_latency_min"]

        # 2. Revenue Impact (₹ Cr):
        # Stockouts directly destroy revenue (-₹74.5 Cr per 1% stockout)
        # OTIF brings revenue gains (+₹38.6 Cr per 1%)
        # Shikhar adoption accelerates replenishment (+₹5.2 Cr per 1%)
        # Distributor credit stretch delays ordering (-₹18.0 Cr per day above baseline)
        rev_delta = (
            (-delta_stockout * 74.5) +
            (delta_otif * 38.6) +
            (delta_shikhar * 5.2) -
            (max(0, delta_wc) * 18.0) +
            (delta_discount * 12.0)
        )
        projected_rev = max(11000.0, self.baseline["net_revenue_cr"] + rev_delta)

        # 3. Gross Margin Impact (%):
        # Hedging shields COGS (+18.5 bps per 10% hedging)
        # Discounting erodes gross margin directly (-85 bps per 1% discount)
        # Stockouts in high margin SKUs erode mix (-42 bps per 1% stockout)
        gross_delta = (
            (delta_hedging * 0.0185) -
            (delta_discount * 0.85) -
            (delta_stockout * 0.42)
        )
        projected_gross = np.clip(self.baseline["gross_margin_pct"] + gross_delta, 42.0, 58.0)

        # 4. EBITDA Margin Impact (bps & %):
        # 1% stockout = -48.2 bps
        # 1% OTIF = +22.4 bps
        # 1% Shikhar = +2.5 bps
        # 1 day distributor credit above 22 = -31.0 bps
        # 1% discount = -42.6 bps
        # 10 min changeover = -16.4 bps
        ebitda_bps_delta = (
            (-delta_stockout * 48.2) +
            (delta_otif * 22.4) +
            (delta_shikhar * 2.5) -
            (max(0, delta_wc) * 31.0) -
            (delta_discount * 42.6) -
            (delta_changeover * 1.64) +
            (delta_hedging * 1.85)
        )
        projected_ebitda_pct = np.clip(self.baseline["ebitda_margin_pct"] + (ebitda_bps_delta / 100.0), 14.0, 31.0)
        
        # 5. EBITDA in ₹ Cr
        baseline_ebitda_cr = self.baseline["net_revenue_cr"] * (self.baseline["ebitda_margin_pct"] / 100.0)
        projected_ebitda_cr = projected_rev * (projected_ebitda_pct / 100.0)
        ebitda_cr_delta = projected_ebitda_cr - baseline_ebitda_cr

        # 6. Free Cash Flow Impact (₹ Cr):
        fcf_delta = (ebitda_cr_delta * 0.72) - (max(0, delta_wc) * 24.0) + (delta_shikhar * 3.5)
        projected_fcf = self.baseline["free_cash_flow_cr"] + fcf_delta

        # Assessment generation
        if ebitda_cr_delta > 120.0:
            strategic_tone = "SIGNIFICANT VALUE ACCRETION"
            summary_memo = f"Aggressive operational posture yields +₹{ebitda_cr_delta:.1f} Cr quarterly EBITDA (+{ebitda_bps_delta:+.0f} bps). Recovering High-Margin SKU on-shelf availability and unlocking distributor liquidity drives sustainable cash flow expansion."
        elif ebitda_cr_delta < -80.0:
            strategic_tone = "MARGIN COMPRESSION RISK"
            summary_memo = f"Simulated operational friction leads to severe financial erosion: ₹{abs(ebitda_cr_delta):.1f} Cr EBITDA drag ({ebitda_bps_delta:+.0f} bps). Root causes stem from distributor credit drag and SKU stockout substitution."
        else:
            strategic_tone = "NEUTRAL / BALANCED EFFICIENCY"
            summary_memo = f"Modest net impact: EBITDA shifts by {ebitda_bps_delta:+.0f} bps (₹{ebitda_cr_delta:+.1f} Cr). Incremental volume gains are offset by operational friction or discounting."

        return {
            "baseline": self.baseline,
            "projected": {
                "net_revenue_cr": round(projected_rev, 1),
                "ebitda_margin_pct": round(projected_ebitda_pct, 2),
                "ebitda_cr": round(projected_ebitda_cr, 1),
                "gross_margin_pct": round(projected_gross, 2),
                "free_cash_flow_cr": round(projected_fcf, 1)
            },
            "deltas": {
                "revenue_cr": round(rev_delta, 1),
                "ebitda_bps": round(ebitda_bps_delta, 0),
                "ebitda_cr": round(ebitda_cr_delta, 1),
                "gross_margin_pct": round(gross_delta, 2),
                "free_cash_flow_cr": round(fcf_delta, 1)
            },
            "strategic_tone": strategic_tone,
            "summary_memo": summary_memo,
            "inputs": {
                "focus_sku_stockout_rate": stockout,
                "otif_secondary_pct": otif,
                "commodity_hedging_coverage_pct": hedging,
                "distributor_wc_days": dist_wc,
                "shikhar_app_order_share_pct": shikhar,
                "trade_scheme_discount_depth_pct": discount,
                "batch_changeover_latency_min": changeover
            }
        }

