from django.contrib import admin
from django.urls import path, include
from . import settings
from core.views import index, coupons, BetSlipView, CouponDetailView

app_name = "bet"

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('premier-league/',include('core.urls')),
    path('bet-slip/',BetSlipView.as_view(),name='bet-slip-view'),
    path('coupons/',coupons,name='coupons'),
    path('coupon-detail/<slug>',CouponDetailView.as_view(),name='coupon-detail'),
]

