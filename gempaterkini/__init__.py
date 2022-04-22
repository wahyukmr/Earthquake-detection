import requests
from bs4 import BeautifulSoup

"""
Method = fungsi
field / Atrribute = variabel
"""


class GempaTerkini:
    def __init__(self):
        self.description = 'to get the latest earthquake in indonesia from BMKG.go.id'
        self.result = None

    def ekstraksi_data(self):
        """
        waktu: 11 maret 2022, 18:49:52 WIB
        Magnitude: 4.0
        Kedalaman: 10 km
        Lokasi: LS=4.06 BT=133.51
        Pusat Gempa: Pusat gempa berada di darat 98 Km Barat Daya Kaimana
        Dirasakan (Skala MMI): II Kaimana
        :return:
        """
        try:
            content = requests.get('https://bmkg.go.id')
        except Exception:
            return None

        if content.status_code == 200:
            soup = BeautifulSoup(content.text, 'html.parser')

            result = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
            result = result.findChildren('li')
            i = 1
            waktu = None
            magnitude = None
            kedalaman = None
            ls = None
            bt = None
            lokasi = None
            dirasakan = None

            for res in result:
                if i == 1:
                    waktu = res.text
                elif i == 2:
                    magnitude = res.text
                elif i == 3:
                    kedalaman = res.text
                elif i == 4:
                    koordinat = res.text.split(' - ')
                    ls = koordinat[0]
                    bt = koordinat[1]
                elif i == 5:
                    lokasi = res.text
                elif i == 6:
                    dirasakan = res.text
                i = i + 1

            hasil = dict()
            hasil['waktu'] = waktu
            hasil['magnitude'] = magnitude
            hasil['kedalaman'] = kedalaman
            hasil['koordinat'] = {'ls': ls, 'bt': bt}
            hasil['lokasi'] = lokasi
            hasil['dirasakan'] = dirasakan
            self.result = hasil
        else:
            return None

    def tampilkan_data(self):
        if self.result is None:
            print("tidak bisa menemukan data gempa terkini")
            return

        print('gempa terakhir berdasarkan BMKG')
        print(f"waktu {self.result['waktu']}")
        print(f"Magnitude {self.result['magnitude']}")
        print(f"Kedalaman {self.result['kedalaman']}")
        print(f"koordinat LS={self.result['koordinat']['ls']}, BT={self.result['koordinat']['bt']}")
        print(f"lokasi {self.result['lokasi']}")
        print(f"Dirasakan {self.result['dirasakan']}")

    def run(self):
        self.ekstraksi_data()
        self.tampilkan_data()


if __name__ == '__main__':
    gempa_di_indonesia = GempaTerkini()
    print('description package', gempa_di_indonesia.description)
    gempa_di_indonesia.run()
    # gempa_di_indonesia.ekstraksi_data()
    # gempa_di_indonesia.tampilkan_data()
