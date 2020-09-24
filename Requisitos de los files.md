### Requisitos de los files

los manifest.py solo deben tener la informacion siguiente dentro de cada modulo 



```
    'version': '13.0.0.0.1',
    'category': 'Medical',
    'author': 'LabViv',
    'website': 'https://labviv.org.ve/',
    'license': 'GPL-3',
```

a 4 espacios .. no tabular las identaciones .  debemos poner todos los IDE que estemos usando para poder configurarlos  que las identaciones sean a 4 espacios

los /py inlcuyendo .los

```
 _init_.py y los _manifest_.py 
```

hacerlos con este otro texto dentro 

```
#
#    Copyright 2020 LabViv
#    License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
#
```

 y los XML  

```
<?xml version="1.0" encoding="utf-8"?>
<!--    Copyright 2020 LabViv -->
<!--    License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html). -->
```

creo que con este tema no tendremos mas necesidades de retocar los modulos nuestros . 

Otra cosa:

La ruta para el icono e imagenes de los modulos es:

```
./static/src/img/
```

