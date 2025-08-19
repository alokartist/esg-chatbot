# scripts/normalize_esg.py
import sqlite3
import pandas as pd
import sys

def normalize(db_path):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM esg_records", conn)

    # Adjust column names below to match your CSV
    # Example assumptions:
    # df columns: company, company_country, plant, location, year, co2_emissions_tons, water_consumption_m3, energy_mwh, renewable_energy_pct, employee_count, lti
    # If your CSV uses different names, update the strings.

    # Companies
    companies = df[['company']].drop_duplicates().reset_index(drop=True)
    companies['company_id'] = companies.index + 1
    companies.to_sql('companies', conn, if_exists='replace', index=False)

    # Plants
    plants_df = df[['company', 'plant', 'location']].drop_duplicates().reset_index(drop=True)
    # map company -> id
    comp_map = dict(zip(companies['company'], companies['company_id']))
    plants_df['company_id'] = plants_df['company'].map(comp_map)
    plants_df['plant_id'] = plants_df.index + 1
    plants_df.to_sql('plants', conn, if_exists='replace', index=False)

    # Reports
    # Build a report row per original row but map plant/company -> ids
    df2 = df.copy()
    # find plant_id
    plant_map = dict(zip(plants_df['plant'], plants_df['plant_id']))
    df2['plant_id'] = df2['plant'].map(plant_map)
    # Keep columns relevant to reports
    report_cols = ['plant_id', 'year']
    # drop duplicates of (plant_id, year)
    reports = df2[report_cols].drop_duplicates().reset_index(drop=True)
    reports['report_id'] = reports.index + 1
    reports.to_sql('reports', conn, if_exists='replace', index=False)

    # Emissions
    # map report_id
    # join df2 with reports to get report_id
    merged = pd.merge(df2, reports, on=['plant_id', 'year'], how='left')
    emissions_cols = ['report_id', 'co2_emissions_tons']
    if 'co2_emissions_tons' in merged.columns:
        emissions = merged[emissions_cols].dropna(subset=['co2_emissions_tons']).copy()
        emissions.to_sql('emissions', conn, if_exists='replace', index=False)
    else:
        print("co2_emissions_tons column not found — skip emissions creation")

    # Resources
    resources_cols = ['report_id']
    for c in ['water_consumption_m3', 'energy_mwh', 'renewable_energy_pct']:
        if c in merged.columns:
            resources_cols.append(c)
    if len(resources_cols) > 1:
        resources = merged[resources_cols].drop_duplicates()
        resources.to_sql('resources', conn, if_exists='replace', index=False)
    else:
        print("No resource columns found; check CSV headers.")

    conn.close()
    print("Normalization complete. Tables created: companies, plants, reports, emissions, resources (if available).")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python normalize_esg.py <db_path>")
        sys.exit(1)
    normalize(sys.argv[1])
