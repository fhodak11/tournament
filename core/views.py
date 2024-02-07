from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *

# Create your views here.
def index(request):
    """
    Index page of the application
    
    Returns:
        - Rendered template
    """
    tournaments = Tournament.objects.all()
    return render(request, 'index.html', {'tournaments': tournaments})

def add_tournament(request):
    """
    Add tournament to the database
    Handles POST request from the form in add_tournament.html template

    Returns:
        - Redirect to the configure_tournament page
        - Rendered template
    """
    if request.method == 'POST':
        # Get form data from POST request
        tournament_name = request.POST.get('tournament')
        team_count = int(request.POST.get('team_count'))

        # Create a new tournament
        new_tournament = Tournament.objects.create(tournament=tournament_name, team_count=team_count/2)

        # Populate teams based on the selected number
        teams = []
        for i in range(team_count):
            team = Team.objects.create(tournament=new_tournament, team_name=f'')
            teams.append(team)

        # Pair up teams and set initial opponents
        for i in range(0, team_count, 2):
            teams[i].opponent = teams[i + 1].team_name
            teams[i + 1].opponent = teams[i].team_name
            teams[i].save()
            teams[i + 1].save()

        # Redirect to the team configuration page for the newly created tournament
        return redirect('configure_tournament', tournament_id=new_tournament.id)

    return render(request, 'add_tournament.html')


def configure_tournament(request, tournament_id):
    """ 
    Configure the tournament

    Arguments:
        - tournament_id {int} -- ID of the tournament

    Returns:
        - Rendered template
    """
    # Get the tournament object
    tournament = Tournament.objects.get(pk=tournament_id)
    teams = Team.objects.filter(tournament=tournament)

    return render(request, 'configure_tournament.html', {'tournament': tournament, 'teams': teams})

def add_team(request):
    """
    Add team to the tournament
    request is handled by AJAX

    params:
        - team_name: Name of the team
        - tournament_id: ID of the tournament

    Returns:
        - JsonResponse
    """
    if request.method == 'GET':
        # print the data
        print(request.GET)
        team_name = request.GET.get('team_name')
        team_id = request.GET.get('team_id')
        opponent = request.GET.get('opponent')
        print(team_name, team_id, opponent)
        # update the team name
        team_id = int(team_id)
        team = Team.objects.get(pk=team_id)
        print(team)
        team.team_name = team_name
        team.opponent = opponent
        team.modified = True
        team.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})

def delete_team(request):
    """Delete team from the tournament
    request is handled by AJAX

    params:
        - team_id: ID of the team to be deleted

    Returns:
        - JsonResponse
    """
    if request.method == 'GET':
        team_id = request.GET.get('team_id')
        team_id = int(team_id)
        team = Team.objects.get(pk=team_id)
        team.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})

def view_players(request, team_id):
    """View players of the team
    
    The request redirects to the view_players.html template where you can see the players of the home team and the opponent team.

    Arguments:
        team_id {int} -- ID of the team

    TODO: This function is not yet complete. Implement this function.

    Returns:
        - Rendered template
    """
    team = Team.objects.get(pk=team_id)
    players = Player.objects.filter(team=team)
    return render(request, 'view_players.html', {'players': players, 'team': team})

def add_player(request):
    """Add player to the team
    
    The request is handled by AJAX to make the page more responsive.

    params:
        - player_name: Name of the player
        - team_id: ID of the team

    TODO: Implement this function

    Returns:
        - JsonResponse
    """
    return JsonResponse({'status': 'success'})

def start_tournament(request, tournament_id):
    """
    Start the tournament
    
    This request is not handled by AJAX because we need to redirect to the index page after the tournament is started.

    Arguments:
        - tournament_id {int} -- ID of the tournament

    Returns:
        - Redirect to the index page
    """
    # if request.method == 'GET':
    # tournament_id = request.GET.get('tournament_id')
    print(tournament_id)
    tournament = Tournament.objects.get(pk=tournament_id)
    print(tournament)
    tournament.started = True
    tournament.save()
    # return JsonResponse({'status': 'success'})
    return redirect('index')

def view_results(request, tournament_id):
    """
    View results of the tournament

    Arguments:
        - tournament_id {int} -- ID of the tournament

    TODO: Implement this function

    Returns:
        - Rendered template

    """
    tournament = Tournament.objects.get(pk=tournament_id)
    teams = Team.objects.filter(tournament=tournament)
    
    context = {}
    context['teams'] = teams
    context['tournament'] = tournament
    return render(request, 'view_results.html', context=context)

def record_scores(request):
    """
    Record scores of the match
    """
    if request.method == 'GET':
        # print the data
        print(request.GET)
        team_name = request.GET.get('team_name')
        team_id = request.GET.get('team_id')
        opponent = request.GET.get('opponent')
        team_score = request.GET.get('team_score')
        opponent_score = request.GET.get('opponent_score')
        table = request.GET.get('table')
        print(team_name, team_id, opponent)
        
        if team_score > opponent_score:
            win = 1
        elif team_score < opponent_score:
            win = 2
        else:
            win = 0
        
        # update the team name
        team_id = int(team_id)
        if table == 'Round_1':
            team = Team.objects.get(pk=team_id)
        elif table == 'Quarters':
            team = Quarters.objects.get(pk=team_id)
        elif table == 'Semis':
            team = Semi.objects.get(pk=team_id)
            print('Semis')
        elif table == 'PosThree':
            team = PosThree.objects.get(pk=team_id)
        elif table == 'Finals':
            team = Finals.objects.get(pk=team_id)
            print('finals')
        print(team)
        team.team_name = team_name
        team.team_score = team_score
        team.opponent = opponent
        team.opponent_score = opponent_score
        team.modified = True
        team.score_modified = True
        team.win = win
        team.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})


