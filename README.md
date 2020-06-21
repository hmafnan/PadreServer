# PadreServer
Temporary server for PaDRE to store visualization schema and associated data. Also serves
visualizations and data as an end-point.

## Dependencies
- Python 3.7
- PaDRE Client/SPA: Communicates with Client and SPA
- PaDRE Java Server: Data-set related information is retrieved from PaDRE server and token has to be
added in views.py

## Instructions to setup
- Extract Project
- CD into root
- Create virtual environment by using python 3.7 or same environment for PaDRE Client can be used with
two extra dependencies: Django==3.0.3 and django-jsonfield==1.0.4.
- Activate newly created virtual environment
- At the root do `pip install -r requirements.txt`
- Run `./manage.py migrate` so that database is initialized
- Run Django Server
- Make sure host path of running server is properly added to PaDRE Client -> DjangoServer back-end and SPA, 
so that they communicate with it properly
