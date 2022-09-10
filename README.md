usage
===========

```bash

#just type on console where answer.py file exists !
$ python3 answer.py
$ 
this script use `sqlite database for default`, if you want prefer use mysql or postgresql database you can change on config file: `answer.ini` or you can use "--setting" option

optional arguments:
  -h, --help            show this help message and exit
  -c, --check           Check for valid string containt bracket / valid json [interactive]
  -C CHECKING, --checking CHECKING
                        Check for valid string containt bracket / valid json
  -s, --show            Show json data (all) or you can use "-S" or "--show-by" to show only categorie name
  -S SHOW_BY, --show-by SHOW_BY
                        Show categorie by name
  --setting             Change setting
  -u, --update          Update data (all) from internet [take a while] or you can update spesific categorie name with "-U" or "--update-category"
  -U UPDATE_CATEGORY, --update-category UPDATE_CATEGORY
                        update only to spesific categorie name with exists data.txt if no data then get from internet first
  -l, --list-category   Show all of categories name
  -d, --debug           Show debug process/variable
  -dd, --debug-detach   Show debug process/variable on new window/terminal
  --use-for             use for in in looping to show categories and sub categories
  -v, --version         show this program version


🤓 Hadi Cahyadi              
┣━━ 🐍 Python expert         
┃   ┣━━ ⭐ Rich (contributor)
┃   ┣━━ ⭐ PyDebugger        
┃   ┗━━ ⭐ etc               
┣━━ 🔧 Full-stack developer  
┣━━ 🔧 DevOps                
┣━━ 🔧 Analyst               
┣━━ 🔧 Security Specialist   
┣━━ 🔧 Network Specialist    
┣━━ 🔧 Debugger              
┣━━ 🔧 Tester                
┣━━ 🔧 Server Admin          
┗━━ 📘 Author     

```

example
===========
* check valid string contain bracket
```bash
$ python answer.py -C "{{8945[234])gf){44434}"
$ FALSE
$ python answer.py -C "{{(89(45[234])gf)}}{44434}"
$ TRUE
$ # or you cant use -c (lowercase) to interactive mod
$ python answer.py -c          
$ Input any text or type 'q' or 'x' for exit: {{8945[234])gf){44434}
$ FALSE
$ Input any text or type 'q' or 'x' for exit: {{(89(45[234])gf)}}{44434}
$ TRUE
```

* show categories
```python
$ python answer.py -l # or python answer.py -s 
01. Buku
02. Makanan & Minuman
03. Produk Lainnya
04. Perlengkapan Pesta & Craft
05. Mainan & Hobi
06. Ibu & Bayi
07. Film & Musik
08. Elektronik
09. Kecantikan
10. Olahraga
11. Otomotif
12. Handphone & Tablet
13. Fashion Anak & Bayi
14. Komputer & Laptop
15. Kamera
16. Office & Stationery
17. Kesehatan
18. Dapur
19. Rumah Tangga
20. Fashion Wanita
21. Fashion Pria
22. Fashion Muslim
23. Gaming
24. Perawatan Tubuh
25. Pertukangan
26. Perawatan Hewan
27. Wedding
28. Logam Mulia
29. Properti
30. Tour & Travel
Do you want to show sub/child category, select number categorie:

```

* show categories by name
```python
$ python answer.py -S Buku 
Buku
   Arsitektur & Desain
      Buku Bangunan
      Buku Codes & Standars
      Buku Dekorasi & Ornamen
      Buku Desain Dapur
      Buku Desain Kamar
      Buku Desain Ruang Keluarga
      Buku Desain Ruang Tamu
      Buku Desain Rumah
      Buku Interior & Eksterior
      Buku Metode & Material Bangunan
      Buku Taman
   Buku Hukum
      Buku Gender & Hukum
      Buku Hukum Dagang
      Buku Hukum Internasional
      Buku Hukum Perdata
      Buku Hukum Pidana
      Buku Kemanusiaan
      Buku Politik & Hukum
      Kumpulan Peraturan Perundang-Undangan
      UUD 1945
   Buku Import
      Agriculture Book Import
      Art & Novel Import
      Child & Teenager Book Import
      Computer Book Import
      Economy Book Import
      Feminity Book Import

    ...

```

author
=========
Hadi Cahyadi


license
=========
MIT