from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import HttpResponseBadRequest, Http404, JsonResponse
from django.shortcuts import resolve_url, redirect
from django.template.loader import render_to_string
from django.views import generic
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.views import (
    LoginView, LogoutView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
...
from django.urls import reverse_lazy
...
from .forms import (
    LoginForm, UserCreateForm, UserUpdateForm,
    MyPasswordResetForm, MySetPasswordForm
)

User = get_user_model()


class TopView(generic.ListView):
    """トップページに新着順で表示"""
    model = User
    template_name = 'register/top.html'
    paginate_by = 8
    queryset = User.objects.order_by('-created_at')

    def get_context_data(self, **kwargs):
        """いいねの多い順に表示"""
        context = super().get_context_data(**kwargs)
        context["like_list"] = User.objects.order_by('-like')[:6]
        return context


class ListView(generic.ListView):
    """検索による表示結果"""
    model = User
    template_name = 'register/search_detail.html'
    paginate_by = 8

    def get_queryset(self):
        query = self.request.GET.get('q')
        skill = self.request.GET.get('skill')

        if query:
            """検索フォーム処理"""
            result = User.objects.filter(Q(username__icontains=query) | Q(self_introduction__icontains=query)).distinct()
            if not result:
                messages.success(self.request, '「{}」の検索結果はありませんでした。'.format(query))
            else:
                messages.success(self.request, '「{}」の検索結果'.format(query))

                return result

        if skill:
            """ドロップダウン処理"""
            result = User.objects.filter(skill__icontains=skill).distinct()
            if not result:
                messages.success(self.request, '「{}」の検索結果はありませんでした。'.format(skill))
            else:
                messages.success(self.request, '「{}」の検索結果'.format(skill))

        return result


class DetailView(generic.DetailView):
    """ユーザーの詳細ページ"""
    model = User
    template_name = 'register/detail.html'


class SignUp(LoginView):
    """会員登録ページ(sign upページ)"""
    template_name = 'register/sign_up.html'

class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'register/login.html'

class GuestLogin(LoginView):
    """ゲストログインページ"""
    form_class = LoginForm
    template_name = 'register/guest_login.html'

class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    model = User
    template_name = 'register/top.html'

class UserCreate(generic.CreateView):
    """ユーザー仮登録"""
    template_name = 'register/user_create.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('register/mail_template/create/subject.txt', context)
        message = render_to_string('register/mail_template/create/message.txt', context)

        user.email_user(subject, message)
        return redirect('register:user_create_done')


class UserCreateDone(generic.TemplateView):
    """ユーザー仮登録"""
    template_name = 'register/user_create_done.html'


class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'register/user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()


class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class UserDetail(OnlyYouMixin, generic.DetailView):
    model = User
    template_name = 'register/user_detail.html'



class UserUpdate(OnlyYouMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'register/user_form.html'
    success_url = reverse_lazy('app:file_list')

    def get_success_url(self):
        return resolve_url('register:user_detail', pk=self.kwargs['pk'])

class TestCreate(generic.CreateView):
    template_name = 'register/user_form.html'
    form_class = UserUpdateForm

    def form_valid(self,form):

        user = form.save(commit=False)
        user.is_active = True
        user.save()

        return redirect('register:user_detail', pk=user.pk)

class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'register/mail_template/password_reset/subject.txt'
    email_template_name = 'register/mail_template/password_reset/message.txt'
    template_name = 'register/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('register:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'register/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('register:password_reset_complete')
    template_name = 'register/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'register/password_reset_complete.html'


def like(request, pk):
    """いいね機能郡"""
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        raise Http404
    user.like += 1 # ここでいいねの数を増やす
    user.save() # 保存をする
    return redirect('register:detail', pk=pk)


def api_like(request, pk):
    """いいね後ページをロードさせない"""
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        raise Http404
    user.like += 1  # ここでいいねの数を増やす
    user.save()  # 保存をする

    return JsonResponse({"like":user.like})