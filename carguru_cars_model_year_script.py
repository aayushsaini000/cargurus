import requests
from itertools import groupby
import csv
import sys
from datetime import datetime


class CarGuruCars(object):

  def __init__(self):
    """
    Fetch all maker_name & maker id and returns dict
    """
    maker_name_url = """https://www.cargurus.co.uk/Cars/getCarPickerReferenceDataAJAX.action?
    showInactive=true&useInventoryService=false&localCountryCarsOnly=false&outputFormat=REACT&
    quotableCarsOnly=false&forPriceAnalysis=false"""
    try:
      maker_name_url_req = requests.get(maker_name_url)
      maker_name_url_res_json = maker_name_url_req.json()
      self.maker_name_dict = {
        d['id']: d['name'] for d in maker_name_url_res_json['allMakerModels']['makers']}
    except requests.exceptions.HTTPError as errh:
      print ("Http Error while requesting maker_name_url:",errh)
      sys.exit()
    except requests.exceptions.ConnectionError as errc:
      print ("Error Connecting requesting maker_name_url:",errc)
      sys.exit()
    except requests.exceptions.Timeout as errt:
      print ("Timeout Error requesting maker_name_url:",errt)
      sys.exit()
    except requests.exceptions.RequestException as err:
      print ("OOps: Something Else error while requesting gmaker_name_urlet_makers",err)
      sys.exit()
  

  def get_all_makers_model(self):
    """
    Fetch all makers along with all models and returns dict
    """
    url = """https://www.cargurus.co.uk/Cars/getCarPickerReferenceDataAJAX.action?
    forPriceAnalysis=false&showInactive=true&newCarsOnly=false&useInventoryService=false&
    quotableCarsOnly=false&carsWithRegressionOnly=false&localeCountryCarsOnly=false"""
    car_models = dict()
    try:
      response = requests.get(url)
      response.raise_for_status()
      json_response = response.json()
      for make, model in json_response['allMakerModels'].items():
        car_models[make] = dict()
        car_models[make].update({
            popular['modelId']: popular['modelName']
            for popular in model.get('popular', []) if popular["isActive"] is True
        })
        car_models[make].update({
            unpopular['modelId']: unpopular['modelName']
            for unpopular in model.get('unpopular', []) if unpopular["isActive"] is True
        })
      return car_models
    except requests.exceptions.HTTPError as errh:
      print ("Http Error while requesting get_makers:",errh)
      sys.exit()
    except requests.exceptions.ConnectionError as errc:
      print ("Error Connecting requesting get_makers:",errc)
      sys.exit()
    except requests.exceptions.Timeout as errt:
      print ("Timeout Error requesting get_makers:",errt)
      sys.exit()
    except requests.exceptions.RequestException as err:
      print ("OOps: Something Else error while requesting get_makers",err)
      sys.exit()
    

  def FetchAllMakerModelYear(self):
    """
    Write all maker's all model's year data to csv file
    """
    car_models_url = """https://www.cargurus.co.uk/Cars/getSelectedMakerModelCarsAJAX.action?
      forPriceAnalysis=false&showInactive=true&newCarsOnly=false&useInventoryService=false&
      quotableCarsOnly=false&carsWithRegressionOnly=false&localeCountryCarsOnly=falseoutputFormat=REACT
      &maker=%s"""
    fieldnames = ['Make', 'Model', 'Year', 'CarId']
    all_makers_dict = self.get_all_makers_model()
    current_date = datetime.now().date().strftime('%Y%m%d')
    csv_filename = f'carguru_cars_{current_date}.csv'
    with open(csv_filename, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for maker, models in all_makers_dict.items():
          if maker in self.maker_name_dict:
            try:            
              car_model_res = requests.get(car_models_url % maker)
              car_model_res.raise_for_status()
              car_years_dict = car_model_res.json()
              for model_id, model_name in models.items():
                if model_id in car_years_dict:
                  car_years_list = car_years_dict[model_id]
                  for dict_obj in car_years_list:
                    item = dict()
                    item['Make'] = self.maker_name_dict.get(maker, maker)
                    item['Model'] = model_name
                    item['Year'] = dict_obj['carName']
                    item['CarId'] = dict_obj['carId']
                    writer.writerow(item)
                    # year_count_dict = self.getModelYearCount(car_years_list)
                    # for key, val in year_count_dict.items():
                    #   item = dict()
                    #   item['Make'] = self.maker_name_dict.get(maker, maker)
                    #   item['Model'] = model_name
                    #   item['Year'] = key
                    #   item['Count'] = val
                    #   # item['Page_Link'] = response.meta['ui_url']
                    #   writer.writerow(item)
            except requests.exceptions.HTTPError as errh:
              print ("Http Error while requesting car models:",errh)
              sys.exit()
            except requests.exceptions.ConnectionError as errc:
              print ("Error Connecting requesting car models:",errc)
              sys.exit()
            except requests.exceptions.Timeout as errt:
              print ("Timeout Error requesting car models:",errt)
              sys.exit()
            except requests.exceptions.RequestException as err:
              print ("OOps: Something Else error requesting car models",err)
              sys.exit()
    

  # def getModelYearCount(self, car_years_list):
  #   year_count_dict = dict()
  #   sorted_car_years_list = sorted(car_years_list, key=lambda x:x['carName'])  
  #   for key, value in groupby(sorted_car_years_list, lambda x:x['carName']): 
  #       count = len(list(value))
  #       year_count_dict[key] = count
  #   return year_count_dict


def main():
  obj = CarGuruCars()
  obj.FetchAllMakerModelYear()


if __name__ == '__main__':
  main()
    