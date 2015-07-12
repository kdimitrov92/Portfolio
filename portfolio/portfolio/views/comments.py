from django.shortcuts import redirect

from portfolio.models.comments import PhotoComment
from portfolio.models.photos import Photo
from portfolio.views.base import AuthenticatedView


class CommentPhotoView(AuthenticatedView):
    """ View that handles commenting on a photo """
    def post(self, request):
        comment_content = request.POST.get('comment', '')
        photo = request.POST.get('photo', 0)
        if comment_content and photo:
            comment = PhotoComment(
                photo=Photo.objects.get(id=photo),
                owner=request.user,
                content=comment_content
            )

            comment.save()

        if not photo:
            return redirect('portfolio.home')

        return redirect('portfolio.photo.view', photo_id=photo)
