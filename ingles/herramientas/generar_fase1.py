#!/usr/bin/env python3
"""Genera ingles/fase1.html (Fase 1 día por día) a partir de los datos de este archivo.

Uso:  python3 ingles/herramientas/generar_fase1.py
Reutiliza el <style> de ingles/index.html para que ambas páginas se vean igual.
"""
import datetime as dt
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
OUT = ROOT / "fase1.html"

base_css = re.search(r"<style>(.*?)</style>", INDEX.read_text(encoding="utf-8"), re.S).group(1)

EXTRA_CSS = """
.mono,code,a{overflow-wrap:anywhere}
.week{margin:14px 0}
.day{border-top:1px solid var(--line);padding:12px 0}
.day:first-of-type{border-top:0}
.dayhead{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-bottom:6px}
.dayhead b{font-size:1rem}
.dayhead label{margin-left:auto;font-size:.85rem;display:flex;gap:6px;align-items:center;color:var(--muted)}
.dayhead input{width:18px;height:18px;accent-color:var(--accent)}
.t-turno{background:var(--warn-soft);color:var(--warn)}
.t-libre{background:var(--ok-soft);color:var(--ok)}
.t-sab{background:var(--accent-soft);color:var(--accent)}
.t-ligera{background:var(--op-soft);color:var(--op)}
.t-cp{background:var(--bad-soft);color:var(--bad)}
.blocks{list-style:none;margin:0;padding:0}
.blocks li{display:grid;grid-template-columns:118px 1fr;gap:2px 12px;padding:4px 0;font-size:.93rem}
.blocks li .h{color:var(--muted);font-variant-numeric:tabular-nums;font-size:.85rem;padding-top:.1em}
.blocks li.rest{color:var(--muted)}
.lesson{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin:14px 0}
.lesson h3{margin-top:0}
.lesson ol li{margin:4px 0}
.hint{color:var(--muted);font-size:.88rem}
.lesson details{margin:10px 0 0;border-radius:8px}
.lesson details > summary{padding:8px 12px;font-size:.92rem}
.lesson details.hintd{display:block;margin:2px 0 0;border:0;background:transparent}
.lesson details.hintd > summary{display:inline;padding:0;font-size:.82rem;font-weight:500;color:var(--accent)}
.lesson details.hintd > .in{padding:2px 0 0}
.tpl{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}
@media (max-width:520px){ .blocks li{grid-template-columns:1fr} .blocks li .h{padding-top:0} }
@media print{ .dayhead label{display:none} }
"""

# ---------------------------------------------------------------- lecciones de gramática
# Cada lección: (titulo, explicación HTML, [(ejercicio, pista o ""), ...], [respuestas])
L = {}
L[1] = ("<i>to be</i> (am / is / are) y pronombres", """
<p><b>I am</b> · <b>you are</b> · <b>he / she / it is</b> · <b>we / you / they are</b>. Negativo: agrega <i>not</i> (<i>I'm not, she isn't, they aren't</i>). Pregunta: invierte el orden (<i>Are you…? Is she…?</i>).</p>
<p><b>Dos trampas para hispanohablantes:</b> (1) las oraciones en inglés casi siempre necesitan sujeto, aunque en español no lo pongas: "Es tarde" → <i>It's late</i>. La excepción son las órdenes e instrucciones (<i>Open the file. Select the layer.</i>), muy comunes en el software. (2) Varias cosas que en español van con "tener" en inglés van con <i>be</i>: "tengo 20 años" → <i>I'm 20</i>; "tengo hambre" → <i>I'm hungry</i>.</p>
<p>Respuestas cortas: <i>Yes, I am. / No, she isn't.</i> En la afirmativa corta no se contrae (<i>Yes, I am</i>, nunca <i>Yes, I'm</i>).</p>""",
 [("My name ___ Sam.", ""), ("I ___ 22 years old.", "En español usarías \"tener\"."), ("___ late. (Es tarde.)", "¿Qué le falta a esta oración que en español no hace falta?"),
  ("They ___ at work.", ""), ("___ you a student?", "Pregunta: el verbo va primero."), ("She is hungry. → negativo", ""),
  ("Traduce: \"No estoy cansado.\"", ""), ("Are you from Mexico? — Yes, ___.", "Respuesta corta afirmativa.")],
 ["is", "am", "It's / It is", "are", "Are", "She isn't hungry. / She's not hungry.", "I'm not tired.", "I am"])
L[2] = ("Posesivos y <i>this / that / these / those</i>", """
<p><b>my, your, his</b> (de él), <b>her</b> (de ella), <b>its</b> (de una cosa), <b>our, their</b>. Para personas: <b>'s</b> → <i>Ana's laptop</i> (la laptop de Ana).</p>
<p>En español "su" sirve para todo; en inglés tienes que decidir de quién es: <i>his</i> o <i>her</i>, <i>its</i> o <i>their</i>.</p>
<p><b>this</b> (aquí, singular) · <b>these</b> (aquí, plural) · <b>that</b> (allá, singular) · <b>those</b> (allá, plural).</p>
<p><b>it's</b> = <i>it is</i>; <b>its</b> = posesivo. Se oyen igual.</p>""",
 [("This is ___ laptop. (de ella)", ""), ("___ name is Carlos. (de él)", ""), ("The studio is big. ___ computers are new.", "¿De quién son las computadoras? De una cosa."),
  ("___ is my phone. (aquí, uno)", ""), ("___ are my headphones. (allá, varios)", ""), ("Es la laptop de Ana → This is ___.", ""),
  ("Corrige: \"Maria and Luis are in they house.\"", "they = ellos (sujeto). ¿Cuál es el posesivo?"), ("___ a good film. ___ story is sad.", "Uno es \"it is\" y el otro es posesivo.")],
 ["her", "His", "Its", "This", "Those", "Ana's laptop", "their house", "It's / Its"])
L[3] = ("Presente simple: afirmativo", """
<p>Para rutinas, hechos y gustos. <b>I / you / we / they work</b>. <b>He / she / it works</b>: la tercera persona del singular lleva <b>-s</b>.</p>
<p>Ortografía: <b>-es</b> después de s, sh, ch, x, o (<i>watches, goes, does</i>); consonante + y → <b>-ies</b> (<i>study → studies</i>); <i>have → has</i>.</p>""",
 [("I ___ (work) at night.", ""), ("She ___ (study) animation.", "Termina en consonante + y."), ("My brother ___ (watch) anime every day.", ""),
  ("The shift ___ (start) at 8 pm.", "\"The shift\" = it."), ("We ___ (go) to school on Mondays.", ""), ("He ___ (have) a new phone.", "Es irregular."),
  ("Corrige: \"My friend work in a studio.\"", ""), ("Escribe 2 oraciones: una sobre ti y una sobre un amigo.", "La del amigo necesita -s.")],
 ["work", "studies", "watches", "starts", "go", "has", "My friend works in a studio.", "Libre. Revisa la -s en la del amigo."])
L[4] = ("Presente simple: negativo y preguntas", """
<p>Negativo: <b>don't</b> + verbo (I, you, we, they) · <b>doesn't</b> + verbo (he, she, it). Pregunta: <b>Do</b> you…? / <b>Does</b> she…?</p>
<p><b>Regla clave:</b> cuando aparece <i>does</i> o <i>doesn't</i>, el verbo principal <u>pierde</u> la -s: <i>She doesn't work</i> (no <i>doesn't works</i>).</p>
<p>Con palabra interrogativa: <i>What do you do? Where does he live? What time do you start?</i></p>""",
 [("I ___ like horror films.", ""), ("She ___ work on Mondays.", ""), ("___ you speak English?", ""), ("___ he live near here?", ""),
  ("Corrige: \"She doesn't works at night.\"", "¿Cuántas veces marcas la tercera persona?"), ("Corrige: \"Does he plays games?\"", ""),
  ("Haz la pregunta para esta respuesta: \"They start at 8.\"", "Empieza con What time…"), ("Traduce: \"¿A qué te dedicas?\"", "Es una pregunta fija en inglés.")],
 ["don't", "doesn't", "Do", "Does", "She doesn't work at night.", "Does he play games?", "What time do they start?", "What do you do?"])
L[5] = ("<i>there is / there are</i>, <i>a / an</i>, <i>some / any</i>", """
<p><b>There is</b> + singular (<i>There's a computer</i>) · <b>There are</b> + plural (<i>There are two monitors</i>). Negativo: <i>there isn't / there aren't any</i>. Pregunta: <i>Is there…? Are there any…?</i></p>
<p><b>a</b> antes de <u>sonido</u> de consonante, <b>an</b> antes de <u>sonido</u> de vocal: <i>a laptop, a university</i> (suena "yu"), <i>an animator, an hour</i> (la h no suena).</p>
<p><b>some</b> en afirmativo; <b>any</b> en negativo y preguntas. Excepción: al ofrecer o pedir algo, la pregunta usa <i>some</i> (<i>Would you like some water? Can I have some help?</i>). Plurales irregulares: <i>person → people, child → children, man → men, woman → women</i>.</p>""",
 [("There ___ a desk in my room.", ""), ("There ___ three chairs.", ""), ("___ there a bathroom here?", ""), ("There aren't ___ windows.", ""),
  ("I have ___ idea.", ""), ("She's ___ university student.", "Fíjate en el sonido, no en la letra."), ("There are ten ___ (person) in the class.", ""),
  ("Describe tu lugar de trabajo en 3 oraciones con there is / there are.", "")],
 ["is", "are", "Is", "any", "an", "a", "people", "Libre."])
