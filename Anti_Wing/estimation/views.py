from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import TestForm
from scraping.models import RaceInfo, RaceResult


# Create your views here.
class EstimationView(TemplateView):
    template_name = "estimation.html"

    def get(self, request):
        context = {'form': TestForm()}

        return render(request, self.template_name, context)

    def post(self, request):
        # 入力値を取得
        f = TestForm(request.POST)
        horse_id = f['horse_id'].value()
        distance = f['distance'].value()
        ground_type = f['ground_type'].value()
        ground_condition = f['ground_condition'].value()

        # horse_idから、学習に使用するデータを取得する
        queryset = RaceInfo.objects.select_related('RaceResult').filter(raceresult__horse_id=horse_id).values('raceresult__horse_weight', 'distance', 'ground_type', 'ground_condition')
        c = queryset[:]
        ground_condition_dict = {'良': 0, '稍重': 1, '重': 2}
        d = [{key: ground_condition_dict.get(value, value) for key, value in my_dict.items()} for my_dict in c]
        return render(request, self.template_name)
