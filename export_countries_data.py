"""
Script to extract country data from REST Countries API
and save it in CSV and JSON formats for visualization.
"""

import requests
import json
import csv
from datetime import datetime
import time


def fetch_countries_by_region(region):
    """Fetch countries for a specific region"""
    url = f"https://restcountries.com/v3.1/region/{region}"
    response = requests.get(url, timeout=30)
    if response.ok:
        return response.json()
    return []


def fetch_all_countries():
    """Fetch all countries from REST Countries API v3.1"""
    print("Fetching data from REST Countries API...")
    
    # Try the /all endpoint first
    url = "https://restcountries.com/v3.1/all"
    try:
        response = requests.get(url, timeout=30)
        if response.ok:
            countries = response.json()
            print(f"Retrieved {len(countries)} countries")
            return countries
    except Exception as e:
        print(f"Direct fetch failed: {e}")
    
    # Fallback: fetch by regions
    print("Falling back to region-by-region fetch...")
    regions = ['africa', 'americas', 'asia', 'europe', 'oceania']
    all_countries = []
    
    for region in regions:
        print(f"  Fetching {region}...")
        try:
            countries = fetch_countries_by_region(region)
            all_countries.extend(countries)
            print(f"    Got {len(countries)} countries")
            time.sleep(0.5)  # Be nice to the API
        except Exception as e:
            print(f"    Error: {e}")
    
    print(f"Total retrieved: {len(all_countries)} countries")
    return all_countries


def transform_country_data(countries):
    """
    Transform raw API data into a flat, visualization-friendly format.
    Returns a list of dictionaries with key fields.
    """
    transformed = []
    
    for country in countries:
        try:
            # Extract languages as comma-separated string
            languages = country.get('languages', {})
            languages_str = ', '.join(languages.values()) if languages else ''
            
            # Extract currencies
            currencies = country.get('currencies', {})
            currency_codes = ', '.join(currencies.keys()) if currencies else ''
            currency_names = ', '.join([c.get('name', '') for c in currencies.values()]) if currencies else ''
            
            # Extract capitals
            capitals = country.get('capital', [])
            capital_str = ', '.join(capitals) if capitals else ''
            
            # Extract borders
            borders = country.get('borders', [])
            borders_str = ', '.join(borders) if borders else ''
            
            # Extract timezones
            timezones = country.get('timezones', [])
            timezones_str = ', '.join(timezones) if timezones else ''
            
            # Extract coordinates
            latlng = country.get('latlng', [None, None])
            latitude = latlng[0] if len(latlng) > 0 else None
            longitude = latlng[1] if len(latlng) > 1 else None
            
            # Extract calling codes
            idd = country.get('idd', {})
            root = idd.get('root', '')
            suffixes = idd.get('suffixes', [])
            calling_code = f"{root}{suffixes[0]}" if root and suffixes else ''
            
            # Calculate population density
            area = country.get('area', 0)
            population = country.get('population', 0)
            pop_density = round(population / area, 2) if area and area > 0 else None
            
            record = {
                'name_common': country.get('name', {}).get('common', ''),
                'name_official': country.get('name', {}).get('official', ''),
                'cca2': country.get('cca2', ''),
                'cca3': country.get('cca3', ''),
                'capital': capital_str,
                'region': country.get('region', ''),
                'subregion': country.get('subregion', ''),
                'population': population,
                'area_km2': area,
                'population_density': pop_density,
                'landlocked': country.get('landlocked', False),
                'independent': country.get('independent', False),
                'un_member': country.get('unMember', False),
                'latitude': latitude,
                'longitude': longitude,
                'languages': languages_str,
                'currencies': currency_codes,
                'currency_names': currency_names,
                'calling_code': calling_code,
                'timezones': timezones_str,
                'borders': borders_str,
                'num_borders': len(borders),
                'flag_emoji': country.get('flag', ''),
                'flag_png': country.get('flags', {}).get('png', ''),
                'flag_svg': country.get('flags', {}).get('svg', ''),
                'continent': ', '.join(country.get('continents', [])),
                'start_of_week': country.get('startOfWeek', ''),
                'driving_side': country.get('car', {}).get('side', ''),
                'gini_index': list(country.get('gini', {}).values())[0] if country.get('gini') else None,
            }
            transformed.append(record)
        except Exception as e:
            print(f"Error processing country: {e}")
            continue
    
    # Sort by population descending
    transformed.sort(key=lambda x: x['population'] or 0, reverse=True)
    return transformed


