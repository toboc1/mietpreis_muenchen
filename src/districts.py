"""
Ordnet die feingranularen regio3-Werte 
aus den 25 offiziellen Münchner Stadtbezirken zu.
Werte die hier fehlen (Landkreis-Gemeinden wie Ottobrunn, Grünwald etc.),
gehören nicht zur Stadt München und werden in data_prep.py rausgefiltert
"""

REGIO3_TO_DISTRICT = {
    "Altstadt": "Altstadt-Lehel",
    "Lehel": "Altstadt-Lehel",
    "Ludwigsvorstadt_Isarvorstadt": "Ludwigsvorstadt-Isarvorstadt",
    "Maxvorstadt": "Maxvorstadt",
    "Schwabing_West": "Schwabing-West",
    "Au": "Au-Haidhausen",
    "Haidhausen": "Au-Haidhausen",
    "Sendling": "Sendling",
    "Sendling_Westpark": "Sendling-Westpark",
    "Schwanthalerhöhe": "Schwanthalerhöhe",
    "Neuhausen": "Neuhausen-Nymphenburg",
    "Nymphenburg": "Neuhausen-Nymphenburg",
    "Moosach": "Moosach",
    "Milbertshofen": "Milbertshofen-Am Hart",
    "Am_Hart": "Milbertshofen-Am Hart",
    "Schwabing": "Schwabing-Freimann",  # ImmoScout trennt "Schwabing" nicht weiter auf; PLZ-Check (80802-80807) legt eher Freimann-Seite nahe
    "Freimann": "Schwabing-Freimann",
    "Bogenhausen": "Bogenhausen",
    "Berg_am_Laim": "Berg am Laim",
    "Trudering": "Trudering-Riem",
    "Riem": "Trudering-Riem",
    "Ramersdorf": "Ramersdorf-Perlach",
    "Perlach": "Ramersdorf-Perlach",
    "Obergiesing": "Obergiesing-Fasangarten",
    "Untergiesing": "Untergiesing-Harlaching",
    "Harlaching": "Untergiesing-Harlaching",
    "Thalkirchen": "Thalkirchen-Obersendling-Forstenried-Fürstenried-Solln",
    "Obersendling": "Thalkirchen-Obersendling-Forstenried-Fürstenried-Solln",
    "Forstenried": "Thalkirchen-Obersendling-Forstenried-Fürstenried-Solln",
    "Fürstenried": "Thalkirchen-Obersendling-Forstenried-Fürstenried-Solln",
    "Solln": "Thalkirchen-Obersendling-Forstenried-Fürstenried-Solln",
    "Hadern": "Hadern",
    "Pasing": "Pasing-Obermenzing",
    "Obermenzing": "Pasing-Obermenzing",
    "Aubing": "Aubing-Lochhausen-Langwied",
    "Lochhausen": "Aubing-Lochhausen-Langwied",
    "Langwied": "Aubing-Lochhausen-Langwied",
    "Allach": "Allach-Untermenzing",
    "Untermenzing": "Allach-Untermenzing",
    "Feldmoching": "Feldmoching-Hasenbergl",
    "Hasenbergl": "Feldmoching-Hasenbergl",
    "Laim": "Laim",
}

CITY_DISTRICTS = sorted(set(REGIO3_TO_DISTRICT.values())) # 42 von 71 regio3-Werten sind Stadt-München, Rest ist Landkreis - die fehlen hier bewusst