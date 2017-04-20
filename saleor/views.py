from django.shortcuts import render

# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import pgettext_lazy, ugettext, gettext

from django.contrib import messages
from django.conf import settings

# temp for products customisations

from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

# dapoaugury
from .product.forms import get_form_class_for_product, get_form_class_for_plan
from .dashboard.product import forms

from .product.models import Product, Category, ProductAttribute, ProductVariant, AttributeChoiceValue
from .cart import Cart
from .core.utils import get_paginator_items
from .registration.utils import get_facebook_login_url, get_google_login_url, get_local_host
from .registration.forms import RequestAppointmentConfirmationForm, RequestPreLaunchForm, RequestBundleForm, RequestContactForm, RequestJoinForm


from badgify.models import Award, Badge
import datetime, calendar
from datetime import date, timedelta
from dateutil import relativedelta
from django.http import JsonResponse
# temp for products customisations

import logging
logger = logging.getLogger(__name__)
# del logging
# from .settings import ContextFilter
# from .settings import RotatingFileHandler

class ContextFilter(logging.Filter, object):
    def filter(self, record):

         # record.ip = choice(ContextFilter.IPS)
        record.ip = '0.0.0.0'
        try:
            request = record.args[0]
            record.ip = request.META.get('REMOTE_ADDR')
            # record.ip = request
            # record.args = None
        except:
            pass

        return True

# Queries handling
from django.db.models import Q


# Calender schedule handling - Django Scheduler
from schedule.models import Calendar, Occurrence, Event
from schedule.conf.settings import (GET_EVENTS_FUNC, OCCURRENCE_CANCEL_REDIRECT,
                                    EVENT_NAME_PLACEHOLDER, CHECK_EVENT_PERM_FUNC,
                                    CHECK_OCCURRENCE_PERM_FUNC, USE_FULLCALENDAR)
from django.utils import timezone
from schedule.periods import Year, Month, Week, Day

User = get_user_model()

def index(request):
    local_host = get_local_host(request)

    # auguried - P2

    if 'next' in request.GET:
        # logger.debug('Debug Message: GET.next=%s', request.GET.get('next'))
        messages.success(request, 'Please Sign In to proceed.')
        next_url = request.GET.get('next')
    else:
        next_url = ''


    base_ctx = {'request': request, 'next': next_url}
    logger.debug('Debug Message: base_ctx=%s', base_ctx)

    # return render_to_response('base_home.html', context_instance=RequestContext(request))

    return render(request, 'base_home.html', base_ctx)

def index2(request):
    return render_to_response('base_home_org.html', context_instance=RequestContext(request))

def why(request):

    # added additional context info if required
    # base_ctx = RequestContext(request, {'request': request})
    base_ctx = {}
    return render(request, 'why_finally.html', base_ctx)

def learnplanning(request):

    return render(request, 'learnplanning.html', {})

def about(request):

    return render(request, 'aboutfinally.html', {})

def getresult(request):
    local_host = get_local_host(request)
    employment_income = ''
    if 'employment_income' in request.GET:
        employment_income =  request.GET['employment_income']
    other_income = ''
    if 'other_income' in request.GET:
        other_income =  request.GET['other_income']

    user = {'name': request.GET['name'], 'smoker':request.GET['smoker'], 'sex':request.GET['sex'], 'birthday':request.GET['birthday'], 'age_retire':request.GET['age_retire'], 'employment_income':employment_income, 'other_income':other_income}
    base_ctx = {'request': request, 'user': user}

    if request.GET['cat'] == 'retirement':
        return render(request, 'result-retirement.html', base_ctx)
    if request.GET['cat'] == 'protection':
        return render(request, 'result-protection.html', base_ctx)
    if request.GET['cat'] == 'child':
        return render(request, 'result-child.html', base_ctx)

    return render(request, 'result-retirement.html', base_ctx)

