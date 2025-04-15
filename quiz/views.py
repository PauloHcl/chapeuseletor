from django.shortcuts import render, redirect
from .models import Participant
import random

questions = [
    {
        "question": "Qual dessas qualidades você mais valoriza?",
        "answers": [("A", "Coragem"), ("B", "Ambição"), ("C", "Inteligência"), ("D", "Lealdade")]
    },
    {
        "question": "Se você encontrasse uma bolsa cheia de galeões caída no chão, o que faria?",
        "answers": [("A", "Procuraria o dono imediatamente"), ("B", "Guardaria – é a sorte sorrindo para mim"),
                    ("C", "Investigaria a origem antes de decidir"), ("D", "Dividiria com quem precisasse mais")]
    },
    {
        "question": "Como você prefere passar o tempo livre?",
        "answers": [("A", "Aventurando-se ao ar livre"), ("B", "Planejando seus próximos objetivos"),
                    ("C", "Lendo ou aprendendo algo novo"), ("D", "Com amigos ou ajudando alguém")]
    },
    {
        "question": "Qual dessas criaturas mágicas você gostaria de ter como companheira?",
        "answers": [("A", "Hipogrifo"), ("B", "Basilisco"), ("C", "Coruja sábia"), ("D", "Pelúcio brincalhão")]
    },
    {
        "question": "Qual feitiço te representa melhor?",
        "answers": [("A", "Expelliarmus"), ("B", "Imperio"), ("C", "Legilimens"), ("D", "Lumos")]
    },
    {
        "question": "Você se destaca mais por...",
        "answers": [("A", "Atitudes ousadas"), ("B", "Liderança estratégica"), ("C", "Sabedoria e lógica"),
                    ("D", "Bondade e empatia")]
    },
    {
        "question": "Diante de um desafio, você...",
        "answers": [("A", "Enfrenta de frente, sem hesitar"), ("B", "Calcula os riscos e elabora um plano"),
                    ("C", "Estuda todas as possibilidades"), ("D", "Confia no trabalho em equipe")]
    },
]

house_map = {
    "A": "Grifinória",
    "B": "Sonserina",
    "C": "Corvinal",
    "D": "Lufa-Lufa",
}

def index(request):
    if request.method == "POST":
        nick = request.POST['nick']
        if Participant.objects.filter(nick=nick).exists():
            return render(request, 'quiz/index.html', {"error": "Nick já utilizado."})
        request.session['nick'] = nick
        return redirect('quiz')
    return render(request, 'quiz/index.html')

def quiz(request):
    if request.method == "POST":
        nick = request.session.get('nick')
        responses = request.POST
        scores = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
        answers = {}

        for key in responses:
            if key.startswith("q"):
                answer = responses[key]
                answers[key] = answer
                scores[answer] += 1

        max_score = max(scores.values())
        tied = [house_map[k] for k, v in scores.items() if v == max_score]

        request.session['answers'] = answers
        request.session['tied'] = tied

        if len(tied) == 1:
            house = tied[0]
            Participant.objects.create(nick=nick, answers=answers, final_house=house)
            return redirect('result')
        else:
            return redirect('choose_house')

    shuffled_questions = random.sample(questions, len(questions))
    for q in shuffled_questions:
        q['shuffled_answers'] = random.sample(q['answers'], len(q['answers']))
    return render(request, 'quiz/quiz.html', {'questions': shuffled_questions})

def choose_house(request):
    if request.method == "POST":
        house = request.POST['house']
        nick = request.session.get('nick')
        answers = request.session.get('answers')
        Participant.objects.create(nick=nick, answers=answers, final_house=house)
        return redirect('result')

    return render(request, 'quiz/choose_house.html', {'tied': request.session['tied']})

def result(request):
    house = Participant.objects.get(nick=request.session['nick']).final_house
    return render(request, 'quiz/result.html', {'house': house})
from django.shortcuts import render
from .models import Participant

def participantes(request):
    participantes = Participant.objects.all()
    return render(request, 'quiz/participantes.html', {'participantes': participantes})
