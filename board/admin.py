from django.contrib import admin
from .models import Board, SubBoard, SubBoardUser

admin.site.register(Board)
admin.site.register(SubBoard)
admin.site.register(SubBoardUser)