def getrecommendation(request):

    local_host = get_local_host(request)
    logger.debug('Debug Message: findcompare request.POST=%s', request.GET)

    base_ctx = {'request': request, 'next': next, 'data': request.GET}
    logger.debug('Debug Message findcompare base_ctx=%s', base_ctx)
    logger.addFilter(ContextFilter())

    l1 = datetime.datetime.now()

    keyword = None
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']

    if keyword is not None:
        category = 0
    else:
        category =  request.GET['radio_plan_category']

    gender = request.GET['radio_gender']
    age = request.GET['age']
    sc_age = u'"3":%s' % (age)
    sc_gender = u'"4":%s' % (gender)

    if category == '1' :
        if 'radio_smoker' in request.GET:
            radio_smoker =  request.GET['radio_smoker']
            sc_radio_smoker = u'"13":%s' % (radio_smoker)
        if 'select_rider_l' in request.GET:
            coverage =  request.GET['select_rider_l']
            sc_coverage = u'"5":%s' % (coverage)
        if 'select_term_years_l' in request.GET:
            insured_term = request.GET['select_term_years_l']
            sc_insured_term = u'"10":%s' % (insured_term)
        if 'select_insured_sum_l' in request.GET:
            insured_sum = request.GET['select_insured_sum_l']
            sc_insured_sum = u'"2":%s' % (insured_sum)

        variants = ProductVariant.objects.filter( Q(attributes__contains=sc_age) & Q(attributes__contains=sc_gender) & Q(attributes__contains=sc_insured_term) & Q(attributes__contains=sc_insured_sum)  & Q(attributes__contains=sc_radio_smoker) & Q( product_id__in = Product.objects.filter( Q(categories = category ) ).values_list('pk') )  ).select_related('product').order_by('price_override')


    if category == '2' :
        if 'radio_smoker' in request.GET:
            radio_smoker =  request.GET['radio_smoker']
            sc_radio_smoker = u'"13":%s' % (radio_smoker)
        if 'select_rider_d' in request.GET:
            coverage =  request.GET['select_rider_d']
            sc_coverage = u'"5":%s' % (coverage)
        if 'select_term_years_d' in request.GET:
            insured_term = request.GET['select_term_years_d']
            sc_insured_term = u'"10":%s' % (insured_term)
        if 'select_insured_sum_d' in request.GET:
            insured_sum = request.GET['select_insured_sum_d']
            sc_insured_sum = u'"2":%s' % (insured_sum)
        if 'select_interest_rate' in request.GET:
            interest_rate = request.GET['select_interest_rate']
            sc_interest_rate = u'"16":%s' % (interest_rate)

        variants = ProductVariant.objects.filter( Q(attributes__contains=sc_age) & Q(attributes__contains=sc_gender) & Q(attributes__contains=sc_insured_term)  & Q(attributes__contains=sc_insured_sum)  & Q(attributes__contains=sc_radio_smoker) & Q(attributes__contains=sc_interest_rate) & Q( product_id__in = Product.objects.filter( Q(categories = category ) ).  values_list('pk') )  ).select_related('product').order_by('price_override')

    if category == '3':
        if 'montly_retire_income' in request.GET:
            montly_retire_income = request.GET['montly_retire_income']
            sc_montly_retire_income = u'"12":%s' % (montly_retire_income)
        if 'payout_age' in request.GET:
            payout_age = request.GET['payout_age']
            sc_payout_age = u'"11":%s' % (payout_age)
        if 'premium_term' in request.GET:
            premium_term = request.GET['premium_term']
            sc_premium_term = u'"14":%s' % (premium_term)
        if 'payout_duration' in request.GET:
            payout_duration = request.GET['payout_duration']
            sc_payout_duration = u'"15":%s' % (payout_duration)
        base_ctx = {'request': request, 'next': next, 'data': request.GET, 'variants': None, 'variants_total': 0}
        logger.debug('Debug Message: findcompare base_ctx=%s', base_ctx)
        sc_gender = u'"4":357' # Male
        sc_radio_smoker = u'"13":474' # n
        # remove sc_premium_term & sc_payout_duration from filter
        variants = ProductVariant.objects.filter( Q(attributes__contains=sc_age) & Q(attributes__contains=sc_gender) & Q(attributes__contains=sc_radio_smoker) & Q(attributes__contains=sc_montly_retire_income) & Q(attributes__contains=sc_payout_age) & Q( product_id__in = Product.objects.filter( Q(categories = category ) ).values_list('pk') ) ).select_related('product').order_by('price_override')

    if category == 0:
        if 'radio_smoker' in request.GET:
            radio_smoker =  request.GET['radio_smoker']
            sc_radio_smoker = u'"13":%s' % (radio_smoker)
        variants = ProductVariant.objects.filter( Q(attributes__contains=sc_age) & Q(attributes__contains=sc_gender) & Q(attributes__contains=sc_radio_smoker)  & Q( product_id__in = Product.objects.filter(   Q( name__contains = keyword ) )) ).order_by('price_override')[:20]
        products = Product.objects.get_available_products().all()
    else:
        products = Product.objects.get_available_products().filter(categories__in=[category])

    l2 = datetime.datetime.now()

    variants_display = []
    json_list = []
    i = 0

    dbg_i = 0

    for variant in variants:

        display = {}
        i = i + 1
        dbg_i = dbg_i + 1

        for attribute in variant.attributes:
            display[attribute] = AttributeChoiceValue.objects.filter(Q (attribute_id = attribute), id = variant.attributes[attribute])[0]
            dbg_i = dbg_i + 1

        product_url = products.filter(pk = variant.product_id)

        product = product_url[0]
        url = product_url[0].get_absolute_url(variant.id)

        json_list.append({ "id": variant.id, "name": product.name,"get_price_per_item": variant.get_price_per_item(),"get_price_option_1_per_item": variant.get_price_option_1_per_item(),"get_price_option_2_per_item": variant.get_price_option_2_per_item(), "description":product.description,"usp1":product.usp1,"usp2":product.usp2,"usp3":product.usp3,"url": url,"attributes": variant.attributes })

    return JsonResponse(json_list, safe=False)

def faq(request):
    local_host = get_local_host(request)

    # added additional context info
    base_ctx = RequestContext(request, {'request': request, 'facebook_login_url': get_facebook_login_url(local_host), 'google_login_url': get_google_login_url(local_host)})
    return render(request, 'faq.html', context=base_ctx)

# views for robo planner

