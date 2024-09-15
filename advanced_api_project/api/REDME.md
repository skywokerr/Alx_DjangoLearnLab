1. I created different views, namely create,list,detail,update,and destroy
2. I added custom views changes for update and delete
3. I added permission classes for update,create, and destroy
4. I added url patterns for the different views I have

#filtering
1. I added django filters on my installed apps after installing it on my project.
2. I then imported djangobackendfilters on the views.
3. I then added the filter, as well as search and ordering.
4. I ensured that I used author__name because it was inheritting from foreign key.
5. I then tested my views.