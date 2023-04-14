# EVALUACE METOD VIZUÁLNÍ ODOMETRIE
## Zadání 
- Proveďte rešerši open-source metod pro vizuální odometrii z kamery. Na základě konzultace s vedoucím zvolte jeden framework a zprovozněte jej pro RPi v2 kameru. Proveďte rešerši dostupných modulů pro vizuální odometrii. Zprovozněte modul na arduino-kompatibilním mikročipu. Srovnejte oba přístupy.

## Testování 
- První verze odometri na RpiCamV2
> Použita knihovna "cv2". Výpočet diference mezi po sobě jdoucími framy pomocí funkce "calcOpticalFlowFarneback"

https://user-images.githubusercontent.com/112206462/232104632-f8db201a-aa83-46ea-a802-f60fb93a3b56.mp4

- Druhá verze odometrie na RPICamV2.
> Přidán grid a nasatvitelné rozlišení mapy

https://user-images.githubusercontent.com/112206462/232104016-29412a96-3c33-44d6-8d5d-7a984b47941b.mp4

- První verze odometrie na Pimoroni PAA5501 
> Prozatím sensor připojen na Rpi. Použita knihovna "PMW3901"

https://user-images.githubusercontent.com/112206462/232104046-932b5f9c-bd2c-4c00-8f89-1c8063521e4f.mp4

Raspberry Pi připojené na 7" touch panel osazený RpiCamV2 a Pimoroni(Optical Flow) sensorem

![341461659_1184261095525722_6360606724627900383_n](https://user-images.githubusercontent.com/112206462/232104096-8f363f1a-45c0-451d-a02b-0a2179048f92.jpg)
![340668499_778234440488964_4237572510477158698_n](https://user-images.githubusercontent.com/112206462/232104120-b92094dd-b910-4e12-b601-42423e852e70.jpg)


## rešerše
Diplomová práce z ČVUT. Dobře vysvětlený optical flow + ground facing camera.
- https://core.ac.uk/download/pdf/81647122.pdf
> v angličtině

## součástky
### Optical Flow
- [Optical Flow Sensor APM 2,5 Multicopter ADNS 3080]( https://dratek.cz/arduino/1383-optical-flow-sensor-apm2.5-multicopter-adns-3080-opticky-senzor-pro-arduino.html?utm_source=ehub&utm_medium=affiliate&ehub=d30bc48507464845a0b6d888e65bfc33)

- [PWM3901](https://www.aliexpress.com/item/1005002091547875.html?pdp_npi=2%40dis%21USD%21US%20%2415.16%21US%20%2412.13%21%21%21%21%21%402103222116774496407811127e047c%2112000018714134976%21btf&_t=pvid:bcf2b3b7-14b4-45c6-a6dc-e6720313ed10&afTraceInfo=1005002091547875__pc__pcBridgePPC__xxxxxx__1677449641&spm=a2g0o.ppclist.product.mainProduct) 
>  nenašel jsem nikde v ČR :/

- [Pimoroni PAA5100JE](https://rpishop.cz/senzory/3859-pimoroni-paa5100je-opticky-sledovaci-senzor-spi-breakout-modul-0769894018262.html)
> mělo by to být podobné PMW3901...upravili pro to knihovnu PMW3091 pro python
### Kamery
- [Raspberry Pi kamera V2](https://rpishop.cz/mipi-kamerove-moduly/329-raspberry-pi-kamera-modul-v2.html?gclid=Cj0KCQiAo-yfBhD_ARIsANr56g5VIHvnlIzASSeSK-qNFbvD6W1O3ZsQqv9FN3JUUhNKdE-j2TJ5GYIaApptEALw_wcB)
>nejvhodnější, je pro ni knihovní funkce a je nejčastěji používána....tz. nemusíme znova vymýšlet kolo a můžem využít něčí kód ze začátku, ať se můžeme o čeho odrazit
- > je i [verze](https://rpishop.cz/mipi-kamerove-moduly/331-raspberry-pi-noir-kamera-modul-v2.html) bez IR filtru (popřemýšlet, kterou vzít)


## 3D model testovacího vozítka (roveru)
- [Pod tímto odkazem uvidíte nejaktuálnější verzi 3D modelu vozítka](https://a360.co/3IGsfze)

## video prototypu roveru
> nemohu nahrát video nad 10MB, proto taková kvalita

https://user-images.githubusercontent.com/112206462/222300169-0a077872-acd8-4c5e-b9a4-cb1fede2d3bf.mp4



## source
- [1](https://www.youtube.com/watch?v=N451VeA8XRA)
- [2](https://github.com/niconielsen32)
- [3](https://www.youtube.com/watch?v=b7f1M1kpY8k&t=73s)
