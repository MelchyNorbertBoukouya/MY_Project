from django.shortcuts import render
from .services import WorldExplorerClient

def index(request):
    return render(request, 'explorer/index.html')

def search(request):
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'name')
    client = WorldExplorerClient()
    results = []
    
    if query:
        if search_type == 'name':
            results = client.get_country_by_name(query)
        elif search_type == 'code':
            results = client.get_country_by_code(query)
            # API might return a single dict for code search, wrap in list if so
            if isinstance(results, dict):
                results = [results]
        elif search_type == 'currency':
            results = client.get_country_by_currency(query)
        elif search_type == 'lang':
            results = client.get_country_by_language(query)
        elif search_type == 'capital':
            results = client.get_country_by_capital(query)
        elif search_type == 'region':
            results = client.get_country_by_region(query)
        elif search_type == 'subregion':
            results = client.get_country_by_subregion(query)
        elif search_type == 'city':
            results = client.get_city_by_name(query)
            
    context = {
        'results': results,
        'query': query,
        'search_type': search_type
    }
    return render(request, 'explorer/results.html', context)

def country_detail(request, code):
    client = WorldExplorerClient()
    country = client.get_country_by_code(code)
    # Ensure we get the dict if it's wrapped in list (sometimes happen with alpha codes if loose match)
    # But usually alpha/code returns one dict.
    if isinstance(country, list) and len(country) > 0:
        country = country[0]
        
    context = {'country': country}
    return render(request, 'explorer/country_detail.html', context)