from django.db.models import F, Max

def view_quarter_finals(request, tournament_id):
    """
    View quarter finals
    """
    # Annotate each team with its highest score (either its own score or its opponent's score)
    teams = Team.objects.filter(tournament_id=tournament_id).annotate(highest_score=Max(F('team_score'), F('opponent_score')))

    # Order the teams by the highest score in descending order and get the top 4
    top_4_teams = teams.order_by('-highest_score')[:4]
    for i in top_4_teams:
        # avoid creating duplicate records
        if not Quarters.objects.filter(team_id=i.id).exists():
            Quarters.objects.create(tournament_id=tournament_id, team_id=i.id)
        
        
    context = {}
    # context['teams'] = top_4_teams
    context['tournament'] = Tournament.objects.get(id=tournament_id)
    
    context['teams'] = Quarters.objects.filter(tournament_id=tournament_id)
    
    context['opponent'] = Team.objects.filter(tournament_id=tournament_id)

    # return JsonResponse({'status': 'success', 'teams': list(top_4_teams.values())})
    return render(request, 'quarters.html', context)

def view_semi_finals(request, tournament_id):
    """
    View semi finals
    """
    # Annotate each team with its highest score (either its own score or its opponent's score)
    teams = Quarters.objects.filter(tournament_id=tournament_id).annotate(highest_score=Max(F('team_score'), F('opponent_score')))

    # Order the teams by the highest score in descending order and get the top 4
    top_2_teams = teams.order_by('-highest_score')[:2]
    print(top_2_teams)
    for i in top_2_teams:
        # avoid creating duplicate records
        print(i.id)
        if not Semi.objects.filter(team_id=i.team_id).exists():
        # Semi.objects.create(tournament_id=tournament_id, team_id=i.id)
            Semi.objects.create(tournament_id=tournament_id, team_id=i.team_id)
            print(i.team_id)        
        
    context = {}
    # context['teams'] = top_4_teams
    context['tournament'] = Tournament.objects.get(id=tournament_id)
    
    context['teams'] = Semi.objects.filter(tournament_id=tournament_id)
    
    context['opponent'] = Quarters.objects.filter(tournament_id=tournament_id)
    for i in context['opponent']:
        print(i)

    # return JsonResponse({'status': 'success', 'teams': list(top_4_teams.values())})
    return render(request, 'semi_finals.html', context)

def view_pos_three(request, tournament_id):
    """
    View semi finals
    """
    # Annotate each team with its highest score (either its own score or its opponent's score)
    teams = Semi.objects.filter(tournament_id=tournament_id).annotate(highest_score=Max(F('team_score'), F('opponent_score')))
    print(teams)

    # Order the teams by the lowest score in descending order and get the bottom 2
    bottom_2_teams = teams.order_by('highest_score')[:2]
    print(bottom_2_teams)
    # bottom_2_teams = bottom_2_teams[::-1]
    top_2_teams = teams.order_by('-highest_score')[:2]
    print('top_2_teams')
    print(top_2_teams[1].team)
    print(bottom_2_teams)
    # for i in bottom_2_teams:
    #     # avoid creating duplicate records
    #     print(i)
    #     if not PosThree.objects.filter(team_id=i.team_id).exists():
    #     # Semi.objects.create(tournament_id=tournament_id, team_id=i.id)
    #         PosThree.objects.create(tournament_id=tournament_id, team_id=i.team_id)
    #         print(i.team_id)    
    
    # save the bottom 2 teams to the PosThree table as team and opponent but just a single record
    if not PosThree.objects.filter(team_id=bottom_2_teams[0].team_id).exists():
        PosThree.objects.create(tournament_id=tournament_id, team_id=bottom_2_teams[0].team_id, opponent=bottom_2_teams[1].team)
    
    if not Finals.objects.filter(team_id=top_2_teams[0].team_id).exists():
        Finals.objects.create(tournament_id=tournament_id, team_id=top_2_teams[0].team_id, opponent=top_2_teams[1].team)
    # for i in top_2_teams:
    #     if not Finals.objects.filter(team_id=i.team_id).exists():
    #         Finals.objects.create(tournament_id=tournament_id, team_id=i.team_id)
    #         print(i.team_id)    
        
    context = {}
    # context['teams'] = top_4_teams
    context['tournament'] = Tournament.objects.get(id=tournament_id)
    
    context['teams'] = PosThree.objects.filter(tournament_id=tournament_id)
    context['finals_teams'] = Finals.objects.filter(tournament_id=tournament_id)
    
    context['opponent'] = Team.objects.filter(tournament_id=tournament_id)
    for i in context['opponent']:
        print(i)

    # return JsonResponse({'status': 'success', 'teams': list(top_4_teams.values())})
    return render(request, 'finals.html', context)

def final_results(request, tournament_id):
    # get the opponent with the highest score ein pos three
    third_place = PosThree.objects.filter(tournament_id=tournament_id).annotate(highest_score=Max(F('team_score'), F('opponent_score'))).order_by('-highest_score')[:1]
    second_place = Finals.objects.filter(tournament_id=tournament_id).annotate(highest_score=Max(F('team_score'), F('opponent_score'))).order_by('-highest_score')[:1]
    first_place = Finals.objects.filter(tournament_id=tournament_id).annotate(highest_score=Max(F('team_score'), F('opponent_score'))).order_by('-highest_score')[:1]
    context = {}
    context['third_place'] = third_place
    context['second_place'] = second_place
    context['first_place'] = first_place
    
    
    return JsonResponse({'message': 'success'})