# Health

Poryecto de migración de GNU Health a Odoo versión 13


# Pre-requisitos:
- Devuan 2.
- Python 3.8
- Odoo 13.
- Mejoras visuales:
    git clone https://github.com/OCA/web --depth 1
    git clone https://github.com/odoo-mastercore/odoo_ux
- Localización para Venezuela:
    git clone https://github.com/odoo-mastercore/odoo-venezuela
    cd odoo-venezuela
    rm territorial_pd
    cd ..
- Códigos de área:
    git clone https://github.com/rhe-mastercore/vzla_code/
- source odoo-13/venv/bin/activate venv
- Para generar los brazaletes con QR:
        sudo apt-get install libfreetype6-dev
- sudo pip3.8 install phonenumbers pyqrcodeng pypng


Instalación:

- Entrar en modo debug (?debug=1#).
- Actualizar lista de módulos.
- Instalar módulo website.
- Instalar módulo web_responsive.
- Instalar módulo backend_theme.
- Instalar módulo territorial_pd.
- Instalar módulo l10n_ve_base.
- Instalar módulo todos los demás módulos:

-i health_lifestyle,medical,\ vzla_legal


POST- Instalación:

- Administrador -> Preferences:
    - Language: Seleccionar Español VE.
    - Timezone: America/Caracas. Guardar.
- Settings -> General Settings -> Languages -> Manage Languages:
    - Activar: Spanish VE.
    - Establecer Lunes como primer día de la semana. Guardar.
    - Archivar inglés.
- Ajustes -> Traducciones -> Términos Traducidos:
    - Cambiar Valor de Traducción: «¡No se encontrarón archivos!» por «No hay registros. Cree uno.».

hacer una rama por cada modulo nuevo en produccion 