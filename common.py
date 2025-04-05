import re
from typing import List, Dict, Any
from pydantic import BaseModel, Field


class Item(BaseModel):
    """
    Модель товара
    """
    id: str = Field(description='ID товара')
    title: str = Field(description='Название товара')
    price: float = Field(description='Цена товара')
    url: str = Field(description='Ссылка на товар')


def cookies_str_to_dict(cookies_str: str) -> dict:
    """
    Конвертация строки с куки в словарь
    :param cookies_str: строка с куки
    :return: словарь с куки
    """
    cookies_dict = {}
    for cookie in cookies_str.split(';'):
        if '=' in cookie:
            key, value = cookie.strip().split('=', 1)
            cookies_dict[key] = value
    return cookies_dict


def extract_items_from_json(json_data: dict) -> List[Item]:
    """
    Извлечение товаров из json
    :param json_data: json с товарами
    :return: список товаров
    """
    items = []
    try:
        # Получаем список товаров из JSON
        products = json_data.get('widgetStates', {}).get('searchResultsV2-252189-default-1', '')
        if not products:
            return items

        # Преобразуем строку в словарь
        import json
        products_dict = json.loads(products)
        
        # Извлекаем данные о товарах
        for item in products_dict.get('items', []):
            try:
                # Получаем основные данные о товаре
                item_data = {
                    'id': str(item.get('id', '')),
                    'title': item.get('title', ''),
                    'price': float(item.get('price', '0').replace(' ', '')),
                    'url': f"https://www.ozon.ru/product/{item.get('id', '')}"
                }
                
                # Создаем объект товара
                item_obj = Item(**item_data)
                items.append(item_obj)
            except Exception as e:
                print(f"Ошибка при обработке товара: {e}")
                continue
                
    except Exception as e:
        print(f"Ошибка при извлечении товаров: {e}")
        
    return items


def extract_llc_info_from_json(json_data: dict) -> Dict[str, Any]:
    """
    Извлечение информации о юридическом лице из json
    :param json_data: json с информацией
    :return: словарь с информацией
    """
    try:
        # Получаем данные из виджета
        widget_data = json_data.get('widgetStates', {}).get('webSellerModalInfoV2-0', '')
        if not widget_data:
            return {}

        # Преобразуем строку в словарь
        import json
        info_dict = json.loads(widget_data)
        
        # Извлекаем основную информацию
        result = {
            'company_name': info_dict.get('companyName', ''),
            'ogrn': info_dict.get('ogrn', ''),
            'inn': info_dict.get('inn', ''),
            'address': info_dict.get('address', '')
        }
        
        return result
        
    except Exception as e:
        print(f"Ошибка при извлечении информации о юр. лице: {e}")
        return {}