def findcompare(request):

    local_host = get_local_host(request)
    logger.debug('Debug Message: findcompare request.POST=%s', request.POST)

    base_ctx = {'request': request, 'next': next, 'data': request.POST}
    logger.debug('Debug Message findcompare base_ctx=%s', base_ctx)
    logger.addFilter(ContextFilter())

    l1 = datetime.datetime.now()
    # logger.info('%s search start', request)

    # default search criteria

    keyword = None
    if 'keyword' in request.POST:
        keyword = request.POST['keyword']

    # if len(keyword) > 0:
    if keyword is not None:
        category = 0
    else:
        category =  request.POST['radio_plan_category']

    gender = request.POST['radio_gender']
    # birthdate = request.POST['date-birthday']
    age = request.POST['age']
    # coverage = -1

    sc_age = u'"3":%s' % (age)
    sc_gender = u'"4":%s' % (gender)
    # sc_coverage = u'"5":%s' % (coverage)
    # sc_insured_term = u'"10":%s' % (insured_term)
    # sc_insured_sum = u'"2":%s' % (insured_sum)

    if category == '1' : # Term Level
    # if 'radio_smoker' in request.POST:
        if 'radio_smoker' in request.POST:
            radio_smoker =  request.POST['radio_smoker']
            sc_radio_smoker = u'"13":%s' % (radio_smoker)
        if 'select_rider_l' in request.POST:
            coverage =  request.POST['select_rider_l']
            sc_coverage = u'"5":%s' % (coverage)
        if 'select_term_years_l' in request.POST:
            insured_term = request.POST['select_term_years_l']
            sc_insured_term = u'"10":%s' % (insured_term)
        if 'select_insured_sum_l' in request.POST:
            insured_sum = request.POST['select_insured_sum_l']
            sc_insured_sum = u'"2":%s' % (insured_sum)
        # auguried - P1m - changes to coverage filter criterias
        # variants = ProductVariant.objects.filter( Q(attributes__contains=sc_age) & Q(attributes__contains=sc_gender) & Q(attributes__contains=sc_coverage) & Q(attributes__contains=sc_insured_term) & Q(attributes__contains=sc_insured_sum)  & Q(attributes__contains=sc_radio_smoker) ).order_by('price_override')
        variants = ProductVariant.objects.filter( Q(attributes__contains=sc_age) & Q(attributes__contains=sc_gender) & Q(attributes__contains=sc_insured_term) & Q(attributes__contains=sc_insured_sum)  & Q(attributes__contains=sc_radio_smoker) & Q( product_id__in = Product.objects.filter( Q(categories = category ) ).values_list('pk') )  ).select_related('product').order_by('price_override')
        # variants = ProductVariant.objects.filter( Q(attributes__contains=sc_age) & Q(attributes__contains=sc_gender) & Q(attributes__contains=sc_insured_term) & Q(attributes__contains=sc_insured_sum)  & Q(attributes__contains=sc_radio_smoker) & Q( product_id__in = Product.objects.filter( Q(categories = category ) ).values_list('pk') )  ).order_by('price_override')
        # variants = ProductVariant.objects.filter( Q(attributes__contains=sc_age) & Q(attributes__contains=sc_gender) & Q(attributes__contains=sc_insured_term) & Q(attributes__contains=sc_insured_sum)  & Q(attributes__contains=sc_radio_smoker) & Q( product_id__in = Product.objects.filter( Q(categories = category ) ).values_list('pk') )  )

    if category == '2' : # Term Decreasing
    # if 'radio_smoker' in request.POST:
        if 'radio_smoker' in request.POST:
            radio_smoker =  request.POST['radio_smoker']
            sc_radio_smoker = u'"13":%s' % (radio_smoker)
        if 'select_rider_d' in request.POST:
            coverage =  request.POST['select_rider_d']
            sc_coverage = u'"5":%s' % (coverage)
        if 'select_term_years_d' in request.POST:
            insured_term = request.POST['select_term_years_d']
            sc_insured_term = u'"10":%s' % (insured_term)
        if 'select_insured_sum_d' in request.POST:
            insured_sum = request.POST['select_insured_sum_d']
            sc_insured_sum = u'"2":%s' % (insured_sum)
        if 'select_interest_rate' in request.POST:
            interest_rate = request.POST['select_interest_rate']
            sc_interest_rate = u'"16":%s' % (interest_rate)
        # auguried - P1m - changes to coverage filter criterias
        # variants = ProductVariant.objects.filter( Q(attributes__contains=sc_age) & Q(attributes__contains=sc_gender) & Q(attributes__contains=sc_coverage) &  Q(attributes__contains=sc_insured_term) & Q(attributes__contains=sc_insured_sum)  & Q(attributes__contains=sc_radio_smoker) ).order_by('price_override')
        variants = ProductVariant.objects.filter( Q(attributes__contains=sc_age) & Q(attributes__contains=sc_gender) & Q(attributes__contains=sc_insured_term)  & Q(attributes__contains=sc_insured_sum)  & Q(attributes__contains=sc_radio_smoker) & Q(attributes__contains=sc_interest_rate) & Q( product_id__in = Product.objects.filter( Q(categories = category ) ).  values_list('pk') )  ).select_related('product').order_by('price_override')

    if category == '3': # Retirement
        if 'montly_retire_income' in request.POST:
            montly_retire_income = request.POST['montly_retire_income']
            sc_montly_retire_income = u'"12":%s' % (montly_retire_income)
        if 'payout_age' in request.POST:
            payout_age = request.POST['payout_age']
            sc_payout_age = u'"11":%s' % (payout_age)
        if 'premium_term' in request.POST:
            premium_term = request.POST['premium_term']
            sc_premium_term = u'"14":%s' % (premium_term)
        if 'payout_duration' in request.POST:
            payout_duration = request.POST['payout_duration']
            sc_payout_duration = u'"15":%s' % (payout_duration)
        base_ctx = {'request': request, 'next': next, 'data': request.POST, 'variants': None, 'variants_total': 0}
        logger.debug('Debug Message: findcompare base_ctx=%s', base_ctx)
        # auguried - 20161223 - Ignore gender and smoker
        # variants = ProductVariant.objects.filter( Q(attributes__contains=sc_age) & Q(attributes__contains=sc_gender) & Q(attributes__contains=sc_montly_retire_income) & Q(attributes__contains=sc_payout_age) & Q(attributes__contains=sc_premium_term) & Q(attributes__contains=sc_payout_duration) & Q( product_id__in = Product.objects.filter( Q(categories = category ) ).values_list('pk') ) ).order_by('price_override')
        sc_gender = u'"4":357' # Male
        sc_radio_smoker = u'"13":474' # n
        variants = ProductVariant.objects.filter( Q(attributes__contains=sc_age) & Q(attributes__contains=sc_gender) & Q(attributes__contains=sc_radio_smoker) & Q(attributes__contains=sc_montly_retire_income) & Q(attributes__contains=sc_payout_age) & Q(attributes__contains=sc_premium_term) & Q(attributes__contains=sc_payout_duration) & Q( product_id__in = Product.objects.filter( Q(categories = category ) ).values_list('pk') ) ).select_related('product').order_by('price_override')
        # logger.debug('Debug Message: findcompare Retirement variants=%s', variants)
        # return render(request, 'findcompare.html', base_ctx)


    # sc9= u'{"10": %s,"3": %s,"2": %s,"5": %s,"4": %s}' % (insured_term, age, insured_sum, coverage, gender)
    # sc8 = u'{"10": %s,"2": %s,"3": %s,"4": %s,"5": %s}' % (insured_term, insured_sum, age, gender, coverage)

    # logger.debug('{"3": %s,"4": %s,"5": %s,"10": %s,"2": %s}' , age, gender, coverage, insured_term, insured_sum)
    # logger.debug('Debug Message: sc age=%s, gender=%s, coverage=%s, insured_term=%s, insured_sum=%s', sc_age, sc_gender, sc_coverage, sc_insured_term, sc_insured_sum)

    # cart = None
    # form_class = get_form_class_for_plan(product)
    # cart = Cart.for_session_cart(request.cart, discounts=request.discounts)
    # form = form_class(cart=cart, product=product, data=request.POST or None)

    # Reduce products to those that matches category_id selected
    # products = products.filter(categories__in=[category])
    if category == 0:
        if 'radio_smoker' in request.POST:
            radio_smoker =  request.POST['radio_smoker']
            sc_radio_smoker = u'"13":%s' % (radio_smoker)
        variants = ProductVariant.objects.filter( Q(attributes__contains=sc_age) & Q(attributes__contains=sc_gender) & Q(attributes__contains=sc_radio_smoker)  & Q( product_id__in = Product.objects.filter(   Q( name__contains = keyword ) )) ).order_by('price_override')[:20]
        products = Product.objects.get_available_products().all()
    else:
        products = Product.objects.get_available_products().filter(categories__in=[category])

    # variants = ProductVariant.objects.all()

    # Reduce variants to those that matches product_ids in products
    # variants = variants.filter(product_id__in = products)

    # Temp retrieve 50 records

    # variants = ProductVariant.objects.all().filter(product_id__in = products.values('pk')).order_by('price_override')[:100]
    # variants = ProductVariant.objects.filter( Q(product_id__in = products.values('pk')) | Q(attributes__contains=sc3) )[:20]

    # variants = ProductVariant.objects.filter( Q(attributes__contains=sc_age) & Q(attributes__contains=sc_gender) & Q(attributes__contains=sc_coverage) & Q(attributes__contains=sc_insured_term) & Q(attributes__contains=sc_insured_sum) ).order_by('price_override')

    # logger.debug('Debug Message: findcompare match variants=%s', variants)
    # logger.debug('Debug INFO: request=%s', request)
    # logger.addHandler(RotatingFileHandler(request))
    logger.info('findcompare search keys category=%s', request.META['REMOTE_ADDR'])
    l2 = datetime.datetime.now()
    logger.info('%s search keys=%s match=%s time=%s', request, request.POST, variants.values_list('sku'), (l2 - l1) )
    logger.info('findcompare match variants=%s', variants)

    # List all attributes values for product variant
    # attributes = ProductAttribute.objects.all()

    variants_display = []

    i = 0

    dbg_i = 0

    for variant in variants:

        display = {}
        i = i + 1
        dbg_i = dbg_i + 1

        # logger.debug('Debug Variant All Attributes: record=%s, sku=%s, price_override=%s, attributes=%s', i, variant, variant.price_override,  variant.attributes)
        # logger.debug('Debug Does this match sku=%s, attributes=%s', variant, variant.attributes)

        for attribute in variant.attributes:
            # logger.debug('Debug variant=%s, attribute=%s, attr_value=%s, attr_display=%s', variant, attribute, variant.attributes[attribute], AttributeChoiceValue.objects.filter(Q (attribute_id = attribute), id = variant.attributes[attribute])[0])
            display[attribute] = AttributeChoiceValue.objects.filter(Q (attribute_id = attribute), id = variant.attributes[attribute])[0]
            dbg_i = dbg_i + 1
            # logger.debug('Debug PERF: findcompare dbg_i=%s', dbg_i)
            # logger.debug('Debug display=%s', display)

        product_url = products.filter(pk = variant.product_id)
        # form_product = get_object_or_404( Product.objects.select_subclasses().prefetch_related( 'images', 'variants'), pk=variant.product_id)
        # logger.debug('Debug Message: findcompare form_product_url=%s', product_url)
        # logger.debug('Debug Message: findcompare form_product=%s', form_product)
        # form = forms.ProductForm(None, instance=form_product)
        # variants_display.append({ "variant": variant, "attribute": display, "url" :  product_url[0].get_absolute_url() } )
        # variants_display.append({ "variant": variant, "attribute": display, "url" :  product_url[0].get_absolute_url(variant.id), "product": product_url[0], "product_form": form } )
        variants_display.append({ "variant": variant, "attribute": display, "url" :  product_url[0].get_absolute_url(variant.id), "product": product_url[0]} )

    # end for variant loop

    base_ctx = {'request': request, 'next': next, 'data': request.POST, 'variants': variants_display, 'variants_total': len(variants_display)}
    logger.debug('Debug Message: findcompare base_ctx=%s', base_ctx)

    return render(request, 'findcompare.html', base_ctx)

    # return TemplateResponse(
    #     request, 'base_planner.html',
    #     {'products': products, 'parent': None, 'variants': variants_template, 'variants_display': variants_display, 'category' : category })


