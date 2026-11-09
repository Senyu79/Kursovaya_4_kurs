from django.contrib import admin
from .models import Position, Trainer, Client, Membership, Workout, MembershipType

admin.site.register(Position)
admin.site.register(MembershipType)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'phone', 'email')
    search_fields = ('last_name', 'first_name', 'phone')

@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'position', 'phone')
    search_fields = ('last_name', 'first_name')

admin.site.register(Membership)
admin.site.register(Workout)