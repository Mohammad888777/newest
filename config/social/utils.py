from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage


def hadle_paginator(obj,res,page):

    paginator=Paginator(obj,res)
    try:
        result=paginator.page(page)
    except PageNotAnInteger:
        result=paginator.page(1)
    except EmptyPage:
        result=paginator.page(paginator.num_pages)
        
    return result

        