def home_planner(request, category, age, gender, coverage, type, insured_sum, insured_term):

    # logger.debug('Debug Message: category=%s, age=%s, gender=%s, coverage=%s, type=%s, insured_sum=%s, insured_term=%s', category, age, gender, coverage, type, insured_sum, insured_term)

#    products = Product.objects.get_available_products()[:12]
#    products = products.prefetch_related('categories', 'images',
#                                         'variants__stock')



    products = Product.objects.get_available_products().select_subclasses()
    products = products.prefetch_related('categories', 'images',
                                         'variants__stock',
                                         'variants__variant_images__image',
                                         'attributes__values')

    # Temp
    product = products.get(pk=3)
    # cart = None
    form_class = get_form_class_for_plan(product)
    cart = Cart.for_session_cart(request.cart, discounts=request.discounts)
    form = form_class(cart=cart, product=product,
                      data=request.POST or None)

    logger.debug('Debug Message: request=%s', request.method)

    if request.method == 'POST':

        logger.debug('Debug Message: request=%s', request.POST)
        # logger.debug('Debug Message: category=%s', request.POST['radio_plan_category'] )

        category =  request.POST['radio_plan_category']
        coverage =  request.POST['select-rider']
        insured_term = request.POST['select-term_years']
        gender = request.POST['radio_gender']
        birthdate = request.POST['date-birthday']
        insured_sum = request.POST['select-insured_sum']

        logger.debug('Debug Message: birthdate=%s', birthdate)
        # born = datetime.datetime(*[int(item) for item in birthdate.split('/')])
        # born = datetime.datetime.strptime(birthdate, "%d/%m/%Y")
        born = datetime.datetime.strptime(birthdate, "%d/%m/%Y").date()
        logger.debug('Debug Message: born=%s', born)
        age = calculate_age(born)
        logger.debug('Debug Message: age=%s', age)
    else:
        # default parameters
        logger.debug('Debug Message: request=%s', request.GET)
        category = 1
        age = 18
        gender = 'm'
        coverage = 'tpd'
        type = 'tpd'
        insured_sum = 150000
        insured_term = 50


    logger.debug('Debug Message: category=%s, age=%s, gender=%s, coverage=%s, type=%s, insured_sum=%s, insured_term=%s', category, age, gender, coverage, type, insured_sum, insured_term)

    logger.debug('Debug Message: products=%s', products)

    # products = get_object_or_404(products, id=1)

    # Reduce products to those that matches category_id selected
    products = products.filter(categories__in=[category])

    # logger.debug('Debug Message: products=%s', products)


    variants = ProductVariant.objects.all()
    # variants.filter(product_id__in = products.values_list('id') ).values_list('sku','price_override')

    # Reduce variants to those that matches product_ids in products
    variants = variants.filter(product_id__in = products)

    logger.debug('Debug Message: Looping thru all match variants=%s', variants)

    # List all attributes values for product variant

    attributes = ProductAttribute.objects.all()

    # Show attributes values for product variant id = 1
    # variant = variants.filter(id=1)

    variants_template = []
    variants_display = []

    # attCV = AttributeChoiceValue.objects.filter(Q(attribute_id = 2, display = insured_sum) | Q(attribute_id = 3,  display = age) | Q(attribute_id = 4,  display = gender) )
    attCV = AttributeChoiceValue.objects.filter(Q(attribute_id = 2, display = insured_sum) | Q(attribute_id = 3,  display = age)
                                              | Q(attribute_id = 4,  display = gender)
                                              | Q(attribute_id = 10,  display = insured_term)
                                              | Q(attribute_id = 5,  display = coverage))
    # attCV = AttributeChoiceValue.objects.all()
    for variant in variants:

        display = {}
        miss = 0
        miss_attr = []

        # attCV = AttributeChoiceValue.objects.filter(Q(attribute_id = 2, display = insured_sum) | Q(attribute_id = 3,  display = age) | Q(attribute_id = 4,  display = gender) )

        logger.debug('Debug Variant All Attributes: sku=%s, price_override=%s, display=%s, attCV=%s', variant, variant.price_override,  display, attCV)
        for attribute in attributes:


            value = variant.get_attribute(attribute.pk)

            attr_values = variant.display_variant(attributes)

            logger.debug('Debug Message: variant=%s: Checking thru attr_value=%s', variant, attr_values)
            # logger.debug('Debug Message: variant=%s, insured_sum attr_value=%s, attribute.pk=%s', variant, attr_values[2], attribute.pk)

            if value:

                # choices = {a.pk: a for a in attCV}
                attr_values = {a.pk: a for a in attCV}

                attr_value = attr_values.get(value)

                if attr_value:
                    display[attribute.pk] = attr_value
                    logger.debug('Debug Message: Variant=%s, Found attribute=%s, attr_value=%s, (key)value=%s', variant, attribute, attr_value, value)

                else:
                    miss = 1
                    logger.debug('Debug Message: Variant=%s: Missing attribute=%s, Missing =%s, (key)value=%s', variant, attribute, miss, value)
                    miss_attr.append(attribute)
                #     display[attribute.pk] = value
            # else:
            #   miss = 1

        if miss:
            logger.debug('Debug Message: Variant=%s : Missing 1 or More attributes. miss_attr=%s, value=%s', variant, miss_attr, value)
        else:
            logger.debug('Debug Message: Variant=%s: No Missing=%s, attr_values=%s', variant, miss, attr_values)
	    # variants_display.append(variant)
            product_url = products.filter(pk = variant.product_id)
            logger.debug('Debug Message: product_url=%s, variant.pk=%s', product_url[0].get_absolute_url(), variant.pk)
            # logger.debug('Debug Message: product_url=%s:', product_url[].get_absolute_url())
            variants_display.append({ "variant": variant, "attribute": display, "url" :  product_url[0].get_absolute_url() } )
            miss = 0


        logger.debug('Debug Display Template: variants_display=%s', variants_display)

        variants_template.append({ "variant": variant, "attribute": display } )

    # end for variant loop


    return TemplateResponse(
        request, 'base_planner.html',
        {'products': products, 'parent': None, 'variants': variants_template, 'variants_display': variants_display, 'category' : category })


