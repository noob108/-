from 疫情动态柱状图.nameMap import city_name_map
def get_province():
    all_province=[]
    for i in city_name_map:
        all_province.append(i)
    return all_province
