Documentos
=======

Documentos is a simple djangoplus app that contains some document types used in Brazil.

It has four model classes:

- RG
- TituloEleitor
- Certidao
- CertidaoMilitar

### Dependecies

djangoplus-enderecos

### Steps

Execute the following steps to use it:

1. Install it

    pip install djangoplus_documentos


1. Add "documentos" to your INSTALLED_APPS settings

    INSTALLED_APPS = \[..., 'documentos']

2. Create the tables

    python manage.py sync

3. Use the models


