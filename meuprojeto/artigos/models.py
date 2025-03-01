from django.db import models

class Articles(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    sumario = models.TextField()
    data = models.DateField()

    def __str__(self):
        return self.titulo


class Comment(models.Model):
    artigo = models.ForeignKey(Articles, related_name='comentarios', on_delete=models.CASCADE)  
    autor = models.CharField(max_length=255) 
    texto = models.TextField()  
    data = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f'Comentário de {self.autor} sobre {self.artigo.titulo}'
