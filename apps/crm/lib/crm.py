import re

import requests
from bs4 import BeautifulSoup


def getOrders(url: str, cookie: dict, project: str, month: str, name: str = "", phone: str = "", email: str = "",
              manager: str = "-1"):
    cookie['Content-Type']= 'text/html; charset=windows-1251'
    res = requests.post(url=url,
                        data={
                            "month": month,
                            "real_crm_id": "",
                            "filter_division_category_id": "",
                            "date_from": "",
                            "date_to": "",
                            "source": "",
                            "status_id": "",
                            "manager_num": manager,
                            "phone": phone,
                            "fio": name.encode('windows-1251'),
                            "email": email,
                            "source_order_num": ""
                        },
                        cookies=cookie)
    print(res.request.body)
    soup = BeautifulSoup(res.text, "lxml")
    login = soup.find(name='input', attrs={"value": "Войти"})
    if login is None:
        data = []
        table = soup.find(name="table", attrs={"class": "bordered"})
        if table is None:
            return 'Таких заявок не найдено'
        rows = table.find_all(name="tr")
        count = 10 if manager == "-1" else 50
        for row in rows[:count]:
            if 'style="width:65px"' in str(row):
                continue
            order = {}
            tds = row.find_all(name="td")
            school = tds[0].find(name='div')
            order["school"] = project if school is None else school.text
            order["datetime"] = tds[0].text.replace(order["school"], '')
            order["name"] = tds[1].text
            phoneEmail = str(tds[2])
            ind1 = phoneEmail.find('<td>')
            ind2 = phoneEmail.find('<br/>')
            ind3 = phoneEmail.find('</td>')
            order["phone"] = ''.join(re.findall(r'[0-9]*', phoneEmail[ind1 + 4:ind2]))
            order['email'] = ''.join(re.findall(r'[a-zA-Z0-9@.-_]', phoneEmail[ind2 + 5:ind3]))
            order["product"] = tds[5].text.replace('\t', '').replace('\n', '')
            data.append(order)
        return data
    else:
        return f"Доступы в CRM {url} устарели, обратитесь к администратору"


def main():
    import io
    hex = 'Антон'.encode('windows-1251').hex().upper()
    print(hex)

    print('%' + '%'.join([hex[2 * i:2 * i + 2] for i in range(int(len(hex) / 2))]))
    print(bytearray.fromhex(hex.lower()).decode('windows-1251'))


if __name__ == "__main__":
    main()
