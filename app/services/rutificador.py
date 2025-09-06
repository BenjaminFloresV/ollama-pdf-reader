




from datetime import datetime, timezone
from bs4 import BeautifulSoup
from app.utils.toolbelt import normalize_text
from app.core.config import DEFAULT_HTTP_TIMEOUT, DEFAULT_HTTP_HEADERS
from rnet import Client, Proxy


_client = Client(timeout=DEFAULT_HTTP_TIMEOUT)


async def _parse_response(response_text: str) -> dict:
    
    parsed_data = []
    try:
        soup = BeautifulSoup(response_text, 'html.parser')
        headers = [normalize_text(header.text.lower()) for header in soup.find('thead').find_all('th')]    
        
        tbody = soup.find('tbody')
        rows = tbody.find_all('tr')

    
        for row in rows:
            columns = row.find_all('td')
            
            parsed_row = {}
            for index, column in enumerate(columns):
                parsed_row[headers[index]] = column.text
            parsed_row['extraction_datetime'] =  str(datetime.now(timezone.utc).isoformat())
            parsed_row['extraction_date'] = datetime.now().date().strftime('%d-%m-%Y')
            parsed_data.append(parsed_row)
    
    except Exception as e:
        print(f'Error parsing response: {e}')
        return []
    
    return parsed_data


async def _search_people_by_name(name: str, should_use_proxy: bool = False, proxy_url: str = ''):
    url = "https://www.nombrerutyfirma.com/nombre"    

    try:
        if should_use_proxy:
            response = await _client.post(url=url, form=[("term", name)], proxy=Proxy.all(
                url=proxy_url,
                custom_http_headers=DEFAULT_HTTP_HEADERS
            ))
        else:
            response = await _client.post(url=url, form=[("term", name)], headers=DEFAULT_HTTP_HEADERS)
        status_code = int(str(response.status_code))
        if status_code != 200:
            raise Exception('Failed request: {}'.format(status_code))

        return await response.text(), status_code
    except Exception as e:
        print(f'Error searching for people by name: {e}')
        return '', 0


async def _search_people_by_rut(rut: str, should_use_proxy: bool = False, proxy_url: str = ''):

    url = "https://www.nombrerutyfirma.com/rut"    

    try:
        if should_use_proxy:
            response = await _client.post(url=url, form=[("term", rut)], proxy=Proxy.all(
                url=proxy_url,
                custom_http_headers=DEFAULT_HTTP_HEADERS
            ))
        else:
            response = await _client.post(url=url, form=[("term", rut)], headers=DEFAULT_HTTP_HEADERS)
    
        status_code = int(str(response.status_code))
        if status_code != 200:
            raise Exception('Failed request: {}'.format(status_code))

        return await response.text(), status_code

    except Exception as e:
        print(f'Error searching for people by rut: {e}')
        return '', 0


async def search_people(search_term: str, search_by: str = 'rut'):
    
    if search_by.lower() == 'rut':
        result, _ = await _search_people_by_rut(search_term)
    elif search_by.lower() == 'name':
        result, _ = await _search_people_by_name(search_term)

    return await _parse_response(result)


if __name__ == '__main__':

    # NOTE: Just for testing purpose
    import asyncio

    async def _main():
        result = await search_people('20.217.', search_by='rut')
        print(result)
    asyncio.run(_main())