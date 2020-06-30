pyredmon2
=======
gRPC + Python + Redis + Mongo

Ejecutar el contenedor
---------------------
Antes de la ejecución, deben configurarse las variables de entorno en el archivo .env

```console
sudo docker run -d -v /home/nelson/Escritorio/so1p2/pyredmon2:/app -p 50051:50051 --env-file .env --name pyredmon2  pyredmon2
```