L[6] = ("Preposiciones <i>in / on / at</i>", """
<p><b>Tiempo:</b> <b>at</b> + hora (<i>at 8 pm, at night</i>) · <b>on</b> + día o fecha (<i>on Monday, on November 9</i>) · <b>in</b> + mes, año o parte del día (<i>in March, in 2027, in the morning</i>). Ojo: <i>at night</i>, pero <i>in the morning / in the evening</i>.</p>
<p><b>Lugar:</b> <b>in</b> = dentro (<i>in my room, in Mexico</i>) · <b>on</b> = sobre una superficie (<i>on the desk, on the wall</i>) · <b>at</b> = punto o lugar de actividad (<i>at work, at school, at home</i>).</p>""",
 [("I start work ___ 8 pm.", ""), ("I don't work ___ Monday.", ""), ("My birthday is ___ March.", ""), ("I study ___ night.", ""),
  ("I'm ___ work now.", ""), ("The poster is ___ the wall.", ""), ("She lives ___ Mexico City.", ""), ("We have class ___ the morning.", "")],
 ["at", "on", "in", "at", "at", "on", "in", "in"])
L[7] = ("Presente continuo", """
<p><b>am / is / are + verbo-ing</b>: lo que pasa ahora o en esta temporada. <i>I'm working. She's studying.</i> Negativo: <i>I'm not watching</i>. Pregunta: <i>Are you listening? What are you doing?</i></p>
<p>Ortografía: <i>make → making</i> (se va la e) · <i>sit → sitting</i> (se duplica la consonante) · <i>study → studying</i>.</p>""",
 [("I ___ (listen) to a podcast now.", ""), ("She ___ (write) an email.", "¿Qué le pasa a la e final?"), ("They ___ (not / watch) TV.", ""),
  ("___ you ___ (work) now?", ""), ("What ___ he ___ (do)?", ""), ("We ___ (sit) in the park.", ""),
  ("Traduce: \"Estoy aprendiendo inglés.\"", ""), ("Corrige: \"I working now.\"", "Falta una pieza.")],
 ["am listening / 'm listening", "is writing", "aren't watching", "Are … working", "is … doing", "are sitting", "I'm learning English.", "I'm working now."])
L[8] = ("Presente simple vs continuo + <i>always, usually, never</i>", """
<p><b>Simple</b> = hábito, siempre (<i>I work at night</i>). <b>Continuo</b> = ahora, temporal (<i>I'm studying right now</i>).</p>
<p>Los adverbios de frecuencia (<i>always, usually, often, sometimes, never</i>) van <u>antes</u> del verbo principal (<i>I usually sleep at 2</i>) pero <u>después</u> de <i>be</i> (<i>I'm always tired</i>).</p>
<p>Verbos de estado casi nunca van en continuo: <i>like, love, know, want, need, understand</i> → <i>I understand</i>, no <i>I'm understanding</i>.</p>
<p>Ojo con <b>have</b>: cuando significa "tener" no va en continuo (<i>I have a phone</i>), pero en acciones sí (<i>I'm having breakfast, We're having a good time</i>).</p>""",
 [("I usually ___ (sleep) at 2 am.", ""), ("Look! It ___ (rain).", ""), ("She ___ (study) English every day.", ""), ("Shh, I ___ (watch) a lesson.", ""),
  ("Pon el adverbio: \"I am tired after work.\" (always)", "Va después de be."), ("Pon el adverbio: \"He drinks coffee.\" (never)", ""),
  ("Corrige: \"I'm understanding now.\"", ""), ("Escribe 1 oración de tu rutina y 1 de lo que haces ahora.", "")],
 ["sleep", "is raining", "studies", "am watching", "I am always tired after work.", "He never drinks coffee.", "I understand now.", "Libre."])
L[9] = ("<i>can / can't</i>", """
<p><b>can + verbo base</b>: habilidad, posibilidad o permiso. <i>I can draw. She can use Blender.</i> Nunca lleva -s ni <i>to</i>: no <i>she cans</i>, no <i>can to swim</i>.</p>
<p>Negativo: <b>can't</b> (cannot). Pregunta: <i>Can you help me? Can I…?</i> (pedir permiso).</p>""",
 [("I ___ draw, but I ___ sing. (sí / no)", ""), ("She ___ use Blender.", ""), ("___ you help me?", ""), ("Corrige: \"He cans speak English.\"", ""),
  ("Corrige: \"I can to swim.\"", ""), ("Pide permiso para usar el baño.", ""), ("Traduce: \"¿Puedes repetir, por favor?\"", "Frase muy útil."),
  ("Escribe 3 cosas que puedes hacer en tu software favorito.", "")],
 ["can / can't", "can", "Can", "He can speak English.", "I can swim.", "Can I use the bathroom?", "Can you repeat that, please?", "Libre."])
L[10] = ("Pronombres objeto + <i>like / love / hate</i> + -ing", """
<p>Sujeto → objeto: <i>I → me, you → you, he → him, she → her, it → it, we → us, they → them</i>. Van después del verbo o de una preposición: <i>Call me. I like her. With them.</i></p>
<p><i>like / love / hate / enjoy</i> + <b>-ing</b>: <i>I like drawing</i>. Con <i>like, love</i> y <i>hate</i> también se usa <i>to</i> (<i>I like to draw</i>), sobre todo en inglés americano; con <i>enjoy</i>, solo -ing.</p>""",
 [("Can you help ___? (a mí)", ""), ("I love this film. I watch ___ every year.", ""), ("Ana is my friend. I talk to ___ every day.", ""),
  ("My parents? I call ___ on Sundays.", ""), ("I enjoy ___ (draw).", ""), ("She hates ___ (wake) up early. (Usa -ing.)", "¿Qué le pasa a la e?"),
  ("Corrige: \"I like she.\"", ""), ("Escribe 2 cosas que te encanta hacer y 1 que odias.", "")],
 ["me", "it", "her", "them", "drawing", "waking (<i>to wake</i> también es correcto, pero aquí practicamos -ing)", "I like her.", "Libre."])
L[11] = ("<i>was / were</i>", """
<p>Pasado de <i>be</i>: <b>I / he / she / it was</b> · <b>you / we / they were</b>. Negativo: <i>wasn't / weren't</i>. Pregunta: <i>Was it…? Were you…?</i></p>
<p>Expresiones de tiempo: <i>yesterday, last night, last week, two days ago</i> (<i>ago</i> va después: "hace dos días" → <i>two days ago</i>).</p>""",
 [("I ___ tired yesterday.", ""), ("They ___ at work last night.", ""), ("The film ___ very good.", ""), ("We ___ at home. (negativo)", ""),
  ("___ you at school yesterday?", ""), ("Where ___ she last night?", ""), ("Traduce: \"Hace dos días estaba enfermo.\"", "ago va al final."), ("Corrige: \"They was happy.\"", "")],
 ["was", "were", "was", "weren't", "Were", "was", "I was sick two days ago.", "They were happy."])
L[12] = ("Pasado simple regular (-ed)", """
<p>Verbo + <b>-ed</b>, igual para todas las personas: <i>I worked, she worked</i>. Ortografía: <i>like → liked, study → studied, stop → stopped</i>.</p>
<p><b>Pronunciación (3 sonidos):</b> /t/ después de sonidos sordos (<i>worked, watched, stopped</i>) · /d/ después de sonidos sonoros (<i>played, called, listened</i>) · /ɪd/ <u>solo</u> después de t o d (<i>wanted, needed, started</i>). Error típico: decir "work-ed" con una sílaba de más.</p>""",
 [("I ___ (work) until 7 am.", ""), ("She ___ (study) for the test.", ""), ("We ___ (watch) a movie.", ""), ("He ___ (stop) the video.", "Una consonante se duplica."),
  ("Clasifica por sonido: worked, played, wanted, listened, watched, needed", "Solo dos agregan una sílaba."), ("¿Cuántas sílabas tiene \"worked\"?", ""),
  ("Escribe 3 cosas que hiciste ayer con verbos regulares.", "")],
 ["worked", "studied", "watched", "stopped", "/t/: worked, watched · /d/: played, listened · /ɪd/: wanted, needed", "Una.", "Libre."])
L[13] = ("Pasado irregular: los 30 más comunes", """
<p>Apréndelos con Anki en dirección español → pasado (5 al día): <i>be → was/were · have → had · do → did · go → went · get → got · make → made · say → said · see → saw · know → knew · think → thought · take → took · come → came · give → gave · find → found · tell → told · feel → felt · leave → left · buy → bought · bring → brought · begin → began · eat → ate · drink → drank · sleep → slept · write → wrote · read → read</i> (se pronuncia "red") · <i>speak → spoke · meet → met · pay → paid · sit → sat · put → put</i>.</p>""",
 [("Yesterday I ___ (go) to work at 8.", ""), ("I ___ (sleep) only 3 hours.", ""), ("She ___ (buy) a new tablet.", ""), ("We ___ (eat) tacos.", ""),
  ("He ___ (read) the whole book.", "Se escribe igual; cambia el sonido."), ("I ___ (make) a short animation.", ""),
  ("Escribe una historia de 5 oraciones sobre tu fin de semana con 4 verbos irregulares.", "")],
 ["went", "slept", "bought", "ate", "read (\"red\")", "made", "Libre."])
L[14] = ("Pasado simple: negativo y preguntas", """
<p><b>didn't + verbo base</b>: <i>I didn't go</i> (no <i>didn't went</i>). Pregunta: <b>Did</b> you + verbo base…? Con palabra interrogativa: <i>What did you do? Where did she go?</i></p>
<p>El pasado se marca <u>una sola vez</u>: si ya está <i>did</i>, el verbo va en base. Excepción: con <i>be</i> no se usa did → <i>I wasn't tired. Were you tired?</i></p>""",
 [("I ___ (not / sleep) well.", ""), ("She didn't ___ (go) to class.", ""), ("___ you see the new Pixar film?", ""), ("What ___ you ___ (do) last night?", ""),
  ("Corrige: \"I didn't went.\"", "¿Quién lleva el pasado: did o el verbo?"), ("Corrige: \"Did you saw it?\"", ""), ("Corrige: \"Did you tired?\"", "tired no es un verbo."),
  ("Haz 2 preguntas sobre el fin de semana de alguien.", "")],
 ["didn't sleep", "go", "Did", "did … do", "I didn't go.", "Did you see it?", "Were you tired?", "Libre."])
