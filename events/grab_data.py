
import time
#from insert_into_db import insert_into_db

def grab_data(data):
    """
    grab_data(json_input)

    This function grab data from JSON to individual vars and sort them to logical sequence
    for sql methods.
    Output of this function is list of values.
    """

    #
    # niektore udaje su key: value
    # ine su naplnene list-ami alebo slovnikmi
    #
    # hodnotove udaje netreba nacitavat nanovo
    # listy a slovniky budu doplnene uz vytianutymi datami v SQL inserte
    #
    # firma aj miesto predaja sa opakuje pre kazdu polozku
    # rozoberem tu
    #

    '''
    # # dynamicke prechadzanie slovnika / json len do 2 podurovne
    # # viac alebo podpla potreby by som vyriesil asi cez rekurziu (?)
    for element in data['receipt']:

        if type(data["receipt"][element]) == list:
            i = 0
            for sub_element in data["receipt"][element]:
                for key in sub_element:
                    print(f'    Key: {key}, Value: {data["receipt"][element][i][key]}')

                i += 1
        elif type(data["receipt"][element]) == dict:

            for sub_element in data["receipt"][element]:
                print(f'    Key: {sub_element}, Value: {data["receipt"][element][sub_element]}')

        else:
            print(f'Key: {element}, Value: {data["receipt"][element]}, {type(data["receipt"][element])}')
    '''

    #
    # # povodny model zberu dat. Udaj po udaji ale ked som si predstavil ako budem volat funciu som
    # # od toho nateraz upustil. No rozpis si ponecham v komentari pre pripadne neskorsie pouzitie
    #
    '''
    

    # # Firma a jej sidlo
    #organization = data['receipt']['organization']  # list
    organization_name = data['receipt']['organization']['name']

    # # Firemna predajna a jej dresa
    unit = data['receipt']['unit']  # list

    # # malym obchodom sa adresy zhoduju (ked maju len 1 predajnu) velke firmy ako:
    # # tesco, lidl, dedoles, ... sa adresy zvycajne lisia

    # # vytvorim z datumu a casu timestamp, napr: 1640099359.0
    date_of_purchase_time_stamp = time.mktime(time.strptime(data['receipt']['createDate'], "%d.%m.%Y %H:%M:%S"))

    date_of_purchase = data['receipt']['createDate'].split(' ')[0]
    # date_of_purchase = date_of_purchase[6:10] + date_of_purchase[3:5] + date_of_purchase[0:3]
    time_of_purchase = data['receipt']['createDate'].split(' ')[1]

    customer_id = data['receipt']['customerId']
    dic = data['receipt']['dic']
    exemption = data['receipt']['exemption']
    free_tax_amount = data['receipt']['freeTaxAmount']
    ic_dph = data['receipt']['icDph']
    ico = data['receipt']['ico']
    invoice_number = data['receipt']['invoiceNumber']
    issue_date = data['receipt']['issueDate']
    okp = data['receipt']['okp']
    paragon = data['receipt']['paragon']
    paragon_number = data['receipt']['paragonNumber']
    pkp = data['receipt']['pkp']
    receipt_id = data['receipt']['receiptId']
    receipt_number = data['receipt']['receiptNumber']
    tax_base_basic = data['receipt']['taxBaseBasic']
    tax_base_reduced = data['receipt']['taxBaseReduced']
    total_price = data['receipt']['totalPrice']
    type_ = data['receipt']['type']
    vat_amount_basic = data['receipt']['vatAmountBasic']
    vat_amount_reduced = data['receipt']['vatAmountReduced']
    vat_rate_basic = data['receipt']['vatRateBasic']  # 20%
    vat_rate_reduced = data['receipt']['vatRateReduced']  # 10%
    '''

    # kedze nechcem uplne vsetky (zbytocne) udaje o predajcovi, vyriahnem ich rucne a nie cez loop

    organization_ico = data['receipt']['organization']['ico']
    organization_dic = data['receipt']['organization']['dic']
    organization_icDph = data['receipt']['organization']['icDph']

    organization_name = data['receipt']['organization']['name']

    organization_streetName = data['receipt']['organization']['streetName']
    organization_propertyRegistrationNumber = data['receipt']['organization']['propertyRegistrationNumber']

    organization_postalCode = data['receipt']['organization']['postalCode']
    organization_municipality = data['receipt']['organization']['municipality']
    organization_country = data['receipt']['organization']['country']

    # info o predajni
    {'cashRegisterCode': '88820202794150761', 'buildingNumber': '4783', 'country': 'Slovensko',
     'municipality': 'Pezinok', 'postalCode': '90201', 'propertyRegistrationNumber': '1', 'streetName': 'Okružná',
     'name': None, 'unitType': 'STANDARD'}

    {'cashRegisterCode': '88820203011401673', 'buildingNumber': 'B', 'country': 'Slovensko', 'municipality': 'Pezinok',
     'postalCode': '90201', 'propertyRegistrationNumber': '2', 'streetName': 'Myslenická', 'name': None,
     'unitType': 'STANDARD'}


    date_of_purchase = data['receipt']['createDate'].split(' ')[0]
    date_of_purchase_time_stamp = time.mktime(time.strptime(data['receipt']['createDate'], "%d.%m.%Y %H:%M:%S"))
    items = data['receipt']['items']  # list

    # pre kazdu polozku na blocku vygenerujem finalny zoznam hodnot
    # ako prve si vytvorim zaklad z kupenej polozky (nazov, mnozstvo, atd )
    # nasledne do riadku vlozim zvysne udaje, nieco pred a nieco za

    # jeden z dovodov preco mam samostatne vytahovanie udajov a samostatne vkladanie do DB je,
    # ze v buducnosti chcem spravit prekladac blockovych nazvov na normalne
    # lebo TS Kurca je jasne, Tesco kurca,
    # ale T. T. KL. K. N. 23 za 2,19€ ani srnka netusi co to je

    list_rows = []

    for comodity in items:
        price_per_one = round(comodity['price'] / comodity['quantity'], 2)

        name = comodity['name'].split(' ')
        count = name.count('')

        for i in range(count):
            name.remove('')

        nn_string = ' '.join(name)

        list_row = [nn_string, comodity['quantity'], price_per_one, comodity['price'], comodity['vatRate'],
                    comodity['itemType']]

        list_row.insert(0, date_of_purchase)
        list_row.insert(0, date_of_purchase_time_stamp)
        list_row.append(organization_name)

        for element in data['receipt']:
            if element != 'items' and element != 'organization' and element != 'unit' and element != 'exemption':
                list_row.append(data["receipt"][element])

        #print(list_row)

        #insert_into_db(list_row)

        # insert items to database + owner
        #def add_items(list_row, owner):
        list_rows.append(list_row)

        #print(list_row)
    return list_rows
