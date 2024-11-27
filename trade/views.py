from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views.generic import CreateView
# django.urlsからreverse_lazyをインポート
from django.urls import reverse_lazy
# formsモジュールからPhotoPostFormをインポート
from .forms import TradePostForm
# method_decoratorをインポート
from django.utils.decorators import method_decorator
# login_requiredをインポート
from django.contrib.auth.decorators import login_required
# photoモデルをインポート
from .models import TradePost
# django.views.genericからDetailViewをインポート
from django.views.generic import DetailView
# django.views.genericからDeleteViewをインポート
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.urls import reverse_lazy
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import EmailMessage



class IndexView(TemplateView):
    template_name = "index.html"

@method_decorator(login_required, name='dispatch')
class CreateTradeView(CreateView):
    form_class = TradePostForm
    template_name = "post_trade.html"
    success_url = reverse_lazy('trade:post_done')

    def form_valid(self, form):
        postdata = form.save(commit=False)
        postdata.user = self.request.user
        postdata.save()
        return super().form_valid(form)
    


class IndexView(ListView):
    template_name = 'index.html'
    queryset = TradePost.objects.order_by('-posted_at')
    paginate_by = 9

class CreatePhotoView(CreateView):
    '''出品ページのビュー
    
    TradePostFormで定義されているモデルとフィールドと連携して
    投稿データをデータベースに登録する
    
    Attributes:
    form_class: モデルとフィールドが登録されたフォームクラス
    template_name: レンダリングするテンプレート
    success_url: データベスへの登録完了後のリダイレクト先
    '''
    # forms.pyのTradePostFormをフォームクラスとして登録
    form_class = TradePostForm
    # レンダリングするテンプレート
    template_name = "post_trade.html"
    # フォームデータ登録完了後のリダイレクト先
    success_url = reverse_lazy('trade:post_done')

    def form_valid(self, form):
        '''CreateViewクラスのform_valid()をオーバーライド
        
        フォームのバリデーションを通過したときに呼ばれる
        フォームデータの登録をここで行う
        
        parameters:
            form(django.forms.Form):
            form_classに格納されているPhotoPostFormオブジェクト
        Return:
            HttpResponseRedirectオブジェクト:
            スーパークラスのform_valid()の戻り値を返すことで、
            success_urlで設定されているURLにリダイレクトさせる
        '''
        # commit=FalseにしてPOSTされたデータを取得
        postdata = form.save(commit=False)
        # 投稿ユーザーのidを取得してモデルのuserフィールドに格納
        postdata.user = self.request.user
        # 投稿データをデータベースに登録
        postdata.save()
        # 戻り値はスーパークラスのform_valid()の戻り値(HttpResponseRedirect)
        return super().form_valid(form)
    
class PostSuccessView(TemplateView):
    '''投稿完了ページのビュー
    Attributes:
    template_name: レンダリングするテンプレート
    '''
    # index.htmlをレンダリングする
    template_name ='post_success.html'



class CategoryView(ListView):
    '''カテゴリページのビュー
    
    Attributes:
    template_name: レンダリングするテンプレート
    paginate_by: 1ページに表示するレコードの件数
    '''
    # index.htmlをレンダリングする
    template_name ='index.html'
    # 1ページに表示するレコードの件数
    paginate_by = 9

    def get_queryset(self):
        '''クエリを実行する
        
        self.kwargsの取得が必要なため、クラス変数querysetではなく、
        get_queryset（）のオーバーライドによりクエリを実行する
        
        Returns:
            クエリによって取得されたレコード
        '''     
        # self.kwargsでキーワードの辞書を取得し、
        # categoryキーの値(Categorysテーブルのid)を取得
        category_id = self.kwargs['category']
        # filter(フィールド名=id)で絞り込む
        categories = TradePost.objects.filter(
        category=category_id).order_by('-posted_at')
        # クエリによって取得されたレコードを返す
        return categories

class UserView(ListView):
    '''ユーザーの投稿一覧ページのビュー
    
    Attributes:
    template_name: レンダリングするテンプレート
    paginate_by: 1ページに表示するレコードの件数
    '''
    # index.htmlをレンダリングする
    template_name ='index.html'
    # 1ページに表示するレコードの件数
    paginate_by = 9

    def get_queryset(self):
        '''クエリを実行する
        
        self.kwargsの取得が必要なため、クラス変数querysetではなく、
        get_queryset（）のオーバーライドによりクエリを実行する
        
        Returns:
            クエリによって取得されたレコード
        '''
        # self.kwargsでキーワードの辞書を取得し、
        # userキーの値(ユーザーテーブルのid)を取得
        user_id = self.kwargs['user']
        # filter(フィールド名=id)で絞り込む
        #  category=category_id　リクエストのIDとテーブルのIDの一致
        user_list = TradePost.objects.filter(
        user=user_id).order_by('-posted_at')
        # クエリによって取得されたレコードを返す
        return user_list
    
class MypageView(ListView):
    # HTMLを指定
    template_name = 'mypage.html'
    # ページネーションを指定
    paginate_by = 9
    # ユーザで絞り込みをする関数
    def get_queryset(self):
        # ログインしてるユーザで絞り込み
        # TradePost.objects.→TradePostモデルから
        # fillter(user=self.request.user) → ログインユーザーとユーザが一致したレコード絞り込み
        queryset = TradePost.objects.filter(
            user=self.request.user).order_by('-posted_at')
        return queryset
    
class DetailView(DetailView):
    template_name = 'detail.html'
    model = TradePost

class TradeDeleteView(DeleteView):
    # 操作の対象はTradePost
    model = TradePost
    # HTMLを指定
    template_name = 'trade_delete.html'
    # 削除完了後にマイページにリダイレクト
    success_url = reverse_lazy('trade:mypage')
    # レコードの削除を行う
    def delete(self, request ,*args ,**kwargs):
        return super().delete(request, *args, **kwargs)
    
class TradeBuyView(DeleteView):
    # 操作の対象はTradePost
    model = TradePost
    # HTMLを指定
    template_name = 'trade_buy.html'
    # 購入完了後、トップページにリダイレクト
    success_url = reverse_lazy('trade:index')
    # レコードの削除を行う
    def delete(self, request ,*args ,**kwargs):
        return super().delete(request, *args, **kwargs)
    
class ContactView(FormView):
        template_name = 'contact.html'

        form_class = ContactForm

        #送信ボタン
        success_url = reverse_lazy('trade:contact')
        #送信完了後に元のコンタクトページへ移動

        #送信ボタンを押したときの処理
        def form_valid(self, form):
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            subject = 'お問い合わせ : {}'
            message = \
                '送信者名:{0}\nメールアドレス:{1}\nメッセージ:{2}'.format(name ,email,  message)
            from_email = 'admin@example.com'
            to_list = ['admin@example.com']
            message = EmailMessage(subject = subject,
                                    body = message,
                                    from_email = from_email ,
                                    to = to_list
                                    )
            message.send()
            messages.success(
                self.request, 'お問い合わせは正常に送信されました。'
            )
            return super().form_valid(form)