@login_required
def wizard(request):
    # ctx = {'addresses': request.user.addresses.all()}

    """
    Enhancement to retrieve Badge assigned as Award to user
    """
    model = Award

    # badge = get_object_or_404(Award, user_id=request.user.id)
    badge = model.objects.filter(user_id=request.user.id)

    if badge.exists():
        # logger.debug('Debug Message: user badge id %s', badge.badge_id)
        # logger.debug('Debug Message: user badge id %s', dir(badge.model))
        logger.debug('Debug Message: user badge id %s', badge.values('badge_id'))

        # badge = get_object_or_404(Badge, id=badge.badge_id)
        badge = get_object_or_404(Badge, id=badge.values('badge_id'))
        logger.debug('Debug Message: badge %s', badge.image)
    else:
        badge.id = 0

    logger.debug('Debug Message: badge %s', badge.id)

    """
    Extended by adding 1 more item to the ctx json to following response
    """
    ctx = {'addresses': request.user.addresses.all(), 'badge': badge}

    return TemplateResponse(request, 'wizard.html', ctx)

@login_required
def user_dashboard(request):

    addresses = request.user.addresses.all()
    logger.debug('Debug Message: user=%s, addresses=%s', request.user, addresses)

    name_user = addresses[0].first_name if addresses else 'Your Name'

    """
    Enhancement to retrieve Badge assigned as Award to user
    """

    model = Award
    logger.debug('Debug Message: user %s, id=%s', request.user, request.user.id)
    """
    logger.debug('Debug Message: user id %s', dir(request.user.id))
    """


    # badge = get_object_or_404(Award, user_id=request.user.id)
    badge = model.objects.filter(user_id=request.user.id)

    if badge.exists():
        # logger.debug('Debug Message: user badge id %s', badge.badge_id)
        # logger.debug('Debug Message: user badge id %s', dir(badge.model))
        logger.debug('Debug Message: user badge id %s', badge.values('badge_id'))

        # badge = get_object_or_404(Badge, id=badge.badge_id)
        badge = get_object_or_404(Badge, id=badge.values('badge_id'))
        logger.debug('Debug Message: badge %s', badge.image)
    else:
        badge.id = 0

    logger.debug('Debug Message: badge %s', badge.id)

    """
    Extended by adding 1 more item to the ctx json to following response
    """
    ctx = {'addresses': addresses, 'badge': badge, 'name_user': name_user}

    return TemplateResponse(request, 'user_dashboard.html', ctx)

