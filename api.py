from dadata import Dadata

def get_adress(key:str, address:str, language:str)->list:
    dadata = Dadata(key)
    result = dadata.suggest("address", address, language=language)
    return [r['unrestricted_value'] for r in result]

def get_coordinates(key:str, address:str, language:str)->list:
    dadata = Dadata(key)
    result = dadata.suggest("address", address, language=language,count=1)
    result=result[0]
    return [result['data']['geo_lat'], result['data']['geo_lon']]

if __name__ == '__main__':
    token = input("token: ")
    query = input("address: ")
    print(get_coordinates(token, query, 'ru'))
# token = input("token: ")
# dadata = Dadata(token)
# result = dadata.suggest("address", "москва хабар")
# # print([r['value'] for r in result])
# print([r['unrestricted_value'] for r in result])
# result = dadata.suggest("address", result[5]['unrestricted_value'], count=1)
# result=result[0]
# print( result['data']['geo_lat'], result['data']['geo_lon'])