L[15] = ("<i>going to</i> y <i>will</i>", """
<p><b>am / is / are + going to + verbo</b>: planes ya decididos (<i>I'm going to study tonight</i>) y predicciones con evidencia (<i>Look at those clouds, it's going to rain</i>).</p>
<p><b>will + verbo</b>: decisión en el momento (<i>I'll help you</i>), promesas (<i>I won't forget</i>) y opiniones sobre el futuro (<i>I think it will be hard</i>). Nunca <i>will to</i>.</p>""",
 [("Plan decidido: \"Next year I ___ (do) a master's degree.\"", ""), ("Decisión en el momento: \"The phone is ringing.\" — \"I ___ (answer) it.\"", ""),
  ("Promesa: \"I ___ (not / forget).\"", ""), ("Opinión: \"I think the exam ___ (be) difficult.\"", ""), ("Evidencia: \"Look at the sky! It ___ (rain).\"", ""),
  ("Corrige: \"I will to call you.\"", ""), ("Escribe 3 planes para 2027 con going to.", "")],
 ["am going to do / 'm going to do", "'ll answer / will answer", "won't forget", "will be", "is going to rain", "I'll call you. / I will call you.", "Libre."])
L[16] = ("Comparativos y superlativos", """
<p><b>Corto</b> (1 sílaba): <i>fast → faster → the fastest</i>; <i>big → bigger</i>. Terminado en -y: <i>easy → easier → the easiest</i>. <b>Largo</b> (3 o más sílabas): <i>more difficult → the most difficult</i>. Con 2 sílabas varía: las que terminan en -y usan -ier (<i>easy → easier, happy → happier</i>); muchas otras usan <i>more</i> (<i>more famous, more modern</i>). Irregulares: <i>good → better → the best · bad → worse → the worst</i>.</p>
<p>Para comparar se usa <b>than</b>: <i>Maya is more expensive than Blender</i>. Igualdad: <i>as … as</i> (<i>as good as</i>).</p>""",
 [("Blender is ___ (cheap) than Maya.", ""), ("English is ___ (easy) than Chinese.", ""), ("This course is ___ (difficult) than the last one.", ""),
  ("It's the ___ (good) film of the year.", "Irregular."), ("My laptop is ___ (bad) than yours.", ""), ("Corrige: \"She is more tall than me.\"", "tall es corto."),
  ("Corrige: \"It's the more interesting.\"", ""), ("Compara 2 películas animadas en 3 oraciones.", "")],
 ["cheaper", "easier", "more difficult", "best", "worse", "She is taller than me.", "It's the most interesting.", "Libre."])

# ---------------------------------------------------------------- contracciones y habla conectada
C = {}
C[1] = ("Contracciones de <i>be</i>", """
<p><i>I'm · you're · he's · she's · it's · we're · they're · isn't · aren't · I'm not</i> (<i>amn't</i> no se usa en el inglés americano estándar: se dice <i>I'm not</i>, y en preguntas <i>aren't I?</i>). Al hablar se usan casi siempre; la forma completa (<i>I am</i>) suena enfática o formal.</p>
<p>Ojo: <i>he's / she's / it's</i> pueden ser <i>is</i> o <i>has</i>: <i>He's tired</i> (is) / <i>He's finished</i> (has).</p>
<p>Para el oído: <i>they're, their, there</i> suenan igual; <i>it's</i> e <i>its</i> también. El contexto te dice cuál es.</p>""")
C[2] = ("<i>don't / doesn't</i> y <i>do you</i> rápido", """
<p><i>don't, doesn't</i>. En habla rápida <b>do you</b> se reduce a algo como "d'ya": <i>Do you want…?</i> → "D'ya want…?"; <i>What do you do?</i> → "Whaddaya do?".</p>
<p>Si en la escucha oyes "d'ya" al inicio, casi seguro es una pregunta.</p>""")
C[3] = ("Palabras pequeñas que casi desaparecen", """
<p>Esta es probablemente la razón por la que "captas palabras pero no entiendes". En inglés, las palabras de contenido (sustantivos, verbos) llevan acento y las palabras de función se debilitan: <b>a</b> → /ə/ · <b>of</b> → /əv/ o /ə/ (<i>a lot of</i> → "a lotta") · <b>and</b> → "n" (<i>you and me</i> → "you 'n' me") · <b>to</b> → /tə/ · <b>for</b> → /fər/ · <b>there's</b>.</p>
<p>Escuchas bien <i>LOT</i> y <i>COFFEE</i>, pero no las piezas que las unen. Eso se entrena con dictado.</p>""")
C[4] = ("-ing → -in' y <i>what are you</i>", """
<p>En habla relajada, <i>doing, going, working</i> suenan "doin', goin', workin'". <i>What are you doing?</i> → "Whatcha doin'?" o "What're ya doin'?"; <i>are</i> se reduce a /ər/.</p>""")
C[5] = ("<i>can</i> vs <i>can't</i> y <i>wanna</i>", """
<p>En inglés americano, <b>can</b> en una oración es débil ("c'n": <i>I c'n go</i>) y <b>can't</b> es fuerte, con vocal abierta y la t casi muda (<i>I CAN'T go</i>). No esperes oír la t. Pero ojo: <i>can</i> también puede ir acentuado (<i>Yes, I CAN</i>), así que ninguna pista sola es infalible; combina acento, vocal y contexto.</p>
<p><b>want to → wanna</b> (<i>I wanna go</i>). Solo con <i>want to</i>: <i>he wants to</i> no se convierte en "wanna".</p>""")
C[6] = ("<i>wasn't / weren't</i>, -ed y la T americana", """
<p><i>wasn't, weren't</i>. Repasa los 3 sonidos de -ed (lección 12).</p>
<p><b>En inglés americano, la T entre vocales, cuando la sílaba que sigue no lleva acento, suena como la "r" suave del español</b> (la de "pero"): <i>water</i> → "wárer", <i>better</i> → "bérer", <i>a lot of</i> → "a lárov", <i>get it</i> → "gérit", <i>what is</i> → "wáris". Si la sílaba con la T lleva el acento, no pasa (<i>attack</i>). Una vez que lo notas, lo oyes en todas partes.</p>""")
C[7] = ("Repaso con VOA <i>How to Pronounce</i>", """
<p>En Kiwix, abre <b>VOA Learning → How to Pronounce</b> (158 videos de 2 min, inglés americano). Mira los que tienen frases completas (por ejemplo <i>What Are You Doing This Weekend?</i> o <i>I Am Going to…</i>), fíjate cómo se unen y reducen las palabras, y repite con ellos las contracciones 1–6.</p>""")
C[8] = ("<i>didn't, didja, gonna, I'll, won't</i>", """
<p><b>did you → "didja"</b> (<i>Did you see it?</i> → "Didja see it?"); <b>what did you → "whadja"</b>. <b>going to → gonna</b>, <u>solo</u> cuando le sigue un verbo: <i>I'm gonna study</i> sí; <i>I'm going to school</i> nunca se convierte en "gonna school".</p>
<p><i>I'll</i> suena parecido a "ail". <b>won't</b> /woʊnt/ vs <b>want</b> /wɑnt/: la diferencia está en la vocal (won't suena "ou"). Otra pista: después de <i>won't</i> va el verbo directo (<i>I won't go</i>); después de <i>want</i> va <i>to</i> (<i>I want to go</i> → "I wanna go").</p>""")
C[9] = ("<i>gotta, hafta, lemme, gimme, dunno, kinda</i>", """
<p><i>got to → gotta</i> (<i>I gotta go</i>) · <i>have to → hafta</i> · <i>has to → hasta</i> · <i>let me → lemme</i> · <i>give me → gimme</i> · <i>don't know → dunno</i> · <i>kind of → kinda</i> · <i>sort of → sorta</i> · <i>out of → outta</i>.</p>
<p><b>Regla:</b> reconócelas siempre al escuchar. Puedes usarlas al hablar en contextos informales. En escritura formal (incluida la escritura de un examen), <u>nunca</u>. Al hablar, incluso en un examen oral, las reducciones naturales están bien si se entienden.</p>""")

CONTR_METHOD = """<p><b>Cómo practicarlas (10 min):</b> (1) lee la explicación; (2) en la transcripción de la lección LLE de esta semana, subraya cada contracción o reducción que encuentres; (3) escucha esos fragmentos y repítelos 3 veces imitando el ritmo; (4) dictado: escucha 3 oraciones con contracciones, escríbelas exactas y compáralas con el texto.</p>"""

# ---------------------------------------------------------------- semanas
START = dt.date(2026, 11, 9)
DIAS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]

def fecha(d):
    return f"{DIAS[d.weekday()]} {d.day} {MESES[d.month-1]}"

