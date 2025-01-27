"""
Modelo para chat com o gemini, vai receber os dados da conversa
e armazena-las poara consultas posteriores.
"""

from django.conf import settings
from django.db import models
from django.utils import timezone


#etiqueta
class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Chat(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('closed', 'Closed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    chat_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    tags = models.ManyToManyField(Tag, blank=True, related_name='chats')

    class Meta:
        ordering = ['-chat_date']

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


class Conversa(models.Model):
    MESSAGE_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('audio', 'Audio'),
        ('file', 'File'),
    ]

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='conversa')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversa')
    is_ai = models.BooleanField(default=False)  # Identifica mensagens da IA
    text = models.TextField(blank=True, null=True)  # Mensagem de texto opcional
    file = models.FileField(upload_to='messageuploads/%Y/%m/%d', blank=True, null=True)  # Arquivos de mídia
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='text')
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"IA: {self.text}" if self.is_ai else f"{self.sender}: {self.text}"

    @classmethod
    def buscar_mensagens(cls, chat_id, termo):
        return cls.objects.filter(chat_id=chat_id, text__icontains=termo)


"""
Modelo para receber e associar o arquivo.
"""

class Arquivo(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='arquivos')
    upload_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='filechatuploads/%d/%m/%Y')
    upload_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File uploaded by {self.upload_by} on {self.upload_at}"


#LOGS

class LogInteracao(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='logs')
    user_message = models.TextField()
    ai_response = models.TextField()
    response_time = models.DurationField()  # Tempo de resposta do Gemini
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log de interação no chat {self.chat.id} em {self.timestamp}"