@login_required
def user_book(request):

    logger.debug('Debug Message: user_book request.POST=%s', request.POST)
    if 'username' in request.POST:
        username = request.POST['username']
        appt_date = request.POST['appt_date']
        appt_time = request.POST['appt_time']
        appt_purpose = request.POST['appt_purpose']
        comment = request.POST['comment']

        form = RequestAppointmentConfirmationForm(local_host=get_local_host(request), data=request.POST or None)
        logger.debug('Debug Message: user_book form=%s', form)
        if form.is_valid():
            form.send()
            msg = 'Your Appointment Request has been received. Our Financial advisers will be reaching out to you shortly.'
            messages.success(request, msg)

    if 'toggle' in request.GET:
        toggle = request.GET.get('toggle')
        s_month = request.GET.get('cm')
        s_year = request.GET.get('cy')
        logger.debug('Debug Message: user_book GET.toggle=%s', toggle)
        logger.debug('Debug Message: user_book GET.cm=%s', s_month)
        logger.debug('Debug Message: user_book GET.cy=%s', s_year)
        if toggle == 'prev':
            m = datetime.date.today().replace(year=int(s_year))
            m = m.replace(day=1)
            m = m.replace(month=int(s_month))
            m = m.replace(day=1) - timedelta(days=1)
            month = m.strftime("%B")
            year = m.strftime("%Y")
            s_month = m.strftime("%m")
        if toggle == 'next':
            m = datetime.date.today().replace(year=int(s_year))
            m = m.replace(day=1)
            m = m.replace(month=int(s_month))
            m = m + relativedelta.relativedelta(months=1)
            month = m.strftime("%B")
            year = m.strftime("%Y")
            s_month = m.strftime("%m")
        date = m
    else:
        month = datetime.datetime.now().strftime("%B")
        s_month = datetime.datetime.now().strftime("%m")
        year = datetime.datetime.now().strftime("%Y")
        date = timezone.now()
    logger.debug('Debug Message: user_book month=%s', month)
    logger.debug('Debug Message: user_book s_month=%s', s_month)

    # Use "public_cal"
    calendar = Calendar.objects.get(id=1)
    ctx = {'addresses': request.user.addresses.all()}

    # date = timezone.now()
    event_list = GET_EVENTS_FUNC(request, calendar)
    local_timezone = timezone.get_current_timezone()
    period_class = Month
    period = period_class(event_list, date, tzinfo=local_timezone)


    """
    need to fit the cal in - refer to - /projects/stg/local/lib/python2.7/site-packages/schedule/views.py
    """

    """
    Extended by adding 1 more item to the ctx json to following response
    """
    ctx = {'addresses': request.user.addresses.all(), 'calendar': calendar, 'period': period, 'month': month, 's_month': s_month, 's_year': year, 'year': year }

    return TemplateResponse(request, 'user_book.html', ctx)

