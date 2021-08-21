from rest_framework import generics, permissions, mixins, views, status, viewsets
import importlib
from django.apps import apps

from products.models import Image
from products.serializers import ImageSerializer

class CheckUser(permissions.BasePermission):
    """Checks f1 data"""

    def has_permission(self, request, view=None):
        if request.method == 'GET':
            return True
        if request.user.is_authenticated:
            return True

        return False


from rest_framework.response import Response


class generalModelViewSet(views.APIView):
    model_to_serializer_mapper = (
        ('TagSerializer', 'Tags', 'tags'),
    )

    url_serializers = {
        'tags':{'serializer': 'TagSerializer', 'app': 'products', 'model': 'Tags' },
        'item':{'serializer': 'ItemSerializer', 'app': 'products', 'model': 'Item' },
    }

    def get_permissions(self):
        return [CheckUser(),]
    
    def initialize(self,request):
        try:
            method = self.url_serializers[request.GET['name']]
            self.method = method
            
            mod = importlib.import_module(self.method['app'] + '.serializers')

            try:
                self.serializer_class = getattr(mod, self.method['serializer'])
                self.model = apps.get_model(self.method['app'], model_name=self.method['model'])

            except:
                return Response({"error":{'message':'Can\'t find the associated Serialization Pattern. Contact Administrator if the issue persists.'}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return True
        except:
            return Response({"error":{'message':'Error in sending the request', 'requirements':'GET Request Fields should be one of the name fields','name':self.url_serializers.keys()}}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        initial_status = self.initialize(request=request)
        if initial_status == True:
            response_data = {'data':None}

            if request.GET.get('design', False):
                response_data = {
                    'method': self.url_serializers[request.GET['name']],
                    'fields':[str(x) for x in self.serializer_class().fields.values()],
                    'columns': self.serializer_class().fields.keys(),
                    'data': None
                    # 'modal': self.url_serializers[request.GET['name']]
                }
            try:
                z = request.GET['list']
                try:
                    z = eval(z)
                    if type(z) == list:
                        objects = self.model.objects.filter(id__in = z)



                except:
                    exists_filters = self.method.get('args', False)
                    if exists_filters:
                        objects = self.model.objects.filter(**exists_filters)
                    else:
                        objects = self.model.objects.all()
                serializer = self.serializer_class(objects, many=True)
                response_data['data'] = serializer.data
            except:
                z = request.GET.get('id', False)
                if z:
                    try:
                        objects = self.model.objects.filter(id = z)
                        serializer = self.serializer_class(objects, many=True)
                        response_data['data'] = serializer.data[0]
                    except:
                        response_data['data'] = []
                        return Response(response_data, status=status.HTTP_200_OK)



            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return initial_status
    
    def post(self,request,format="json"):
        self.permission_classes = [ permissions.IsAuthenticated ]
        initial_status = self.initialize(request=request)
        if initial_status == True:  #Successfull initialization of required models and serializer class
            output = {
                    # 'body': request.data,
                    # 'method': self.url_serializers[request.GET['name']]
                }
            try:
                data = request.data['data']   # Getting User passed Data
                if type(data) == str :
                    data = eval(data)
                if type(data) == list:
                    try: # Deleting Request
                        if request.data['delete']:
                            y = self.model.objects.filter(id__in = data)
                            output['delete_status'] = list(y.values_list("id", flat=True))
                            y.delete()
                        return Response(output, status=status.HTTP_202_ACCEPTED)
                    except:
                        # Saving multiple Objects
                        output['data'] = []
                        output['errors'] = []
                        for one_data in data:
                            instance = None
                            if one_data.get('id', False):
                                instance = self.model.objects.get(id=one_data['id'])
                                y = self.serializer_class(instance = instance, data=one_data)
                            else:
                                y = self.serializer_class(data=one_data)
                            if y.is_valid():
                                instance = y.save()
                                output['data'].append(self.serializer_class(instance).data)
                            else:
                                output['errors'].append(y.errors)

                    output['formats'] = 'many'
                else:   # Saving single data
                    output['formats'] = 'single entry data'
                    instance_id = data.get("id", False)
                    if instance_id:
                        instance = self.model.objects.get(id=instance_id)
                    else:
                        instance = None
                    y = self.serializer_class(instance=instance, data=data)
                    if y.is_valid():
                        instance = y.save()
                        output['data'] = self.serializer_class(instance).data
                    else:
                        output['error'] = "Error saving Data"
                        output['errors'] = y.errors
                        return Response(output, status=status.HTTP_400_BAD_REQUEST)

            except:

                data = "Not Available"
                output['invalids'] = "Data must be available in data field"
                return Response(output, status=status.HTTP_403_FORBIDDEN)




            return Response(output, status=status.HTTP_200_OK)

        else:
            return initial_status


class ImageViewSet(viewsets. ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    
