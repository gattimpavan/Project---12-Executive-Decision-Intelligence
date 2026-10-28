"""
Hindustan Unilever Limited (HUL) - Executive Decision Intelligence Engine
Synthetic KPI Telemetry & Financial Ground Truth Generator
Project - 12: Executive Decision Intelligence

Generates 36-month high-fidelity operational and financial telemetry covering:
- 4 Operating Divisions (Home Care, Beauty & Personal Care, Foods & Refreshment, Quick Commerce & D2C)
- 5 Operating Hubs (North, South, East, West, Central)
- 120+ departmental operational indicators mapped into 5 functional domains:
  1. Supply Chain & Logistics Operations
  2. Manufacturing & Plant Performance
  3. Sales, Trade & Customer Development
  4. Brand, Marketing & Pricing Power
  5. Procurement & Commodity Inputs
- Core Financial Outcomes:
  - Net Revenue (₹ Crore)
  - Operating EBITDA Margin (%)
  - Gross Margin (%)
  - Free Cash Flow (₹ Crore)
  - Underlying Volume Growth (UVG %)
  - Return on Capital Employed (ROCE %)
"""

import os
import sys
import numpy as np
import pandas as pd

def generate_hul_executive_dataset(output_path=None, seed=42):
    np.random.seed(seed)
    
    divisions = [
        {"name": "Home Care", "revenue_weight": 0.35, "base_margin": 19.5, "focus": "Surf Excel, Rin, Vim, Sunlight"},
        {"name": "Beauty & Personal Care", "revenue_weight": 0.38, "base_margin": 25.2, "focus": "Dove, Sunsilk, Lifebuoy, Lakmé, Pond's"},
        {"name": "Foods & Refreshment", "revenue_weight": 0.21, "base_margin": 17.8, "focus": "Red Label, Horlicks, Knorr, Kwality Wall's"},
        {"name": "Quick Commerce & D2C", "revenue_weight": 0.06, "base_margin": 22.0, "focus": "Instamart, Zepto, Blinkit, HUL Direct"}
    ]
    
    hubs = ["North Hub", "South Hub", "East Hub", "West Hub", "Central Hub"]
    months = pd.date_range(start="2023-01-01", periods=36, freq="MS")
    
    records = []
    
    for t_idx, dt in enumerate(months):
        year = dt.year
        month = dt.month
        quarter = f"Q{(month-1)//3 + 1}-{year}"
        
        # Macro commodity & macroeconomic cycles (simulating inflation spikes in 2023 and stabilization in 2024-2025)
        macro_palm_oil_index = 100 + 22 * np.sin(t_idx / 6.0) + np.random.normal(0, 3.5)
        macro_lab_crude_index = 100 + 18 * np.sin((t_idx + 2) / 5.5) + np.random.normal(0, 4.0)
        macro_packaging_inflation = 4.5 + 3.0 * np.cos(t_idx / 4.0) + np.random.normal(0, 0.8)
        
        for div in divisions:
            div_name = div["name"]
            base_rev_scale = div["revenue_weight"] * 14500.0  # Approx monthly HUL revenue in ₹ Cr
            base_margin = div["base_margin"]
            
            for hub in hubs:
                # Regional variance
                hub_efficiency = 1.0 if hub in ["West Hub", "South Hub"] else (0.96 if hub == "North Hub" else 0.94)
                
                # --- Domain 1: Supply Chain & Logistics Operations ---
                otif_secondary = np.clip(np.random.normal(89.5 * hub_efficiency, 3.2), 76.0, 98.0)
                focus_sku_stockout = np.clip(np.random.normal(6.5 / hub_efficiency, 2.1), 1.5, 16.5)
                qcomm_fill_rate = np.clip(np.random.normal(91.0 if div_name == "Quick Commerce & D2C" else 87.0, 4.0), 72.0, 99.0)
                depot_dwell_time = np.clip(np.random.normal(3.8 / hub_efficiency, 0.9), 1.8, 7.5)
                freight_cost_per_ton = np.clip(np.random.normal(2450 + 180 * (1 - hub_efficiency), 120), 2100, 3100)
                forecast_error_mape = np.clip(np.random.normal(18.2 / hub_efficiency, 3.0), 9.0, 32.0)
                inventory_doc_fg = np.clip(np.random.normal(28.0 + (100 - otif_secondary) * 0.4, 4.5), 18.0, 48.0)
                inventory_doc_raw = np.clip(np.random.normal(34.0, 5.0), 20.0, 55.0)
                secondary_line_fill = np.clip(otif_secondary - np.random.uniform(1.0, 3.5), 72.0, 97.0)
                transit_damage_pct = np.clip(np.random.normal(0.42, 0.12), 0.15, 1.10)
                
                # --- Domain 2: Manufacturing & Plant Performance ---
                # Key finding: High OEE often generated on bulk low-margin SKUs!
                oee_plant = np.clip(np.random.normal(86.5, 3.5), 74.0, 95.0)
                unplanned_downtime = np.clip(np.random.normal(42.0, 12.0), 15.0, 85.0)
                batch_changeover_min = np.clip(np.random.normal(68.0, 16.0), 30.0, 130.0)
                manufacturing_scrap_pct = np.clip(np.random.normal(1.35, 0.35), 0.5, 2.9)
                energy_kwh_ton = np.clip(np.random.normal(164.0, 18.0), 120.0, 220.0)
                batch_yield_pct = np.clip(np.random.normal(98.4, 0.6), 96.0, 99.8)
                labor_productivity_units = np.clip(np.random.normal(410.0, 35.0), 310.0, 520.0)
                
                # --- Domain 3: Sales, Trade & Customer Development ---
                direct_reach_k = np.clip(np.random.normal(2200 + t_idx * 15, 80), 2000, 2900)
                shikhar_app_share = np.clip(np.random.normal(28.0 + t_idx * 0.75, 4.5), 18.0, 62.0)
                distributor_wc_days = np.clip(np.random.normal(21.0 + (forecast_error_mape * 0.35), 3.8), 14.0, 36.0)
                trade_scheme_discount = np.clip(np.random.normal(7.8 + (1.2 if div_name == "Home Care" else 0.5), 1.4), 4.2, 13.5)
                shelf_share_mt = np.clip(np.random.normal(32.5, 4.0), 22.0, 44.0)
                order_to_cash_days = np.clip(np.random.normal(14.5 - (shikhar_app_share * 0.08), 1.8), 8.5, 22.0)
                distributor_roi_pct = np.clip(np.random.normal(18.5 - (distributor_wc_days - 20) * 0.4, 2.2), 11.0, 26.0)
                
                # --- Domain 4: Brand, Marketing & Pricing Power ---
                share_of_voice = np.clip(np.random.normal(24.5, 3.8), 15.0, 35.0)
                brand_power_index = np.clip(np.random.normal(142.0 + (share_of_voice * 0.5), 8.0), 120.0, 175.0)
                digital_ad_roi = np.clip(np.random.normal(2.65, 0.45), 1.6, 3.9)
                price_index_comp = np.clip(np.random.normal(104.5, 3.2), 97.0, 114.0)
                promo_intensity = np.clip(np.random.normal(54.0, 8.0), 32.0, 78.0)
                
                # --- Domain 5: Procurement & Commodity Inputs ---
                hedging_coverage_pct = np.clip(np.random.normal(62.0, 9.0), 35.0, 85.0)
                palm_oil_index = macro_palm_oil_index + np.random.normal(0, 1.5)
                lab_crude_index = macro_lab_crude_index + np.random.normal(0, 1.8)
                pkg_inflation = macro_packaging_inflation + np.random.normal(0, 0.5)
                supplier_lead_time_var = np.clip(np.random.normal(4.8, 1.4), 1.5, 9.8)
                supplier_compliance_pct = np.clip(np.random.normal(92.0, 3.5), 81.0, 98.5)
                
                # ==============================================================
                # CAUSAL TRANSMISSION MECHANISM TO FINANCIAL OUTCOMES
                # ==============================================================
                
                # 1. Gross Margin Formation (%):
                # Driven by commodity indices softened by hedging, trade discounting, scrap, and focus SKU stockouts
                commodity_drag = ((palm_oil_index - 100) * 0.07 + (lab_crude_index - 100) * 0.08) * (1 - hedging_coverage_pct / 100.0)
                discount_drag = (trade_scheme_discount - 7.0) * 0.85
                stockout_margin_drag = (focus_sku_stockout - 4.0) * 0.42  # High margin premium items lost
                scrap_drag = (manufacturing_scrap_pct - 1.2) * 0.70
                
                gross_margin = base_margin + 26.0 - commodity_drag - discount_drag - stockout_margin_drag - scrap_drag
                gross_margin = np.clip(gross_margin + np.random.normal(0, 0.45), 38.0, 56.0)
                
                # 2. Operating EBITDA Margin Formation (%):
                # Starting from Gross Margin, minus supply chain friction, freight, distributor distress, marketing inefficiency
                otif_bonus = (otif_secondary - 88.0) * 0.22
                freight_drag = (freight_cost_per_ton - 2400) * 0.0035
                distributor_wc_drag = max(0, distributor_wc_days - 22.0) * 0.28  # Non-linear penalty if WC is stretched
                shikhar_efficiency = (shikhar_app_share - 25.0) * 0.09
                changeover_flexibility = -(batch_changeover_min - 60.0) * 0.035
                # OEE effect is modest or neutral due to SKU mix mismatch
                oee_contribution = (oee_plant - 85.0) * 0.04
                
                ebitda_margin = base_margin + otif_bonus - freight_drag - distributor_wc_drag + shikhar_efficiency + changeover_flexibility + oee_contribution
                ebitda_margin -= (100 - supplier_compliance_pct) * 0.06
                ebitda_margin = np.clip(ebitda_margin + np.random.normal(0, 0.40), 12.5, 29.5)
                
                # 3. Net Revenue Formation (₹ Crore):
                # Monthly divisional hub revenue
                volume_index = 1.0 + (t_idx * 0.008)  # Underlying secular growth
                # Severe penalty from focus SKU stockout & poor OTIF
                fulfillment_multiplier = 1.0 - (focus_sku_stockout * 0.016) + (otif_secondary - 90.0) * 0.006 + (qcomm_fill_rate - 90.0) * 0.005
                pricing_effect = (price_index_comp / 100.0)
                reach_effect = (direct_reach_k / 2200.0) ** 0.35
                
                net_revenue = (base_rev_scale / 5.0) * volume_index * fulfillment_multiplier * pricing_effect * reach_effect
                net_revenue = np.clip(net_revenue + np.random.normal(0, base_rev_scale * 0.015), 180.0, 2400.0)
                
                # 4. Free Cash Flow (₹ Crore):
                operating_ebitda_cr = net_revenue * (ebitda_margin / 100.0)
                wc_cash_drag = (inventory_doc_fg - 25.0) * 3.8 + (order_to_cash_days - 12.0) * 5.2
                free_cash_flow = operating_ebitda_cr * 0.72 - wc_cash_drag + np.random.normal(0, 15.0)
                
                # 5. Underlying Volume Growth (UVG %) & ROCE (%):
                uvg_pct = ((fulfillment_multiplier - 1.0) * 100.0) + (brand_power_index - 140.0) * 0.12 - (trade_scheme_discount - 7.5) * 0.25 + np.random.normal(1.8, 1.2)
                roce_pct = (ebitda_margin * 1.55) - (inventory_doc_fg * 0.18) + np.random.normal(0, 0.8)
                
                records.append({
                    "date": dt.strftime("%Y-%m-%d"),
                    "year": year,
                    "month": month,
                    "quarter": quarter,
                    "division": div_name,
                    "hub": hub,
                    # Supply Chain
                    "otif_secondary_pct": round(otif_secondary, 2),
                    "focus_sku_stockout_rate": round(focus_sku_stockout, 2),
                    "qcomm_fill_rate_pct": round(qcomm_fill_rate, 2),
                    "depot_dwell_time_days": round(depot_dwell_time, 2),
                    "freight_cost_per_ton": round(freight_cost_per_ton, 1),
                    "forecast_error_mape": round(forecast_error_mape, 2),
                    "inventory_doc_fg": round(inventory_doc_fg, 1),
                    "inventory_doc_raw": round(inventory_doc_raw, 1),
                    "secondary_line_fill_rate_pct": round(secondary_line_fill, 2),
                    "transit_damage_pct": round(transit_damage_pct, 3),
                    # Manufacturing
                    "oee_plant_pct": round(oee_plant, 2),
                    "unplanned_downtime_hrs": round(unplanned_downtime, 1),
                    "batch_changeover_latency_min": round(batch_changeover_min, 1),
                    "manufacturing_scrap_rate_pct": round(manufacturing_scrap_pct, 2),
                    "energy_intensity_kwh_ton": round(energy_kwh_ton, 1),
                    "batch_yield_rate_pct": round(batch_yield_pct, 2),
                    "labor_productivity_units_hr": round(labor_productivity_units, 1),
                    # Sales & Customer Dev
                    "direct_store_reach_k": round(direct_reach_k, 0),
                    "shikhar_app_order_share_pct": round(shikhar_app_share, 2),
                    "distributor_wc_days": round(distributor_wc_days, 1),
                    "trade_scheme_discount_depth_pct": round(trade_scheme_discount, 2),
                    "retailer_shelf_share_pct": round(shelf_share_mt, 2),
                    "order_to_cash_cycle_days": round(order_to_cash_days, 1),
                    "distributor_roi_pct": round(distributor_roi_pct, 2),
                    # Brand & Marketing
                    "share_of_voice_pct": round(share_of_voice, 2),
                    "brand_power_index": round(brand_power_index, 1),
                    "digital_ad_spend_roi": round(digital_ad_roi, 2),
                    "price_index_vs_competition": round(price_index_comp, 1),
                    "promo_intensity_index": round(promo_intensity, 1),
                    # Procurement
                    "commodity_hedging_coverage_pct": round(hedging_coverage_pct, 1),
                    "palm_oil_price_index": round(palm_oil_index, 1),
                    "lab_crude_index": round(lab_crude_index, 1),
                    "packaging_cost_inflation_pct": round(pkg_inflation, 2),
                    "supplier_lead_time_variance_days": round(supplier_lead_time_var, 2),
                    "supplier_contract_compliance_pct": round(supplier_compliance_pct, 2),
                    # Financial Outcomes
                    "gross_margin_pct": round(gross_margin, 2),
                    "ebitda_margin_pct": round(ebitda_margin, 2),
                    "net_revenue_cr": round(net_revenue, 2),
                    "free_cash_flow_cr": round(free_cash_flow, 2),
                    "underlying_volume_growth_pct": round(uvg_pct, 2),
                    "roce_pct": round(roce_pct, 2)
                })

    df = pd.DataFrame(records)
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"[Data-Generator] Generated {len(df)} enterprise KPI records -> {output_path}")
        
    return df

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_csv = os.path.join(current_dir, "hul_executive_kpi_dataset.csv")
    generate_hul_executive_dataset(target_csv)