# Por semana: lle = lecciones de Let's Learn English en los turnos [mar, mié, vie, dom]
# la = lección nueva del martes · lb = lección nueva del viernes ("R" = repaso general)
# wa / wb = escritura del martes / viernes · sa = speaking del jueves · sb = speaking del sábado
W = {
 1: dict(lle=[4,5,6,7], la=1, lb=2, c=1, esc="el video <i>Speaking Practice</i> de una lección de esta semana (en Kiwix; su guion está en el PDF del curso)", lec="un cuento de Storybooks Canada nivel 1 (PDF + audio) o relee la <i>Conversation</i> de lecciones pasadas en el PDF",
         wa="5 oraciones: preséntate (nombre, edad, trabajo, qué estudias).", sa="Preséntate en voz alta 1 min.",
         wb="Describe 4 objetos de tu escritorio o mochila con my / this / that.", sb="Describe tu cuarto en voz alta.", tema="About me", atras=None),
 2: dict(lle=[8,9,10,11], la=3, lb=4, c=2, esc="el video <i>Speaking Practice</i> de una lección de esta semana (en Kiwix; su guion está en el PDF del curso)", lec="un cuento de Storybooks Canada nivel 1 (PDF + audio) o relee la <i>Conversation</i> de lecciones pasadas en el PDF",
         wa="6 oraciones: tu rutina en un día de trabajo.", sa="Cuenta tu rutina en 1 min.",
         wb="5 preguntas para un compañero sobre su rutina, con respuestas inventadas.", sb="Hazte las 5 preguntas y contéstalas en voz alta.", tema="My routine", atras=None),
 3: dict(lle=[12,13,14,15], la=5, lb=6, c=3, esc="el video <i>Speaking Practice</i> de una lección de esta semana (en Kiwix; su guion está en el PDF del curso)", lec="un cuento de Storybooks Canada nivel 1 (PDF + audio) o relee la <i>Conversation</i> de lecciones pasadas en el PDF",
         wa="Describe tu lugar de trabajo con there is / there are (6 oraciones).", sa="Describe tu lugar de trabajo en voz alta.",
         wb="Tu semana con in / on / at (horarios, días, lugares).", sb="Cuenta tu semana en 1 min.", tema="My workplace", atras=None),
 4: dict(lle=[16,17,18,19], la=7, lb=8, c=4, esc="el video <i>Speaking Practice</i> de una lección de esta semana (en Kiwix; su guion está en el PDF del curso)", lec="Storybooks Canada nivel 1–2 o la transcripción de un episodio Beginner de Easy Stories (con su audio)",
         wa="6 oraciones de lo que la gente a tu alrededor está haciendo ahora.", sa="Narra en voz alta lo que haces mientras ordenas tu cuarto.",
         wb="Un día normal vs hoy: 3 oraciones de cada uno.", sb="Cuéntalo en 1 min.", tema="A normal day vs today", atras=1),
 5: dict(lle=[20,21,22,23], la=9, lb=10, c=5, esc="Easy Stories in English, un episodio Beginner (con su transcripción gratis)", lec="Storybooks Canada nivel 1–2 o la transcripción de un episodio Beginner de Easy Stories (con su audio)",
         wa="Qué puedes y no puedes hacer (software, dibujo, idiomas, deportes).", sa="Cuéntalo en 1 min.",
         wb="Qué te encanta, te gusta y odias hacer (con -ing).", sb="Cuéntalo en 1 min.", tema="My skills and hobbies", atras=3),
 6: dict(lle=[24,25,26,27], la=11, lb=12, c=6, esc="Easy Stories in English, un episodio Beginner (con su transcripción gratis)", lec="Storybooks Canada nivel 1–2 o la transcripción de un episodio Beginner de Easy Stories (con su audio)",
         wa="Dónde estabas ayer a las 8 am, 12, 4 pm, 10 pm y 2 am (was / were).", sa="Dilo en voz alta.",
         wb="6 cosas que hiciste ayer con verbos regulares.", sb="Cuéntalo cuidando el sonido de -ed.", tema="Yesterday", atras=5,
         irreg="Agrega a Mis frases los primeros 10 verbos de L13 (pasado irregular), cada uno en una frase corta (<i>Yesterday I went to work.</i>)."),
 7: dict(lle=[28,None,29,None], la=13, lb=None, c=7, esc="re-escucha libre", lec="lo que quieras de tu nivel", tema=None, atras=None, ligera=True),
 8: dict(lle=[30,None,31,None], la=None, lb=None, c=7, esc="re-escucha libre", lec="lo que quieras de tu nivel", tema=None, atras=None, ligera=True),
 9: dict(lle=[32,33,34,35], la=14, lb=15, c=8, esc="Easy Stories in English (un episodio Beginner, con transcripción) o un Speaking Practice", lec="Storybooks Canada nivel 2–3, Easy Stories Beginner, o Breaking News English nivel 0 si lo entiendes casi todo",
         wa="4 preguntas sobre el fin de semana de alguien, con respuestas.", sa="Pregúntate y contesta en voz alta.",
         wb="Tus planes para 2027 (going to) y 2 predicciones (will).", sb="Cuéntalo en 1 min.", tema="My plans for 2027", atras=10),
 10: dict(lle=[36,37,38,39], la=16, lb="R", c=9, esc="Easy Stories in English (un episodio Beginner, con transcripción) o un Speaking Practice", lec="Storybooks Canada nivel 2–3, Easy Stories Beginner, o Breaking News English nivel 0 si lo entiendes casi todo",
         wa="Compara 2 películas animadas o 2 programas (Blender / Maya).", sa="Compáralos en voz alta en 1 min.",
         wb="Reescribe tu peor texto de la fase con todo lo que aprendiste.", sb="", tema=None, atras=12, cp=True),
}

def li(h, txt, rest=False):
    cls = ' class="rest"' if rest else ""
    return f'<li{cls}><span class="h">{h}</span><span>{txt}</span></li>'

def ref_L(n):
    return f'<a href="#L{n}">L{n}</a>'

def ref_C(n):
    return f'<a href="#C{n}">C{n}</a>'

def anki_li():
    return li("Antes de dormir · 15–20 min", "Anki: repasos + nuevas (máx. 12: 8 del Oxford + 4 de Mis frases). Si los repasos pasan de 20 min, pon las nuevas en 0 hasta que bajen.")

def anki_turno():
    return [li("01:15–01:35 · Anki", "Repasos + nuevas (máx. 12). Si los repasos pasan de 20 min, pon las nuevas en 0 hasta que bajen."),
            li("01:35–02:00 · Sin pantalla", "Apaga el celular (o modo oscuro y brillo al mínimo) y prepárate para dormir.", rest=True)]

def manana_li():
    return li("05:00–06:00 · opcional", "No cuenta en tu meta semanal. Solo si dormiste y te sientes bien: los primeros 15–20 min re-escucha algo conocido; luego relee tus notas y di de memoria 5 oraciones. Si estás agotado, descansa.")

def dia_turno(w, lle, modo, lnum, lec, tarea=""):
    """modo: 'nueva' (lección nueva + escritura) o 'practica' (repaso + construir significado + contracciones)."""
    c = W[w]["c"]
    out = []
    facil = "re-escucha sin pausar lecciones de semanas anteriores" if w < 5 else "un episodio Beginner de Easy Stories leyendo su transcripción, o lecciones anteriores sin pausar"
    if lle:
        paso5 = "dictado de 2–3 oraciones" if modo == "nueva" else "overlapping (lee en voz alta junto con el audio, mirando el texto) y luego shadowing sin texto de esas 2–3 oraciones"
        out.append(li("Al quedar libre · 40 min", f"<b>Escucha intensiva (20–25 min):</b> <i>Let's Learn English</i>, <b>lección {lle}</b>, con el protocolo, en fragmentos de 30–90 s (transcripción: PDF del curso, sección <i>Conversation</i>). Paso 5 de hoy: {paso5}. Subraya las contracciones de {ref_C(c)}. <b>Escucha fácil (15 min):</b> {facil}. Últimos min: 3 frases de la lección a <a href='#anki'>Mis frases</a>."))
    else:
        out.append(li("Al quedar libre · 40 min", "Escucha: re-escucha lecciones que ya trabajaste, sin texto. Nota cuánto más entiendes."))
    out.append(li("Descanso · 10 min", "Ojos cerrados o estirarte. Sin celular.", rest=True))
    if lnum == "R" and modo == "nueva":
        out.append(li("40 min · Gramática", f"Repaso general: 1 ejercicio de cada lección, de {ref_L(1)} a {ref_L(16)}, sin ver respuestas. Marca las que fallaste. Luego, escritura (15 min): {tarea}"))
    elif lnum == "R":
        out.append(li("40 min · Gramática", f"Rehaz los ejercicios que fallaste el viernes (20 min) → contracciones {ref_C(c)} en voz alta, imitando el audio (20 min)."))
    elif modo == "nueva":
        out.append(li("40 min · Gramática + escritura", f"<b>Lección nueva {ref_L(lnum)}</b>: explicación → ejercicios en libreta → pista → respuestas (25 min). Escritura (15 min): {tarea} Al final, dilo en voz alta sin leer."))
    else:
        out.append(li("40 min · Repaso + significado", f"Repaso de {ref_L(lnum)} (15 min): rehaz sin ver respuestas los que fallaste. <b>Construye el significado (10 min):</b> toma 2 oraciones de la <i>Conversation</i> y responde: ¿quién hace qué?, ¿cuándo?, ¿es afirmativa, negativa o pregunta?, ¿a quién se refiere cada pronombre? Luego tradúcela completa. Contracciones {ref_C(c)} en voz alta (15 min)."))
    out.append(li("Descanso · 10 min", "Sin pantalla.", rest=True))
    out.append(li("40 min · Lectura + contar", f"Lectura extensiva (30 min): {lec}. Si trae audio, léela escuchándola. Luego cuenta en voz alta, en 1–2 min y sin mirar, lo que leíste (10 min)."))
    out.append(li("Si te sobra tiempo", "Opcional: más lectura, re-escuchar lecciones ya trabajadas o descansar (también cuenta)."))
    out.extend(anki_turno())
    out.append(manana_li())
    return out

