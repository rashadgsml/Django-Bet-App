from django.urls import path

from core.views import (premier_league_matches, premier_league_odds,
                        premier_league_standings,add_to_bet_slip,BetSlipView,coupons)

app_name = 'core'

urlpatterns = [
    path('',premier_league_matches,name='premier-league-matches'),
    path('odds/',premier_league_odds,name='premier-league-odds'),
    path('standings/',premier_league_standings,name='premier-league-standings'),
    path('add-to-bet-slip/',add_to_bet_slip,name='add-to-bet-slip'),
]