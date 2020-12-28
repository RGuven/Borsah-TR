from lxml import html
import requests
import re

#########################################################################################################################################
																	#	
own_companies=[]
		   # eğer sadece kendi istediğin şirketleri hesaplamak istersen buradaki köşeli parantez içine yaz kodlarını 		#
		   # örn: ['OTKAR','EGGUB','EGEEN']											#
	           # EĞER tüm şirketler için tek seferde hesaplamak istersen boş bırak burayı  						#
		   # yani bu satır own_companies= [] şeklinde kalsın									#
																	#
#########################################################################################################################################






session1=requests.session()
kap_html=session1.get('https://www.kap.org.tr/tr/bist-sirketler').text
companies=[]
for row in kap_html.split('comp-row" >')[1:]:
	try:
		codes = re.findall('<div class="comp-cell _04 vtable">\s+<a[^<]+>([^<]*)</a>', row)[0].split(',')

		for code in codes:
			companies.append(code.strip())
	except:
	    pass
			
print("{} adet şirket bulundu ".format(len(companies)))
print("""
	Bedelli Potansiyeli Hesaplama işlemi başlıyor .. Tahmini süre 15-20 dk
	Sirketin ozsermayesi/toplam hisse adedi orani ne kadar yuksek olursa bedelsiz verme ihtimali de o kadar yuksek olabilir kesin değill!
	ve hesaplamalar sonucunda çıkan oran *100 yaparsan yüzde kaç bedelsiz vereceğini bulursun ve mesela 
	15 kat falan olmali yani %1500 bedelsiz vermesi için (15 üstü sevindirebilir)
      """)


url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse={}"
session2=requests.session()
result={}


				   
if len(own_companies) != 0:
	for company in own_companies:
		try:

			page = session2.get(url.format(company))
			content = html.fromstring(page.content)
			oz_kaynak = float(content.xpath("//*[@id='malitabloShortTbody']/tr[1]/td[2][text()]")[0].text.replace(",", "."))
			odenmis_sermaye=float(content.xpath("//*[@id='malitabloShortTbody']/tr[2]/td[2][text()]")[0].text.replace(",", "."))

			potential=round(oz_kaynak/odenmis_sermaye,3) # veya -> round(((oz_kaynak-odenmis_sermaye)/odenmis_sermaye)*100,3)
			result["".join([company])]=potential
			print("{} ---> {}".format(company,potential))
		except Exception as e:
			pass

else:	
	for company in companies:
		try:
		
			page = session2.get(url.format(company))
			content = html.fromstring(page.content)
			oz_kaynak = float(content.xpath("//*[@id='malitabloShortTbody']/tr[1]/td[2][text()]")[0].text.replace(",", "."))
			odenmis_sermaye=float(content.xpath("//*[@id='malitabloShortTbody']/tr[2]/td[2][text()]")[0].text.replace(",", "."))

			potential=round(oz_kaynak/odenmis_sermaye,3)
			result["".join([company])]=potential
			print("{} ---> {}".format(company,potential))
		except Exception as e:
			pass

print(dict(sorted(result.items(), key=lambda item: item[1],reverse=True)))





