from dadata import Dadata

def get_adress(key:str, address:str, language:str)->list:
    result = []
    try:
        dadata = Dadata(key)
        result = dadata.suggest("address", address, language=language)
        result = [r['unrestricted_value'] for r in result]
    except Exception as e:
        pass
    finally: return result

def get_coordinates(key:str, address:str, language:str)->list:
    dadata = Dadata(key)
    result = dadata.suggest("address", address, language=language,count=1)
    result=result[0]
    return [result['data']['geo_lat'], result['data']['geo_lon']]

# if __name__ == '__main__':
#     token = input("token: ")
#     query = input("address: ")
#     print(get_coordinates(token, query, 'ru'))