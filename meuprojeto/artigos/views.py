from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action  # Import @action here
from .models import Articles, Comment
from .serializers import ArticleSerializer, CommentSerializer
import requests

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Articles.objects.all()
    serializer_class = ArticleSerializer

    # Ação customizada para buscar artigos do NYTimes
    @action(detail=False, methods=['get'])
    def search_articles(self, request):
        query = request.query_params.get('query', '')
        if query:
            response = requests.get(
                f'https://api.nytimes.com/svc/search/v2/articlesearch.json',
                params={'q': query, 'api-key': 'RTp8gZGPtZZL51SWkQvj2hepCRqS4avG'}
            )
            data = response.json()
            articles = data.get('response', {}).get('docs', [])
            
            # Salvar artigos no banco de dados
            for article_data in articles:
                article = Articles(
                    titulo=article_data.get('headline', {}).get('main', 'No Title'),  
                    descricao=article_data.get('abstract', ''), 
                    sumario=article_data.get('snippet', ''),  
                    data=article_data.get('pub_date', '').split('T')[0],  
                )
                article.save()

            return Response(articles)  # Retorne uma resposta adequada, por exemplo, com o status e os artigos
        else:
            return Response({"error": "Query parameter is required."}, status=400)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
