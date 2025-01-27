from django.contrib import admin
from .models import Tag, Chat, Conversa, Arquivo, LogInteracao

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# Inline para mostrar mensagens e arquivos diretamente no Chat
class ConversaInline(admin.TabularInline):
    model = Conversa
    extra = 1  # Linhas extras no formulário


class ArquivoInline(admin.TabularInline):
    model = Arquivo
    extra = 1


# Ação personalizada: Arquivar chats
@admin.action(description="Arquivar chats selecionados")
def arquivar_chats(modeladmin, request, queryset):
    queryset.update(status='archived')


# Ação personalizada: Excluir chats selecionados
@admin.action(description="Excluir chats selecionados")
def excluir_chats(modeladmin, request, queryset):
    queryset.delete()  # Exclui os chats e seus relacionamentos (Conversa, Arquivo, etc.)


# Configuração do modelo Chat no Django Admin
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'status', 'chat_date')
    list_filter = ('status', 'chat_date', 'tags')  # Filtros laterais
    search_fields = ('title', 'user__username')  # Pesquisa
    ordering = ('-chat_date',)
    filter_horizontal = ('tags',)  # Interface para selecionar tags
    inlines = [ConversaInline, ArquivoInline]  # Exibe mensagens e arquivos no detalhe do Chat
    actions = [arquivar_chats, excluir_chats]  # Adiciona as ações personalizadas


@admin.register(Conversa)
class ConversaAdmin(admin.ModelAdmin):
    list_display = ('chat', 'sender', 'is_ai', 'message_type', 'timestamp')
    list_filter = ('is_ai', 'message_type', 'timestamp')
    search_fields = ('text', 'chat__title', 'sender__username')
    ordering = ('-timestamp',)

@admin.register(Arquivo)
class ArquivoAdmin(admin.ModelAdmin):
    list_display = ('chat', 'upload_by', 'file', 'upload_at')
    list_filter = ('upload_at',)
    search_fields = ('file', 'chat__title', 'upload_by__username')
    ordering = ('-upload_at',)


@admin.register(LogInteracao)
class LogInteracaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'user_message', 'ai_response', 'response_time', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('user_message', 'ai_response', 'response_time', 'chat__title')
    ordering = ('-timestamp',)
