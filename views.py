# Create your views here.

from django.core.context_processors import csrf
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper

import os
from .iscore import *

def iscore(request):
    content = ''
    result = ''
    if request.method == 'POST':
        result_path = '/tmp/result.txt'
        visitor_path = '/tmp/visitor.csv'
        home_path = '/tmp/home.csv'
        if os.path.isfile(result_path): os.remove(result_path)
        if os.path.isfile(visitor_path): os.remove(visitor_path)
        if os.path.isfile(home_path): os.remove(home_path)
        f1 = request.FILES.get('file1')
        f2 = request.FILES.get('file2')
        visit = f1.read()
        home = f2.read()

        with open(visitor_path, 'wb+') as destination:
            destination.write(visit)
            visit_info = os.stat(visitor_path)
            if visit_info.st_size > 50000:
                return render_to_response("utils/iscore.html", {'visit': visit, 'home': home, 'result': result.read()}, context_instance=RequestContext(request))
                
        with open(home_path, 'wb+') as destination:
            destination.write(home)
            home_info = os.stat(home_path)
            if home_info.st_size > 50000:
                return render_to_response("utils/iscore.html", {'visit': visit, 'home': home, 'result': result.read()}, context_instance=RequestContext(request))

        main(visitor_path, home_path)
        result = open(result_path, 'rb')
        
        return render_to_response("utils/iscore.html", {'visit': visit, 'home': home, 'result': result.read(), 'download_btn': True }, context_instance=RequestContext(request))
    return render_to_response("utils/iscore.html", {'content': content}, context_instance=RequestContext(request))




def iscore_download(request):
    #add stuff so new line looks right in windows
    f = open('/tmp/result.txt', 'rb')
    content = f.read()
    f.close()
    import re
    content = re.sub(r'(\n)', '\r\n', content)
    f = open('/tmp/result.txt', 'wb')
    f.write(content)
    f.close()
    f = open('/tmp/result.txt', 'rb')
    response = HttpResponse(FileWrapper(f), content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=result.txt'
    return response
