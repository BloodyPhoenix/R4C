# R4C - Robots for consumers

A little project with 3 different API.

## First API - json to django model.
First API is designed to deserialize json file into django model format. Made via Django Rest Framework ModelSerializer + ModelViewset. Realized in seralizers.py, api.py files of robots app.

## Second API - excel file download link
Second API is designed to generate .xlsx file, which user can download via link. Made via openpyxl library + standart Django tools. Realized in views.py file of robots app.

## Third API - email sending
Third api is designed to send email to customers when the goods they wanted are produced. Realized via standart Django tools in orders/siganls.py file. 