def dia_libre(w, dia):
    """dia: 'lun' o 'jue'. ~1 h: lo que conviene grabar + escucha + repaso espaciado."""
    d = W[w]
    out = []
    extra = ""
    if dia == "lun":
        prev = W.get(w - 1, {})
        if w == 1:
            habla = "Grábate 1 min presentándote como puedas (es tu punto de partida de la semana)."
            repaso = f"Vista previa: lee solo la explicación de {ref_L(1)} (sin ejercicios)."
            extra = "Cambia el idioma de Blender (o de tu software principal) a inglés: es exposición diaria gratis a vocabulario de tu carrera."
        else:
            tema = prev.get("tema") or "What I did on vacation"
            habla = f"4/3/2 con el tema de la semana pasada (<i>{tema}</i>). Antes, escribe 5–6 palabras clave (no oraciones)."
            prev_l = prev.get("lb") if isinstance(prev.get("lb"), int) else (prev.get("la") or 13)
            repaso = f"Repaso espaciado: 3 ejercicios de {ref_L(prev_l)} sin ver respuestas."
    else:
        habla = d["sa"]
        repaso = f"Repaso espaciado: 3 ejercicios de {ref_L(d['la'])} sin ver respuestas."
        if w >= 3:
            extra = "Con wifi, si encuentras compañero: 10 min de intercambio guiado (presentarte, preguntar horarios, pedir que te repitan: <i>Can you repeat that, please?</i>)."
    out.append(li("Bloque 1 · 40 min", f"<b>Speaking grabado (15 min):</b> {habla} → <b>escucha (25 min):</b> {d['esc']} con el protocolo."))
    out.append(li("Descanso · 10 min", "Camina o estírate, sin pantalla.", rest=True))
    out.append(li("Bloque 2 · 20 min", repaso))
    if extra:
        out.append(li("Opcional", extra))
    out.append(anki_li())
    return out

def dia_sabado(w):
    d = W[w]
    out = []
    atras = f" + 2 de {ref_L(d['atras'])} (hace ~4 semanas)" if d.get("atras") else ""
    presion = " Hasta la semana 4, sin presión de velocidad." if w <= 4 else ""
    out.append(li("Bloque 1 · 40 min", f"Repaso de la semana: rehaz sin ver respuestas 2 ejercicios de {ref_L(d['la'])} y de {ref_L(d['lb'])}{atras}. Si ya te sabes las respuestas de memoria, inventa 2 oraciones nuevas con la misma estructura."))
    out.append(li("Descanso · 10 min", "Sin pantalla.", rest=True))
    out.append(li("Bloque 2 · 40 min", f"<b>Speaking:</b> {d['sb']} → 4/3/2 grabado (2 / 1.5 / 1 min): <i>{d['tema']}</i>. Antes, escribe 5–6 palabras clave.{presion} Cuenta las palabras de tu último minuto."))
    out.append(li("Descanso · 10 min", "Sin pantalla.", rest=True))
    out.append(li("Bloque 3 · 45–60 min", f'<b>Preparación con wifi</b> para la semana {w+1}: ver <a href="#descargas">descargas</a>; manda tu resumen semanal. Agrega a Mis frases 3 términos de tu software en inglés (<i>render, keyframe, layer</i>…).'))
    if d.get("irreg"):
        out.append(li("Anki", d["irreg"]))
    out.append(anki_li())
    return out

def dia_ligero(lle, extra="", turno=False):
    out = []
    if lle:
        out.append(li("15 min · Escucha", f"<i>Let's Learn English</i> nivel 1, lección {lle} (escuchas 1 y 2 del protocolo)."))
    else:
        out.append(li("15 min · Escucha", "Re-escucha una lección que te guste."))
    if extra:
        out.append(li("Opcional" if "verbos" not in extra else "Anki", extra))
    if turno:
        out.append(li("Opcional", "Si en el turno te sobra tiempo y tienes ganas, lee por gusto. Si no, descansa."))
    out.append(li("Antes de dormir · 10–15 min", "Anki: solo repasos y los verbos irregulares de la semana. Oxford: 0 nuevas."))
    return out

def tipo(t):
    m = {"turno": ("TURNO", "t-turno"), "libre": ("LIBRE", "t-libre"), "sab": ("LIBRE + PREPARACIÓN", "t-sab"),
         "ligera": ("SEMANA LIGERA", "t-ligera"), "cp": ("EXAMEN DE PRÁCTICA", "t-cp")}
    a, b = m[t]
    return f'<span class="pill {b}">{a}</span>'

def day_html(d, t, blocks, key, nota=""):
    nota_html = f'<p class="hint" style="margin:.2em 0 .4em">{nota}</p>' if nota else ""
    return (f'<div class="day"><div class="dayhead"><b>{fecha(d)}</b>{tipo(t)}'
            f'<label><input type="checkbox" data-key="{key}"> hecho</label></div>{nota_html}'
            f'<ul class="blocks">{"".join(blocks)}</ul></div>')

def semana_html(w):
    d = W[w]
    ini = START + dt.timedelta(weeks=w-1)
    fin = ini + dt.timedelta(days=6)
    days = []
    lle = d["lle"]
    if d.get("ligera"):
        extras = {0: (f"{ref_L(13)}: agrega otros 10 verbos irregulares a Mis frases (son tus únicas tarjetas nuevas esta semana)." if w == 7 else f"{ref_L(13)}: agrega los últimos 10 verbos irregulares a Mis frases."),
                  3: f"Contracciones {ref_C(7)} con VOA <i>How to Pronounce</i>.",
                  5: "Preparación con wifi para la próxima semana (30 min)."}
        for i in range(7):
            l = {1: lle[0], 4: lle[2]}.get(i)
            day = ini + dt.timedelta(days=i)
            days.append(day_html(day, "ligera", dia_ligero(l, extras.get(i, ""), turno=i in (1, 2, 4, 6)), f"w{w}d{i}",
                                 "Días mínimos (30 min), con el Oxford en 0 nuevas. Mínimo de emergencia: 2–5 min (una ronda corta de Anki o 2 min de audio conocido). Fiestas o enfermedad: descansa sin culpa." if i == 0 else ""))
        titulo = f"Semana {w} · {ini.day} {MESES[ini.month-1]} – {fin.day} {MESES[fin.month-1]} · semana ligera (fiestas)"
    else:
        lb_int = d["lb"] if isinstance(d["lb"], int) else "R"
        days.append(day_html(ini, "libre", dia_libre(w, "lun"), f"w{w}d0"))
        days.append(day_html(ini + dt.timedelta(days=1), "turno", dia_turno(w, lle[0], "nueva", d["la"], d["lec"], d["wa"]), f"w{w}d1"))
        days.append(day_html(ini + dt.timedelta(days=2), "turno", dia_turno(w, lle[1], "practica", d["la"], d["lec"]), f"w{w}d2"))
        if d.get("cp"):
            jue = [li("Bloque 1 · ~105 min", "<b>A2 Key, examen de muestra (parte 1):</b> Reading and Writing (60 min) → descanso 10 min → Listening (~35 min). Califícate con la clave; la escritura, con el mensaje de corrección de la página principal."),
                   anki_li()]
            days.append(day_html(ini + dt.timedelta(days=3), "cp", jue, f"w{w}d3", "Examen de práctica 1, primer día. No requiere internet."))
        else:
            days.append(day_html(ini + dt.timedelta(days=3), "libre", dia_libre(w, "jue"), f"w{w}d3"))
        days.append(day_html(ini + dt.timedelta(days=4), "turno", dia_turno(w, lle[2], "nueva", lb_int, d["lec"], d["wb"]), f"w{w}d4"))
        if d.get("cp"):
            cp = [li("Bloque 1 · ~90 min", "<b>EF SET de 4 habilidades</b> (90 min, gratis, requiere internet; si no te da el tiempo, el de 50 min). Compáralo con tu 29 del día 0."),
                  li("Descanso · 15 min", "Sin pantalla.", rest=True),
                  li("Bloque 2 · 35 min", "Grábate 2 min con el tema del día 0 y escúchate junto a la grabación original · escribe 10 min sobre <i>My life right now</i> y compáralo con tu texto del día 0 · escucha un audio que <u>no</u> hayas estudiado y anota cuánto entiendes. Responde las preguntas de la sección de exámenes de la página principal."),
                  anki_li()]
            days.append(day_html(ini + dt.timedelta(days=5), "cp", cp, f"w{w}d5", "Examen de práctica 1, segundo día: decide si pasas a la fase 2 o alargas la fase 1."))
        else:
            days.append(day_html(ini + dt.timedelta(days=5), "sab", dia_sabado(w), f"w{w}d5"))
        days.append(day_html(ini + dt.timedelta(days=6), "turno", dia_turno(w, lle[3], "practica", lb_int, d["lec"]), f"w{w}d6"))
        foco = [L[d["la"]][0]]
        if isinstance(d["lb"], int): foco.append(L[d["lb"]][0])
        titulo = f"Semana {w} · {ini.day} {MESES[ini.month-1]} – {fin.day} {MESES[fin.month-1]} · " + " + ".join(foco)
        if d.get("cp"): titulo += " · examen de práctica"
    s, e = ini.isoformat(), fin.isoformat()
    return f'<details class="week" data-start="{s}" data-end="{e}"><summary>{titulo}</summary><div class="in">{"".join(days)}</div></details>'

