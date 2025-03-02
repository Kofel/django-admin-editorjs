from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from app.models import Post, PostImage


class IndexView(ListView):
    model = Post
    template_name = 'index_view.tmpl'

    def get_queryset(self):
        return Post.published.all()


class PostDetailView(DetailView):
    model = Post
    template_name = 'detail_view.tmpl'


@method_decorator(csrf_exempt, name='dispatch')
class PostImageUploadView(View):
    def post(self, request):
        if not request.user.is_staff:
            return JsonResponse(
                {'success': 0, 'message': 'У вас нет прав!'},
                status=401
            )

        if 'image' not in request.FILES:
            return JsonResponse({
                'success': 0, 'message': 'Вы не выбрали изображение!'},
                status=400
            )

        post_id = request.POST.get('post_id')

        if not post_id:
            return JsonResponse(
                {'success': 0, 'message': 'Необходимо ID записи'},
                status=400
            )

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse(
                {'success': 0, 'message': 'Запись не найдена'},
                status=404
            )

        image = request.FILES['image']
        image_obj = PostImage.objects.create(post=post, image=image)

        return JsonResponse({
            'success': 1,
            'file': {
                'url': request.build_absolute_uri(image_obj.image.url),
            }
        })