def contact(request):

    logger.debug('Debug Message: contact request.POST=%s', request.POST)
    local_host = get_local_host(request)

    # added additional context info

    if request.user.is_authenticated():
        form_username = request.user
        form_email = request.user.email
    else:
        form_username = ''
        form_email = ''

    # ctx = RequestContext(request, {'request': request, 'form_username':form_username, 'form_email': form_email})
    # base_ctx = RequestContext(request, {'request': request, 'facebook_login_url': get_facebook_login_url(local_host), 'google_login_url': get_google_login_url(local_host), 'form_username':form_username, 'form_email': form_email})
    base_ctx = {'form_username':form_username, 'form_email': form_email}
    if 'username' in request.POST:
        username = request.POST['username']
        email = request.POST['email']
        subject = request.POST['subject']
        phone = request.POST['phone']
        comment = request.POST['comment']
        form = RequestContactForm(local_host=get_local_host(request), data=request.POST or None)
        logger.debug('Debug Message: contact form=%s', form)
        if form.is_valid():
            form.send()
            msg = 'Thank you for contacting FinAlly. Our Financial advisers will be reaching out to you shortly to followup.'
            messages.success(request, msg)

    # return render_to_response('contact.html', context_instance=ctx)
    return render(request, 'contact.html', base_ctx)

def join(request):
    logger.debug('Debug Message: join request.POST=%s', request.POST)

    local_host = get_local_host(request)
    ctx = RequestContext(request, {'request': request, 'facebook_login_url': get_facebook_login_url(local_host), 'google_login_url': get_google_login_url(local_host), 'next': next})
    if 'username' in request.POST:
        username = request.POST['username']
        email = request.POST['email']
        # pwd = request.POST['pwd']

        if User.objects.filter(email=email).exists():
            msg = 'The email (' + email + ') has already been registered. Please use another email address.'
            messages.error(request, msg)

        else:

            form = RequestJoinForm(local_host=get_local_host(request), data=request.POST or None)
            logger.debug('Debug Message: join form=%s', form)
            if form.is_valid():
                form.send()
                msg = 'Thank you for your interest to join FinAlly. A confirmation mail has been sent to your email address. Please check your mail to proceed with the login.'
                messages.success(request, msg)
                return render_to_response('homewhy.html', context_instance=ctx)

    return render_to_response('Join.html', context_instance=ctx)


