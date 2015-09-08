# orb/rating/views.py
import json

from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseBadRequest

from orb.models import Resource, Collection, CollectionUser, CollectionResource



def resource_bookmark_view(request):
    if request.user.is_anonymous():
        raise Http404()
    if request.method == 'POST':
        resource_id = request.POST.get('resource_id')
        
        if resource_id is None:
            return HttpResponseBadRequest()
        
        resource = Resource.objects.get(pk=resource_id)
        # check if user already has a bookmark collection object
        try:
            collection = Collection.objects.get(visibility=Collection.PRIVATE, collectionuser__user=request.user)
        # if not create it
        except Collection.DoesNotExist:
            collection = Collection()
            collection.title = "My Bookmarks"
            collection.user = request.user
            collection.save()
            
            c_user = CollectionUser()
            c_user.collection = collection
            c_user.user = request.user
            c_user.save()
        
        # check if resource already bookmarked or not
        bookmarked = CollectionResource.objects.filter(resource=resource, collection=collection ).count()
        if bookmarked == 0:
            cu = CollectionResource()
            cu.collection = collection
            cu.resource = resource
            cu.save()
            
        resp_obj = {} 
        resp_obj['success'] = True
        
        return HttpResponse(json.dumps(resp_obj),content_type="application/json; charset=utf-8")
    else:
        return HttpResponseBadRequest()   
    