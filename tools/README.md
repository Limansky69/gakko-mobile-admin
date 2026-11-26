Narzędzia testowe prototypu Gakko Admin (Python 3 + Playwright: pip install playwright --break-system-packages && playwright install chromium)

flowx.py      python3 flowx.py /ścieżka/work.html flows/nfb.json   -> na końcu "errors: []"; zrzuty w /home/claude/shots
              Loguje się sam (localStorage gakko-admin-auth), więc scenariusze nie zatrzymują się na ekranie logowania.
run_all.sh    bash run_all.sh /ścieżka/work.html   -> cała regresja: e1 nfb cfm md rv2 z1b del more au au4 au6
scan_tekst.py GAKKO_HTML=/ścieżka/work.html python3 scan_tekst.py -> "·", "•", AM/PM, interpunkcja, zakresy godzin/dat inne niż " – "
drag.py       pomocnicze funkcje setup/lay/drag do testów przeciągania widżetów Pulpitu (from drag import *)

Scenariusze:
  nfb.json, z1b.json – aktualne wersje nf i z1 (nowe pola: prowadzący i sala to przycisk z listą, data-tg="open").
  nf.json, z1.json   – stare, zostawione dla porównania; odwołują się do usuniętych pól #ttF-lect i #ttRS.
  md.json (kroki 4–5, #ttF-to) i z1b.json (kroki 20–24, .tt-cfw) mają kroki dla dawnego interfejsu – te JSERR są znane, "errors: []" na końcu się liczy.
