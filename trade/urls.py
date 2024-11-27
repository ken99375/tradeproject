from django.urls import path
from .import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'trade'

urlpatterns = [
    path('',views.IndexView.as_view(), name='index'),

    path('post/',views.CreateTradeView.as_view(), name='post'),

    path('post_done/',views.PostSuccessView.as_view(), name='post_done'),

    # カテゴリ一覧ページ
    path('trades/<int:category>',views.CategoryView.as_view(),name = 'trades_cat'),

    # 詳細ページ
    path('trade-detail/<int:pk>',views.DetailView.as_view(),name = 'trade_detail'),
    
    # ユーザー詳細ページ
    path('user-list/<int:user>',views.UserView.as_view(),name = 'user_list'),
    # マイページ
    path('mypage/',views.MypageView.as_view(),name='mypage'), 

    path('trade/<int:pk>/delete/',views.TradeDeleteView.as_view(),name='trade_delete'),

    path('trade/<int:pk>/buy/',views.TradeBuyView.as_view(),name='trade_buy'),

    # お問い合わせページ
    path('contact/', views.ContactView.as_view(), name='contact'),

]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root = settings.MEDIA_ROOT
)