def semana0_html():
    d0 = dt.date(2026, 11, 5)
    days = []
    days.append(day_html(d0, "libre", [
        li("Con wifi · 60–90 min", "✔ EF SET (hecho: 29, A1). Haz la <b>grabación de 2 min</b> y el <b>texto de referencia</b> si no los hiciste (ve la página principal)."),
        li("Descargar", 'Con wifi, lo de <a href="#descargas">Qué descargar</a> (Kiwix: VOA Learning; PDF del curso; AntennaPod) y configura Anki como dice <a href="#anki">Anki: cómo usarlo</a>.'),
        li("20 min · Escucha", "<i>Let's Learn English</i> lección 1, con el protocolo de 5 pasos (transcripción en el PDF)."),
        anki_li()], "w0d0", "Arranque: hoy solo preparas tus herramientas y pruebas el protocolo."))
    days.append(day_html(d0 + dt.timedelta(days=1), "turno", [
        li("Al quedar libre · 40 min", "<i>Let's Learn English</i> nivel 1, lección 2 (protocolo)."),
        li("Descanso · 10 min", "Sin celular.", rest=True),
        li("40 min · Lectura", "Lee las mini-lecciones " + ref_C(1) + " (contracciones) y " + ref_L(1) + " (gramática), solo para conocerlas. Luego, la transcripción de las lecciones 1 y 2."),
        li("Si te sobra tiempo", "Re-escucha las lecciones 1 y 2 sin texto, o descansa."),
        li("01:15–01:35 · Anki", "Configura tus mazos y haz 8 nuevas para aprender a usar la app."),
        manana_li()], "w0d1"))
    days.append(day_html(d0 + dt.timedelta(days=2), "sab", [
        li("30 min · Escucha", "<i>Let's Learn English</i> nivel 1, lección 3 (protocolo)."),
        li("Descanso · 10 min", "Sin pantalla.", rest=True),
        li("45–60 min · Preparación", 'Prepara la semana 1: ver <a href="#descargas">descargas</a>. Si puedes, pasa a la biblioteca de tu escuela (ve <a href="#biblioteca">biblioteca</a>).'),
        anki_li()], "w0d2"))
    days.append(day_html(d0 + dt.timedelta(days=3), "turno", [
        li("Al quedar libre · 40 min", "Re-escucha las lecciones 1–3 sin texto."),
        li("Descanso · 10 min", "Sin celular.", rest=True),
        li("40 min · Lectura", "Un cuento de Storybooks Canada nivel 1 (PDF + audio)."),
        li("01:15–01:35 · Anki", "Repasos + 8 nuevas."),
        manana_li()], "w0d3"))
    return f'<details class="week" open data-start="2026-11-05" data-end="2026-11-08"><summary>Semana 0 · 5 – 8 nov · arranque</summary><div class="in">{"".join(days)}</div></details>'

def leccion_html(n):
    t, exp, ejs, resp = L[n]
    items = []
    for i, (q, h) in enumerate(ejs):
        hint = f' <details class="hintd"><summary>Pista</summary><div class="in hint">{h}</div></details>' if h else ""
        items.append(f"<li>{q}{hint}</li>")
    answers = "".join(f"<li>{r}</li>" for r in resp)
    return (f'<div class="lesson" id="L{n}"><h3>L{n} · {t}</h3>{exp}<p><b>Ejercicios</b> (en tu libreta, sin ver la explicación):</p>'
            f'<ol>{"".join(items)}</ol><details><summary>Respuestas (solo después de intentarlo)</summary><div class="in"><ol>{answers}</ol></div></details></div>')

def contr_html(n):
    t, exp = C[n]
    return f'<div class="lesson" id="C{n}"><h3>C{n} · {t}</h3>{exp}</div>'

TPL = """
<div class="tpl">
<div class="card"><p><b>Día de TURNO</b> <span class="pill t-turno">mar · mié · vie · dom</span><br><small class="muted">≈ 2 h 15 desde que quedas libre (22:00–23:00) hasta las 2:00, sin internet, + 5:00–6:00 ligero</small></p>
<ul class="blocks">
<li><span class="h">Al quedar libre · 40</span><span>Escucha intensiva (20–25) + escucha fácil (15)</span></li>
<li class="rest"><span class="h">10 min</span><span>Descanso sin pantalla</span></li>
<li><span class="h">40 min</span><span>Gramática nueva + escritura (mar, vie) o repaso + construir el significado + contracciones en voz alta (mié, dom)</span></li>
<li class="rest"><span class="h">10 min</span><span>Descanso</span></li>
<li><span class="h">40 min</span><span>Lectura extensiva + contar en voz alta lo que leíste</span></li>
<li><span class="h">Lo que sobre</span><span>Opcional: más lectura, re-escucha o descansar</span></li>
<li><span class="h">01:15–01:35</span><span>Anki</span></li>
<li class="rest"><span class="h">01:35–02:00</span><span>Sin pantalla, a dormir</span></li>
<li><span class="h">05:00–06:00</span><span>Opcional y fuera de la meta: solo si dormiste bien</span></li></ul></div>
<div class="card"><p><b>Día LIBRE</b> <span class="pill t-libre">lun · jue</span><br><small class="muted">≈ 1 h; tú eliges la hora</small></p>
<ul class="blocks">
<li><span class="h">Bloque 1 · 40</span><span>Speaking grabado (15) + escucha (25)</span></li>
<li class="rest"><span class="h">10 min</span><span>Descanso: caminar, sin pantalla</span></li>
<li><span class="h">Bloque 2 · 20</span><span>Repaso espaciado de gramática</span></li>
<li><span class="h">Antes de dormir</span><span>Anki</span></li></ul></div>
<div class="card"><p><b>SÁBADO</b> <span class="pill t-sab">libre + preparación</span><br><small class="muted">≈ 2 h 30; el último bloque es en casa con wifi y laptop</small></p>
<ul class="blocks">
<li><span class="h">Bloque 1 · 40</span><span>Repaso espaciado de gramática</span></li>
<li class="rest"><span class="h">10 min</span><span>Descanso</span></li>
<li><span class="h">Bloque 2 · 40</span><span>Speaking + 4/3/2 grabado</span></li>
<li class="rest"><span class="h">10 min</span><span>Descanso</span></li>
<li><span class="h">Bloque 3 · 45–60</span><span>Descargas + sincronizar Anki + corrección + resumen + 3 términos de tu software</span></li>
<li><span class="h">Antes de dormir</span><span>Anki</span></li></ul></div>
</div>"""

html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Fase 1 Día a Día</title>
<meta name="description" content="Fase 1 del plan de inglés (A1 → A2), día por día: 5 nov 2026 – 17 ene 2027, ajustada a turnos nocturnos y solo con recursos gratis.">
<style>{base_css}{EXTRA_CSS}</style>
</head>
<body>
<div class="wrap">
<header>
  <p class="muted" style="margin:0"><a href="index.html">← Plan completo</a> · versión del 5 de noviembre de 2026</p>
  <h1>Fase 1, día por día</h1>
  <p class="lead">De A1 (EF SET 29) a A2 · 5 nov 2026 → 17 ene 2027 · ajustada a tus turnos nocturnos · solo recursos gratis.</p>
  <div class="summary">
    <div><b>~14 h/semana</b><span>4 turnos de ~2 h 15 + días libres de ~1 h</span></div>
    <div><b>16 lecciones</b><span>de gramática, con pistas y respuestas</span></div>
    <div><b>9 mini-lecciones</b><span>de contracciones y habla conectada</span></div>
    <div><b>Semana 10</b><span>examen de práctica: decide si sigues</span></div>
  </div>
  <nav class="toc" aria-label="Contenido">
    <a href="#plantillas">Tus 3 tipos de día</a><a href="#semanas">Día por día</a><a href="#descargas">Qué descargar</a><a href="#anki">Anki</a>
    <a href="#gramatica">Gramática L1–L16</a><a href="#contracciones">Contracciones C1–C9</a><a href="#biblioteca">Biblioteca</a><a href="#porque">Por qué así</a>
  </nav>
</header>

<h2 id="plantillas">Tus 3 tipos de día</h2>
<p>En el turno quedas libre entre las 22:00 y las 23:00 (varía) y lo estás hasta las 2:00; luego, de 5:00 a 6:00. Como la hora de inicio cambia, los bloques del turno <b>empiezan cuando quedas libre</b>, no a una hora fija. El turno es tu tiempo principal de estudio, incluido hablar en voz alta; los días libres son cortos (~1 h) y se quedan con lo que conviene grabar. En días libres, <b>elige una hora y repítela siempre</b>: la misma hora y el mismo lugar ayudan a que se vuelva automático.</p>
<p><b>Mínimo de emergencia (2–5 min):</b> una ronda corta de Anki o 2 min de un audio conocido. Si estás enfermo o agotado, descansa: un día perdido no rompe el hábito. <b>Las primeras 2 semanas, anota cada día cuántas horas dormiste en total y qué tan despierto estuviste al estudiar (1 a 5):</b> con eso ajustamos la carga en serio.</p>
{TPL}
<p class="muted">Por qué Anki va justo antes de dormir y por qué los descansos son sin pantalla: ve <a href="#porque">Por qué así</a>.</p>

<h2 id="semanas">Día por día</h2>
<p>Marca "hecho" en cada día (se guarda en este celular). La semana actual se abre sola. Si un día no puedes con todo, haz el <b>día mínimo</b>: Anki + 15 min de escucha. Eso cuenta.</p>
<div class="toolbar noprint"><button class="btn" type="button" id="openAll">Abrir todas</button><button class="btn" type="button" id="closeAll">Cerrar todas</button></div>
{semana0_html()}
{"".join(semana_html(w) for w in range(1, 11))}

