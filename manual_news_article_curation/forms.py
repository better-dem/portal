from django import forms
from manual_news_article_curation.models import NewsArticleItem, ManualNewsCurationProject

class CreateArticleForm(forms.ModelForm):
    class Meta:
        model = ManualNewsCurationProject
        fields = ['name', 'url', 'img_url', 'first_paragraph']