def homewhy(request):

    local_host = get_local_host(request)

    if 'next' in request.GET:
        next = request.GET.get('next')
    else:
        next = '/' + settings.LOGIN_REDIRECT_URL

    # base_ctx = RequestContext(request, {'request': request, 'facebook_login_url': get_facebook_login_url(local_host), 'google_login_url': get_google_login_url(local_host), 'next': next, 'data': request.POST})
    base_ctx = {'request': request, 'next': next, 'data': request.POST}

    logger.debug('Debug Message: homewhy request.POST=%s', request.POST)
    if 'username' in request.POST:
        username = request.POST['username']
        birthday = request.POST['birthday']
        radio_gender = request.POST['radio_gender']
        radio_smoker = request.POST['radio_smoker']
        email = request.POST['email']
        phone = request.POST['phone']
        if 'term_life' in  request.POST:
            term_life = request.POST['term_life']
        else:
            term_life = 'No'
        if 'mortage_term' in  request.POST:
            mortage_term = request.POST['mortage_term']
        else:
            mortage_term = 'No'
        if 'whole_life' in  request.POST:
            whole_life = request.POST['whole_life']
        else:
            whole_life = 'No'
        if 'universal_life' in  request.POST:
            universal_life = request.POST['universal_life']
        else:
            universal_life = 'No'
        if 'diff_ci' in  request.POST:
            diff_ci = request.POST['diff_ci']
        else:
            diff_ci = 'No'
        if 'disability_income' in  request.POST:
            disability_income = request.POST['disability_income']
        else:
            disability_income = 'No'
        if 'endowment' in  request.POST:
            endowment = request.POST['endowment']
        else:
            endowment = 'No'
        if 'education' in  request.POST:
            education = request.POST['education']
        else:
            education = 'No'
        if 'spay_retire' in  request.POST:
            spay_retire = request.POST['spay_retire']
        else:
            spay_retire = 'No'
        if 'lpay_retire' in  request.POST:
            lpay_retire = request.POST['lpay_retire']
        else:
            lpay_retire = 'No'
        if 'natal' in  request.POST:
            natal = request.POST['natal']
        else:
            natal = 'No'
        if 'prelaunch' in  request.POST:
            prelaunch = request.POST['prelaunch']
        else:
            prelaunch = 'No'
        if 'referrer' in  request.POST:
            referrer = request.POST['referrer']
        else:
            referrer = 'No'

        form = RequestPreLaunchForm(local_host=get_local_host(request), data=request.POST or None)
        logger.debug('Debug Message: homewhy form=%s', form)
        if form.is_valid():

            # new_user = get_user_model().objects.get_or_create(email=email, name_user=username, phone=phone, defaults={'is_active': False})
            # if new_user:
            #     logger.debug('Debug Message: homewhy new_user=%s', new_user)
            # else:
            #     logger.debug('Debug Message: homewhy error creating new_user')

            form.send()
            # msg = 'Thank you for indicating interest with FinAlly\'s Prelaunch Bundles and Offers. Our Financial advisers will be reaching out to you shortly to followup.'
            # messages.success(request, msg)

            born = datetime.datetime.strptime(birthday, "%d/%m/%Y").date()
            logger.debug('Debug Message: born=%s', born)
            age = calculate_age(born)
            logger.debug('Debug Message: age=%s', age)
            # base_ctx = RequestContext(request, {'request': request, 'facebook_login_url': get_facebook_login_url(local_host), 'google_login_url': get_google_login_url(local_host), 'next': next, 'data': request.POST, 'age':age})
            base_ctx = {'next': next, 'data': request.POST, 'age':age}
            logger.debug('Debug Message: homewhy redirect to home_success ctx=%s', base_ctx)
            return render(request, 'home_success.html', base_ctx)

        else:
            logger.debug('Debug Message form RequestPreLaunchForm not valid=%s', form.errors.as_data())
            form_errors = form.errors.as_data()
            for key, value in form_errors.items():
                logger.debug('Debug Message form RequestPreLaunchForm not valid field=%s', value[0][0])
                messages.error(request, value[0][0])

    """
    Extended by adding 1 more item to the ctx json to following response
    """
    ctx = {}

    # return TemplateResponse(request, 'homewhy.html', ctx)
    # return render_to_response('homewhy.html', context_instance=base_ctx)
    logger.debug('Debug Message homewhy base_ctx=%s', base_ctx)
    return render(request, 'homewhy.html', base_ctx)

def home_success(request):
    logger.debug('Debug Message: home_sucess request.POST=%s', request.POST)

    ctx = RequestContext(request, {'request': request})
    logger.debug('Debug Message: home_sucess ctx=%s', ctx)

    # return render_to_response('home_success.html', context_instance=ctx)
    return render(request, 'home_success.html', base_ctx)

def easybundle(request):
    local_host = get_local_host(request)

    logger.debug('Debug Message: easybundle request.POST=%s', request.POST)
    if 'username' in request.POST:
        username = request.POST['username']
        birthday = request.POST['birthday']
        radio_gender = request.POST['radio_gender']
        radio_smoker = request.POST['radio_smoker']
        email = request.POST['email']
        phone = request.POST['phone']
        if 'startstart' in  request.POST:
	    startstart = request.POST['startstart']
        else:
            startstart = 'No'
        if 'fortyfab' in  request.POST:
            fortyfab = request.POST['fortyfab']
        else:
            fortyfab = 'No'
        if 'babyboon' in  request.POST:
            babyboon = request.POST['babyboon']
        else:
            babyboon = 'No'
        if 'prelaunch' in  request.POST:
            prelaunch = request.POST['prelaunch']
        else:
            prelaunch = 'No'
        if 'referrer' in  request.POST:
            referrer = request.POST['referrer']
        else:
            referrer = 'No'

        form = RequestBundleForm(local_host=get_local_host(request), data=request.POST or None)
        logger.debug('Debug Message: easybundle form=%s', form)
        if form.is_valid():
            form.send()
            msg = 'Thank you for indicating interest with FinAlly\'s Prelaunch Bundles and Offers. Our Financial advisers will be reaching out to you shortly to followup.'
            messages.success(request, msg)
    """
    Extended by adding 1 more item to the ctx json to following response
    """

    # base_ctx = RequestContext(request, {'request': request, 'facebook_login_url': get_facebook_login_url(local_host), 'google_login_url': get_google_login_url(local_host)})
    logger.debug('Debug Message: easybundle request=%s', request.GET)
    # logger.debug('Debug Message: easybundle tag=%s', tag)
    return render(request, 'easybundle.html', {})
    # return redirect('/easybundle1#forty-fabulous')
    # return redirect('http://prd.finally.sg/static/ux/5/easybundle.html#baby-boon')


def home(request):
    logger.debug('Debug Message: HomePage request=%s', request)
    if request.method == 'POST':
        logger.debug('Debug Message: HomePage request=%s', request.POST)
    else:
        logger.debug('Debug Message: HomePage request=%s', request.GET)

    return TemplateResponse(
        request, 'base_home.html')

def calculate_age(born):
    today = date.today()
    try:
        birthday = born.replace(year=today.year)
    except ValueError: # raised when birth date is February 29 and the current year is not a leap year
        birthday = born.replace(year=today.year, month=born.month+1, day=1)
    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year