<h2 id="descargas">Qué descargar</h2>
<h3>Una sola vez (con wifi, antes del lunes 9)</h3>
<div class="card">
<ul class="check" data-group="unavez">
  <li><input type="checkbox" data-key="u-1"><span><b>Revisa tu espacio:</b> en Ajustes → Almacenamiento necesitas <b>~8 GB libres</b>. Si tienes tarjeta SD, Kiwix puede guardar ahí (en Kiwix: Ajustes → Almacenamiento). Si no te alcanza, dime cuánto tienes libre y busco otra opción.</span></li>
  <li><input type="checkbox" data-key="u-2"><span><b>Kiwix → pestaña de descargas (Online / Biblioteca) → busca <code>VOA</code> → descarga "VOA Learning"</b> (7.1 GB, de enero 2025). Ya no hay paquetes separados: todo viene ahí, en estas listas:<br>· <b>Let's Learn English</b>: las 52 lecciones del nivel 1, con sus videos <i>Speaking Practice</i> y <i>Pronunciation Practice</i>. Es tu escucha principal.<br>· <b>How to Pronounce</b>: para las contracciones (C7).<br>· <b>Let's Learn English Level 2</b>: para la fase 2.<br>Los videos <u>no traen transcripción</u>; por eso necesitas el PDF del siguiente punto. Al terminar la descarga, <b>prueba en modo avión</b> que abran los videos.</span></li>
  <li><input type="checkbox" data-key="u-3"><span><b>PDF del curso <i>Let's Learn English – Level 1</i></b> (601 páginas, 161 MB), publicado gratis por el Departamento de Estado de EE. UU.: <span class="mono">americanspaces.state.gov/wp-content/uploads/sites/292/LetsLearnEnglishLevel1.pdf</span>. Cada lección trae la <b>Conversation</b> (la transcripción del video), las <b>Key Words</b> y el guion del <i>Speaking Practice</i>. El índice está en la página 2: por ejemplo, la lección 4 empieza en la página 34.</span></li>
  <li><input type="checkbox" data-key="u-4"><span><b>AntennaPod → busca y suscríbete a <i>Easy Stories in English</i></b> (Ariel Goodbody). Por ahora es <b>el único podcast</b>: no te suscribas a diez. Descarga 3 episodios que digan <b>(Beginner)</b> en el título. <b>La transcripción es gratis</b> en la página de cada episodio en easystoriesinenglish.com, con botón <i>Download as a PDF</i>: guárdala junto con el audio. ("Beginner" es la etiqueta del autor, no garantiza A1: si no sigues la historia ni con el texto, espera unas semanas.) Entran fuerte desde la semana 5.</span></li>
  <li><input type="checkbox" data-key="u-5"><span><b>Storybooks Canada</b> (<span class="mono">storybookscanada.ca</span>): cuentos cortos con audio, en 5 niveles, licencia abierta. Son infantiles, pero el nivel 1–2 es justo lo que necesitas para leer con audio. Descarga 5–6 del nivel 1: en los sitios de la misma red hay botón <i>Download PDF</i> y el audio se guarda desde el reproductor (mantén presionado → descargar).</span></li>
</ul>
<p class="muted">Por qué conviene tener tu copia: VOA casi dejó de operar en 2025 y, según reportes de ese año, Learning English dejó de publicar contenido nuevo. Hoy (5 nov 2026) el sitio y el PDF siguen en línea, pero no hay garantía de que sigan.</p>
</div>
<h3>Cada sábado (con wifi, ~30 min)</h3>
<div class="card">
<ul class="check" data-group="semanal">
  <li><input type="checkbox" data-key="dl-2"><span><b>Lectura:</b> 3–4 cuentos de Storybooks Canada (PDF + audio) de tu nivel. Elige por comprensión, no por semana: si lo entiendes casi todo, perfecto; la lectura fácil también sirve. ER-Central sirve en línea, pero si lo guardas como PDF pierdes el audio.</span></li>
  <li><input type="checkbox" data-key="dl-3"><span><b>AntennaPod</b> (desde la semana 5): descarga 2 episodios <i>(Beginner)</i> de Easy Stories y guarda su transcripción en PDF.</span></li>
  <li><input type="checkbox" data-key="dl-4"><span><b>Anki:</b> sincroniza (botón de sincronizar arriba), para respaldar tu avance y tus frases.</span></li>
  <li><input type="checkbox" data-key="dl-5"><span><b>Gramática de la próxima semana</b> (opcional): si el tema está en British Council <i>LearnEnglish</i> (A1–A2), haz su ejercicio en línea como prueba previa.</span></li>
  <li><input type="checkbox" data-key="dl-6"><span><b>Corrección:</b> manda 2–3 textos de tu libreta con el mensaje de corrección de la página principal y reescríbelos.</span></li>
  <li><input type="checkbox" data-key="dl-7"><span><b>Resumen semanal:</b> mándame la plantilla de la página principal.</span></li>
</ul>
<div class="toolbar noprint"><button class="btn" type="button" id="resetWeek">Desmarcar la lista del sábado</button></div>
</div>

<h2 id="anki">Anki: cómo usarlo (mazo Oxford 3000 + "Mis frases")</h2>
<p>Usas <b>dos mazos</b>: el de Oxford 3000 que ya descargaste (palabras frecuentes, elegidas por otros) y uno tuyo, <b>Mis frases</b>, con frases de lo que estudias. El tuyo tiene una ventaja práctica: las palabras aparecen en una frase que ya oíste y entendiste <span class="pill ev-c">Opinión</span>. Lo que sí tiene evidencia es practicar en dirección español → inglés para poder <i>producir</i> las palabras (Webb, 2009) <span class="pill ev-b">Evidencia moderada</span>.</p>
<div class="card">
<p><b>Antes, una aclaración: notas vs tarjetas.</b> Cada frase que agregas es una <i>nota</i>; si es del tipo "y tarjeta invertida", crea <b>2 tarjetas</b> (inglés → español y español → inglés). Los límites de Anki cuentan <b>tarjetas</b>, no notas. Por eso los números de abajo están en tarjetas.</p>
<p><b>1 · Configura (una vez)</b></p>
<ol>
  <li><b>Oxford 3000:</b> toca los 3 puntos (o mantén presionado) junto al mazo → <i>Opciones</i> → <i>Límites diarios</i> → <i>Tarjetas nuevas/día</i> = <b>8</b>. (Los nombres pueden variar un poco según la versión.)</li>
  <li><b>Revisa el orden:</b> abre el mazo y mira las primeras tarjetas nuevas. Si van en orden alfabético (<i>a, abandon, ability…</i>), dime el nombre del mazo y te digo cómo ordenarlo por nivel (A1 primero).</li>
  <li><b>Crea el mazo "Mis frases":</b> botón <b>+</b> → <i>Crear mazo</i> → "Mis frases". En sus opciones: <i>Tarjetas nuevas/día</i> = <b>4</b>.</li>
  <li><b>Si tu versión lo tiene, activa FSRS</b> en las opciones (es un algoritmo de repaso más eficiente; sus creadores reportan menos repasos para la misma retención) <span class="pill ev-c">Opinión</span>, basada en las pruebas de sus desarrolladores, no en estudios independientes.</li>
</ol>
<p><b>Total: máximo 12 tarjetas nuevas al día.</b> Es menos que lo que te dije antes (15) a propósito: con tu sueño y tus turnos, es mejor empezar ligero y subir. <b>Regla de seguridad:</b> si los repasos te toman más de 20 min, pon las nuevas en 0 en ambos mazos hasta que bajen. Nunca dejes de hacer los repasos para hacer nuevas.</p>
<p><b>2 · Cuándo agregas tus frases</b></p>
<p>En los <b>días de turno</b>, en los últimos minutos del bloque de escucha, justo después de trabajar la lección. <b>3 frases por lección</b> × 4 lecciones = 12 frases por semana = 24 tarjetas, que entran a ~4 por día. Además, cada sábado, 3 términos de tu software.</p>
<p><b>3 · Qué frases eliges</b> (de la <i>Conversation</i> o las <i>Key Words</i> del PDF)</p>
<ul>
  <li>Que tengan algo que <b>no sabías</b> (una palabra o una forma de decir algo).</li>
  <li>Que <b>tú dirías</b> en tu vida. <i>"Nice to meet you"</i> sí; un nombre de calle, no.</li>
  <li><b>Frases completas o pedazos</b> (<i>"What do you do?"</i>, <i>"I'm new to D.C."</i>), no palabras sueltas: esas ya te las da el Oxford.</li>
  <li>Cortas: máximo ~8 palabras.</li>
</ul>
<p><b>4 · Cómo se crea cada tarjeta</b> (sin internet, en AnkiDroid)</p>
<ol>
  <li>Botón <b>+</b> → <i>Agregar</i>. Arriba elige <b>Tipo: "Básico (y tarjeta invertida)"</b> (<i>Basic (and reversed card)</i>) y <b>Mazo: Mis frases</b>.</li>
  <li><b>Anverso:</b> la frase en inglés, con la palabra nueva en negritas. Ejemplo: <i>I have a pen in my <b>bag</b>.</i></li>
  <li><b>Reverso:</b> el significado en español de la frase completa: <i>Tengo una pluma en mi bolsa.</i></li>
  <li>Guardar. Anki te muestra la segunda tarjeta (la invertida) otro día, no el mismo. La de español → inglés es la que ataca tu "no sé qué palabra decir".</li>
</ol>
<p><b>5 · Al repasar</b> (de 1:15 a 1:35 en el turno, o antes de dormir en días libres): <b>di la respuesta en voz alta antes de voltear</b>. Si no te salió, presiona <i>Otra vez</i> (<i>Again</i>) sin culpa.</p>
</div>

<h2 id="gramatica">Gramática: L1–L16</h2>
<p>Cada lección: explicación corta → ejercicios → <b>pista</b> si te atoras → <b>respuestas</b> escondidas. Primero intenta, luego mira la pista y al final la respuesta: equivocarte al intentar recordar es parte del aprendizaje. Para más ejemplos, busca el mismo tema en British Council <i>LearnEnglish</i>.</p>
{"".join(leccion_html(n) for n in range(1, 17))}

