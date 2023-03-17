from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

class AccountAdmin(UserAdmin):
    
    #campos que queremos exibir na tabela
    list_display = (
        'email',
        'first_name',
        'last_name',
        'username',
        'last_login',
        'date_joined',
        'is_active',
        
    )
    
    #criar linsk nos titulos das colunas    
    list_display_links = (
        'email',
        'first_name',
        'last_name',
        
        
    )
    #exibir os campos somente leitura
    readonly_fields = ('last_login','date_joined')
    
    #exibir em ordem decrescente
    ordering = ('-date_joined',)
    
    filter_horizontal=()
    list_filter = ()
    #aqui tornamos a senha somente leitura
    fieldsets=()

# Register models Account.
#regitrar AccountAdmin para exibir os campos no admin
admin.site.register(Account, AccountAdmin)

