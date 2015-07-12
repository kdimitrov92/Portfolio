from django.db.models import Q

from portfolio.models.photos import Photo


def get_search_context(search_parameters):
    """ Method that by given parameters filters through the photos and gives all results that may be relevant """
    query = Q()
    for parameter in search_parameters:
        query |= Q(name__icontains=parameter)
        query |= Q(owner__username__icontains=parameter)
        query |= Q(tags__name__in=[parameter])

    return {'photos': Photo.objects.filter(query).order_by('-date_created', '-liked')}