def save_to_json(data, filename):
    """Save data to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved JSON to: {filename}")


def save_to_csv(data, filename):
    """Save data to CSV file"""
    if not data:
        print("No data to save")
        return
    
    fieldnames = data[0].keys()
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Saved CSV to: {filename}")


def create_summary_stats(data):
    """Create summary statistics for the data"""
    stats = {
        'total_countries': len(data),
        'total_population': sum(c['population'] or 0 for c in data),
        'total_area_km2': sum(c['area_km2'] or 0 for c in data),
        'regions': {},
        'top_10_by_population': [],
        'top_10_by_area': [],
    }
    
    # Count by region
    for country in data:
        region = country['region'] or 'Unknown'
        if region not in stats['regions']:
            stats['regions'][region] = {'count': 0, 'population': 0}
        stats['regions'][region]['count'] += 1
        stats['regions'][region]['population'] += country['population'] or 0
    
    # Top 10 by population
    sorted_by_pop = sorted(data, key=lambda x: x['population'] or 0, reverse=True)[:10]
    stats['top_10_by_population'] = [{'name': c['name_common'], 'population': c['population']} for c in sorted_by_pop]
    
    # Top 10 by area
    sorted_by_area = sorted(data, key=lambda x: x['area_km2'] or 0, reverse=True)[:10]
    stats['top_10_by_area'] = [{'name': c['name_common'], 'area_km2': c['area_km2']} for c in sorted_by_area]
    
    return stats


def main():
    print("=" * 60)
    print("REST Countries Data Exporter")
    print("=" * 60)
    
    # Fetch data
    raw_data = fetch_all_countries()
    
    if not raw_data:
        print("ERROR: Could not fetch any country data!")
        return
    
    # Transform data
    print("\nTransforming data for visualization...")
    transformed_data = transform_country_data(raw_data)
    
    # Generate filenames with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save transformed data
    json_filename = f"countries_data.json"
    save_to_json(transformed_data, json_filename)
    
    csv_filename = f"countries_data.csv"
    save_to_csv(transformed_data, csv_filename)
    
    # Save raw API response
    raw_json_filename = f"countries_raw.json"
    save_to_json(raw_data, raw_json_filename)
    
    # Create and save summary stats
    stats = create_summary_stats(transformed_data)
    stats_filename = f"countries_summary.json"
    save_to_json(stats, stats_filename)
    
    print("\n" + "=" * 60)
    print("Export Complete!")
    print("=" * 60)
    print(f"\nFiles created:")
    print(f"  1. {csv_filename} - Flat CSV for spreadsheets/Tableau/Power BI")
    print(f"  2. {json_filename} - Transformed JSON for D3.js/Chart.js visualization")
    print(f"  3. {raw_json_filename} - Raw API response (full detail)")
    print(f"  4. {stats_filename} - Summary statistics")
    print(f"\nTotal countries exported: {len(transformed_data)}")
    
    # Print summary
    print("\n--- Summary Statistics ---")
    print(f"Total World Population: {stats['total_population']:,}")
    print(f"Total Land Area: {stats['total_area_km2']:,.0f} km²")
    print("\nCountries by Region:")
    for region, data in sorted(stats['regions'].items(), key=lambda x: x[1]['population'], reverse=True):
        print(f"  {region}: {data['count']} countries, {data['population']:,} population")
    
    print("\nTop 5 by Population:")
    for i, c in enumerate(stats['top_10_by_population'][:5], 1):
        print(f"  {i}. {c['name']}: {c['population']:,}")


if __name__ == "__main__":
    main()
