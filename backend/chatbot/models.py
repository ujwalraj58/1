from django.db import models

class ChatHistory(models.Model):
    session_id = models.CharField(max_length=100)
    user_input = models.TextField()
    bot_response = models.TextField()
    source_documents = models.TextField(blank=True, null=True)
    tokens_used = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.timestamp}] {self.session_id} → {self.user_input[:30]}..."

# Create your models here.
