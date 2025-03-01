from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Articles, Comment
from .serializers import ArticleSerializer, CommentSerializer
import requests

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Articles.objects.all()
    serializer_class = ArticleSerializer

    @action(detail=False, methods=['get'])
    def search_articles(self, request):
        query = request.query_params.get('query', '')
        
        # Verifica se o parâmetro "query" foi fornecido
        if query:
            # Faz a requisição à API do NY Times
            response = requests.get(
                'https://api.nytimes.com/svc/search/v2/articlesearch.json',
                params={'q': query, 'api-key': 'RTp8gZGPtZZL51SWkQvj2hepCRqS4avG'}
            )
            
            # Verifica se a requisição foi bem-sucedida
            if response.status_code == 200:
                data = response.json()
                articles_data = data.get('response', {}).get('docs', [])
                
                articles_list = []
                for article_data in articles_data:
                    # Verifica se o artigo já existe no banco antes de salvar
                    article, created = Articles.objects.get_or_create(
                        titulo=article_data.get('headline', {}).get('main', 'No Title'),
                        defaults={
                            'descricao': article_data.get('abstract', ''),
                            'sumario': article_data.get('snippet', ''),
                            'data': article_data.get('pub_date', '').split('T')[0],
                        }
                    )
                    if created:
                        articles_list.append(article)
                
                # Serializa os artigos para a resposta
                serializer = ArticleSerializer(articles_list, many=True)
                return Response(serializer.data)
            else:
                return Response({"error": "Erro ao acessar a API do NY Times."}, status=response.status_code)
        else:
            return Response({"error": "Parâmetro 'query' é necessário."}, status=400)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