<h2 id="contracciones">Contracciones y habla conectada: C1–C9</h2>
<p><b>Dos cosas distintas</b> que conviene separar: (1) <b>contracciones gramaticales</b> (<i>I'm, don't, can't</i>): son normales y se escriben en textos informales; (2) <b>reducciones del habla</b> (<i>gonna, wanna, didja</i>): son cómo suena el inglés rápido y <u>no</u> se escriben en textos formales ni en exámenes. Y no son solo de los estadounidenses: todo el inglés hablado las tiene. Aquí uso inglés americano porque es el que quieres entender.</p>
<p><b>Tu prioridad es reconocerlas al escuchar</b>, porque eso ataca directamente tu "capto palabras pero no entiendo". Enseñar formas reducidas mejoró la comprensión auditiva en Brown y Hilferty (1986) y en estudios posteriores pequeños <span class="pill ev-b">Evidencia moderada</span>.</p>
{CONTR_METHOD}
{"".join(contr_html(n) for n in range(1, 10))}

<h2 id="biblioteca">La biblioteca de tu escuela es tu recurso gratis más valioso</h2>
<p>Lo que más falta en los recursos gratis son <b>libros graduados</b> (readers) y un <b>libro de gramática con ejercicios</b>. Las bibliotecas universitarias suelen tener <i>Essential Grammar in Use</i> / <i>English Grammar in Use</i> (Murphy) y readers de Oxford Bookworms o Penguin Readers. Pregunta por ellos. Si los encuentras, el Murphy sustituye o complementa las lecciones L, y un reader nivel Starter o 1 sustituye a ER-Central en la lectura.</p>
<p>Pregunta también en la <b>Coordinación de Lenguas Extranjeras</b>: qué certificaciones aceptan para titularte (detalles en la página principal).</p>

<h2 id="porque">Por qué está armado así</h2>
<ul>
  <li><b>Anki poco antes de dormir, y luego 25 min sin pantalla:</b> en Gais, Lucas y Born (2006), quienes aprendieron vocabulario y luego durmieron lo recordaron mejor que quienes pasaron el día despiertos <span class="pill ev-b">Evidencia moderada</span>. Pero ese estudio usó una noche completa de sueño, no 3 horas en el trabajo, así que para tu caso es una apuesta razonable, no algo probado <span class="pill ev-c">Opinión</span>. Si a esa hora repasas agotado, mueve Anki al inicio del turno. Lo que sí está claro es que dormir poco perjudica la memoria: proteger tus 3 horas va primero.</li>
  <li><b>Descansos de 5–10 min:</b> un metaanálisis de micro-descansos (Albulescu et al., 2022) encontró que aumentan la energía y reducen la fatiga, pero el efecto sobre el rendimiento fue pequeño y no significativo <span class="pill ev-a">Evidencia fuerte</span> para el ánimo, débil para el aprendizaje. Que el descanso sea <u>sin pantalla</u> viene de Dewar et al. (2012): 10 min de reposo con los ojos cerrados después de aprender mejoraron el recuerdo una semana después, pero en adultos mayores <span class="pill ev-b">Evidencia moderada</span>. Las duraciones exactas (25/5, 40/10) son <span class="pill ev-c">Opinión</span>.</li>
  <li><b>Lo más difícil va al inicio de la ventana del turno</b> (escucha intensiva y gramática nueva) y la lectura al final; <b>de 5 a 6 solo cosas ligeras</b>. En turnos nocturnos, el estado de alerta y el rendimiento mental caen en la madrugada, con el punto más bajo hacia las 3–5 am, y al despertar hay un atontamiento ("inercia del sueño") que suele durar hasta ~30 min (Tassi y Muzet, 2000) <span class="pill ev-a">Evidencia fuerte</span> sobre esos fenómenos. Que eso implique este orden de estudio es mi aplicación <span class="pill ev-c">Opinión</span>.</li>
  <li><b>Como puedes hablar en el turno</b>, el shadowing, las contracciones en voz alta y contar lo que leíste van ahí. Las grabaciones (4/3/2) quedan para días libres y el sábado, en casa <span class="pill ev-c">Opinión</span>, por logística.</li>
  <li><b>Gramática nueva martes y viernes, repaso al día siguiente, el jueves o lunes y el sábado</b>: cada tema se ve 3–4 veces separadas en la semana y otra vez a las 4 semanas <span class="pill ev-a">Evidencia fuerte</span> (repaso espaciado).</li>
  <li><b>La escucha se divide en intensiva y fácil:</b> la intensiva (analizar un fragmento) enseña a reconocer; la fácil (escuchar sin parar algo que casi entiendes) da volumen y fluidez. En Chang y Millett (2014), la escucha extensiva apoyada mejoró la fluidez auditiva <span class="pill ev-b">Evidencia moderada</span>. La proporción exacta (20–25 / 15) es <span class="pill ev-c">Opinión</span>.</li>
  <li><b>"Construir el significado"</b> (quién hace qué, cuándo, negación, pronombres) apunta a tu problema de "capto palabras pero no armo la frase". Que el vocabulario y la gramática se relacionan fuerte con la comprensión lectora sí tiene respaldo (Jeon y Yamashita, 2014, metaanálisis correlacional) <span class="pill ev-a">Evidencia fuerte</span>; el ejercicio concreto es <span class="pill ev-c">Opinión</span>.</li>
  <li><b>Por qué no meto más gramática con el tiempo extra:</b> va a lectura y escucha, que es lo que más te falta para pasar de captar palabras a entender frases, y lo que menos cansa a esas horas <span class="pill ev-c">Opinión</span>, apoyada en el peso que da Nation al input y en Jeon y Day (2016).</li>
  <li><b>Solo la Fase 1 está día por día</b> a propósito: el examen de práctica de la semana 10 va a mostrar si tu ritmo es el estimado, y la Fase 2 se arma con ese dato.</li>
</ul>
<h3>Fuentes de esta página</h3>
<ul>
  <li>Gais, Lucas y Born (2006), <a href="https://ecommons.cornell.edu/entities/publication/f609cbe6-fa54-42f8-842d-d5232c58ce63">Sleep after learning aids memory recall</a>, Learning &amp; Memory</li>
  <li>Albulescu et al. (2022), <a href="https://doaj.org/article/c6f37b6ba159469296b2cb968b65505f">"Give me a break!" Micro-breaks meta-analysis</a>, PLOS ONE</li>
  <li>Dewar et al. (2012), <a href="https://www.psychologicalscience.org/news/releases/boosting-new-memories-with-wakeful-resting.html">Brief wakeful resting boosts new memories over the long term</a> (resumen de APS)</li>
  <li>Jeon y Yamashita (2014), <a href="https://doi.org/10.1111/lang.12034">L2 reading comprehension and its correlates: A meta-analysis</a>, Language Learning</li>
  <li>Tassi y Muzet (2000), <a href="https://www.em-consulte.com/article/588100/sleep-inertia">Sleep inertia</a>, Sleep Medicine Reviews · <a href="https://pubmed.ncbi.nlm.nih.gov/34969316/">Disturbance of the circadian system in shift work</a> (revisión)</li>
  <li>Brown y Hilferty (1986), RELC Journal 17(2): 59–70 · <a href="https://cambridge.org/core/services/aop-cambridge-core/content/view/555DB88EE394C8ABA480DBCD20FF408D/S0261444822000441a.pdf/jd-browns-essential-bookshelf-connected-speech.pdf">J.D. Brown, bibliografía sobre habla conectada</a></li>
  <li>Recursos: <a href="https://americanspaces.state.gov/wp-content/uploads/sites/292/LetsLearnEnglishLevel1.pdf">PDF del curso Let's Learn English – Level 1</a> (Departamento de Estado de EE. UU.) · <a href="https://library.kiwix.org">biblioteca de Kiwix</a> ("VOA Learning") · <a href="https://learningenglish.voanews.com/a/lets-learn-english-level-1-lesson-50/5182991.html">VOA Let's Learn English</a> (52 lecciones en el nivel 1) · <a href="https://www.easystoriesinenglish.com/">Easy Stories in English</a> · <a href="https://www.storybookscanada.ca/">Storybooks Canada</a> · <a href="https://www.elllo.org/">ELLLO</a> · <a href="https://www.er-central.com/help/">ER-Central</a> · <a href="https://breakingnewsenglish.com/news_levels.html">Breaking News English</a> · <a href="https://learnenglish.britishcouncil.org/grammar/a1-a2-grammar">British Council: gramática A1–A2</a> · <a href="https://kiwix.org">Kiwix</a></li>
</ul>
<footer><p>Fase 1 · v3 · 5 nov 2026 (cambios tras la revisión de Gemini y ChatGPT). Se rehace después del examen de práctica de la semana 10.</p></footer>
</div>
<script>
(function(){{
  var KEY='plan-ingles-fase1-v1';
  function load(){{try{{return JSON.parse(localStorage.getItem(KEY))||{{}}}}catch(e){{return {{}}}}}}
  function save(s){{try{{localStorage.setItem(KEY,JSON.stringify(s))}}catch(e){{}}}}
  var state=load();
  document.querySelectorAll('input[type=checkbox][data-key]').forEach(function(b){{
    if(state[b.dataset.key]) b.checked=true;
    b.addEventListener('change',function(){{state[b.dataset.key]=b.checked;save(state)}});
  }});
  var reset=document.getElementById('resetWeek');
  if(reset) reset.addEventListener('click',function(){{
    document.querySelectorAll('[data-group=semanal] input').forEach(function(b){{b.checked=false;state[b.dataset.key]=false}});save(state);
  }});
  var weeks=document.querySelectorAll('details.week');
  var today=new Date(); var iso=today.getFullYear()+'-'+String(today.getMonth()+1).padStart(2,'0')+'-'+String(today.getDate()).padStart(2,'0');
  var found=false;
  weeks.forEach(function(d){{ if(iso>=d.dataset.start && iso<=d.dataset.end){{d.open=true;found=true}} }});
  if(found) weeks.forEach(function(d){{ if(!(iso>=d.dataset.start && iso<=d.dataset.end)) d.open=false }});
  function setAll(o){{weeks.forEach(function(d){{d.open=o}})}}
  var oa=document.getElementById('openAll'),ca=document.getElementById('closeAll');
  if(oa) oa.addEventListener('click',function(){{setAll(true)}});
  if(ca) ca.addEventListener('click',function(){{setAll(false)}});
  window.addEventListener('beforeprint',function(){{document.querySelectorAll('details').forEach(function(d){{d.open=true}})}});
}})();
</script>
</body>
</html>
"""

OUT.write_text(html, encoding="utf-8")
print(f"Escrito {OUT} ({len(html)//1024} KB)")
