import pandas as pd

from bs4 import BeautifulSoup as bs


def parse_med_centre(bs_obj):
    result = {'med_centre_name': '', 'address': ''}
    doctors = []
    med_centre = bs_obj.find('div', {'class': '_1njbaK'})
    result['med_centre_name'] = med_centre.text
    result['address'] = bs_obj.find('div', {'class': '_3LO55l'}).text
    doctors = bs_obj.find_all('li', {'class': '_1HyuCf'})
    return result, doctors


def parse_doctor(bs_obj):
    # result = {'doc_name': '', 'nearest_date': '', 'doc_type': '', 'room': ''}
    result = {'doc_name': bs_obj.find('div', {'class': '_2-nIhZ'}).text,
              'nearest_date': bs_obj.find('div', {'class': '_3rzMNf'}).text,
              'doc_type': bs_obj.find('span', {'class': '_9LDJkS'}).text.strip().replace('\xa0', ''),
              'room': bs_obj.find('div', {'class': '_2N0Raa'}).text}
    return result


def find_specialist(specialists, target_spec_type):
    for specialist in specialists:
        spec_type = specialist.find_element_by_class_name(
            '_2O3nTn').text
        if spec_type == target_spec_type:
            return specialist


def parse_all_doctors(page_source):
    bs_obj = bs(page_source, 'html.parser')
    med_centres = bs_obj.find_all('li', {'class': 'box _3KeUxT'})
    columns = ['med_centre_name', 'address', 'doc_name', 'nearest_date',
               'doc_type', 'room']
    result = pd.DataFrame({}, columns=columns)

    if len(med_centres) > 0:
        cnt = 0
        for med_centre in med_centres:
            med_centre_data, doctors = parse_med_centre(med_centre)
            for doctor in doctors:
                doctor_data = parse_doctor(doctor)
                for key in med_centre_data.keys():
                    doctor_data[key] = med_centre_data[key]
                doctor_data = pd.DataFrame(doctor_data, index=[cnt, ])
                cnt += 1
                result = result.append(doctor_data)
    return result
