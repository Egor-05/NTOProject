from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        import csv
        from .models import ShareInfo

        with open('main/data.csv') as csv_file:
            reader = csv.DictReader(csv_file)
            fieldnames = {i: [] for i in set(reader.fieldnames[1:])}
            for row in reader:
                for i in fieldnames:
                    fieldnames[i].append(float(row[i]))
            si_names = [i.name for i in ShareInfo.objects.all()]
            for i in fieldnames:
                si = ShareInfo(name=i, info=fieldnames[i])
                if si.name not in si_names:
                    si_names.append(si.name)
                    si.save()
