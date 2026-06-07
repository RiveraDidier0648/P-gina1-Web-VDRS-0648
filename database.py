#Esta es nuestra conexión con MongoDB, donde vamos a colocar la URL que nos da la página. 

from pymongo import MongoClient
#Tienes que instalar pymongo desde la terminal, ingresa "pip install pymongo" y listo. 

client = MongoClient('mongodb+srv://didier:didi123@vdrs0648.ygunpnl.mongodb.net/?appName=VDRS0648')

#Aquí va el nombre de su base de datos. 
db = client['veterinaria']