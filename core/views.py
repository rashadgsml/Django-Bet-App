from django.shortcuts import render,redirect
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from .models import BetSlip, Game, Profile, User
from .premier_league import matches, odds, standings

from django.contrib.auth.decorators import login_required

def add_to_bet_slip(request):
    data = request.POST.get('odd')
    data = data.split("|")
    odd = data[0]
    home_team = data[1]
    away_team = data[2]
    location = data[3]
    prediction = data[4]

    game,created = Game.objects.get_or_create(
        home_team=home_team,
        away_team=away_team,
        location=location,
        odd=odd,
        prediction=prediction
    )

    profile,created = Profile.objects.get_or_create(user=request.user)

    bet_slip_qs = BetSlip.objects.filter(
        profile=profile,
        accepted=False
    )
    if bet_slip_qs.exists():
        bet_slip = bet_slip_qs[0]
        if bet_slip.games.filter(home_team=home_team,away_team=away_team,location=location,odd=odd,prediction=prediction):
            bet_slip.games.remove(game)
            messages.success(request,"Successfully deleted")
            return redirect('core:premier-league-odds')
        elif bet_slip.games.filter(home_team=home_team,away_team=away_team,location=location):
            bet_slip.games.remove(game)
            bet_slip.games.add(game)
            messages.success(request,"Successfully updated")
            return redirect('core:premier-league-odds')
        else:
            bet_slip.games.add(game)
            messages.success(request,"Successfully added to the bet slip")
            return redirect('core:premier-league-odds')
    else:
        bet_slip = BetSlip.objects.create(profile=profile)
        bet_slip.games.add(game)
        messages.success(request,"Successfully added to the bet slip")
        return redirect('core:premier-league-odds')
    return redirect('core:premier-league-odds')

def index(request):
    return render(request,"index.html")

def premier_league_matches(request):
    items = matches()
    context = {
        'items':items,
    }
    return render(request,"premier_league/premier_league_detail.html",context)

def premier_league_odds(request):
    odd_data = odds()
    profile,created = Profile.objects.get_or_create(user=request.user)
    bet_slip_qs, created = BetSlip.objects.get_or_create(
        profile=profile,
        accepted=False
    )
    context = {
        'odds':odd_data,
        'bet_slip':bet_slip_qs
    }
    return render(request,"premier_league/odds.html",context)

def premier_league_standings(request):
    standing = standings()
    context = {
        'standings':standing
    }
    return render(request,"premier_league/standings.html",context)

class BetSlipView(View):
    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        bet_slip_qs = BetSlip.objects.filter(profile=profile, accepted=False)
        context = {'profile':profile}
        if bet_slip_qs.exists():
            bet_slip = bet_slip_qs[0]
            if bet_slip.games.all():
                context["bet_slip"] = bet_slip
            else:
                messages.warning(request,"You do not have any game in your bet slip")
                return redirect('index')
        else:
            messages.warning(request,"You do not have bet slip")
            return redirect('index')
        return render(self.request,"bet_slip.html",context)

    def post(self, request, *args, **kwargs):
        amount = self.request.POST.get('amount')
        profile = Profile.objects.get(user=self.request.user)
        if float(amount) < 0.3:
            messages.warning(request,"Your stake has to be at least 0.3 AZN")
            return redirect('core:bet-slip-view')
        if profile.balance >= float(amount):
            new_balance = profile.balance - float(amount)
            Profile.objects.filter(user=self.request.user).update(balance=new_balance)
            bet_slip = BetSlip.objects.get(profile=profile, accepted=False)
            bet_slip.accepted = True
            bet_slip.stake = float(amount)
            bet_slip.save()
        else:
            messages.warning(request,"You do not have enough funds in your balance")
            return redirect('core:bet-slip-view')
        return redirect('index')

def coupons(request):
    profile = Profile.objects.get(user=request.user)
    bet_slip_qs = BetSlip.objects.filter(profile=profile, accepted=True)
    if bet_slip_qs.exists():
        context = {
            'coupons':bet_slip_qs.order_by("-datetime")
        }
        return render(request,"coupons.html",context)
    else:
        messages.warning(request,"You do not have any coupon")
        return redirect('index')

class CouponDetailView(DetailView):
    model = BetSlip
    template_name = 'coupon_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['matches'] = get_game_result(self.request,self.kwargs['slug'])
        game_result = []
        for i in get_game_result(self.request,self.kwargs['slug']):
            if i['Eps'] == 'FT':
                if i['Tr1'] > i['Tr2']:
                    data = {'home_team':i['T1'][0]['Nm'],'away_team':i['T2'][0]['Nm'],'result':'W1'}
                    game_result.append(data)
                elif i['Tr1'] < i['Tr2']:
                    data = {'home_team':i['T1'][0]['Nm'],'away_team':i['T2'][0]['Nm'],'result':'W2'}
                    game_result.append(data)
                else:
                    data = {'home_team':i['T1'][0]['Nm'],'away_team':i['T2'][0]['Nm'],'result':'Draw'}
                    game_result.append(data)

        get_game_status(self.request, game_result, self.kwargs['slug'])
        get_coupon_status(self.request,self.kwargs['slug'])
        return context

def get_game_status(request, game_result, slug):
    profile = Profile.objects.get(user=request.user)
    coupon_qs = BetSlip.objects.filter(profile=profile, slug=slug, accepted=True, status='NR')
    if coupon_qs.exists():
        coupon = coupon_qs[0]
        for i in coupon.games.all():
            for j in game_result:
                if i.home_team == j['home_team'] and i.away_team == j['away_team']:
                    i.result = j['result']
                    i.save()
                    coupon.save()
                    if i.result == i.prediction:
                        i.status = 'Won'
                    else:
                        i.status = 'Lost'
                    i.save()
                    coupon.save()

def get_coupon_status(request, slug):
    profile = Profile.objects.get(user=request.user)
    coupon_qs = BetSlip.objects.filter(profile=profile, slug=slug, accepted=True, status='NR')
    if coupon_qs.exists():
        coupon = coupon_qs[0]
        if all(x == "Won" for x in coupon.games.all()[0].status):
            coupon.status = 'Won'
            new_balance = profile.balance + coupon.get_potential_return()
            profile.balance = new_balance
            profile.save()
            coupon.save()

        for i in coupon.games.all():
            if i.status == 'Lost':
                coupon.status = 'Lost'
                coupon.save()
                break

def get_game_result(request, slug):
    profile = Profile.objects.get(user=request.user)
    coupon = BetSlip.objects.get(profile=profile, slug=slug, accepted=True)
    items = []
    for match in matches():
        for game in coupon.games.all():
            if match['T1'][0]['Nm'] == game.home_team and match['T2'][0]['Nm'] == game.away_team:
                items.append(match)
    return items




